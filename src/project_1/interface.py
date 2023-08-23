from os import path
import sys
from typing import Dict, Callable, Any
from pprint import pprint

from xrpl.clients import JsonRpcClient

from src.xrpl_wrapper.account import XrplAccount
from src.xrpl_wrapper.request import XrplRequest
from src.xrpl_wrapper.transaction import XrplTransaction
from src.xrpl_wrapper.utils import (
    Address,
    Result,
    TESTNET_URL,
    function_name_to_pretty,
    to_classic_address,
    AccountSetFlag,
)

# Directory where wallet files will be stored
WALLET_DIR = path.join(path.dirname(__file__), "wallets")

# Default invalid choice response
invalid_choice = Result({"status": "error", "error": "Invalid choice"})


class Interface:
    """
    XRPL과 상호작용을 위한 인터페이스입니다.

    Attributes:
        client (JsonRpcClient): XRPL 클라이언트.
        account (XrplAccount): 현재 계정.
        address (Address): 현재 계정의 주소.
        menu (dict): 인터페이스의 메뉴.
    """

    def __init__(self, client_url: str = TESTNET_URL) -> None:
        """
        XRPL 클라이언트를 사용하여 인터페이스를 초기화합니다.

        Args:
            client_url (str, optional): XRPL 클라이언트의 URL. 기본값은 TESTNET_URL입니다.
        """
        self._client = JsonRpcClient(client_url)
        self._account: XrplAccount = None
        self._menu: Dict[str, Dict[str, Callable]] = {
            "start": {
                "1": self.create_new_wallet,
                "2": self.connect_existing_wallet,
                "3": self.exit,
            },
            "main": {
                "1": {
                    "name": "Transactions",
                    "1": self.send_xrp,
                    "2": self.set_trust_line,
                    "3": self.send_token,
                    "4": self.set_account_properties,
                },
                "2": {
                    "name": "Requests",
                    "1": self.get_xrp_balance,
                    "2": self.get_trust_lines,
                    "3": self.get_account_information,
                },
                "3": self.disconnect_wallet,
                "4": self.exit,
            },
        }

    # Property methods
    @property
    def client(self) -> JsonRpcClient:
        """
        Returns:
            JsonRpcClient: XRPL에 요청을 보내기 위해 사용되는 JsonRpcClient 객체를 반환합니다.
        """
        return self._client

    @property
    def account(self) -> XrplAccount:
        """
        Returns:
            XrplAccount: XRPL에서 트랜잭션을 진행하는데 사용되는 XrplAccount 객체를 반환합니다.
        """
        return self._account

    @property
    def address(self) -> Address:
        """
        Returns:
            Address: 계정의 클래식 주소를 반환합니다.
        """
        return self._account.address

    @property
    def menu(self) -> Dict[str, Dict[str, callable]]:
        """
        Returns:
            Dict[str, Dict[str, callable]]: 인터페이스의 메뉴를 반환합니다.
        """
        return self._menu

    # Wallet methods
    def create_new_wallet(self) -> str:
        """
        새로운 지갑을 생성하고 현재 계정으로 설정합니다.

        Returns:
            str: 지갑이 생성되었다는 메시지를 반환합니다.
        """

        wallet_path = path.join(WALLET_DIR, self.get_wallet_name())
        self._account = XrplAccount(wallet_path=wallet_path, create=True)
        return f"Wallet created at {wallet_path}.\nAddress: {self.address}"

    def connect_existing_wallet(self) -> str:
        """
        기존 지갑에 연결하고 현재 계정으로 설정합니다.

        Returns:
            str: 지갑에 연결되었다는 메시지를 반환합니다.
        """
        wallet_path = path.join(WALLET_DIR, self.get_wallet_name())
        self._account = XrplAccount(wallet_path=wallet_path, create=False)
        return f"Wallet connected from {wallet_path}.\nAddress: {self.address}"

    # Transaction methods
    def send_xrp(self) -> Result:
        """
        현재 계정에서 지정된 주소로 XRP를 보냅니다.

        Returns:
            Result: 트랜잭션의 결과를 반환합니다.
        """
        receiver_address = input("Enter receiver address: ")
        amount = input("Enter XRP amount: ")
        return XrplTransaction.send_xrp(
            account=self.account, destination_address=receiver_address, amount=amount
        )

    def set_trust_line(self) -> Result:
        """
        현재 계정에 대한 trust line을 설정합니다.

        Returns:
            Result: 작업의 결과를 반환합니다.
        """
        issuer_address = input("Enter issuer address: ")
        token_name = input("Enter token name: ")
        limit = input("Enter trust line limit: ")
        return XrplTransaction.set_trust_line(
            account=self.account,
            token_symbol=token_name,
            issuer=issuer_address,
            limit=limit,
        )

    def send_token(self) -> Result:
        """
        현재 계정에서 지정된 주소로 토큰을 보냅니다.

        Returns:
            Result: 트랜잭션의 결과를 반환합니다.
        """
        destination_address = input("Enter receiver address: ")
        token_name = input("Enter token name: ")
        amount = input("Enter token amount: ")
        return XrplTransaction.send_token(
            account=self.account,
            destination_address=destination_address,
            issuer=self.address,
            token_symbol=token_name,
            amount=amount,
        )

    def set_account_properties(self) -> Result:
        """
        현재 계정의 속성을 설정합니다.

        Returns:
            Result: 작업의 결과를 반환합니다.
        """
        set_or_clear = input("Set or Clear? (s/c): ").lower()
        if set_or_clear == "s":
            set_or_clear = True
        elif set_or_clear == "c":
            set_or_clear = False
        else:
            return invalid_choice

        account_flag_dict = {
            1: AccountSetFlag.ASF_REQUIRE_DEST,
            2: AccountSetFlag.ASF_REQUIRE_AUTH,
            3: AccountSetFlag.ASF_DISALLOW_XRP,
            4: AccountSetFlag.ASF_DISABLE_MASTER,
            5: AccountSetFlag.ASF_ACCOUNT_TXN_ID,
            6: AccountSetFlag.ASF_NO_FREEZE,
            7: AccountSetFlag.ASF_GLOBAL_FREEZE,
            8: AccountSetFlag.ASF_DEFAULT_RIPPLE,
            9: AccountSetFlag.ASF_DEPOSIT_AUTH,
            10: AccountSetFlag.ASF_AUTHORIZED_NFTOKEN_MINTER,
            12: AccountSetFlag.ASF_DISABLE_INCOMING_NFTOKEN_OFFER,
            13: AccountSetFlag.ASF_DISABLE_INCOMING_CHECK,
            14: AccountSetFlag.ASF_DISABLE_INCOMING_CHECK,
            15: AccountSetFlag.ASF_DISABLE_INCOMING_PAYCHAN,
        }

        for key, value in account_flag_dict.items():
            print(f"{key}: {str(value)[18:]}")

        try:
            flag_number = int(input("Enter account flag number: "))
        except ValueError:
            return invalid_choice

        try:
            account_flag = account_flag_dict[flag_number]
        except KeyError:
            return invalid_choice
        if set_or_clear:
            set_flag = account_flag
            clear_flag = None
        else:
            set_flag = None
            clear_flag = account_flag

        return XrplTransaction.set_account_properties(
            account=self.account,
            set_flag=set_flag,
            clear_flag=clear_flag,
        )

    # Request methods
    def get_xrp_balance(self) -> Result:
        """
        현재 계정의 XRP 잔액을 가져옵니다.

        Returns:
            Result: 계정의 잔액을 반환합니다.
        """
        address = self.input_address(default=self.address)
        return f"XRP Balance at {address}: {XrplRequest.get_xrp_balance(client=self.client, address=address)}"

    def get_trust_lines(self) -> Result:
        """
        현재 계정의 신뢰선을 가져옵니다.

        Returns:
            Result: 계정의 신뢰선을 반환합니다.
        """
        address = self.input_address(default=self.address)
        return XrplRequest.get_trust_lines(client=self.client, address=address)

    def get_account_information(self) -> Result:
        """
        현재 계정의 정보를 가져옵니다.

        Returns:
            Result: 계정의 정보를 반환합니다.
        """
        address = self.input_address(default=self.address)
        return XrplRequest.get_account_info(client=self.client, address=address)

    # Interface methods
    def disconnect_wallet(self) -> str:
        """
        현재 지갑의 연결을 해제합니다.

        Returns:
            str: 지갑이 연결 해제되었다는 메시지를 반환합니다.
        """
        self._account = None
        return "Wallet disconnected successfully."

    def exit(self) -> None:
        """
        인터페이스를 종료합니다.
        """
        print("Exiting...")
        sys.exit(0)

    def run(self) -> None:
        """
        인터페이스를 실행합니다.
        """
        while self.account is None:
            self.display_and_execute_menu(self.menu["start"])

            while self.account is not None:
                self.display_and_execute_menu(self.menu["main"])

    @staticmethod
    def get_wallet_name() -> str:
        """
        사용자로부터 지갑의 이름을 입력 받습니다.
        .json으로 끝나지 않으면 자동으로 .json을 붙입니다.

        Returns:
            str: 지갑의 이름.
        """
        wallet_name = input("Enter wallet name: ")
        return wallet_name if wallet_name.endswith(".json") else wallet_name + ".json"

    @staticmethod
    def input_address(default: Address) -> Address:
        """
        사용자로부터 주소를 받습니다.

        Args:
            default (Address): 사용자가 주소를 제공하지 않을 경우 사용할 기본 주소.

        Returns:
            Address: 사용자가 제공한 주소 또는 기본 주소.
        """
        address = input("Enter account address: ")
        address = to_classic_address(address)
        if address is None:
            address = default
        return address

    @staticmethod
    def display_menu(menu: Dict[str, Any]) -> None:
        """
        사용자에게 메뉴를 표시합니다.

        Args:
            menu (dict): 표시할 메뉴.
        """

        for key, value in menu.items():
            if callable(value):
                value = function_name_to_pretty(value)

            elif isinstance(value, dict):
                value = value["name"]

            else:
                continue

            print(f"{key}. {value}")
        print()

    def display_and_execute_menu(self, menu):
        """
        사용자에게 메뉴를 표시하고 선택한 옵션을 실행합니다.

        Args:
            menu (dict): 표시할 메뉴.
        """
        self.display_menu(menu)

        try:
            selected_menu = menu[input()]
        except KeyError:
            print("Going back.\n")
            return
        print()

        if isinstance(selected_menu, dict):
            self.display_and_execute_menu(selected_menu)
        else:
            result = selected_menu()
            if isinstance(result, dict):
                pprint(result)
                print()
            else:
                print(result)
                print()
