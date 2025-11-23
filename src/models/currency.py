"""Currency and currency pair models."""

from enum import Enum
from dataclasses import dataclass


class Currency(str, Enum):
    """Supported currencies."""
    
    EUR = "EUR"
    USD = "USD"
    JPY = "JPY"
    
    @classmethod
    def from_string(cls, value: str) -> "Currency":
        """Create Currency from string (case-insensitive).
        
        Args:
            value: Currency code (e.g., 'eur', 'EUR', 'usd')
            
        Returns:
            Currency enum value
            
        Raises:
            ValueError: If currency code is not supported
        """
        value_upper = value.upper()
        try:
            return cls[value_upper]
        except KeyError:
            raise ValueError(f"Unsupported currency: {value}. Supported: {', '.join([c.value for c in cls])}")


@dataclass(frozen=True)
class CurrencyPair:
    """Currency pair (e.g., EUR/USD)."""
    
    base: Currency
    quote: Currency
    
    def __post_init__(self):
        """Validate that base and quote currencies are different."""
        if self.base == self.quote:
            raise ValueError(f"Base and quote currencies must be different: {self.base}")
    
    def __str__(self) -> str:
        """String representation (e.g., 'EUR/USD')."""
        return f"{self.base.value}/{self.quote.value}"
    
    def __repr__(self) -> str:
        """Developer representation."""
        return f"CurrencyPair(base={self.base.value}, quote={self.quote.value})"
    
    def to_slash_format(self) -> str:
        """Return pair in slash format (e.g., 'EUR/USD')."""
        return f"{self.base.value}/{self.quote.value}"
    
    def to_underscore_format(self) -> str:
        """Return pair in underscore format (e.g., 'eur_usd')."""
        return f"{self.base.value.lower()}_{self.quote.value.lower()}"
    
    @classmethod
    def from_string(cls, pair_string: str) -> "CurrencyPair":
        """Create CurrencyPair from string.
        
        Args:
            pair_string: Pair string like 'EUR/USD', 'eur_usd', 'eur/usd', or 'EURUSD'
            
        Returns:
            CurrencyPair instance
            
        Examples:
            >>> CurrencyPair.from_string("EUR/USD")
            CurrencyPair(base=EUR, quote=USD)
            >>> CurrencyPair.from_string("eur_usd")
            CurrencyPair(base=EUR, quote=USD)
            >>> CurrencyPair.from_string("eurusd")
            CurrencyPair(base=EUR, quote=USD)
        """
        pair_string = pair_string.upper().replace("/", "").replace("-", "").replace("_", "")
        
        if len(pair_string) != 6:
            raise ValueError(f"Invalid currency pair format: {pair_string}. Expected format: 'EUR/USD' or 'EURUSD'")
        
        base_str = pair_string[:3]
        quote_str = pair_string[3:]
        
        base = Currency.from_string(base_str)
        quote = Currency.from_string(quote_str)
        
        return cls(base=base, quote=quote)
    
    def inverse(self) -> "CurrencyPair":
        """Get the inverse pair (e.g., EUR/USD -> USD/EUR)."""
        return CurrencyPair(base=self.quote, quote=self.base)
