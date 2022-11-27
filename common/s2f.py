#!/usr/bin/env python3

"""Show Stock-to-Flow values for Bitcoin."""

# Don't change tabbing, spacing, formating as file is automatically linted.
#
# Use this linter script:
#
# isort s2f.py
# flake8  --max-line-length 88 --max-doc-length 79 s2f.py
# python3 -m black s2f.py


import argparse
import datetime
import logging
import os
import re
import sys
import traceback

import requests


def infoFromBitcoinblockhalf(proxies):
    """Get Halving date from Bitcoinblockhalf."""
    url = "https://bitcoinblockhalf.com"
    cont = requests.get(url, proxies=proxies).content.decode()  # html
    logger.debug(f"cont {cont}")
    # HTML contains a line like this:
    # Reward-Drop ETA date: <strong>06 May 2024 19:26:00 UTC</strong>
    pattern = r"Reward-Drop ETA date: <strong>(.*?) ..:..:.. .*</strong>"
    m = re.search(pattern, cont)
    if m:
        next_halving_date = m.group(1)
    else:
        next_halving_date = "unknown"
    logger.debug(f"Estimate date of next halving: {next_halving_date}")
    return next_halving_date


def infoFromMessari(proxies):
    """Get data from Messari."""
    url = "https://data.messari.io/api/v1/assets/bitcoin/metrics"
    cont = requests.get(url, proxies=proxies).json()
    logger.debug(f"cont {cont}")
    fwd_stock_to_flow = cont["data"]["supply"]["stock_to_flow"]
    # conservative formula: 0.18 * s2f^3.3
    # aggressive formula:  exp(-1.84) * s2f^3.36
    # conservative gives slightly lower price
    # conservative formula: 0.18*s2f^3.3
    fwd_stock_to_flow_usd = 0.18 * fwd_stock_to_flow ** 3.3
    annual_inflation_percent = cont["data"]["supply"]["annual_inflation_percent"]
    circulating = cont["data"]["supply"]["circulating"]
    usd_price = cont["data"]["market_data"]["price_usd"]
    logger.debug(
        f"Data {fwd_stock_to_flow} {fwd_stock_to_flow_usd} "
        f"{annual_inflation_percent} {circulating}"
    )
    # example output: Data 54.73928728956236 98097.8891323435
    # 1.826841468925517 18410936.0981691
    return (
        float(usd_price),
        float(circulating),
        float(annual_inflation_percent),
        float(fwd_stock_to_flow),
        float(fwd_stock_to_flow_usd),
    )


def btcSupplyOnDate(date, proxies):
    """Provide BTC supply on a given date."""
    # API v2 depreciated in 2022
    # url = (
    #     "https://community-api.coinmetrics.io/"
    #     + "v2/assets/btc/metricdata?metrics=SplyCur&start="
    #     + str(date)
    #     + "&end="
    #     + str(date)
    # )
    #
    # HTTP API
    # https://docs.coinmetrics.io/api/v4#operation/getTimeseriesAssetMetrics
    # E.g.  get USD price for BTC:
    # https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?
    #    assets=btc&metrics=PriceUSD&frequency=1d&pretty=true&
    #    start_time=2022-01-10T00:00:00Z&end_time=2022-01-10T00:00:00Z
    # https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?
    #    assets=btc&metrics=SplyCur&frequency=1d&pretty=true&
    #    start_time=2022-01-10T00:00:00Z&end_time=2022-01-10T00:00:00Z
    url = (
        "https://community-api.coinmetrics.io/"
        + "v4/timeseries/asset-metrics?assets=btc&metrics=SplyCur&"
        + "frequency=1d&start_time="
        + str(date)
        + "&end_time="
        + str(date)
    )
    cont = requests.get(url, proxies=proxies).json()
    # JSON Response:
    #    {'data': [{'asset': 'btc', 'time': '2022-01-11T00:00:00.000000000Z',
    #               'SplyCur': '18926306.29127818'}]}
    logger.debug(
        f"API URL call: {url} \n"
        f"JSON Response: {cont}"
    )
    supply = cont["data"][0]["SplyCur"]
    return float(supply)


def infoFromCoinMetrics(period, proxies):
    """Compute Stock-to-Flow ratio and price."""
    dateYesterday = datetime.date.today() - datetime.timedelta(days=1)
    datePeriodInit = dateYesterday - datetime.timedelta(days=period)
    supplyYesterday = btcSupplyOnDate(dateYesterday, proxies)
    supplyPeriodAgo = btcSupplyOnDate(datePeriodInit, proxies)
    stock_to_flow_ratio = supplyPeriodAgo / (
        (supplyYesterday - supplyPeriodAgo) / period * 365
    )
    # conservative formula: 0.18*s2f^3.3, see comments above
    stock_to_flow_usd = 0.18 * stock_to_flow_ratio ** 3.3
    return stock_to_flow_ratio, stock_to_flow_usd


