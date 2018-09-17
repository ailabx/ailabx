class Algo(object):
    def __init__(self, name=None):
        self._name = name

    @property
    def name(self):
        if self._name is None:
            self._name = self.__class__.__name__
        return self._name

    def __call__(self, target):
        raise NotImplementedError("%s not implemented!" % self.name)

from .common.logging_utils import logger
class AlgoStack(Algo):

    def __init__(self, *algos):
        super(AlgoStack, self).__init__()
        self.algos = algos
        self.check_run_always = any(hasattr(x, 'run_always')
                                    for x in self.algos)

    def __call__(self, target):
        # normal runing mode
        if not self.check_run_always:
            for algo in self.algos:
                if not algo(target):
                    return False
            return True
        # run mode when at least one algo has a run_always attribute
        else:
            # store result in res
            # allows continuation to check for and run
            # algos that have run_always set to True
            res = True
            for algo in self.algos:
                if res:
                    res = algo(target)
                elif hasattr(algo, 'run_always'):
                    if algo.run_always:
                        algo(target)
            return res

class PrintDate(Algo):

    def __call__(self, target):
        logger.info('当前idx:{}'.format(target.idx))
        return True

class RunOnce(Algo):
    def __init__(self):
        super(RunOnce, self).__init__()
        self.has_run = False

    def __call__(self, target):
        # if it hasn't run then we will
        # run it and set flag
        if not self.has_run:
            self.has_run = True
            return True

        # return false to stop future execution
        return False


class SelectAll(Algo):
    def __init__(self, include_no_data=False):
        super(SelectAll, self).__init__()
        self.include_no_data = include_no_data

    def __call__(self, target,direction='LONG'):
        target.context[direction] = target.context['universe']
        return True

class SelectWhere(Algo):

    """
    Selects securities based on an indicator DataFrame.

    Selects securities where the value is True on the current date
    (target.now) only if current date is present in signal DataFrame.

    For example, this could be the result of a pandas boolean comparison such
    as data > 100.

    Args:
        * signal (DataFrame): Boolean DataFrame containing selection logic.

    Sets:
        * selected

    """

    def __init__(self, signal):
        self.signal = signal #df:['AAPL':[1,0,-1],'AMZN':[...]]

    def __call__(self, target):

        #这里得到某一天的信号，是一个Series, index = ['AAPL'...]
        day_signal = self.signal.loc[target.now]

        #LONG or FLAT
        day_signal_long = day_signal[day_signal==1]
        day_signal_flat = day_signal[day_signal == -1]

        #按方向过滤完信号后，取索引就是证券代码列表
        selected = day_signal.index
        target.context['LONG'] = list(day_signal_long.index)
        target.context['FLAT'] = list(day_signal_flat.index)

        return True

class WeighEqually(Algo):
    def __init__(self):
        super(WeighEqually, self).__init__()

    def __call__(self, target):
        #FLAT不用权重，这个列表里的都平仓，rebalance会自动处理
        selected = target.context['LONG']
        n = len(selected)

        if n == 0:
            target.context['weights'] = {}
        else:
            w = 1.0 / n
            target.context['weights'] = {x: w for x in selected}

        return True

class Rebalance(Algo):

    """
    Rebalances capital based on temp['weights']

    Rebalances capital based on temp['weights']. Also closes
    positions if open but not in target_weights. This is typically
    the last Algo called once the target weights have been set.

    Requires:
        * weights
        * cash (optional): You can set a 'cash' value on temp. This should be a
            number between 0-1 and determines the amount of cash to set aside.
            For example, if cash=0.3, the strategy will allocate 70% of its
            value to the provided weights, and the remaining 30% will be kept
            in cash. If this value is not provided (default), the full value
            of the strategy is allocated to securities.

    """

    def __init__(self):
        super(Rebalance, self).__init__()

    def __call__(self, target):
        if 'weights' not in target.context:
            return True

        weights = target.context['weights']

        target.rebalance(weights)
        return True