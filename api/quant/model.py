from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class QuantData:
    stock: str
    quant_type: str
    initial_price: float
    initial_trend_follow: float
    initial_status: str

@dataclass
class RebalancingRecommendation:
    date: str
    recommendation: str
    returns: Dict[str, float]
    best_return: float
    cash_return: float
    should_rebalance: bool
    error: Optional[str] = None