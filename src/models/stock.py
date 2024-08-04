from typing import Optional


class Stock:
    def __init__(self, **data):
        self.stock_name: str = self._validate_string(data["stock_name"])
        self.price: int = self._parse_int(data["price"])
        self.previous_day: int = self._parse_int(data["previous_day"])
        self.opening_price: int = self._parse_int(data["opening_price"])
        self.high_price: int = self._parse_int(data["high_price"])
        self.low_price: int = self._parse_int(data["low_price"])
        self.market_cap: int = self._parse_int(data["market_cap"])
        self.trading_volume: str = self._validate_string(data["trading_volume"])
        self.trading_value: str = self._validate_string(data["trading_value"])
        self.foreign_ownership_ratio: float = self._parse_percentage(
            data["foreign_ownership_ratio"]
        )
        self.fifty_two_week_high: int = self._parse_int(data["fifty_two_week_high"])
        self.fifty_two_week_low: int = self._parse_int(data["fifty_two_week_low"])
        self.per: Optional[float] = self._parse_optional_ratio(data["per"])
        self.eps: int = self._parse_int(data["eps"])
        self.forward_per: float = self._parse_ratio(data["forward_per"])
        self.forward_eps: int = self._parse_int(data["forward_eps"])
        self.pbr: float = self._parse_ratio(data["pbr"])
        self.bps: int = self._parse_int(data["bps"])
        self.dividend_yield: Optional[float] = self._parse_optional_percentage(
            data["dividend_yield"]
        )
        self.expected_dividend_yield: Optional[int] = self._parse_optional_int(
            data["expected_dividend_yield"]
        )

    @staticmethod
    def _validate_string(value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Invalid string value")
        return value.strip()

    @staticmethod
    def _parse_int(value: str) -> int:
        try:
            return int(value.replace(",", "").replace("원", ""))
        except ValueError:
            raise ValueError(f"Cannot parse integer from: {value}")

    @staticmethod
    def _parse_percentage(value: str) -> float:
        try:
            return float(value.rstrip("%"))
        except ValueError:
            raise ValueError(f"Cannot parse percentage from: {value}")

    @staticmethod
    def _parse_ratio(value: str) -> float:
        try:
            return float(value.rstrip("배"))
        except ValueError:
            raise ValueError(f"Cannot parse ratio from: {value}")

    @staticmethod
    def _parse_optional_ratio(value: str) -> Optional[float]:
        if value == "N/A":
            return None
        return Stock._parse_ratio(value)

    @staticmethod
    def _parse_optional_percentage(value: str) -> Optional[float]:
        if value == "N/A":
            return None
        return Stock._parse_percentage(value)

    @staticmethod
    def _parse_optional_int(value: str) -> Optional[int]:
        if value == "N/A":
            return None
        return Stock._parse_int(value)

    def __repr__(self):
        return f"Stock(name={self.stock_name}, price={self.price})"

    def to_dict(self):
        return {
            "stock_name": self.stock_name,
            "price": self.price,
            "previous_day": self.previous_day,
            "opening_price": self.opening_price,
            "high_price": self.high_price,
            "low_price": self.low_price,
            "market_cap": self.market_cap,
            "trading_volume": self.trading_volume,
            "trading_value": self.trading_value,
            "foreign_ownership_ratio": self.foreign_ownership_ratio,
            "fifty_two_week_high": self.fifty_two_week_high,
            "fifty_two_week_low": self.fifty_two_week_low,
            "per": self.per,
            "eps": self.eps,
            "forward_per": self.forward_per,
            "forward_eps": self.forward_eps,
            "pbr": self.pbr,
            "bps": self.bps,
            "dividend_yield": self.dividend_yield,
            "expected_dividend_yield": self.expected_dividend_yield,
        }
