from dataclasses import dataclass

@dataclass
class QuantData:
    stock: str
    quant_type: str
    initial_price: float
    initial_trend_follow: float
    initial_status: str