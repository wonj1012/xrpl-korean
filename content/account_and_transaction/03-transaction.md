# 트랜잭션 (Transaction)

이 챕터에서는 XRP Ledger의 트랜잭션에 관한 설명과 트랜잭션을 생성하고 제출하는 방법을 소개합니다.

## 트랜잭션이란?

"트랜잭션"이란 일반적으로 거래나 이동을 의미하는 것으로, 어떤 것을 한 곳에서 다른 곳으로 옮기는 작업을 나타냅니다. 트랜잭션은 물리적 또는 디지털 상품의 교환, 정보의 전송, 또는 금융 거래에 모두 적용될 수 있습니다.

XRP Ledger에서 트랜잭션은 원장의 상태를 바꾸는 유일한 방법입니다. 트랜잭션은 서명, 제출, 그리고 합의(consensus) 과정을 거친 후에 확인된 원장 버전에 포함되어야만 최종적으로 확정됩니다. 일부 원장 규칙은 또한 pseudo-트랜잭션을 생성하는데, 이는 서명되거나 제출되지 않지만 여전히 합의를 통해 수락되어야 합니다. 실패한 거래도 레저에 포함되는데, 이는 스팸 거래 비용을 지불하기 위해 XRP의 잔액을 수정하기 때문입니다.

트랜잭션은 돈을 보내는 것 이상의 역할을 할 수 있습니다. 여러 가지 결제 유형을 지원하는 것 외에도 XRP Ledger의 트랜잭션은 암호화키를 바꾸는 것, 기타 설정을 관리하는 것, 그리고 XRP 원장의 분산형 거래소에서 거래하는 것 등을 위해 사용됩니다.

## XRPL의 트랜잭션 구조

XRP Ledger의 트랜잭션은 JSON 형식으로 표현됩니다. 트랜잭션은 다음과 같은 필드를 포함합니다:

-   **계정 주소**: 트랜잭션을 보내는 계정의 주소입니다.

-   **트랜잭션 유형**: 트랜잭션의 유형을 나타내는 문자열입니다. 예를 들어, `Payment`는 XRP 또는 사용자 정의 통화를 한 계정에서 다른 계정으로 전송하는 트랜잭션을 나타냅니다.

-   **트랜잭션 필드**: 트랜잭션 유형에 따라 필요한 필드가 다릅니다. 예를 들어, `Payment` 트랜잭션에는 `Amount` 필드가 있습니다. 이 필드는 송금할 금액을 나타냅니다.

-   **서명**: 트랜잭션은 송신자의 비밀키로 서명되어야 합니다. 이는 트랜잭션의 발송인이 자신의 계정을 제어하고 트랜잭션을 생성했음을 증명합니다.

-   **공개 키**: 트랜잭션의 서명을 검증하는 데 사용되는 공개 키입니다. 이는 트랜잭션의 유효성을 검사하거나 트랜잭션을 조회할 때 사용됩니다.

-   **수수료**: 트랜잭션을 제출할 때는 일반적으로 트랜잭션 비용이 부과됩니다. 이 비용은 스팸 트랜잭션을 방지하고, 시스템의 자원을 공정하게 분배하기 위한 것입니다. 트랜잭션 비용은 송신자의 XRP 잔고에서 차감되며, 복구할 수 없습니다.

-   **트랜잭션 해시**: 트랜잭션은 해시 값으로 식별됩니다. 이는 트랜잭션의 내용을 요약한 값으로, 트랜잭션의 유효성을 검사하거나 트랜잭션을 조회할 때 사용됩니다.

## 트랜잭션의 종류

XRP Ledger에서는 다양한 종류의 트랜잭션이 있습니다. 대표적인 트랜잭션 유형은 다음과 같습니다.

-   **Payment**: XRP 또는 사용자가 정의한 통화를 한 계정에서 다른 계정으로 전송하는 트랜잭션입니다. 이는 XRP Ledger의 가장 기본적인 트랜잭션 유형 중 하나입니다.

-   **AccountSet**: 계정의 설정을 변경하는 트랜잭션입니다. 이 설정에는 전송률, 자체 주소에서 토큰을 수신하는 것을 허용할지 여부, 계정 관련 정보 등이 포함될 수 있습니다.

-   **OfferCreate**: 거래소에서 새로운 주문을 만드는 트랜잭션입니다. 이 주문은 XRP와 사용자 정의 통화 간의 거래를 나타낼 수 있습니다.