def s2f(args):
    """Compute and print the Stock-to-Flow ratio and price.
    For ratio the 463-day Stock-to-Flow is used. Why 463?
    See: https://twitter.com/digitaliknet/status/1270892084929626112?s=21
    It was 365 days in a past formula, then in June 2020 adjusted to 463 as
    463 is the value fitting the curve best
    """
    if args.tor:
        if os.name == "nt":
            TOR_PORT = 9150  # Windows
        else:
            TOR_PORT = 9050  # LINUX
        proxies = {
            "http": f"socks5://127.0.0.1:{TOR_PORT}",
            "https": f"socks5://127.0.0.1:{TOR_PORT}",
        }
        proxyindicator = " (via Tor)"
    else:
        proxies = {}
        proxyindicator = ""

    period = 463
    stock_to_flow_ratio, stock_to_flow_usd = infoFromCoinMetrics(period, proxies)
    (
        usd_price,
        circulating,
        annual_inflation_percent,
        fwd_stock_to_flow,
        fwd_stock_to_flow_usd,
    ) = infoFromMessari(proxies)

    if args.verbose:
        print(
            "Read about Stock-to-Flow here:    "
            "https://medium.com/@100trillionUSD/fficient-market-hypothesis-"
            "and-bitcoin-stock-to-flow-model-db17f40e6107"
        )
        print(
            "Compare with Stock-to-Flow data:  "
            "https://bitcoin.clarkmoody.com/dashboard/"
        )
        print("Compare with Stock-to-Flow graph: https://digitalik.net/btc/")

    if not args.terse:
        print(
            "Data sources:                     "
            f"messari.io and coinmetrics.io{proxyindicator}"
        )
        print(f"Calculated for date:              {datetime.date.today()}")
        print(f"Circulating BTC:                  {circulating:,.0f} BTC")
        print("Annual inflation:                 " f"{annual_inflation_percent:.2f} %")
        print(
            "Estimated next halving date:      " f"{infoFromBitcoinblockhalf(proxies)}"
        )
    if args.terse:
        labelForwRatio = "F/"
        labelForwPrice = "F$"
        labelBckwRatio = "B/"
        labelBckwPrice = "B$"
        labelCurrPrice = " $"
        labelDeviation = "D%"
    else:
        labelForwRatio = "Forward stock-to-flow ratio:     "
        labelForwPrice = "Forward stock-to-flow price:     "
        labelBckwRatio = str(period) + "-day Stock-to-flow ratio:     "
        labelBckwPrice = str(period) + "-day Stock-to-flow price:     "
        labelCurrPrice = "Current price:                   "
        labelDeviation = "Deviation of " + str(period) + "-day S2F price:  "
    print(f"{labelForwRatio} {fwd_stock_to_flow:.2f}")
    print(f"{labelForwPrice} {fwd_stock_to_flow_usd:,.0f} USD")
    print(f"{labelBckwRatio} {stock_to_flow_ratio:.2f}")
    print(f"{labelBckwPrice} {stock_to_flow_usd:,.0f} USD")
    print(f"{labelCurrPrice} {usd_price:,.0f} USD")
    print(
        f"{labelDeviation} "
        f"{(stock_to_flow_usd -usd_price) / stock_to_flow_usd * 100:,.2f} %"
    )


if __name__ == "__main__":
    logging.basicConfig()  # initialize root logger, a must
    if "DEBUG" in os.environ:
        logging.getLogger().setLevel(logging.DEBUG)  # set root logger log level
    else:
        logging.getLogger().setLevel(logging.INFO)  # set root logger log level

    # Construct the argument parser
    ap = argparse.ArgumentParser(
        description="This program prints Bitcoin Stock-to-Flow ratio and price"
    )
    # Add the arguments to the parser
    ap.add_argument(
        "-d",
        "--debug",
        required=False,
        action="store_true",
        help="Print debug information",
    )
    ap.add_argument(
        "-v",
        "--verbose",
        required=False,
        action="store_true",
        help="Print verbose output",
    )
    ap.add_argument(
        "-t",
        "--terse",
        required=False,
        action="store_true",
        help="Print only terse condensed output",
    )
    ap.add_argument(
        "-o",  # onion
        "--tor",
        required=False,
        action="store_true",
        help="Use Tor, go through Tor Socks5 proxy",
    )
    args = ap.parse_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)  # set root logger log level
        logging.getLogger().info("Debug is turned on.")
    logger = logging.getLogger("s2f")

    try:
        s2f(args)
    except requests.exceptions.ConnectionError:
        if args.tor:
            print("ConnectionError. Maybe Tor is not running.", file=sys.stderr)
        else:
            print(
                "ConnectionError. Maybe network connection is not down.",
                file=sys.stderr,
            )
        sys.exit(1)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)