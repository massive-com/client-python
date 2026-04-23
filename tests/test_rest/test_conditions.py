from massive.rest.models import (
    Condition,
    SipMapping,
    UpdateRules,
    Consolidated,
    MarketCenter,
)
from base import BaseTest


class ConditionsTest(BaseTest):
    def test_list_conditions(self):
        conditions = [c for c in self.c.list_conditions("stocks")]
        expected = [
            Condition(
                abbreviation=None,
                asset_class="stocks",
                data_types=["trade"],
                description=None,
                exchange=None,
                id=1,
                legacy=None,
                name="Acquisition",
                sip_mapping=SipMapping(CTA=None, OPRA=None, UTP="A"),
                type="sale_condition",
                update_rules=UpdateRules(
                    consolidated=Consolidated(
                        updates_high_low=True,
                        updates_open_close=True,
                        updates_volume=True,
                    ),
                    market_center=MarketCenter(
                        updates_high_low=True,
                        updates_open_close=True,
                        updates_volume=True,
                    ),
                ),
            ),
            Condition(
                abbreviation=None,
                asset_class="stocks",
                data_types=["trade"],
                description=None,
                exchange=None,
                id=2,
                legacy=None,
                name="Average Price Trade",
                sip_mapping=SipMapping(CTA="B", OPRA=None, UTP="W"),
                type="sale_condition",
                update_rules=UpdateRules(
                    consolidated=Consolidated(
                        updates_high_low=False,
                        updates_open_close=False,
                        updates_volume=True,
                    ),
                    market_center=MarketCenter(
                        updates_high_low=False,
                        updates_open_close=False,
                        updates_volume=True,
                    ),
                ),
            ),
            Condition(
                abbreviation=None,
                asset_class="stocks",
                data_types=["trade"],
                description=None,
                exchange=None,
                id=3,
                legacy=None,
                name="Automatic Execution",
                sip_mapping=SipMapping(CTA="E", OPRA=None, UTP=None),
                type="sale_condition",
                update_rules=UpdateRules(
                    consolidated=Consolidated(
                        updates_high_low=True,
                        updates_open_close=True,
                        updates_volume=True,
                    ),
                    market_center=MarketCenter(
                        updates_high_low=True,
                        updates_open_close=True,
                        updates_volume=True,
                    ),
                ),
            ),
            Condition(
                abbreviation=None,
                asset_class="stocks",
                data_types=["trade"],
                description=None,
                exchange=None,
                id=4,
                legacy=None,
                name="Bunched Trade",
                sip_mapping=SipMapping(CTA=None, OPRA=None, UTP="B"),
                type="sale_condition",
                update_rules=UpdateRules(
                    consolidated=Consolidated(
                        updates_high_low=True,
                        updates_open_close=True,
                        updates_volume=True,
                    ),
                    market_center=MarketCenter(
                        updates_high_low=True,
                        updates_open_close=True,
                        updates_volume=True,
                    ),
                ),
            ),
            Condition(
                abbreviation=None,
                asset_class="stocks",
                data_types=["trade"],
                description=None,
                exchange=None,
                id=5,
                legacy=None,
                name="Bunched Sold Trade",
                sip_mapping=SipMapping(CTA=None, OPRA=None, UTP="G"),
                type="sale_condition",
                update_rules=UpdateRules(
                    consolidated=Consolidated(
                        updates_high_low=True,
                        updates_open_close=False,
                        updates_volume=True,
                    ),
                    market_center=MarketCenter(
                        updates_high_low=True,
                        updates_open_close=False,
                        updates_volume=True,
                    ),
                ),
            ),
            Condition(
                abbreviation=None,
                asset_class="stocks",
                data_types=["trade"],
                description=None,
                exchange=None,
                id=6,
                legacy=True,
                name="CAP Election",
                sip_mapping=SipMapping(CTA="I", OPRA=None, UTP=None),
                type="sale_condition",
                update_rules=UpdateRules(
                    consolidated=Consolidated(
                        updates_high_low=True,
                        updates_open_close=True,
                        updates_volume=True,
                    ),
                    market_center=MarketCenter(
                        updates_high_low=True,
                        updates_open_close=True,
                        updates_volume=True,
                    ),
                ),
            ),
            Condition(
                abbreviation=None,
                asset_class="stocks",
                data_types=["trade"],
                description=None,
                exchange=None,
                id=7,
                legacy=None,
                name="Cash Sale",
                sip_mapping=SipMapping(CTA="C", OPRA=None, UTP="C"),
                type="sale_condition",
                update_rules=UpdateRules(
                    consolidated=Consolidated(
                        updates_high_low=False,
                        updates_open_close=False,
                        updates_volume=True,
                    ),
                    market_center=MarketCenter(
                        updates_high_low=False,
                        updates_open_close=False,
                        updates_volume=True,
                    ),
                ),
            ),
            Condition(
                abbreviation=None,
                asset_class="stocks",
                data_types=["trade"],
                description=None,
                exchange=None,
                id=8,
                legacy=None,
                name="Closing Prints",
                sip_mapping=SipMapping(CTA=None, OPRA=None, UTP="6"),
                type="sale_condition",
                update_rules=UpdateRules(
                    consolidated=Consolidated(
                        updates_high_low=True,
                        updates_open_close=True,
                        updates_volume=True,
                    ),
                    market_center=MarketCenter(
                        updates_high_low=True,
                        updates_open_close=True,
                        updates_volume=True,
                    ),
                ),
            ),
            Condition(
                abbreviation=None,
                asset_class="stocks",
                data_types=["trade"],
                description=None,
                exchange=None,
                id=9,
                legacy=None,
                name="Cross Trade",
                sip_mapping=SipMapping(CTA="X", OPRA=None, UTP="X"),
                type="sale_condition",
                update_rules=UpdateRules(
                    consolidated=Consolidated(
                        updates_high_low=True,
                        updates_open_close=True,
                        updates_volume=True,
                    ),
                    market_center=MarketCenter(
                        updates_high_low=True,
                        updates_open_close=True,
                        updates_volume=True,
                    ),
                ),
            ),
            Condition(
                abbreviation=None,
                asset_class="stocks",
                data_types=["trade"],
                description=None,
                exchange=None,
                id=10,
                legacy=None,
                name="Derivatively Priced",
                sip_mapping=SipMapping(CTA="4", OPRA=None, UTP="4"),
                type="sale_condition",
                update_rules=UpdateRules(
                    consolidated=Consolidated(
                        updates_high_low=True,
                        updates_open_close=False,
                        updates_volume=True,
                    ),
                    market_center=MarketCenter(
                        updates_high_low=True,
                        updates_open_close=False,
                        updates_volume=True,
                    ),
                ),
            ),
        ]
        self.assertEqual(conditions, expected)