-   **OfferCancel**: 거래소에서 기존의 주문을 취소하는 트랜잭션입니다. 이 트랜잭션을 통해 더 이상 원하지 않는 거래를 중지할 수 있습니다.

-   **EscrowCreate**: XRP를 조건부로 잠그는 트랜잭션입니다. 이 조건은 시간이나 암호 해제와 같은 특정 요구사항을 충족하는 것일 수 있습니다.

-   **EscrowFinish**: 잠겨진 XRP의 조건이 충족되면, 이 트랜잭션을 통해 해당 XRP를 해제할 수 있습니다.

-   **EscrowCancel**: 시간이 만료되면, 이 트랜잭션을 사용해 잠겨진 XRP를 취소하고 원래의 송신자에게 돌려줄 수 있습니다.

-   **CheckCreate**: 특정 수신자가 나중에 현금화할 수 있는 '체크'를 만드는 트랜잭션입니다.

-   **CheckCash**: 체크를 현금화하여 해당 체크의 XRP 또는 사용자 정의 통화를 받는 트랜잭션입니다.

-   **CheckCancel**: 아직 현금화되지 않은 체크를 취소하는 트랜잭션입니다.

이외에도 다양한 트랜잭션 유형이 있습니다. 자세한 내용은 [XRPL 공식 문서](https://xrpl.org/transaction-types.html)를 참고하세요.

## 트랜잭션 Lifecycle

트랜잭션의 생명주기는 트랜잭션 생성부터 최종적으로 레저에 포함될 때까지의 과정을 포함합니다. 각 단계는 다음과 같습니다:

1. **트랜잭션 생성**:

    트랜잭션 객체는 필요한 필드(트랜잭션 유형, 계정, 수신자, 금액 등)를 포함하여 생성됩니다. 이 단계에서는 필요한 모든 데이터를 수집하고 유효성을 검사합니다.
    [`xrpl.models.transactions`](https://xrpl-py.readthedocs.io/en/latest/source/xrpl.models.transactions.html#module-xrpl.models.transactions)에서 올바른 트랜잭션 유형을 선택하고, 필요한 필드를 채워넣어 트랜잭션을 생성할 수 있습니다.  
    필요한 필드는 직접 채우거나 [`xrpl.transaction.autofill`](https://xrpl-py.readthedocs.io/en/latest/source/xrpl.transaction.html#xrpl.transaction.autofill) 함수를 사용하여 자동으로 채워넣을 수 있습니다.

2. **트랜잭션 서명**:

    트랜잭션은 송신자의 비밀키로 서명되어야 합니다. 이는 트랜잭션의 발송인이 자신의 계정을 제어하고 트랜잭션을 생성했음을 증명합니다.

    트랜잭션 객체의 [`sign`](https://xrpl-py.readthedocs.io/en/latest/source/xrpl.transaction.html#xrpl.transaction.sign) 메서드를 사용하여 트랜잭션을 서명할 수 있습니다.

3. **트랜잭션 제출**:

    서명된 트랜잭션은 XRP Ledger에 제출되어 다음 유효성 검사 단계로 넘어갑니다. 제출된 트랜잭션은 대기열에 들어가며, 다음 레저에서 처리될 차례를 기다립니다.

    트랜잭션 객체의 [`submit`](https://xrpl-py.readthedocs.io/en/latest/source/xrpl.transaction.html#xrpl.transaction.submit) 메서드를 사용하여 트랜잭션을 제출할 수 있습니다.

4. **트랜잭션 검증**:

    레저의 새 버전을 만드는 검증자들은 제출된 트랜잭션을 검증하고 처리합니다. 트랜잭션이 유효하다면 (예: 충분한 잔고, 올바른 서명 등), 이는 새 레저에 포함됩니다.

    _트랜잭션이 레저에 포함되면, 이는 더 이상 변경될 수 없습니다._

5. **최종 트랜잭션**:

    트랜잭션이 레저에 포함되면, 이는 완료된 상태로 간주되며, 관련된 계정 상태(예: 잔고)는 이 트랜잭션에 따라 업데이트됩니다.

## 트랜잭션 클래스의 주요 속성과 메서드

모든 트랜잭션에는 동일한 일련의 공통 필드와 [트랜잭션 유형](transaction-types.html)에 따른 추가 필드가 있습니다. 모든 트랜잭션의 공통 필드는 다음과 같습니다:

| 필드                            | JSON 타입   | [내부 타입][] | 설명                                                                                                                                                                                                                                                                                                          |
| :------------------------------ | :---------- | :------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Account`                       | 문자열      | AccountID     | _(필수)_ 트랜잭션을 시작한 [계정](accounts.html)의 고유 주소입니다.                                                                                                                                                                                                                                           |
| `TransactionType`               | 문자열      | UInt16        | _(필수)_ 트랜잭션의 유형입니다. 유효한 [트랜잭션 유형](transaction-types.html)은 `Payment`, `OfferCreate`, `TrustSet` 등이 있습니다.                                                                                                                                                                          |
| `Fee`                           | 문자열      | Amount        | _(필수; [자동-입력 가능])_ 이 트랜잭션을 네트워크에 배포하는 비용으로 파괴될 XRP의 정수량입니다(드롭 단위). 일부 트랜잭션 유형에는 다른 최소 요구사항이 있습니다. 자세한 내용은 [트랜잭션 비용][]을 참조하세요.                                                                                               |
| `Sequence`                      | 숫자        | UInt32        | _(필수; [자동-입력 가능])_ 트랜잭션을 보내는 계정의 [시퀀스 번호](basic-data-types.html#account-sequence)입니다. `Sequence` 번호가 같은 계정에서 이전 트랜잭션보다 정확히 1 더 큰 경우에만 트랜잭션이 유효합니다. 특수한 경우인 `0`은 트랜잭션이 대신 [티켓](tickets.html)을 사용하고 있다는 것을 의미합니다. |
| [`AccountTxnID`](#accounttxnid) | 문자열      | Hash256       | _(선택)_ 다른 트랜잭션을 식별하는 해시 값입니다. 제공되면, 이 트랜잭션은 보내는 계정의 이전에 보낸 트랜잭션이 제공된 해시와 일치하는 경우에만 유효합니다.                                                                                                                                                     |
| [`Flags`](#flags-field)         | 숫자        | UInt32        | _(선택)_ 이 트랜잭션에 대한 비트-플래그 세트입니다.                                                                                                                                                                                                                                                           |
| `LastLedgerSequence`            | 숫자        | UInt32        | _(선택; 강력히 권장)_ 이 트랜잭션이 나타날 수 있는 최대 원장 인덱스입니다. 이 필드를 명시하면 트랜잭션이 유효하거나 거부될 때까지 기다릴 수 있는 시간에 엄격한 상한선이 생깁니다. 자세한 내용은 [신뢰할 수 있는 트랜잭션 제출](reliable-transaction-submission.html)을 참조하세요.                            |
| [`Memos`](#memos-field)         | 객체의 배열 | 배열          | _(선택)_ 이 트랜잭션을 식별하는데 사용되는 추가 임의 정보입니다.                                                                                                                                                                                                                                              |
| [`NetworkID`](#networkid-field) | 숫자        | UInt32        | _(네트워크-특정)_ 이 트랜잭션이 의도한 체인의 네트워크 ID입니다. Mainnet 및 일부 테스트 네트워크에 대해서는 **반드시 생략해야 합니다**. 네트워크 ID가 1025 이상인 체인에는 **필수**입니다.                                                                                                                    |
| [`Signers`](#signers-field)     | 배열        | 배열          | _(선택)_ 이 트랜잭션을 승인하는 [다중 서명](multi-signing.html)을 나타내는 객체의 배열입니다.                                                                                                                                                                                                                 |
| `SourceTag`                     | 숫자        | UInt32        | _(선택)_ 이 결제의 이유를 식별하는 임의의 정수, 또는 이 트랜잭션이 대신 만든 보내는 사람입니다. 원칙적으로, 환불은 초기 결제의 `SourceTag`를 환불 결제의 `DestinationTag`로 지정해야 합니다.                                                                                                                  |
| `SigningPubKey`                 | 문자열      | Blob          | _(서명시 자동 추가)_ 이 트랜잭션을 서명하는 데 사용된 개인 키에 해당하는 공개 키의 16진수 표현입니다. 빈 문자열인 경우, `Signers` 필드에 대신 다중 서명이 있음을 나타냅니다.                                                                                                                                  |
| `TicketSequence`                | 숫자        | UInt32        | _(선택)_ `Sequence` 번호 대신 사용할 [티켓](tickets.html)의 시퀀스 번호입니다. 이 정보가 제공되면 `Sequence`는 `0`이어야 합니다. `AccountTxnID`와 함께 사용할 수 없습니다.                                                                                                                                    |
| `TxnSignature`                  | 문자열      | Blob          | _(서명시 자동 추가)_ 이 트랜잭션이 말하고 있는 계정에서 원래 발생한 것임을 검증하는 서명입니다.                                                                                                                                                                                                               |

이 클래스는 또한 여러 메소드를 포함합니다. 예를 들어, `is_valid()` 메소드는 트랜잭션 객체의 유효성을 확인하며, `sign()` 메소드는 트랜잭션을 서명하는 데 사용됩니다. 그 외에도 트랜잭션 객체의 해시 값을 얻는 `get_hash()` 메소드, 특정 플래그가 설정되어 있는지 확인하는 `has_flag()` 메소드 등 다양한 메소드가 제공됩니다.

더 자세한 내용은 [XRPL 공식 문서](https://xrpl.org/transaction-common-fields.html)를 참고하세요.

## 트랜잭션 비용(Fee)

XRP Ledger에서 트랜잭션을 제출할 때는 일반적으로 트랜잭션 비용이 부과됩니다. 이 비용은 스팸 트랜잭션을 방지하고, 시스템의 자원을 공정하게 분배하기 위한 것입니다. 트랜잭션 비용은 송신자의 XRP 잔고에서 차감되며, 복구할 수 없습니다.

트랜잭션 비용은 보통 XRP의 소수점 아래 여섯 번째 자리까지 계산됩니다. 트랜잭션 비용은 레저의 부하와 함께 변동하며, 그 값은 일반적으로 0.00001 XRP에서 0.0005 XRP 사이입니다.

## 트랜잭션 상태

제출한 트랜잭션의 상태를 조회하려면 [`xrpl.transaction.get_transaction`](https://xrpl-py.readthedocs.io/en/latest/source/xrpl.transaction.html#xrpl.transaction.get_transaction) 메서드를 사용할 수 있습니다. 이 메서드는 트랜잭션 해시를 입력으로 받아, 해당 트랜잭션의 현재 상태를 반환합니다.

## 멀티 서명(Multisigning)

XRP Ledger는 여러 사람이 서명해야 하는 트랜잭션을 지원합니다. 이는 공동 소유 계정이나 특정 권한이 필요한 조직에서 유용합니다.

멀티 서명을 사용하려면, 먼저 멀티 서명 주소를 생성해야 합니다. 그런 다음, 이 주소를 사용해 트랜잭션을 생성하고 각각의 서명자가 트랜잭션을 서명해야 합니다. 서명된 트랜잭션은 XRPL에 제출됩니다.

멀티 서명을 사용한 트랜잭션의 생성과 제출에 대한 자세한 내용은 [Multisigning](https://xrpl.org/multi-signing.html)를 참조하세요.

## 재제출과 구현 세부사항

네트워크가 바쁠 때는 트랜잭션이 대기열에서 제외되거나 무시될 수 있습니다. 이런 경우, 트랜잭션을 재제출해야 합니다. 그러나 재제출을 할 때는 새로운 트랜잭션 번호(Sequence)를 사용하거나 같은 트랜잭션 번호를 사용하면서도 서로 다른 결과를 초래하지 않도록 주의해야 합니다.

또한, XRP Ledger의 트랜잭션 처리는 매우 세밀한 부분이 많습니다. 예를 들어, 동일한 트랜잭션 번호를 가진 여러 트랜잭션을 동시에 제출하면 '테크어웃'(tec) 결과를 반환하는 트랜잭션만 처리되고, 나머지는 무시됩니다. 이러한 세부사항은 [Reliable Transaction Submission Guide](https://xrpl.org/reliable-transaction-submission.html)에서 자세히 설명되어 있습니다.

이 외에도 트랜잭션에 대한 다양한 세부사항과 복잡한 사례를 다루기 위한 정보를 찾을 수 있습니다. 자세한 내용은 [XRPL 공식 문서](https://xrpl.org/transaction-formats.html)를 참조하세요.

## XRP 보내기

가장 기본적인 transaction인 XRP를 현재 주소로부터 다른 주소로 보내는 payment transaction을 생성해보겠습니다.

```python
from pprint import pprint

from xrpl.models.transactions import Payment
from xrpl.wallet import generate_faucet_wallet
from xrpl.clients import JsonRpcClient
from xrpl.ledger import get_latest_validated_ledger_sequence
from xrpl.transaction import (
    autofill_and_sign,
    submit_and_wait,
    XRPLReliableSubmissionException,
)


# 클라이언트와 지갑을 생성합니다.
client = JsonRpcClient("https://s.altnet.rippletest.net:51234/")
wallet = generate_faucet_wallet(client=client, debug=True)

# 현재 레저 시퀀스를 가져옵니다.
ledger_sequence = get_latest_validated_ledger_sequence(client)

# Payment 트랜잭션을 생성합니다.
payment_tx = Payment(
    account=wallet.classic_address,
    amount="1000",
    destination="rPT1Sjq2YGrBMTttX4GZHjKu9dyfzbpAYe",
    last_ledger_sequence=ledger_sequence + 10,
)

# 트랜잭션을 서명합니다.
signed_payment_tx = autofill_and_sign(
    transaction=payment_tx, client=client, wallet=wallet, check_fee=True
)

# 트랜잭션의 유효성을 검사합니다.
signed_payment_tx.validate()

# 트랜잭션을 제출하고 트랜잭션이 성공적으로 처리될 때까지 기다립니다.
response = submit_and_wait(transaction=signed_payment_tx, client=client)

# 트랜잭션이 성공적으로 처리되지 않으면 예외를 발생시킵니다.
if not response.is_successful():
    raise XRPLReliableSubmissionException(response.result)

# 트랜잭션의 결과를 출력합니다.
pprint(response.result)
```

이 과정이 기본적인 트랜잭션 생성과 제출의 과정입니다. 이제부터는 트랜잭션의 각 단계를 자세히 살펴보겠습니다.

### 트랜잭션 생성

```python
payment_tx = Payment(
    account=wallet.classic_address,
    amount="1000",
    destination="rPT1Sjq2YGrBMTttX4GZHjKu9dyfzbpAYe",
    last_ledger_sequence=ledger_sequence + 10,
)
```

트랜잭션 객체는 클라이언트와 소통하지 않고 로컬에서 필요한 필드를 채우는 것으로 생성됩니다.

[`Payment`](https://xrpl-py.readthedocs.io/en/latest/source/xrpl.models.transactions.html#xrpl.models.transactions.Payment) 클래스는 [`Transaction`](https://xrpl-py.readthedocs.io/en/latest/source/xrpl.models.transactions.html#xrpl.models.transactions.transaction.Transaction) 클래스를 상속받습니다. `Transaction` 클래스는 트랜잭션의 공통 필드를 포함하며, `Payment` 클래스는 `Transaction` 클래스의 필드에 더해 특정한 트랜잭션 유형에 필요한 추가 필드를 포함합니다.

모든 트랜잭션 객체들은 `Transaction` 클래스를 상속받으며, 트랜잭션 유형에 따라 필요한 추가 필드를 포함합니다.

### 트랜잭션 자동 채우기와 서명

```python
signed_payment_tx = autofill_and_sign(
    transaction=payment_tx, client=client, wallet=wallet, check_fee=True
)
```

트랜잭션 객체가 생성되면, 이를 자동으로 채우고 서명할 수 있습니다. 이를 위해 [`autofill_and_sign`](https://xrpl-py.readthedocs.io/en/latest/source/xrpl.transaction.html#xrpl.transaction.autofill_and_sign) 함수를 사용합니다. 이 함수는 트랜잭션 객체를 채우고 서명한 후, 채워진 트랜잭션 객체를 반환합니다.

자동 채우기(`autofill`)은 클라이언트를 통해 네트워크와 소통하여, `Fee` 값과 `sequence`값이 사용자에 의해 주어지지 않았다면 올바르게 채웁니다. `autofill` 함수의 `check_fee` 매개변수는 `True`로 설정하면 `Fee` 값이 네트워크의 예상 `Fee` 값보다 너무 높으면 예외를 발생시킵니다.

서명(`sign`)은 로컬에서 사용자의 지갑(private key)을 통해 트랜잭션을 서명합니다. 이 과정에서 `SigningPubKey` 필드와 `TxnSignature` 필드가 자동으로 채워집니다. `SigningPubKey`는 사용자의 공개키이고, `TxnSignature`는 서명 값입니다. 블록체인 네트워크에서는 이 두 필드를 이용해 서명 값을 공개키로 검증하여 트랜잭션의 유효성을 검증합니다.

### 트랜잭션 유효성 검사

```python
signed_payment_tx.validate()
```

트랜잭션의 필수 필드가 모두 채워졌는지, 필드의 값이 유효한지 등을 검사합니다. 이 과정에서 필드의 값이 유효하지 않으면 예외를 발생시킵니다.

### 트랜잭션 제출

```python
response = submit_and_wait(transaction=signed_payment_tx, client=client)

if not response.is_successful():
    raise XRPLReliableSubmissionException(response.result)
```

`submit_and_wait` 함수는 트랜잭션을 제출하고, 트랜잭션이 성공적으로 처리될 때까지 기다립니다. 이 과정에서 트랜잭션은 대기열에 들어가며, 다음 레저에서 처리될 차례를 기다립니다. 트랜잭션이 성공적으로 처리되지 않으면 예외를 발생시킵니다.

### 트랜잭션 결과

```python
pprint(response.result)
```

```python
{'Account': 'rh215fU5Pk9N4p2zLdDfRFSKniYqP3qxp7',
 'Amount': '1000',
 'Destination': 'rPT1Sjq2YGrBMTttX4GZHjKu9dyfzbpAYe',
 'Fee': '10',
 'Flags': 0,
 'LastLedgerSequence': 39630981,
 'Sequence': 39630970,
 'SigningPubKey': 'EDFDBDBD538F1D8DD89A21C91BA824FC9AAA516DAC9BD8144E0E5C0CB3F6FF80AC',
 'TransactionType': 'Payment',
 'TxnSignature': 'B7E679A367C0F89E131CC6E6EB969936B2C69EED5D083E6B11EC7566CE6B7471B1C2BF322100D633C64F53D4F8419F939F3AD50741DF18CF4FC303AE77F3B206',
 'date': 743129490,
 'hash': '99B0DFDD6E2A0CD830919B29DECAD78DA76250ACC94805A6B8C89BA4E57F5D97',
 'inLedger': 39630974,
 'ledger_index': 39630974,
 'meta': {'AffectedNodes': [{'ModifiedNode': {'FinalFields': {'Account': 'rPT1Sjq2YGrBMTttX4GZHjKu9dyfzbpAYe',
                                                              'Balance': '87893903718205934',
                                                              'Flags': 0,
                                                              'OwnerCount': 0,
                                                              'Sequence': 6154587},
                                              'LedgerEntryType': 'AccountRoot',
                                              'LedgerIndex': '31CCE9D28412FF973E9AB6D0FA219BACF19687D9A2456A0C2ABC3280E9D47E37',
                                              'PreviousFields': {'Balance': '87893903718204934'},
                                              'PreviousTxnID': '219D7A899BEF52A6C657B1FE3ED6DCAD7EDAF8BC6D1D279E358CDF6BAB5E5BA4',
                                              'PreviousTxnLgrSeq': 39630970}},
                            {'ModifiedNode': {'FinalFields': {'Account': 'rh215fU5Pk9N4p2zLdDfRFSKniYqP3qxp7',
                                                              'Balance': '9999998990',
                                                              'Flags': 0,
                                                              'OwnerCount': 0,
                                                              'Sequence': 39630971},
                                              'LedgerEntryType': 'AccountRoot',
                                              'LedgerIndex': 'EC06857C98943B84709530C08941FA74DAFC92B30B194D8386209B6D48BB7D3D',
                                              'PreviousFields': {'Balance': '10000000000',
                                                                 'Sequence': 39630970},
                                              'PreviousTxnID': '219D7A899BEF52A6C657B1FE3ED6DCAD7EDAF8BC6D1D279E358CDF6BAB5E5BA4',
                                              'PreviousTxnLgrSeq': 39630970}}],
          'TransactionIndex': 1,
          'TransactionResult': 'tesSUCCESS',
          'delivered_amount': '1000'},
 'validated': True}
```

트랜잭션이 성공적이었다면, 트랜잭션의 결과는 위와 같이 나타납니다.
