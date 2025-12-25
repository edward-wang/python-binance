"""
Centralized type declaration module - provides type hints for async mixins

This module defines the AsyncClientCoreLike Protocol, used in TYPE_CHECKING mode
to provide type hints for various mixins, eliminating Pyright attribute errors.

This module is not imported at runtime, only used for static type checking.
"""
from typing import Protocol, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List, Tuple, AsyncIterator


class AsyncClientCoreLike(Protocol):
    """
    Protocol declaration for AsyncClientCore
    
    This Protocol declares all methods and attributes that mixins depend on,
    allowing Pyright to recognize the existence of these members.
    """

    # Request methods - from AsyncClientCore
    async def _request_api(
        self,
        method: str,
        path: str,
        signed: bool = False,
        version: str = "v3",
        **kwargs: Any,
    ) -> Dict[str, Any]: ...

    async def _request_futures_api(
        self, method: str, path: str, signed: bool = False, version: int = 1, **kwargs: Any
    ) -> Dict[str, Any]: ...

    async def _request_futures_data_api(
        self, method: str, path: str, signed: bool = False, **kwargs: Any
    ) -> Dict[str, Any]: ...

    async def _request_futures_coin_api(
        self, method: str, path: str, signed: bool = False, version: int = 1, **kwargs: Any
    ) -> Dict[str, Any]: ...

    async def _request_futures_coin_data_api(
        self, method: str, path: str, signed: bool = False, version: int = 1, **kwargs: Any
    ) -> Dict[str, Any]: ...

    async def _request_margin_api(
        self, method: str, path: str, signed: bool = False, version: int = 1, **kwargs: Any
    ) -> Dict[str, Any]: ...

    async def _request_options_api(
        self, method: str, path: str, signed: bool = False, **kwargs: Any
    ) -> Dict[str, Any]: ...

    async def _request_papi_api(
        self, method: str, path: str, signed: bool = False, version: int = 1, **kwargs: Any
    ) -> Dict[str, Any]: ...

    async def _request_website(
        self, method: str, path: str, signed: bool = False, **kwargs: Any
    ) -> Dict[str, Any]: ...

    async def _get(
        self, path: str, signed: bool = False, version: str = "v3", **kwargs: Any
    ) -> Dict[str, Any]: ...

    async def _post(
        self, path: str, signed: bool = False, version: str = "v3", **kwargs: Any
    ) -> Dict[str, Any]: ...

    async def _put(
        self, path: str, signed: bool = False, version: str = "v3", **kwargs: Any
    ) -> Dict[str, Any]: ...

    async def _delete(
        self, path: str, signed: bool = False, version: str = "v3", **kwargs: Any
    ) -> Dict[str, Any]: ...

    # Spot methods - implemented by AsyncSpotMixin
    async def create_oco_order(self, **params: Any) -> Dict[str, Any]: ...

    # Futures methods - implemented by AsyncFuturesUmMixin / AsyncFuturesCmMixin
    async def futures_klines(self, **params: Any) -> Dict[str, Any]: ...
    async def futures_coin_klines(self, **params: Any) -> Dict[str, Any]: ...
    async def futures_mark_price_klines(self, **params: Any) -> Dict[str, Any]: ...
    async def futures_index_price_klines(self, **params: Any) -> Dict[str, Any]: ...
    async def futures_coin_mark_price_klines(self, **params: Any) -> Dict[str, Any]: ...
    async def futures_coin_index_price_klines(self, **params: Any) -> Dict[str, Any]: ...

    # WebSocket API methods - from BaseClient
    async def _ws_api_request(
        self, method: str, signed: bool, params: Dict[str, Any]
    ) -> Dict[str, Any]: ...

    async def _ws_futures_api_request(
        self, method: str, signed: bool, params: Dict[str, Any]
    ) -> Dict[str, Any]: ...

    # Utility methods - from BaseClient (static methods)
    @staticmethod
    def uuid22(length: int = 22) -> str: ...

    # Constants - from BaseClient
    # BaseClient attributes used by mixins
    tld: str

    SPOT_ORDER_PREFIX: str
    CONTRACT_ORDER_PREFIX: str
    ORDER_TYPE_LIMIT: str
    ORDER_TYPE_MARKET: str
    SIDE_BUY: str
    SIDE_SELL: str

    AGG_ID: str
    AGG_PRICE: str
    AGG_QUANTITY: str
    AGG_FIRST_TRADE_ID: str
    AGG_LAST_TRADE_ID: str
    AGG_TIME: str
    AGG_BUYER_MAKES: str
    AGG_BEST_MATCH: str

    # Historical klines helpers - implemented by AsyncClient / AsyncSpotMixin
    async def _historical_klines(
        self,
        symbol: str,
        interval: str,
        start_str: "Optional[str]" = None,
        end_str: "Optional[str]" = None,
        limit: "Optional[int]" = None,
        klines_type: Any = ...,
    ) -> Any: ...

    def _historical_klines_generator(
        self,
        symbol: str,
        interval: str,
        start_str: "Optional[str]" = None,
        end_str: "Optional[str]" = None,
        limit: int = 1000,
        klines_type: Any = ...,
    ) -> "AsyncIterator[Any]": ...

    # Order helper - implemented by BaseClient
    @staticmethod
    def _order_params(data: Dict[str, Any]) -> "List[Tuple[str, str]]": ...

