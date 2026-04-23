from base import BaseTest
from massive.rest.models.aggs import Agg
from massive.rest.models.indicators import (
    SingleIndicatorResults,
    SMAIndicatorResults,
    EMAIndicatorResults,
    RSIIndicatorResults,
    MACDIndicatorResults,
    IndicatorValue,
    MACDIndicatorValue,
    IndicatorUnderlying,
)


class IndicatorsTest(BaseTest):
    def test_get_sma_indicators(self):
        indicators = self.c.get_sma(
            ticker="AAPL",
            window=30,
            timespan="quarter",
            timestamp="1483958600",
            expand_underlying=True,
        )
        expected = SMAIndicatorResults(
            values=[
                IndicatorValue(timestamp=1578027600, value=141.34),
                IndicatorValue(timestamp=1578035600, value=139.33),
                IndicatorValue(timestamp=1578049600, value=138.22),
            ],
            underlying=IndicatorUnderlying(
                url="https://api.massive.com/v2/aggs/ticker/AAPL/range/1/day/1626912000000/1629590400000?adjusted=true&limit=50000&sort=desc",
                aggregates=[
                    Agg(
                        open=74.06,
                        high=75.15,
                        low=73.7975,
                        close=75.0875,
                        volume=135647456,
                        vwap=74.6099,
                        timestamp=1577941200000,
                        transactions=1,
                        otc=None,
                    ),
                    Agg(
                        open=74.2875,
                        high=75.145,
                        low=74.125,
                        close=74.3575,
                        volume=146535512,
                        vwap=74.7026,
                        timestamp=1578027600000,
                        transactions=1,
                        otc=None,
                    ),
                ],
            ),
        )
        self.assertEqual(indicators, expected)

    def test_get_ema_indicators(self):
        indicators = self.c.get_ema(
            ticker="AAPL",
            timestamp_lte="1478393873000",
            window=5,
            adjusted=False,
            timestamp_gte="1477972800000",
        )

        expected = EMAIndicatorResults(
            values=[
                IndicatorValue(timestamp=1478232000000, value=110.96883950617286),
                IndicatorValue(timestamp=1478145600000, value=112.03325925925927),
                IndicatorValue(timestamp=1478059200000, value=113.1348888888889),
                IndicatorValue(timestamp=1477972800000, value=113.90733333333334),
            ],
            underlying=IndicatorUnderlying(
                url="http://localhost:8081/v2/aggs/ticker/AAPL/range/1/day/1477368000000/1478393873000?adjusted=false&limit=50000&sort=desc",
                aggregates=[],
            ),
        )

        self.assertEqual(indicators, expected)

    def test_get_macd_indicators(self):
        indicators = self.c.get_macd(
            ticker="SPY",
            signal_window=10,
            long_window=20,
            timestamp_gt="2022-08-09",
        )

        expected = MACDIndicatorResults(
            values=[
                MACDIndicatorValue(
                    timestamp=1660881600000,
                    value=6.912856964275647,
                    signal=49.504484615884834,
                    histogram=-42.59162765160919,
                ),
                MACDIndicatorValue(
                    timestamp=1660795200000,
                    value=7.509881940545313,
                    signal=58.96929076068688,
                    histogram=-51.45940882014157,
                ),
                MACDIndicatorValue(
                    timestamp=1660708800000,
                    value=7.734132135566654,
                    signal=70.40471494294057,
                    histogram=-62.67058280737392,
                ),
                MACDIndicatorValue(
                    timestamp=1660622400000,
                    value=7.973958808765531,
                    signal=84.331511122357,
                    histogram=-76.35755231359147,
                ),
                MACDIndicatorValue(
                    timestamp=1660536000000,
                    value=7.90112075397235,
                    signal=101.2998560809329,
                    histogram=-93.39873532696055,
                ),
                MACDIndicatorValue(
                    timestamp=1660276800000,
                    value=7.719066821080332,
                    signal=122.05513059803525,
                    histogram=-114.33606377695492,
                ),
                MACDIndicatorValue(
                    timestamp=1660190400000,
                    value=7.468267821253335,
                    signal=147.4631447706919,
                    histogram=-139.99487694943858,
                ),
                MACDIndicatorValue(
                    timestamp=1660104000000,
                    value=7.542041992364375,
                    signal=178.5731174261227,
                    histogram=-171.03107543375833,
                ),
            ],
            underlying=IndicatorUnderlying(
                url="http://localhost:8081/v2/aggs/ticker/SPY/range/1/day/1657670400000/1660926503659?limit=50000&sort=desc",
                aggregates=[],
            ),
        )

        self.assertEqual(indicators, expected)

    def test_get_rsi_indicators(self):
        indicators = self.c.get_rsi(
            ticker="AAPL",
            window=20,
            timespan="minute",
            adjusted=True,
            timestamp_gt="2022-08-18",
        )

        expected = RSIIndicatorResults(
            values=[
                IndicatorValue(timestamp=1660928400000, value=172.46568754351864),
                IndicatorValue(timestamp=1660927500000, value=172.43049675862588),
                IndicatorValue(timestamp=1660926600000, value=172.39791747006018),
                IndicatorValue(timestamp=1660925700000, value=172.37032983532967),
                IndicatorValue(timestamp=1660924800000, value=172.39246981799596),
                IndicatorValue(timestamp=1660923900000, value=172.4199719041008),
                IndicatorValue(timestamp=1660923000000, value=172.4462847361114),
                IndicatorValue(timestamp=1660922100000, value=172.48168312938628),
                IndicatorValue(timestamp=1660921200000, value=172.5318603009006),
                IndicatorValue(timestamp=1660920300000, value=172.60100349046908),
                IndicatorValue(timestamp=1660919400000, value=172.68216175262373),
                IndicatorValue(timestamp=1660918500000, value=172.7343682528999),
                IndicatorValue(timestamp=1660917600000, value=172.7937754374157),
                IndicatorValue(timestamp=1660916700000, value=172.8239623255647),
                IndicatorValue(timestamp=1660915800000, value=172.82964257036102),
                IndicatorValue(timestamp=1660914900000, value=172.8215102093464),
                IndicatorValue(timestamp=1660914000000, value=172.7816691787513),
                IndicatorValue(timestamp=1660913100000, value=172.79237119756723),
                IndicatorValue(timestamp=1660912200000, value=172.8094629025743),
                IndicatorValue(timestamp=1660911300000, value=172.82942741863474),
                IndicatorValue(timestamp=1660910400000, value=172.85463030480682),
                IndicatorValue(timestamp=1660909500000, value=172.88038086320753),
                IndicatorValue(timestamp=1660908600000, value=172.91094726986097),
                IndicatorValue(timestamp=1660907700000, value=172.95420487721478),
                IndicatorValue(timestamp=1660906800000, value=172.99148960113214),
                IndicatorValue(timestamp=1660905900000, value=173.03796219072498),
                IndicatorValue(timestamp=1660905000000, value=173.0998529476434),
                IndicatorValue(timestamp=1660904100000, value=173.17457431055323),
                IndicatorValue(timestamp=1660903200000, value=173.23505581692726),
                IndicatorValue(timestamp=1660902300000, value=173.3166406397617),
                IndicatorValue(timestamp=1660901400000, value=173.3920764965787),
                IndicatorValue(timestamp=1660900500000, value=173.4628213909554),
                IndicatorValue(timestamp=1660899600000, value=173.5494341689507),
                IndicatorValue(timestamp=1660898700000, value=173.63884829199816),
                IndicatorValue(timestamp=1660897800000, value=173.73872705957692),
                IndicatorValue(timestamp=1660896900000, value=173.8480667500587),
                IndicatorValue(timestamp=1660896000000, value=173.97207377638065),
            ],
            underlying=IndicatorUnderlying(
                url="https://api.massive.com/v2/aggs/ticker/AAPL/range/15/minute/1660521600000/1660928746001?limit=50000&sort=desc",
                aggregates=[],
            ),
        )

        self.assertEqual(indicators, expected)
