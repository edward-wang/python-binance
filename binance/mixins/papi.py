"""
PapiMixin - Portfolio Margin(组合保证金)

此 mixin 包含所有 Portfolio Margin(组合保证金) 相关的方法。
"""
from typing import Dict, Any, Optional

# 此 mixin 依赖 ClientCore 提供的请求方法


class PapiMixin:
    """
    Portfolio Margin(组合保证金) API Mixin
    
    此 mixin 提供所有 Portfolio Margin(组合保证金) 相关的方法。
    这些方法依赖 AsyncClientCore 或 ClientCore 提供的请求基础设施。
    """

    def papi_get_balance(self, **params):
        """Query account balance.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account

        :param asset: required
        :type asset: str

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api("get", "balance", signed=True, data=params)


    def papi_get_rate_limit(self, **params):
        """Query User Rate Limit

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Query-User-Rate-Limit


        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api("get", "rateLimit/order", signed=True, data=params)


    def papi_stream_get_listen_key(self):
        """Start a new user data stream for Portfolio Margin account.

        https://developers.binance.com/docs/derivatives/portfolio-margin/user-data-streams/Start-User-Data-Stream

        :returns: API response

            {
                "listenKey": "pM_XXXXXXX"
            }

        The stream will close after 60 minutes unless a keepalive is sent.
        If the account has an active listenKey, that listenKey will be returned and its validity will be extended for 60 minutes.

        Weight: 1

        """
        res = self._request_papi_api("post", "listenKey", signed=False, data={})
        return res["listenKey"]


    def papi_stream_keepalive(self, listenKey):
        """Keepalive a user data stream to prevent a time out.

        https://developers.binance.com/docs/derivatives/portfolio-margin/user-data-streams/Keepalive-User-Data-Stream

        :returns: API response

            {}

        User data streams will close after 60 minutes. It's recommended to send a ping about every 60 minutes.

        Weight: 1

        """
        params = {"listenKey": listenKey}
        return self._request_papi_api("put", "listenKey", signed=False, data=params)


    def papi_stream_close(self, listenKey):
        """Close out a user data stream.

        https://developers.binance.com/docs/derivatives/portfolio-margin/user-data-streams/Close-User-Data-Stream

        :returns: API response

            {}

        Weight: 1

        """
        params = {"listenKey": listenKey}
        return self._request_papi_api("delete", "listenKey", signed=False, data=params)


    def papi_get_account(self, **params):
        """Query account information.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Account-Information

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api("get", "account", signed=True, data=params)


    def papi_get_margin_max_borrowable(self, **params):
        """Query margin max borrow.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Margin-Max-Borrow

        :param asset: required
        :type asset: str

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "margin/maxBorrowable", signed=True, data=params
        )


    def papi_get_margin_max_withdraw(self, **params):
        """Query margin max borrow.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Query-Margin-Max-Withdraw

        :param asset: required
        :type asset: str

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "margin/maxWithdraw", signed=True, data=params
        )


    def papi_get_um_position_risk(self, **params):
        """Query margin max borrow.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Query-UM-Position-Information

        :param symbol: required
        :type symbol: str

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "um/positionRisk", signed=True, data=params
        )


    def papi_get_cm_position_risk(self, **params):
        """Query margin max borrow.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Query-CM-Position-Information

        :param asset: required
        :type asset: str

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "cm/positionRisk", signed=True, data=params
        )


    def papi_set_um_leverage(self, **params):
        """Query margin max borrow.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Change-UM-Initial-Leverage

        :param asset: required
        :type asset: str

        :param leverage: required
        :type leverage: int

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api("post", "um/leverage", signed=True, data=params)


    def papi_set_cm_leverage(self, **params):
        """Query margin max borrow.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Change-CM-Initial-Leverage

        :param asset: required
        :type asset: str

        :param leverage: required
        :type leverage: int

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api("post", "cm/leverage", signed=True, data=params)


    def papi_change_um_position_side_dual(self, **params):
        """Change user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol in UM.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Change-UM-Position-Mode

        :param dualSidePosition: required
        :type dualSidePosition: str

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "post", "um/positionSide/dual", signed=True, data=params
        )


    def papi_change_cm_position_side_dual(self, **params):
        """Change user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol in CM.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Change-CM-Position-Mode

        :param dualSidePosition: required
        :type dualSidePosition: str

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "post", "cm/positionSide/dual", signed=True, data=params
        )


    def papi_get_um_position_side_dual(self, **params):
        """Get user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol in UM.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Current-Position-Mode

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "um/positionSide/dual", signed=True, data=params
        )


    def papi_get_cm_position_side_dual(self, **params):
        """Get user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol in CM.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-CM-Current-Position-Mode

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "cm/positionSide/dual", signed=True, data=params
        )


    def papi_get_um_leverage_bracket(self, **params):
        """Query UM notional and leverage brackets.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/UM-Notional-and-Leverage-Brackets

        :param symbol: optional
        :type symbol: str

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "um/leverageBracket", signed=True, data=params
        )


    def papi_get_cm_leverage_bracket(self, **params):
        """Query CM notional and leverage brackets.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/CM-Notional-and-Leverage-Brackets

        :param symbol: optional
        :type symbol: str

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "cm/leverageBracket", signed=True, data=params
        )


    def papi_get_um_api_trading_status(self, **params):
        """Portfolio Margin UM Trading Quantitative Rules Indicators.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Portfolio-Margin-UM-Trading-Quantitative-Rules-Indicators

        :param symbol: optional
        :type symbol: str

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "um/apiTradingStatus", signed=True, data=params
        )


    def papi_get_um_comission_rate(self, **params):
        """Get User Commission Rate for UM.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-User-Commission-Rate-for-UM

        :param symbol: required
        :type symbol: str

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "um/commissionRate", signed=True, data=params
        )


    def papi_get_cm_comission_rate(self, **params):
        """Get User Commission Rate for CM.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-User-Commission-Rate-for-CM

        :param symbol: required
        :type symbol: str

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "cm/commissionRate", signed=True, data=params
        )


    def papi_get_margin_margin_loan(self, **params):
        """Query margin loan record.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Query-Margin-Loan-Record

        :param asset: required
        :type asset: str

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "margin/marginLoan", signed=True, data=params
        )


    def papi_get_margin_repay_loan(self, **params):
        """Query margin repay record.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Query-Margin-repay-Record

        :param asset: required
        :type asset: str

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "margin/repayLoan", signed=True, data=params
        )


    def papi_get_repay_futures_switch(self, **params):
        """Query Auto-repay-futures Status.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-Auto-repay-futures-Status

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "repay-futures-switch", signed=True, data=params
        )


    def papi_repay_futures_switch(self, **params):
        """Change Auto-repay-futures Status.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Change-Auto-repay-futures-Status

        :param autoRepay: required
        :type autoRepay: str

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "post", "repay-futures-switch", signed=True, data=params
        )


    def papi_get_margin_interest_history(self, **params):
        """Get Margin Borrow/Loan Interest History.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-Margin-BorrowLoan-Interest-History

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "margin/marginInterestHistory", signed=True, data=params
        )


    def papi_repay_futures_negative_balance(self, **params):
        """Repay futures Negative Balance.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Repay-futures-Negative-Balance

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "post", "repay-futures-negative-balance", signed=True, data=params
        )


    def papi_get_portfolio_interest_history(self, **params):
        """Query interest history of negative balance for portfolio margin.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Query-Portfolio-Margin-Negative-Balance-Interest-History

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "portfolio/interest-history", signed=True, data=params
        )



    def papi_get_portfolio_negative_balance_exchange_record(self, **params):
        """Query user negative balance auto exchange record.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Query-User-Negative-Balance-Auto-Exchange-Record

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "portfolio/negative-balance-exchange-record", signed=True, data=params
        )


    def papi_fund_auto_collection(self, **params):
        """Fund collection for Portfolio Margin.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Fund-Auto-collection

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "post", "auto-collection", signed=True, data=params
        )


    def papi_fund_asset_collection(self, **params):
        """Transfers specific asset from Futures Account to Margin account.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Fund-Collection-by-Asset

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "post", "asset-collection", signed=True, data=params
        )


    def papi_bnb_transfer(self, **params):
        """Transfer BNB in and out of UM.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/BNB-transfer

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api("post", "bnb-transfer", signed=True, data=params)


    def papi_get_um_income_history(self, **params):
        """Get UM Income History.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Income-History

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api("get", "um/income", signed=True, data=params)


    def papi_get_cm_income_history(self, **params):
        """Get CM Income History.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-CM-Income-History

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api("get", "cm/income", signed=True, data=params)


    def papi_get_um_account(self, **params):
        """Get current UM account asset and position information.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Account-Detail

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api("get", "um/account", signed=True, data=params)


    def papi_get_um_account_v2(self, **params):
        """Get current UM account asset and position information.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Account-Detail-V2

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "um/account", version=2, signed=True, data=params
        )


    def papi_get_cm_account(self, **params):
        """Get current CM account asset and position information.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-CM-Account-Detail

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api("get", "cm/account", signed=True, data=params)


    def papi_get_um_account_config(self, **params):
        """Query UM Futures account configuration.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Futures-Account-Config

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "um/accountConfig", signed=True, data=params
        )


    def papi_get_um_symbol_config(self, **params):
        """Get current UM account symbol configuration.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Futures-Symbol-Config

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "um/symbolConfig", signed=True, data=params
        )


    def papi_get_um_trade_asyn(self, **params):
        """Get download id for UM futures trade history.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-Download-Id-For-UM-Futures-Trade-History

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api("get", "um/trade/asyn", signed=True, data=params)


    def papi_get_um_trade_asyn_id(self, **params):
        """Get UM futures trade download link by Id.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Futures-Trade-Download-Link-by-Id

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "um/trade/asyn/id", signed=True, data=params
        )


    def papi_get_um_order_asyn(self, **params):
        """Get download id for UM futures order history.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-Download-Id-For-UM-Futures-Order-History

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api("get", "um/order/asyn", signed=True, data=params)


    def papi_get_um_order_asyn_id(self, **params):
        """Get UM futures order download link by Id.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Futures-Order-Download-Link-by-Id

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "um/order/asyn/id", signed=True, data=params
        )


    def papi_get_um_income_asyn(self, **params):
        """Get download id for UM futures transaction history.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-Download-Id-For-UM-Futures-Transaction-History

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api("get", "um/income/asyn", signed=True, data=params)


    def papi_get_um_income_asyn_id(self, **params):
        """Get UM futures Transaction download link by Id.

        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Get-UM-Futures-Transaction-Download-Link-by-Id

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_papi_api(
            "get", "um/income/asyn/id", signed=True, data=params
        )

    # Public papi endpoints


    def papi_ping(self, **params):
        """Test connectivity to the Rest API.

        https://developers.binance.com/docs/derivatives/portfolio-margin/market-data

        :returns: API response

        """
        return self._request_papi_api("get", "ping", signed=False, data=params)

    # Trade papi endpoints


    def papi_create_um_order(self, **params):
        """Place new UM order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade

        :returns: API response

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return self._request_papi_api("post", "um/order", signed=True, data=params)


    def papi_create_um_conditional_order(self, **params):
        """Place new UM Conditional order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/New-UM-Conditional-Order

        :returns: API response

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return self._request_papi_api(
            "post", "um/conditional/order", signed=True, data=params
        )


    def papi_create_cm_order(self, **params):
        """Place new CM order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/New-CM-Order

        :returns: API response

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return self._request_papi_api("post", "cm/order", signed=True, data=params)


    def papi_create_cm_conditional_order(self, **params):
        """Place new CM Conditional order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/New-CM-Conditional-Order

        :returns: API response

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return self._request_papi_api(
            "post", "cm/conditional/order", signed=True, data=params
        )


    def papi_create_margin_order(self, **params):
        """New Margin Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/New-Margin-Order

        :returns: API response

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return self._request_papi_api("post", "margin/order", signed=True, data=params)


    def papi_margin_loan(self, **params):
        """Apply for a margin loan.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-Borrow

        :returns: API response

        """
        return self._request_papi_api("post", "marginLoan", signed=True, data=params)


    def papi_repay_loan(self, **params):
        """Repay for a margin loan.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-Repay

        :returns: API response

        """
        return self._request_papi_api("post", "repayLoan", signed=True, data=params)


    def papi_margin_order_oco(self, **params):
        """Send in a new OCO for a margin account.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-New-OCO

        :returns: API response

        """
        return self._request_papi_api(
            "post", "margin/order/oco", signed=True, data=params
        )


    def papi_cancel_um_order(self, **params):
        """Cancel an active UM LIMIT order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-UM-Order

        :returns: API response

        """
        return self._request_papi_api("delete", "um/order", signed=True, data=params)


    def papi_cancel_um_all_open_orders(self, **params):
        """Cancel an active UM LIMIT order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-All-UM-Open-Orders

        :returns: API response

        """
        return self._request_papi_api(
            "delete", "um/allOpenOrders", signed=True, data=params
        )


    def papi_cancel_um_conditional_order(self, **params):
        """Cancel UM Conditional Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-UM-Conditional-Order

        :returns: API response

        """
        return self._request_papi_api(
            "delete", "um/conditional/order", signed=True, data=params
        )


    def papi_cancel_um_conditional_all_open_orders(self, **params):
        """Cancel All UM Open Conditional Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-All-UM-Open-Conditional-Orders

        :returns: API response

        """
        return self._request_papi_api(
            "delete", "um/conditional/allOpenOrders", signed=True, data=params
        )


    def papi_cancel_cm_order(self, **params):
        """Cancel an active CM LIMIT order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-CM-Order

        :returns: API response

        """
        return self._request_papi_api("delete", "cm/order", signed=True, data=params)


    def papi_cancel_cm_all_open_orders(self, **params):
        """Cancel an active CM LIMIT order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-All-CM-Open-Orders

        :returns: API response

        """
        return self._request_papi_api(
            "delete", "cm/allOpenOrders", signed=True, data=params
        )


    def papi_cancel_cm_conditional_order(self, **params):
        """Cancel CM Conditional Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-CM-Conditional-Order

        :returns: API response

        """
        return self._request_papi_api(
            "delete", "cm/conditional/order", signed=True, data=params
        )


    def papi_cancel_cm_conditional_all_open_orders(self, **params):
        """Cancel All CM Open Conditional Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-All-CM-Open-Conditional-Orders

        :returns: API response

        """
        return self._request_papi_api(
            "delete", "cm/conditional/allOpenOrders", signed=True, data=params
        )


    def papi_cancel_margin_order(self, **params):
        """Cancel Margin Account Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-Margin-Account-Order

        :returns: API response

        """
        return self._request_papi_api(
            "delete", "margin/order", signed=True, data=params
        )


    def papi_cancel_margin_order_list(self, **params):
        """Cancel Margin Account OCO Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-Margin-Account-OCO-Orders

        :returns: API response

        """
        return self._request_papi_api(
            "delete", "margin/orderList", signed=True, data=params
        )


    def papi_cancel_margin_all_open_orders(self, **params):
        """Cancel Margin Account All Open Orders on a Symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-Margin-Account-All-Open-Orders-on-a-Symbol

        :returns: API response

        """
        return self._request_papi_api(
            "delete", "margin/allOpenOrders", signed=True, data=params
        )


    def papi_modify_um_order(self, **params):
        """Order modify function, currently only LIMIT order modification is supported, modified orders will be reordered in the match queue.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Modify-UM-Order

        :returns: API response

        """
        return self._request_papi_api("put", "um/order", signed=True, data=params)


    def papi_modify_cm_order(self, **params):
        """Order modify function, currently only LIMIT order modification is supported, modified orders will be reordered in the match queue.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Modify-CM-Order

        :returns: API response

        """
        return self._request_papi_api("put", "cm/order", signed=True, data=params)


    def papi_get_um_order(self, **params):
        """Check an UM order's status.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-UM-Order

        :returns: API response

        """
        return self._request_papi_api("get", "um/order", signed=True, data=params)


    def papi_get_um_all_orders(self, **params):
        """Get all account UM orders; active, canceled, or filled.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-UM-Orders

        :returns: API response

        """
        return self._request_papi_api("get", "um/allOrders", signed=True, data=params)


    def papi_get_um_open_order(self, **params):
        """Query current UM open order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-UM-Open-Order

        :returns: API response

        """
        return self._request_papi_api("get", "um/openOrder", signed=True, data=params)


    def papi_get_um_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Current-UM-Open-Orders

        :returns: API response

        """
        return self._request_papi_api("get", "um/openOrders", signed=True, data=params)


    def papi_get_um_conditional_all_orders(self, **params):
        """Query All UM Conditional Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-UM-Conditional-Orders

        :returns: API response

        """
        return self._request_papi_api(
            "get", "um/conditional/allOrders", signed=True, data=params
        )


    def papi_get_um_conditional_open_orders(self, **params):
        """Get all open conditional orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Current-UM-Open-Conditional-Orders

        :returns: API response

        """
        return self._request_papi_api(
            "get", "um/conditional/openOrders", signed=True, data=params
        )


    def papi_get_um_conditional_open_order(self, **params):
        """Query Current UM Open Conditional Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-UM-Open-Conditional-Order

        :returns: API response

        """
        return self._request_papi_api(
            "get", "um/conditional/openOrder", signed=True, data=params
        )


    def papi_get_um_conditional_order_history(self, **params):
        """Get all open conditional orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-UM-Conditional-Order-History

        :returns: API response

        """
        return self._request_papi_api(
            "get", "um/conditional/orderHistory", signed=True, data=params
        )


    def papi_get_cm_order(self, **params):
        """Check an CM order's status.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-CM-Order

        :returns: API response

        """
        return self._request_papi_api("get", "cm/order", signed=True, data=params)


    def papi_get_cm_all_orders(self, **params):
        """Get all account CM orders; active, canceled, or filled.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-CM-Orders

        :returns: API response

        """
        return self._request_papi_api("get", "cm/allOrders", signed=True, data=params)


    def papi_get_cm_open_order(self, **params):
        """Query current CM open order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-CM-Open-Order

        :returns: API response

        """
        return self._request_papi_api("get", "cm/openOrder", signed=True, data=params)


    def papi_get_cm_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Current-CM-Open-Orders

        :returns: API response

        """
        return self._request_papi_api("get", "cm/openOrders", signed=True, data=params)


    def papi_get_cm_conditional_all_orders(self, **params):
        """Query All CM Conditional Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-CM-Conditional-Orders

        :returns: API response

        """
        return self._request_papi_api(
            "get", "cm/conditional/allOrders", signed=True, data=params
        )


    def papi_get_cm_conditional_open_orders(self, **params):
        """Get all open conditional orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Current-CM-Open-Conditional-Orders

        :returns: API response

        """
        return self._request_papi_api(
            "get", "cm/conditional/openOrders", signed=True, data=params
        )


    def papi_get_cm_conditional_open_order(self, **params):
        """Query Current UM Open Conditional Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-CM-Open-Conditional-Order

        :returns: API response

        """
        return self._request_papi_api(
            "get", "cm/conditional/openOrder", signed=True, data=params
        )


    def papi_get_cm_conditional_order_history(self, **params):
        """Get all open conditional orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-CM-Conditional-Order-History

        :returns: API response

        """
        return self._request_papi_api(
            "get", "cm/conditional/orderHistory", signed=True, data=params
        )


    def papi_get_um_force_orders(self, **params):
        """Query User's UM Force Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Users-UM-Force-Orders

        :returns: API response

        """
        return self._request_papi_api("get", "um/forceOrders", signed=True, data=params)


    def papi_get_cm_force_orders(self, **params):
        """Query User's CM Force Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Users-CM-Force-Orders

        :returns: API response

        """
        return self._request_papi_api("get", "cm/forceOrders", signed=True, data=params)


    def papi_get_um_order_amendment(self, **params):
        """Get order modification history.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-UM-Modify-Order-History

        :returns: API response

        """
        return self._request_papi_api(
            "get", "um/orderAmendment", signed=True, data=params
        )


    def papi_get_cm_order_amendment(self, **params):
        """Get order modification history.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-CM-Modify-Order-History

        :returns: API response

        """
        return self._request_papi_api(
            "get", "cm/orderAmendment", signed=True, data=params
        )


    def papi_get_margin_force_orders(self, **params):
        """Query user's margin force orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Users-Margin-Force-Orders

        :returns: API response

        """
        return self._request_papi_api(
            "get", "margin/forceOrders", signed=True, data=params
        )


    def papi_get_um_user_trades(self, **params):
        """Get trades for a specific account and UM symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/UM-Account-Trade-List

        :returns: API response

        """
        return self._request_papi_api("get", "um/userTrades", signed=True, data=params)


    def papi_get_cm_user_trades(self, **params):
        """Get trades for a specific account and CM symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/CM-Account-Trade-List

        :returns: API response

        """
        return self._request_papi_api("get", "cm/userTrades", signed=True, data=params)


    def papi_get_um_adl_quantile(self, **params):
        """Query UM Position ADL Quantile Estimation.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/UM-Position-ADL-Quantile-Estimation

        :returns: API response

        """
        return self._request_papi_api("get", "um/adlQuantile", signed=True, data=params)


    def papi_get_cm_adl_quantile(self, **params):
        """Query CM Position ADL Quantile Estimation.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/CM-Position-ADL-Quantile-Estimation

        :returns: API response

        """
        return self._request_papi_api("get", "cm/adlQuantile", signed=True, data=params)


    def papi_set_um_fee_burn(self, **params):
        """Change user's BNB Fee Discount for UM Futures (Fee Discount On or Fee Discount Off ) on EVERY symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Toggle-BNB-Burn-On-UM-Futures-Trade

        :returns: API response

        """
        return self._request_papi_api("post", "um/feeBurn", signed=True, data=params)


    def papi_get_um_fee_burn(self, **params):
        """Get user's BNB Fee Discount for UM Futures (Fee Discount On or Fee Discount Off).

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Get-UM-Futures-BNB-Burn-Status

        :returns: API response

        """
        return self._request_papi_api("get", "um/feeBurn", signed=True, data=params)


    def papi_get_margin_order(self, **params):
        """Query Margin Account Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-Order

        :returns: API response

        """
        return self._request_papi_api("get", "margin/order", signed=True, data=params)


    def papi_get_margin_open_orders(self, **params):
        """Query Current Margin Open Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-Margin-Open-Order

        :returns: API response

        """
        return self._request_papi_api(
            "get", "margin/openOrders", signed=True, data=params
        )


    def papi_get_margin_all_orders(self, **params):
        """Query All Margin Account Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Margin-Account-Orders

        :returns: API response

        """
        return self._request_papi_api(
            "get", "margin/allOrders", signed=True, data=params
        )


    def papi_get_margin_order_list(self, **params):
        """Retrieves a specific OCO based on provided optional parameters.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-OCO

        :returns: API response

        """
        return self._request_papi_api(
            "get", "margin/orderList", signed=True, data=params
        )


    def papi_get_margin_all_order_list(self, **params):
        """Query all OCO for a specific margin account based on provided optional parameters.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-all-OCO

        :returns: API response

        """
        return self._request_papi_api(
            "get", "margin/allOrderList", signed=True, data=params
        )


    def papi_get_margin_open_order_list(self, **params):
        """Query Margin Account's Open OCO.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-Open-OCO

        :returns: API response

        """
        return self._request_papi_api(
            "get", "margin/openOrderList", signed=True, data=params
        )


    def papi_get_margin_my_trades(self, **params):
        """Margin Account Trade List.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-Trade-List

        :returns: API response

        """
        return self._request_papi_api(
            "get", "margin/myTrades", signed=True, data=params
        )


    def papi_get_margin_repay_debt(self, **params):
        """Repay debt for a margin loan.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-Repay-Debt

        :returns: API response

        """
        return self._request_papi_api(
            "post", "margin/repay-debt", signed=True, data=params
        )

