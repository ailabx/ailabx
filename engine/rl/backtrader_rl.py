import backtrader as bt
import pandas as pd
from backtrader.utils import num2date, date2num
import datetime
import numpy as np


class BTEngine(bt.Cerebro):
    params = (
        ('preload', False),
        ('runonce', False),
        ('maxcpus', None),
        ('stdstats', False),
        ('oldbuysell', False),
        ('oldtrades', False),
        ('lookahead', 0),
        ('exactbars', False),
        ('optdatas', True),
        ('optreturn', True),
        ('objcache', False),
        ('live', False),
        ('writer', False),
        ('tradehistory', False),
        ('oldsync', False),
        ('tz', None),
        ('cheat_on_open', False),
        ('broker_coo', True),
        ('quicknotify', False),
    )

    def __init__(self):
        super().__init__()


    ## ==============================
    ## Default Interface Methods
    ## ==============================

    def step(self, action=None):
        self.terminated = self._step(self.runstrats_container, **self.bt_state_container)
        self.step_count += 1

        observation = None

        for strat in self.runstrats_container:
            reward = strat._computeReward()
        print(reward)

        return observation, reward, self.terminated

    def reset(self, **kwargs):
        self.run(**kwargs)

    def close(self):
        # Last notification chance before stopping
        self._datanotify()
        if self._event_stop:  # stop if requested
            return
        self._storenotify()
        if self._event_stop:  # stop if requested
            return

    ## ==============================
    ## Cerebro Dissection Methods
    ## ==============================

    # Makes Cerebro Stapable in Backtests (not in live moe yet)
    # Disects the _runnext method into a stepable function
    # the reset method has to call the cerebro run method

    def _runnext(self, runstrats):
        '''
        Actual implementation of run in full next mode. All objects have its
        ``next`` method invoke on each data arrival
        '''
        self.runstrats_container = runstrats
        self._init_run()

    def _init_run(self):
        datas = sorted(self.datas,
                       key=lambda x: (x._timeframe, x._compression))
        datas1 = datas[1:]
        data0 = datas[0]
        d0ret = True
        rsonly = [i for i, x in enumerate(datas)
                  if x.resampling and not x.replaying]
        onlyresample = len(datas) == len(rsonly)
        noresample = not rsonly

        clonecount = sum(d._clone for d in datas)
        ldatas = len(datas)
        ldatas_noclones = ldatas - clonecount
        dt0 = date2num(datetime.datetime.max) - 2  # default at max

        self.bt_state_container = {"datas": datas,
                                   "datas1": datas1,
                                   "data0": data0,
                                   "d0ret": d0ret,
                                   "rsonly": rsonly,
                                   "onlyresample": onlyresample,
                                   "noresample": noresample,
                                   "ldatas_noclones": ldatas_noclones,
                                   "dt0": dt0,
                                   }

    def _step(self, runstrats, datas, datas1, data0, d0ret, rsonly,
              onlyresample, noresample, ldatas_noclones, dt0):

        # if any has live data in the buffer, no data will wait anything
        newqcheck = not any(d.haslivedata() for d in datas)
        if not newqcheck:
            # If no data has reached the live status or all, wait for
            # the next incoming data
            livecount = sum(d._laststatus == d.LIVE for d in datas)
            newqcheck = not livecount or livecount == ldatas_noclones

        lastret = False
        # Notify anything from the store even before moving datas
        # because datas may not move due to an error reported by the store
        self._storenotify()
        if self._event_stop:  # stop if requested
            return True
        self._datanotify()
        if self._event_stop:  # stop if requested
            return True

        # record starting time and tell feeds to discount the elapsed time
        # from the qcheck value
        drets = []
        qstart = datetime.datetime.utcnow()
        for d in datas:
            qlapse = datetime.datetime.utcnow() - qstart
            d.do_qcheck(newqcheck, qlapse.total_seconds())
            drets.append(d.next(ticks=False))

        d0ret = any((dret for dret in drets))
        if not d0ret and any((dret is None for dret in drets)):
            d0ret = None

        if d0ret:
            dts = []
            for i, ret in enumerate(drets):
                dts.append(datas[i].datetime[0] if ret else None)

            # Get index to minimum datetime
            if onlyresample or noresample:
                dt0 = min((d for d in dts if d is not None))
            else:
                dt0 = min((d for i, d in enumerate(dts)
                           if d is not None and i not in rsonly))

            dmaster = datas[dts.index(dt0)]  # and timemaster
            self._dtmaster = dmaster.num2date(dt0)
            self._udtmaster = num2date(dt0)

            # slen = len(runstrats[0])
            # Try to get something for those that didn't return
            for i, ret in enumerate(drets):
                if ret:  # dts already contains a valid datetime for this i
                    continue

                # try to get a data by checking with a master
                d = datas[i]
                d._check(forcedata=dmaster)  # check to force output
                if d.next(datamaster=dmaster, ticks=False):  # retry
                    dts[i] = d.datetime[0]  # good -> store
                    # self._plotfillers2[i].append(slen)  # mark as fill
                else:
                    # self._plotfillers[i].append(slen)  # mark as empty
                    pass

            # make sure only those at dmaster level end up delivering
            for i, dti in enumerate(dts):
                if dti is not None:
                    di = datas[i]
                    rpi = False and di.replaying  # to check behavior
                    if dti > dt0:
                        if not rpi:  # must see all ticks ...
                            di.rewind()  # cannot deliver yet
                        # self._plotfillers[i].append(slen)
                    elif not di.replaying:
                        # Replay forces tick fill, else force here
                        di._tick_fill(force=True)

                    # self._plotfillers2[i].append(slen)  # mark as fill

        elif d0ret is None:
            # meant for things like live feeds which may not produce a bar
            # at the moment but need the loop to run for notifications and
            # getting resample and others to produce timely bars
            for data in datas:
                data._check()
        else:
            lastret = data0._last()
            for data in datas1:
                lastret += data._last(datamaster=data0)

            if not lastret:
                # Only go extra round if something was changed by "lasts"
                return True  # return somethin signaling the end

        # Datas may have generated a new notification after next
        self._datanotify()
        if self._event_stop:  # stop if requested
            return True

        if d0ret or lastret:  # if any bar, check timers before broker
            self._check_timers(runstrats, dt0, cheat=True)
            if self.p.cheat_on_open:
                for strat in runstrats:
                    strat._next_open()
                    if self._event_stop:  # stop if requested
                        return True

        self._brokernotify()
        if self._event_stop:  # stop if requested
            return True

        if d0ret or lastret:  # bars produced by data or filters
            self._check_timers(runstrats, dt0, cheat=False)
            for strat in runstrats:
                strat._next()
                if self._event_stop:  # stop if requested
                    return True

                self._next_writers(runstrats)

        self.bt_state_container = {"datas": datas,
                                   "datas1": datas1,
                                   "data0": data0,
                                   "d0ret": d0ret,
                                   "rsonly": rsonly,
                                   "onlyresample": onlyresample,
                                   "noresample": noresample,
                                   "ldatas_noclones": ldatas_noclones,
                                   "dt0": dt0,
                                   }

        return False



if __name__ == '__main__':
    from pathlib import Path

    root = Path().absolute()
    file = "BNB_USDT_5m.csv"
    df = pd.read_csv(Path(root, file), index_col=0)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp", drop=True)
    data = bt.feeds.PandasData(dataname=df)

    cerebro = BTEngine()
    cerebro.adddata(data)

    from engine.rl.strategy_rl import BaseStrategy, PositionBasedStrategy
    cerebro.addstrategy(PositionBasedStrategy)
    #cerebro.run()
    cerebro.reset()
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    observation, reward, terminated = cerebro.step()

    terminated = False

    rewards = []

    while not terminated:
        observation, reward, terminated = cerebro.step()
        print(cerebro.datas[0][0])

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
