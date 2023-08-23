from typing import Optional, Dict
from xrpl.clients import JsonRpcClient, XRPLRequestFailureException
from xrpl.models.requests import *
from src.xrpl_wrapper.utils import Address


class XrplRequest:
    """
    XrplRequest 클래스는 XRPL 네트워크에 요청을 보내는 메서드를 정의합니다.
    """

    @classmethod
    def get_server_info(cls, client: JsonRpcClient, **kwargs) -> Dict[str, any]:
        """
        XRPL 네트워크에서 서버 정보를 가져옵니다.

        Args:
            client (JsonRpcClient): 요청을 보낼 클라이언트입니다.
            **kwargs: 추가적인 선택적 매개변수들입니다.

        Returns:
            Result: 서버 정보를 포함하는 Result 객체입니다.

        Raises:
            XRPLRequestFailureException: 서버 정보를 검색하는 데 실패하면 발생합니다.
        """
        return cls.request_ledger(client, ServerInfo(**kwargs))

    @classmethod
    def get_transaction(
        cls, client: JsonRpcClient, transaction_hash: str, **kwargs
    ) -> Dict[str, any]:
        """
        트랜잭션 해시 값으로 XRPL 네트워크에서 거래 정보를 가져옵니다.

        Args:
            client (JsonRpcClient): 요청을 보낼 클라이언트입니다.
            transaction_hash (str): 거래 정보를 조회할 거래의 해시 값입니다.
            **kwargs: 추가적인 선택적 매개변수들입니다.

        Returns:
            Result: 거래 정보를 포함하는 Result 객체입니다.

        Raises:
            XRPLRequestFailureException: 거래 정보를 검색하는 데 실패하면 발생합니다.
        """
        return cls.request_ledger(client, Tx(transaction=transaction_hash, **kwargs))

    @classmethod
    def get_account_info(
        cls, client: JsonRpcClient, address: Address, **kwargs
    ) -> Dict[str, any]:
        """
        XRPL 네트워크에서 이 계정의 정보를 가져옵니다.

        Args:
            client (JsonRpcClient): 요청을 보낼 클라이언트입니다.
            address (Address): 계정 정보를 조회할 계정의 주소입니다.
            **kwargs: 추가적인 선택적 매개변수들입니다.

        Returns:
            Result: 이 계정의 정보를 포함하는 Result 객체입니다.
        """
        return cls.request_ledger(client, AccountInfo(account=address, **kwargs))

    @classmethod
    def get_account_objects(
        cls, client: JsonRpcClient, address: Address, **kwargs
    ) -> Dict[str, any]:
        """
        XRPL 네트워크에서 이 계정의 계정 객체들을 가져옵니다.

        Args:
            client (JsonRpcClient): 요청을 보낼 클라이언트입니다.
            address (Address): 계정 객체들을 조회할 계정의 주소입니다.
            **kwargs: 추가적인 선택적 매개변수들입니다.

        Returns:
            Result: 이 계정의 객체를 포함하는 Result 객체입니다.
        """
        return cls.request_ledger(client, AccountObjects(account=address, **kwargs))

    @classmethod
    def get_account_transactions(
        cls, client: JsonRpcClient, address: Address, limit: Optional[int] = 0, **kwargs
    ) -> Dict[str, any]:
        """
        XRPL 네트워크에서 이 계정의 거래 내역을 가져옵니다.

        Args:
            client (JsonRpcClient): 요청을 보낼 클라이언트입니다.
            address (Address): 거래 내역을 조회할 계정의 주소입니다.
            limit (Optional[int]): 검색할 거래의 최대 개수입니다. 0이면 모두 검색합니다. 기본값은 0입니다.
            **kwargs: 추가적인 선택적 매개변수들입니다.

        Returns:
            Result: 이 계정의 거래 내역을 포함하는 Result 객체입니다.
        """
        result = cls.request_ledger(
            client, AccountTx(account=address, limit=limit, **kwargs)
        )
        return result["transactions"]

    @classmethod
    def get_xrp_balance(cls, client: JsonRpcClient, address: Address, **kwargs) -> int:
        """
        XRPL 네트워크에서 이 계정의 XRP 잔액을 가져옵니다.

        Args:
            client (JsonRpcClient): 요청을 보낼 클라이언트입니다.
            address (Address): XRP 잔액을 조회할 계정의 주소입니다.
            **kwargs: 추가적인 선택적 매개변수들입니다.

        Returns:
            int: 이 계정의 XRP 잔액입니다.
        """
        result = cls.get_account_info(client, address, **kwargs)
        return int(result["account_data"]["Balance"])

    @classmethod
    def get_trust_lines(
        cls,
        client: JsonRpcClient,
        address: Address,
        token_symbol: Optional[str] = None,
        **kwargs
    ) -> Dict[str, any]:
        """
        이 계정의 trust line을 조회합니다.

        Args:
            client (JsonRpcClient): 요청을 보낼 클라이언트입니다.
            address (Address): trust line을 조회할 계정의 주소입니다.
            token_symbol (Optional[str], optional): 조회할 토큰의 심볼입니다. None이면 모두 조회합니다. 기본값은 None입니다.
            **kwargs: 추가적인 선택적 매개변수들입니다.

        Returns:
            Result: 이 계정의 trust line을 포함하는 Result 객체입니다.
        """
        # Get trust lines
        result = cls.request_ledger(client, AccountLines(account=address, **kwargs))

        # Filter by token_name (if provided)
        if token_symbol is not None:
            return [
                line for line in result["lines"] if line["currency"] == token_symbol
            ]

        # Return trust lines
        return result["lines"]

    @classmethod
    def get_account_currencies(
        cls, client: JsonRpcClient, address: Address, **kwargs
    ) -> Dict[str, any]:
        """
        이 계정과 연결된 trust line의 토큰들을 조회합니다.

        Args:
            client (JsonRpcClient): 요청을 보낼 클라이언트입니다.
            **kwargs: 추가적인 선택적 매개변수들입니다.

        Returns:
            Result: 이 계정과 연결된 trust line의 토큰들을 포함하는 Result 객체입니다.
        """
        # Get currencies
        result = cls.request_ledger(
            client, AccountCurrencies(account=address, **kwargs)
        )

        # Return currencies
        return result

    @classmethod
    def get_account_channels(
        cls, client: JsonRpcClient, address: Address, **kwargs
    ) -> Dict[str, any]:
        """
        이 계정의 채널들을 조회합니다.

        Args:
            client (JsonRpcClient): 요청을 보낼 클라이언트입니다.
            **kwargs: 추가적인 선택적 매개변수들입니다.

        Returns:
            Result: 이 계정의 채널들을 포함하는 Result 객체입니다.
        """
        # Get channels
        result = cls.request_ledger(client, AccountChannels(account=address, **kwargs))

        # Return channels
        return result

    @classmethod
    def authorize_channel(
        cls,
        client: JsonRpcClient,
        channel_id: str,
        amount: str | int,
        secret: str | None = None,
        **kwargs
    ) -> Dict[str, any]:
        """
        Args:
            client (JsonRpcClient): 요청을 보낼 클라이언트입니다.
            channel_id (str): 채널 ID입니다.
            amount (str | int): 채널에 예치할 XRP의 양입니다.
            secret (str | None, optional): 서명에 사용할 비밀키입니다. 이 값을 제공하지 않으면 seed, seed_hex, passphrase 중 하나를 제공해야 합니다.
            **kwargs: 추가적인 선택적 매개변수들입니다.

        Returns:
            Result:
        """
        # Get channels
        result = cls.request_ledger(
            client,
            ChannelAuthorize(
                channel_id=channel_id, amount=str(amount), secret=secret, **kwargs
            ),
        )

        # Return channels
        return result

    @classmethod
    def verify_channel(
        cls,
        client: JsonRpcClient,
        channel_id: str,
        amount: str | int,
        public_key: str | None = None,
        signature: str | None = None,
        **kwargs
    ) -> Dict[str, any]:
        """_summary_

        Args:
            client (JsonRpcClient): _description_
            channel_id (str): _description_
            amount (str | int): _description_
            public_key (str | None, optional): _description_. Defaults to None.
            signature (str | None, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        # Get channels
        result = cls.request_ledger(
            client,
            ChannelVerify(
                channel_id=channel_id,
                amount=str(amount),
                public_key=public_key,
                signature=signature,
                **kwargs
            ),
        )

        # Return channels
        return result

    @classmethod
    def get_orderbook_info(cls, client: JsonRpcClient, **kwargs) -> Dict[str, any]:
        """
        XRPL 네트워크에서 orderbook 정보를 가져옵니다.

        Args:
            client (JsonRpcClient): 요청을 보낼 클라이언트입니다.
            **kwargs: 추가적인 선택적 매개변수들입니다.

        Returns:
            Result: orderbook 정보를 포함하는 Result 객체입니다.
        """
        # Get orderbook info
        result = cls.request_ledger(client, BookOffers(**kwargs))

        # Return orderbook info
        return result

    @classmethod
    def request_ledger(cls, client: JsonRpcClient, request: Request) -> Dict[str, any]:
        """
        XRPL 네트워크에 ledger 요청을 보냅니다.

        Args:
            client (JsonRpcClient): 요청을 보낼 클라이언트입니다.
            request (Request): 보낼 요청 객체입니다.

        Returns:
            Result: 요청의 결과를 포함하는 Result 객체입니다.

        Raises:
            XRPLRequestFailureException: 요청이 실패하면 발생합니다.
        """
        # Send request and get response
        response = client.request(request)

        # Raise exception if request failed
        if not response.is_successful():
            raise XRPLRequestFailureException(response.result)

        # Return result
        return response.result
