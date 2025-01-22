from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ChangeType(Enum):
    NEW_ENTRY = "NEW_ENTRY"
    EXIT = "EXIT"
    INCREASED = "INCREASED"
    DECREASED = "DECREASED"
    NO_CHANGE = "NO_CHANGE"


@dataclass
class SecurityMetrics:
    quantity: float
    market_value: float
    nav_percentage: float
    industry: str


@dataclass
class SecurityChange:
    change_type: ChangeType
    old_metrics: Optional[SecurityMetrics]
    new_metrics: Optional[SecurityMetrics]
    percentage_change: float
    value_change: float
