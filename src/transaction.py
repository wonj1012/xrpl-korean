from typing import Optional

from xrpl.wallet import Wallet
from xrpl.models.transactions import (
    Transaction,
    Payment,
    AccountSet,
    SetRegularKey,
    TrustSet,
)
from xrpl.models.currencies import IssuedCurrency
from xrpl.transaction import (
    autofill_and_sign,
    submit_and_wait,
    XRPLReliableSubmissionException,
)
from xrpl.ledger import get_latest_validated_ledger_sequence
from xrpl.constants import CryptoAlgorithm
from xrpl.clients import JsonRpcClient

from account import XrplAccount
from utils import Address, Result, AccountSetAsfFlag


class XrplTransaction:
    """
    XRP Ledger에서 트랜잭션을 관리하는 클래스입니다.
    """

    @classmethod
    def send_xrp(
        cls,
        account: XrplAccount,
        destination_address: Address,
        amount: str | int,
        **kwargs,
    ) -> Result:
        """
        이 계정에서 특정 주소로 XRP를 보냅니다.

        Args:
            account (XrplAccount): 트랜잭션을 제출할 계정입니다.
            destination_address (Address): XRP를 받을 주소입니다.
            amount (str | int): 보낼 XRP의 양입니다.
            **kwargs: 추가로 설정할 트랜잭션의 속성입니다.

        Returns:
            Result: 트랜잭션의 결과입니다.
        """
        # Pop check_fee from kwargs
        check_fee = kwargs.pop("check_fee", True)

        # Create payment transaction
        payment_tx = Payment(
            account=account.address,
            amount=str(amount),
            destination=destination_address,
            **kwargs,
        )

        # Submit transaction and return result
        return cls.submit_transaction(
            account=account, transaction=payment_tx, check_fee=check_fee
        )

    @classmethod
    def set_account_properties(
        cls,
        account: XrplAccount,
        set_flag: Optional[AccountSetAsfFlag] = None,
        clear_flag: Optional[AccountSetAsfFlag] = None,
        **kwargs,
    ) -> Result:
        """
        이 계정의 속성을 설정하거나 해제합니다.

        Args:
            account (XrplAccount): 트랜잭션을 제출할 계정입니다.
            set_flag (Optional[AccountSetAsfFlag]): 설정할 계정 속성입니다.
            clear_flag (Optional[AccountSetAsfFlag]): 해제할 계정 속성입니다.
            **kwargs: 추가로 설정할 트랜잭션의 속성입니다.

        Returns:
            Result: 트랜잭션의 결과입니다.
        """
        # Pop check_fee from kwargs
        check_fee = kwargs.pop("check_fee", True)

        # Create AccountSet transaction
        account_set_tx = AccountSet(
            account=account.address,
            set_flag=set_flag,
            clear_flag=clear_flag,
            **kwargs,
        )

        # Submit transaction and return result
        return cls.submit_transaction(
            account=account, transaction=account_set_tx, check_fee=check_fee
        )

    @classmethod
    def set_regular_key(
        cls,
        account: XrplAccount,
        algorithm: CryptoAlgorithm = CryptoAlgorithm.ED25519,
        **kwargs,
    ) -> Result:
        """
        계정의 정규 키를 설정합니다.

        Args:
            account (XrplAccount): 트랜잭션을 제출할 계정입니다.
            algorithm (CryptoAlgorithm, optional): 사용할 암호화 알고리즘입니다. 기본값은 CryptoAlgorithm.ED25519입니다.
            **kwargs: 트랜잭션 설정에 추가로 전달할 선택적 매개변수입니다.

        Returns:
            Result: 트랜잭션의 결과입니다.
        """
        # Pop check_fee from kwargs
        check_fee = kwargs.pop("check_fee", True)

        # create regular key wallet
        regular_key_wallet = Wallet.create(algorithm=algorithm)

        # create SetRegularKey transaction
        set_regular_key_tx = SetRegularKey(
            account=account.address,
            regular_key=regular_key_wallet.classic_address,
            **kwargs,
        )

        # Submit transaction and return result
        return cls.submit_transaction(
            account=account, transaction=set_regular_key_tx, check_fee=check_fee
        )

    @classmethod
    def set_trust_line(
        cls,
        account: XrplAccount,
        token_symbol: str,
        issuer: Address,
        limit: str | int,
        **kwargs,
    ) -> Result:
        """
        이 계정과 발행자 사이에 특정 토큰에 대한 trust line을 설정합니다.

        Args:
            account (XrplAccount): 트랜잭션을 제출할 계정입니다.
            token_symbol (str): trust line의 토큰입니다.
            issuer (Address): 토큰의 발행자입니다.
            limit (str | int): trust line의 한도입니다.
            **kwargs: 트랜잭션 설정에 추가로 전달할 선택적 매개변수입니다.

        Returns:
            Result: 트랜잭션의 결과입니다.
        """
        # Pop check_fee from kwargs
        check_fee = kwargs.pop("check_fee", True)

        # create issued currency instance and add to tokens
        issued_currency = IssuedCurrency(currency=token_symbol, issuer=issuer)
        account.add_token(token_symbol, issuer, issued_currency)

        # convert to IssuedCurrencyAmount
        limit_amount = issued_currency.to_amount(value=str(limit))

        # create TrustSet transaction
        trust_set_tx = TrustSet(
            account=account.address,
            limit_amount=limit_amount,
            **kwargs,
        )

        # Submit transaction and return result
        return cls.submit_transaction(
            account=account, transaction=trust_set_tx, check_fee=check_fee
        )

    @classmethod
    def close_token_trust_line(
        cls, account: XrplAccount, token_symbol: str, issuer: Address, **kwargs
    ) -> Result:
        """
        이 계정과 발행자 사이에 특정 토큰에 대한 trust line을 닫습니다.
        (즉, trust line의 한도를 0으로 설정합니다.)

        Args:
            account (XrplAccount): 트랜잭션을 제출할 계정입니다.
            token_symbol (str): 한도를 0으로 설정할 토큰의 심볼입니다.
            issuer (Address): 토큰의 발행자입니다.
            **kwargs: 트랜잭션 설정에 추가로 전달할 선택적 매개변수입니다.

        Returns:
            Result: 트랜잭션의 결과입니다.
        """
        return cls.set_trust_line(
            account=account, currency=token_symbol, issuer=issuer, limit=0, **kwargs
        )

    @classmethod
    def send_token(
        cls,
        account: XrplAccount,
        destination_address: Address,
        token_symbol: str,
        issuer: Address,
        amount: str | int,
        **kwargs,
    ) -> Result:
        """
        이 계정에서 목적지 주소로 토큰을 보냅니다.

        Args:
            account (XrplAccount): 트랜잭션을 제출할 계정입니다.
            destination_address (Address): 토큰을 받을 계정의 주소입니다.
            token_symbol (str): 보낼 토큰의 이름입니다.
            issuer (Address): 보낼 토큰의 발행자입니다.
            amount (Union[str, int]): 보낼 토큰의 양입니다.
            **kwargs: 트랜잭션 설정에 추가로 전달할 선택적 매개변수입니다.

        Returns:
            Result: 트랜잭션의 결과입니다.
        """
        # Pop check_fee from kwargs
        check_fee = kwargs.pop("check_fee", True)

        # create issued currency instance
        issued_currency = IssuedCurrency(currency=token_symbol, issuer=issuer)
        account.add_token(token_symbol, issuer, issued_currency)

        # convert to IssuedCurrencyAmount
        amount = issued_currency.to_amount(value=amount)

        # create payment transaction
        payment_tx = Payment(
            account=account.address,
            amount=amount,
            destination=destination_address,
            **kwargs,
        )

        # Submit transaction and return result
        return cls.submit_transaction(
            account=account, transaction=payment_tx, check_fee=check_fee
        )

    @classmethod
    def submit_transaction(
        cls,
        account: XrplAccount,
        transaction: Transaction,
        check_fee: bool = True,
        log: bool = True,
    ) -> Result:
        """
        트랜잭션을 제출하고 그 결과를 반환합니다.

        Args:
            account (XrplAccount): 트랜잭션을 제출할 계정입니다.
            transaction (Transaction): 제출할 트랜잭션입니다.
            check_fee (bool, optional): 수수료를 확인할지 여부입니다. 기본값으로 True를 사용합니다.
            log (bool, optional): 트랜잭션을 로깅할지 여부입니다. 기본값으로 True를 사용합니다.

        Returns:
            Result: 트랜잭션의 결과입니다.

        Raises:
            XRPLReliableSubmissionException: 트랜잭션 제출이 실패하면 발생합니다.
        """
        # Autofill and sign transactionxx
        signed_tx = autofill_and_sign(
            transaction=transaction,
            client=account.client,
            wallet=account.wallet,
            check_fee=check_fee,
        )

        # Validate transaction
        signed_tx.validate()

        # Send transaction and get response
        response = submit_and_wait(
            transaction=signed_tx, client=account.client, wallet=account.wallet
        )

        # Raise exception if transaction failed
        if not response.is_successful():
            raise XRPLReliableSubmissionException(response.result)

        # Log transaction
        if log:
            account.log_transaction(
                tx_hash=response.result["hash"], tx_result=response.result
            )

        # Return result
        return response.result

    @staticmethod
    def calculate_last_ledger_sequence(
        client: JsonRpcClient, tolerance: int = 10
    ) -> int:
        """
        트랜잭션의 추가 매개변수인 last_ledger_sequence를 계산합니다.
        트랜잭션은 last_ledger_sequence 이하의 ledger sequence에서 제출되지 않으면 거부됩니다.
        즉, 현재 ledger sequence로부터 tolerance만큼의 시퀀스 안에 제출되지 않으면 거부됩니다.

        Args:
            client (JsonRpcClient): XRPL 클라이언트입니다.
            tolerance (int, optional): 트랜잭션이 현재로부터 몇개의 시퀀스 안에 제출되어야 하는지를 나타내는 tolerance입니다. 기본값으로 10을 사용합니다. Defaults to 10.

        Raises:
            ValueError: 0 이하의 tolerance가 주어지면 발생합니다.

        Returns:
            int: 트랜잭션이 제출될 마지막 ledger sequence입니다. 이 값보다 큰 ledger sequence에서는 트랜잭션이 거부됩니다.
        """
        if tolerance < 0:
            raise ValueError("Tolerance must be greater than or equal to 0.")

        return get_latest_validated_ledger_sequence(client) + tolerance
