import json

from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet, generate_faucet_wallet


class XrplWallet:
    """
    XRP Ledger에서 지갑을 관리하는 클래스입니다.
    """

    def load_wallet(self, wallet_path: str) -> Wallet:
        """
        지정된 파일에서 지갑 정보를 로드하고 새 지갑 인스턴스를 생성합니다.

        Args:
            wallet_path (str): 지갑 정보를 포함하는 파일의 경로입니다.

        Returns:
            Wallet: 로드된 지갑 인스턴스입니다.
        """

        # Load wallet info from file
        with open(wallet_path, "r", encoding="UTF-8") as file:
            wallet_info = json.load(file)

        # Create new wallet instance
        wallet = Wallet(
            public_key=wallet_info["public_key"],
            private_key=wallet_info["private_key"],
            master_address=wallet_info["address"],
            seed=wallet_info["seed"],
            algorithm=wallet_info["algorithm"],
        )

        # Return wallet instance
        return wallet

    @staticmethod
    def create_wallet(
        client: JsonRpcClient, wallet_path: str = "wallet.json"
    ) -> Wallet:
        """
        새 지갑을 생성하고 그 정보를 지정된 파일에 저장합니다.

        Args:
            client (JsonRpcClient): XRPL 클라이언트입니다.
            wallet_path (str, optional): 지갑 정보를 저장할 파일의 경로입니다. 기본값은 "wallet.json"입니다.

        Returns:
            Wallet: 생성된 새 지갑입니다.
        """
        # Create new wallet instance
        new_wallet = generate_faucet_wallet(
            client=client, debug=True, usage_context="testing"
        )

        # Save wallet info to file
        XrplWallet.save_wallet(new_wallet, wallet_path)

        # Return wallet instance
        return new_wallet

    @staticmethod
    def fund_wallet(client: JsonRpcClient, wallet: Wallet) -> None:
        """
        지정된 지갑을 테스트용 자금으로 충전합니다.

        Args:
            client (JsonRpcClient): XRPL 클라이언트입니다.
            wallet (Wallet): 충전할 지갑입니다.
        """
        # Fund wallet
        generate_faucet_wallet(
            client=client,
            debug=True,
            wallet=wallet,
            usage_context="test funding",
        )

    @staticmethod
    def save_wallet(wallet: Wallet, wallet_path: str = "wallet.json") -> None:
        """
        지갑 정보를 지정된 파일에 저장합니다.

        Args:
            wallet (Wallet): 정보를 저장할 지갑입니다.
            wallet_path (str, optional): 지갑 정보를 저장할 파일의 경로입니다. 기본값은 "wallet.json"입니다.
        """
        wallet_json = wallet.__dict__
        wallet_json["address"] = wallet_json.pop("_address")
        # Save wallet info to file
        with open(wallet_path, "w", encoding="UTF-8") as file:
            json.dump(wallet.__dict__, file)
