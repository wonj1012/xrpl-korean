from typing import Dict

from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.currencies import IssuedCurrency

from utils import Address, Result, TESTNET_URL
from wallet import XrplWallet


class XrplAccount:
    """
    XRP Ledger에서 계정을 관리하는 클래스입니다.

    Attributes:
        client_url (str): XRPL 네트워크에 연결하는 데 사용하는 클라이언트 URL입니다.
        wallet_path (str): 지갑 정보를 저장하는 파일의 경로입니다.
    """

    def __init__(
        self,
        client_url: str = TESTNET_URL,
        wallet_path: str = "wallet.json",
        create: bool = False,
    ) -> None:
        """
        XRPL 객체의 모든 필요한 속성을 구성합니다.

        Args:
            wallet_path (str): 지갑 정보를 저장하는 파일의 경로입니다.
        """
        # Set client
        self._client = JsonRpcClient(client_url)
        self._wallet = None
        self._transactions: Dict[str, Result] = {}
        self._tokens: Dict[str, IssuedCurrency] = {}

        # Create new wallet if create is True
        if create:
            self._wallet = XrplWallet.create_wallet(
                client=self.client, wallet_path=wallet_path
            )

        # Load wallet from file
        self._wallet = XrplWallet.load_wallet(self.client, wallet_path=wallet_path)

    def __str__(self) -> str:
        return f"XrplAccount({self.address})"

    def __dict__(self) -> dict:
        return {
            "client": self.client,
            "wallet": self.wallet,
            "classic_address": self.address,
            "transactions": self.transactions,
        }

    # Property methods
    @property
    def client(self) -> JsonRpcClient:
        """
        Returns:
            JsonRpcClient: 현재 JsonRpcClient 인스턴스입니다.
        """
        return self._client

    @property
    def wallet(self) -> Wallet:
        """
        Returns:
            Wallet: 현재 지갑입니다.
        """
        return self._wallet

    @property
    def address(self) -> Address:
        """
        Returns:
            Address: 지갑의 클래식 주소입니다.
        """
        return Address(self.wallet.classic_address)

    @property
    def transactions(self) -> Dict[str, Result]:
        """
        Returns:
            Dict[str, Result]: 트랜잭션 기록 (트랜잭션 해시: 트랜잭션 결과)
        """
        return self._transactions

    @property
    def tokens(self) -> Dict[str, IssuedCurrency]:
        """
        Returns:
            Dict[str, IssuedCurrency]: 토큰들 (토큰 심볼.발행자: 토큰 정보)
        """
        return self._tokens

    # Setter methods
    def add_token(self, symbol: str, issuer: Address, token: IssuedCurrency) -> None:
        """
        토큰을 사용자의 토큰 목록에 추가합니다.

        Args:
            symbol (str): 토큰 심볼입니다.
            issuer (Address): 토큰 발행자의 주소입니다.
            token (IssuedCurrency): IssuedCurrency 객체입니다.
        """
        self._tokens.update({f"{symbol}.{issuer}": token})

    def delete_token(self, symbol: str, issuer: Address) -> None:
        """
        토큰을 사용자의 토큰 목록으로부터 삭제합니다.

        Args:
            symbol (str): 삭제할 토큰의 심볼입니다.
            issuer (Address): 삭제할 토큰의 발행자 주소입니다.
        """
        self._tokens.pop(f"{symbol}.{issuer}")

    def log_transaction(self, tx_hash: str, tx_result: Result) -> None:
        """
        트랜잭션을 기록합니다.

        Args:
            tx_hash (str): 트랜잭션의 해시값입니다.
            tx_result (Result): 트랜잭션의 결과입니다.
        """
        self._transactions.update({tx_hash: tx_result})
