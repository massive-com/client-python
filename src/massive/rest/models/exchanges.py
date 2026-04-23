from typing import Optional
from ...modelclass import modelclass


@modelclass
class Exchange:
    "Exchange contains data for a condition that Massive.com uses."
    acronym: Optional[str] = None
    asset_class: Optional[str] = None
    id: Optional[int] = None
    locale: Optional[str] = None
    mic: Optional[str] = None
    name: Optional[str] = None
    operating_mic: Optional[str] = None
    participant_id: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return Exchange(**d)
