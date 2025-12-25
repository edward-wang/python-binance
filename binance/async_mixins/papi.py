"""
AsyncPapiMixin - Portfolio Margin

This mixin contains all Portfolio Margin related methods.
"""
from typing import Dict, Any, Optional, TYPE_CHECKING

# This mixin depends on request methods provided by AsyncClientCore

if TYPE_CHECKING:
    from ._core_typing import AsyncClientCoreLike as _AsyncClientCoreLike
else:
    class _AsyncClientCoreLike:
        pass


class AsyncPapiMixin(_AsyncClientCoreLike):
    """
    Portfolio Margin API Mixin
    
    This mixin provides all Portfolio Margin related methods.
    These methods depend on request infrastructure provided by AsyncClientCore or ClientCore.
    """

    async def papi_stream_get_listen_key(self):
        res = await self._request_papi_api("post", "listenKey", signed=False, data={})
        return res["listenKey"]


    async def papi_stream_keepalive(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._request_papi_api(
            "put", "listenKey", signed=False, data=params
        )


    async def papi_stream_close(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._request_papi_api(
            "delete", "listenKey", signed=False, data=params
        )


    async def papi_get_balance(self, **params):
        return await self._request_papi_api("get", "balance", signed=True, data=params)


    async def papi_get_rate_limit(self, **params):
        return await self._request_papi_api(
            "get", "rateLimit/order", signed=True, data=params
        )


    async def papi_get_account(self, **params):
        return await self._request_papi_api("get", "account", signed=True, data=params)


    async def papi_get_margin_max_borrowable(self, **params):
        return await self._request_papi_api(
            "get", "margin/maxBorrowable", signed=True, data=params
        )


    async def papi_get_margin_max_withdraw(self, **params):
        return await self._request_papi_api(
            "get", "margin/maxWithdraw", signed=True, data=params
        )


    async def papi_get_um_position_risk(self, **params):
        return await self._request_papi_api(
            "get", "um/positionRisk", signed=True, data=params
        )


    async def papi_get_cm_position_risk(self, **params):
        return await self._request_papi_api(
            "get", "cm/positionRisk", signed=True, data=params
        )


    async def papi_set_um_leverage(self, **params):
        return await self._request_papi_api(
            "post", "um/leverage", signed=True, data=params
        )


    async def papi_set_cm_leverage(self, **params):
        return await self._request_papi_api(
            "post", "cm/leverage", signed=True, data=params
        )


    async def papi_change_um_position_side_dual(self, **params):
        return await self._request_papi_api(
            "post", "um/positionSide/dual", signed=True, data=params
        )


    async def papi_get_um_position_side_dual(self, **params):
        return await self._request_papi_api(
            "get", "um/positionSide/dual", signed=True, data=params
        )


    async def papi_get_cm_position_side_dual(self, **params):
        return await self._request_papi_api(
            "get", "cm/positionSide/dual", signed=True, data=params
        )


    async def papi_get_um_leverage_bracket(self, **params):
        return await self._request_papi_api(
            "get", "um/leverageBracket", signed=True, data=params
        )


    async def papi_get_cm_leverage_bracket(self, **params):
        return await self._request_papi_api(
            "get", "cm/leverageBracket", signed=True, data=params
        )


    async def papi_get_um_api_trading_status(self, **params):
        return await self._request_papi_api(
            "get", "um/apiTradingStatus", signed=True, data=params
        )


    async def papi_get_um_comission_rate(self, **params):
        return await self._request_papi_api(
            "get", "um/commissionRate", signed=True, data=params
        )


    async def papi_get_cm_comission_rate(self, **params):
        return await self._request_papi_api(
            "get", "cm/commissionRate", signed=True, data=params
        )


    async def papi_get_margin_margin_loan(self, **params):
        return await self._request_papi_api(
            "get", "margin/marginLoan", signed=True, data=params
        )


    async def papi_get_margin_repay_loan(self, **params):
        return await self._request_papi_api(
            "get", "margin/repayLoan", signed=True, data=params
        )


    async def papi_get_repay_futures_switch(self, **params):
        return await self._request_papi_api(
            "get", "repay-futures-switch", signed=True, data=params
        )


    async def papi_repay_futures_switch(self, **params):
        return await self._request_papi_api(
            "post", "repay-futures-switch", signed=True, data=params
        )


    async def papi_get_margin_interest_history(self, **params):
        return await self._request_papi_api(
            "get", "margin/marginInterestHistory", signed=True, data=params
        )


    async def papi_repay_futures_negative_balance(self, **params):
        return await self._request_papi_api(
            "post", "repay-futures-negative-balance", signed=True, data=params
        )


    async def papi_get_portfolio_interest_history(self, **params):
        return await self._request_papi_api(
            "get", "portfolio/interest-history", signed=True, data=params
        )


    async def papi_get_portfolio_negative_balance_exchange_record(self, **params):
        return await self._request_papi_api(
            "get",
            "portfolio/negative-balance-exchange-record",
            signed=True,
            data=params,
        )


    async def papi_fund_auto_collection(self, **params):
        return await self._request_papi_api(
            "post", "auto-collection", signed=True, data=params
        )


    async def papi_fund_asset_collection(self, **params):
        return await self._request_papi_api(
            "post", "asset-collection", signed=True, data=params
        )


    async def papi_bnb_transfer(self, **params):
        return await self._request_papi_api(
            "post", "bnb-transfer", signed=True, data=params
        )


    async def papi_get_um_income_history(self, **params):
        return await self._request_papi_api(
            "get", "um/income", signed=True, data=params
        )


    async def papi_get_cm_income_history(self, **params):
        return await self._request_papi_api(
            "get", "cm/income", signed=True, data=params
        )


    async def papi_get_um_account(self, **params):
        return await self._request_papi_api(
            "get", "um/account", signed=True, data=params
        )


    async def papi_get_um_account_v2(self, **params):
        return await self._request_papi_api(
            "get", "um/account", version=2, signed=True, data=params
        )


    async def papi_get_cm_account(self, **params):
        return await self._request_papi_api(
            "get", "cm/account", signed=True, data=params
        )


    async def papi_get_um_account_config(self, **params):
        return await self._request_papi_api(
            "get", "um/accountConfig", signed=True, data=params
        )


    async def papi_get_um_symbol_config(self, **params):
        return await self._request_papi_api(
            "get", "um/symbolConfig", signed=True, data=params
        )


    async def papi_get_um_trade_asyn(self, **params):
        return await self._request_papi_api(
            "get", "um/trade/asyn", signed=True, data=params
        )


    async def papi_get_um_trade_asyn_id(self, **params):
        return await self._request_papi_api(
            "get", "um/trade/asyn/id", signed=True, data=params
        )


    async def papi_get_um_order_asyn(self, **params):
        return await self._request_papi_api(
            "get", "um/order/asyn", signed=True, data=params
        )


    async def papi_get_um_order_asyn_id(self, **params):
        return await self._request_papi_api(
            "get", "um/order/asyn/id", signed=True, data=params
        )


    async def papi_get_um_income_asyn(self, **params):
        return await self._request_papi_api(
            "get", "um/income/asyn", signed=True, data=params
        )


    async def papi_get_um_income_asyn_id(self, **params):
        return await self._request_papi_api(
            "get", "um/income/asyn/id", signed=True, data=params
        )


    async def papi_ping(self, **params):
        return await self._request_papi_api("get", "ping", signed=False, data=params)

    # papi trading endpoints


    async def papi_create_um_order(self, **params):
        """Place new UM order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade

        :returns: API response

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_papi_api(
            "post", "um/order", signed=True, data=params
        )


    async def papi_create_um_conditional_order(self, **params):
        """Place new UM Conditional order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/New-UM-Conditional-Order

        :returns: API response

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_papi_api(
            "post", "um/conditional/order", signed=True, data=params
        )


    async def papi_create_cm_order(self, **params):
        """Place new CM order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/New-CM-Order

        :returns: API response

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_papi_api(
            "post", "cm/order", signed=True, data=params
        )


    async def papi_create_cm_conditional_order(self, **params):
        """Place new CM Conditional order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/New-CM-Conditional-Order

        :returns: API response

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_papi_api(
            "post", "cm/conditional/order", signed=True, data=params
        )


    async def papi_create_margin_order(self, **params):
        """New Margin Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/New-Margin-Order

        :returns: API response

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_papi_api(
            "post", "margin/order", signed=True, data=params
        )


    async def papi_margin_loan(self, **params):
        """Apply for a margin loan.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-Borrow

        :returns: API response

        """
        return await self._request_papi_api(
            "post", "marginLoan", signed=True, data=params
        )


    async def papi_repay_loan(self, **params):
        """Repay for a margin loan.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-Repay

        :returns: API response

        """
        return await self._request_papi_api(
            "post", "repayLoan", signed=True, data=params
        )


    async def papi_margin_order_oco(self, **params):
        """Send in a new OCO for a margin account.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-New-OCO

        :returns: API response

        """
        return await self._request_papi_api(
            "post", "margin/order/oco", signed=True, data=params
        )


    async def papi_cancel_um_order(self, **params):
        """Cancel an active UM LIMIT order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-UM-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "um/order", signed=True, data=params
        )


    async def papi_cancel_um_all_open_orders(self, **params):
        """Cancel an active UM LIMIT order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-All-UM-Open-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "um/allOpenOrders", signed=True, data=params
        )


    async def papi_cancel_um_conditional_order(self, **params):
        """Cancel UM Conditional Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-UM-Conditional-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "um/conditional/order", signed=True, data=params
        )


    async def papi_cancel_um_conditional_all_open_orders(self, **params):
        """Cancel All UM Open Conditional Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-All-UM-Open-Conditional-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "um/conditional/allOpenOrders", signed=True, data=params
        )


    async def papi_cancel_cm_order(self, **params):
        """Cancel an active CM LIMIT order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-CM-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "cm/order", signed=True, data=params
        )


    async def papi_cancel_cm_all_open_orders(self, **params):
        """Cancel an active CM LIMIT order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-All-CM-Open-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "cm/allOpenOrders", signed=True, data=params
        )


    async def papi_cancel_cm_conditional_order(self, **params):
        """Cancel CM Conditional Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-CM-Conditional-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "cm/conditional/order", signed=True, data=params
        )


    async def papi_cancel_cm_conditional_all_open_orders(self, **params):
        """Cancel All CM Open Conditional Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-All-CM-Open-Conditional-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "cm/conditional/allOpenOrders", signed=True, data=params
        )


    async def papi_cancel_margin_order(self, **params):
        """Cancel Margin Account Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-Margin-Account-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "margin/order", signed=True, data=params
        )


    async def papi_cancel_margin_order_list(self, **params):
        """Cancel Margin Account OCO Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-Margin-Account-OCO-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "margin/orderList", signed=True, data=params
        )


    async def papi_cancel_margin_all_open_orders(self, **params):
        """Cancel Margin Account All Open Orders on a Symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-Margin-Account-All-Open-Orders-on-a-Symbol

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "margin/allOpenOrders", signed=True, data=params
        )


    async def papi_modify_um_order(self, **params):
        """Order modify function, currently only LIMIT order modification is supported, modified orders will be reordered in the match queue.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Modify-UM-Order

        :returns: API response

        """
        return await self._request_papi_api("put", "um/order", signed=True, data=params)


    async def papi_modify_cm_order(self, **params):
        """Order modify function, currently only LIMIT order modification is supported, modified orders will be reordered in the match queue.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Modify-CM-Order

        :returns: API response

        """
        return await self._request_papi_api("put", "cm/order", signed=True, data=params)


    async def papi_get_um_order(self, **params):
        """Check an UM order's status.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-UM-Order

        :returns: API response

        """
        return await self._request_papi_api("get", "um/order", signed=True, data=params)


    async def papi_get_um_all_orders(self, **params):
        """Get all account UM orders; active, canceled, or filled.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-UM-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/allOrders", signed=True, data=params
        )


    async def papi_get_um_open_order(self, **params):
        """Query current UM open order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-UM-Open-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/openOrder", signed=True, data=params
        )


    async def papi_get_um_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Current-UM-Open-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/openOrders", signed=True, data=params
        )


    async def papi_get_um_conditional_all_orders(self, **params):
        """Query All UM Conditional Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-UM-Conditional-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/conditional/allOrders", signed=True, data=params
        )


    async def papi_get_um_conditional_open_orders(self, **params):
        """Get all open conditional orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Current-UM-Open-Conditional-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/conditional/openOrders", signed=True, data=params
        )


    async def papi_get_um_conditional_open_order(self, **params):
        """Query Current UM Open Conditional Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-UM-Open-Conditional-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/conditional/openOrder", signed=True, data=params
        )


    async def papi_get_um_conditional_order_history(self, **params):
        """Get all open conditional orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-UM-Conditional-Order-History

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/conditional/orderHistory", signed=True, data=params
        )


    async def papi_get_cm_order(self, **params):
        """Check an CM order's status.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-CM-Order

        :returns: API response

        """
        return await self._request_papi_api("get", "cm/order", signed=True, data=params)


    async def papi_get_cm_all_orders(self, **params):
        """Get all account CM orders; active, canceled, or filled.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-CM-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/allOrders", signed=True, data=params
        )


    async def papi_get_cm_open_order(self, **params):
        """Query current CM open order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-CM-Open-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/openOrder", signed=True, data=params
        )


    async def papi_get_cm_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Current-CM-Open-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/openOrders", signed=True, data=params
        )


    async def papi_get_cm_conditional_all_orders(self, **params):
        """Query All CM Conditional Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-CM-Conditional-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/conditional/allOrders", signed=True, data=params
        )


    async def papi_get_cm_conditional_open_orders(self, **params):
        """Get all open conditional orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Current-CM-Open-Conditional-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/conditional/openOrders", signed=True, data=params
        )


    async def papi_get_cm_conditional_open_order(self, **params):
        """Query Current UM Open Conditional Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-CM-Open-Conditional-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/conditional/openOrder", signed=True, data=params
        )


    async def papi_get_cm_conditional_order_history(self, **params):
        """Get all open conditional orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-CM-Conditional-Order-History

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/conditional/orderHistory", signed=True, data=params
        )


    async def papi_get_um_force_orders(self, **params):
        """Query User's UM Force Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Users-UM-Force-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/forceOrders", signed=True, data=params
        )


    async def papi_get_cm_force_orders(self, **params):
        """Query User's CM Force Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Users-CM-Force-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/forceOrders", signed=True, data=params
        )


    async def papi_get_um_order_amendment(self, **params):
        """Get order modification history.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-UM-Modify-Order-History

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/orderAmendment", signed=True, data=params
        )


    async def papi_get_cm_order_amendment(self, **params):
        """Get order modification history.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-CM-Modify-Order-History

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/orderAmendment", signed=True, data=params
        )


    async def papi_get_margin_force_orders(self, **params):
        """Query user's margin force orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Users-Margin-Force-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "margin/forceOrders", signed=True, data=params
        )


    async def papi_get_um_user_trades(self, **params):
        """Get trades for a specific account and UM symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/UM-Account-Trade-List

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/userTrades", signed=True, data=params
        )


    async def papi_get_cm_user_trades(self, **params):
        """Get trades for a specific account and CM symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/CM-Account-Trade-List

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/userTrades", signed=True, data=params
        )


    async def papi_get_um_adl_quantile(self, **params):
        """Query UM Position ADL Quantile Estimation.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/UM-Position-ADL-Quantile-Estimation

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/adlQuantile", signed=True, data=params
        )


    async def papi_get_cm_adl_quantile(self, **params):
        """Query CM Position ADL Quantile Estimation.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/CM-Position-ADL-Quantile-Estimation

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/adlQuantile", signed=True, data=params
        )


    async def papi_set_um_fee_burn(self, **params):
        """Change user's BNB Fee Discount for UM Futures (Fee Discount On or Fee Discount Off ) on EVERY symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Toggle-BNB-Burn-On-UM-Futures-Trade

        :returns: API response

        """
        return await self._request_papi_api(
            "post", "um/feeBurn", signed=True, data=params
        )


    async def papi_get_um_fee_burn(self, **params):
        """Get user's BNB Fee Discount for UM Futures (Fee Discount On or Fee Discount Off).

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Get-UM-Futures-BNB-Burn-Status

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/feeBurn", signed=True, data=params
        )


    async def papi_get_margin_order(self, **params):
        """Query Margin Account Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "margin/order", signed=True, data=params
        )


    async def papi_get_margin_open_orders(self, **params):
        """Query Current Margin Open Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "margin/openOrders", signed=True, data=params
        )


    async def papi_get_margin_all_orders(self, **params):
        """Query All Margin Account Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Margin-Account-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "margin/allOrders", signed=True, data=params
        )


    async def papi_get_margin_order_list(self, **params):
        """Retrieves a specific OCO based on provided optional parameters.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-OCO

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "margin/orderList", signed=True, data=params
        )


    async def papi_get_margin_all_order_list(self, **params):
        """Query all OCO for a specific margin account based on provided optional parameters.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-all-OCO

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "margin/allOrderList", signed=True, data=params
        )


    async def papi_get_margin_open_order_list(self, **params):
        """Query Margin Account's Open OCO.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-Open-OCO

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "margin/openOrderList", signed=True, data=params
        )


    async def papi_get_margin_my_trades(self, **params):
        """Margin Account Trade List.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-Trade-List

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "margin/myTrades", signed=True, data=params
        )


    async def papi_get_margin_repay_debt(self, **params):
        """Repay debt for a margin loan.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-Trade-List

        :returns: API response

        """
        return await self._request_papi_api(
            "post", "margin/repay-debt", signed=True, data=params
        )


    async def papi_v1_post_ping(self, **params):
        return await self._request_papi_api(
            "post", "ping", signed=True, data=params, version=1
        )

