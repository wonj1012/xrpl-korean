---
sidebar_position: 1
author: wonj1012
---

# 크로스 통화 결제 (Cross-Currency Payments)

XRP Ledger는 광범위한 트랜잭션 유형을 제공하는 플랫폼으로서, 다양한 화폐 간 결제, 즉 크로스 통화 결제의 구현이 가능합니다. 이는 사용자가 토큰이나 XRP, 또는 둘 다를 서로 교환하고 결제할 수 있도록 합니다. 크로스 통화 결제는 XRP Ledger 내에서 `Payment`라는 거래 유형으로 처리되며, 이는 직접적인 XRP 결제와 같은 방식으로 동작합니다.

이러한 결제들은 완전히 '원자적'(atomic)이라는 점을 강조하고자 합니다. '원자적'이란 개념은 트랜잭션이 '모두 완료'되거나 '전혀 실행되지 않음'을 보장하는 성질을 의미합니다. 이로 인해 사용자는 트랜잭션 중간에 실패하는 경우, 일부만 완료되는 상황을 경험하지 않습니다.

기본적인 원칙으로, 크로스 통화 결제는 송금자가 가변적인 비용을 지불하고 수신자에게 고정된 금액을 전달하는 방식을 따릅니다. 이는 통화 변환 비율의 변동에 따라 송금자가 지불하는 비용이 변동할 수 있음을 의미하며, 수신자는 항상 예상한 금액을 받게 됩니다.

그러나 이러한 결제는 '부분 결제'(partial payments) 옵션을 통해 보다 유연하게 구성될 수도 있습니다. 부분 결제는 송금자가 설정한 한도 내에서 수신자가 가변적인 금액을 받을 수 있게 하는 방식입니다. 이렇게 하면 송금자는 예상치 못한 환율 변동에 대해 보호받을 수 있으며, 수신자는 가능한 최대한의 금액을 받게 됩니다. 이 방식은 주로 환율 변동이 크거나 예측하기 어려운 시장 조건에서 유용합니다.

## 예시

XRP Ledger의 다양한 화폐 간 결제(Cross-Currency Payments) 기능은 사용자가 두 가지 다른 화폐 간에 자연스럽게 결제할 수 있도록 해줍니다. 아래에 이를 설명하는 예시를 제시해 보겠습니다.

### XRP에서 USD로 결제

Alice는 XRP를 가지고 있고, Bob은 USD를 받고 싶어합니다. Alice는 XRP Ledger를 사용해 자신의 XRP를 USD로 변환하고, Bob에게 전송하려고 합니다. Alice나 Bob이 직접 환율을 계산하거나 거래소를 이용하지 않고도, XRP Ledger는 자동으로 최적의 환율을 계산하여 Alice의 XRP를 USD로 변환하고, Bob에게 전송합니다.

1. Alice는 먼저 XRP Ledger에 접속하여 결제를 시작합니다. 이때, 결제 세부 정보를 입력합니다: 보내는 화폐(XRP), 받는 화폐(USD), 받는 사람(Bob), 그리고 보내려는 금액.

2. XRP Ledger는 Alice의 XRP를 USD로 변환할 수 있는 최적의 경로를 자동으로 찾습니다. 이 경로는 다양한 환율과 거래 수수료를 고려한 것입니다.

3. 결제 경로가 확정되면, Alice의 XRP는 자동으로 USD로 변환되고, Bob에게 전송됩니다. 이 과정은 원자적으로 이루어져, 결제가 완전히 성공하거나 아예 실패합니다.

4. 결제가 완료되면, Alice는 원하는 금액만큼의 XRP를 소비하고, Bob은 원하는 금액만큼의 USD를 받게 됩니다.

## 작동 방식

크로스 통화 결제를 위해서 XRP Ledger는 다음과 같은 기능들을 제공합니다.

### 결제 경로 찾기 (Payment Paths)

크로스 통화 결제는 통화를 바꿔줄 때, XRP Ledger의 네이티브 DEX (Decentralized Exchange)를 이용해서 최적의 경로를 찾습니다.

예를 들어, XRP로 USD를 결제하려고 할 때, XRP Ledger는 XRP를 USD로 바꿔줄 수 있는 경로를 찾습니다. 이 때, XRP Ledger는 먼저 DEX에서 XRP/USD 거래 쌍을 찾습니다.

만약 이러한 거래 쌍이 존재하지 않거나 거래를 완료할 수 있을만큼 유동성이 충분하지 않다면, XRP Ledger는 XRP를 USD로 바꿔줄 수 있는 다른 거래쌍들을 찾아서 경로로 제공합니다. 예를 들어, XRP/ETH, ETH/USD 거래쌍이 존재한다면, XRP Ledger는 XRP -> ETH -> USD 경로를 제공합니다.

거래를 완료할 수 없는 상황 뿐만 아니라 다른 통화를 거쳐서 더 저렴하게 거래할 수 있는 경우도 XRP Ledger가 경로를 찾아주어 최적의 경로로 거래를 진행할 수 있도록 합니다.

또한, 경로가 하나가 아닌 여러 개일 수도 있습니다. 예를 들어, XRP로 USD 100개의 결제를 진행할 때, 50개는 XRP -> USD로 결제 되고, 나머지 50개는 XRP -> ETH -> USD로 결제될 수 있습니다.

거래가 성공적으로 이루어지면, DEX에서는 XRP/USD 거래 쌍(`offer`)이 그만큼 소모되고, XRP/ETH, ETH/USD 거래 쌍이 사용된 만큼 소모됩니다.

주의할 점은, 서버가 알려준 최적의 경로가 실제 최적의 경로는 아닐 수 있다는 점입니다. 네트워크 과부하나 계산의 한계로 인해 실제로는 더 좋은 경로가 존재할 수 있습니다. 또한, 최적의 경로는 실시간으로 변하며, 결제가 처리되는 시점에서는 원래 계산했던 경로가 최적이 아닐 수도 있습니다. 또한, 신뢰할 수 없는 `rippled` 인스턴스는 수익을 위해 이 동작을 변경할 수 있으므로, 경로를 결정할 때는 신뢰성 있는 정보와 서버를 사용하거나 여러 서버로부터 정보를 받아오는 것이 중요합니다.

더 자세한 내용은 공식문서 링크 [paths](https://xrpl.org/paths.html)와 [path_find](https://xrpl.org/path_find.html)를 참고하세요.

### 원자적 거래 (Atomic Transactions)

크로스 통화 결제는 원자적 거래를 지원합니다. 이는 트랜잭션이 '모두 완료'되거나 '전혀 실행되지 않음'을 보장하는 성질을 의미합니다. 이로 인해 사용자는 트랜잭션 중간에 실패하는 경우, 일부만 완료되는 상황을 경험하지 않습니다.

예를 들어, Alice가 XRP를 USD로 결제하려고 할 때, XRP -> ETH -> USD 의 경로를 찾았습니다. 이 때, XRP -> ETH 교환만 성공하고, ETH -> USD 교환은 실패하는 경우는 없습니다. 만약 ETH -> USD 교환에 실패한다면, XRP -> ETH 교환도 실패하게 됩니다. 이는 XRP Ledger가 원자적 거래를 지원하기 때문입니다.

### 최대 수량 (SendMax)

크로스 통화 결제는 기본적으로 받는 사람이 일정한 양의 통화를 받도록 하고, 보내는 양은 당시의 환율에 따라 변동됩니다. 그러므로, 보내는 사람은 예상치 못한 변동에 예상보다 더 많은 통화를 지불할 수가 있습니다.

이를 방지하기 위해, 보내는 사람은 최대 수량(`SendMax`)을 설정할 수 있습니다. 이는 보내는 사람이 최대 얼마까지 지불할 수 있는지를 설정하는 것입니다. 이를 통해 보내는 사람은 예상치 못한 변동에 대해 보호받을 수 있습니다.

또한 `SendMax`를 지정하지 않은 경우, 가지고 있는 토큰을 모두 고려해서 최적의 경로를 찾기 때문에, 특정 통화만 이용하여 결제하고 싶다면, `SendMax`를 지정해야 합니다.

### 부분 결제 (Partial Payments)

부분 결제(Partial Payment)는 XRP Ledger에서 `Payment` 트랜잭션을 발생시킬 때 사용할 수 있는 옵션입니다. 부분 결제를 사용하면 결제를 시작하는 주체가 원하는 최종 금액을 수신자가 완전히 받지 못하더라도 결제가 성공적으로 처리될 수 있습니다.

부분 결제의 대표적인 사용 사례는 크로스 통화 결제입니다. 예를 들어, 유동성이 부족한 경우 결제를 시작하는 주체는 모든 결제를 한 번에 처리할 수 없을 수 있습니다. 이 경우, 부분 결제를 통해 가능한 한 많은 수량의 자산을 전송하고, 결제의 일부를 반환하는 방법을 사용할 수 있습니다.

이를 가능하게 하려면 결제 트랜잭션에 `tfPartialPayment` 플래그를 설정해야 합니다. 그러나 이는 옵션이며, 일부 경우에서만 적절할 수 있습니다. 부분 결제 옵션은 주로 결제를 반환하는 데 사용되며, 이는 자신이 추가 비용을 부담하지 않고도 자금을 반환할 수 있게 합니다. 일반적으로는 모든 결제가 목표 금액을 완전히 전달하도록 설정하는 것이 바람직합니다.

결제를 수신하는 주체는 `delivered_amount` 메타데이터 필드를 체크해야 합니다. 이 필드는 실제로 수신자가 받은 금액을 나타냅니다. 만약 이 필드가 결제 트랜잭션의 Amount 필드와 일치하지 않는다면, 이는 부분 결제가 이루어졌음을 나타냅니다. 따라서 수신자는 항상 이 `delivered_amount` 필드를 검증해야 합니다.

마지막으로, 부분 결제 트랜잭션을 성공적으로 수행하기 위해서는 `tfPartialPayment` 플래그 외에도 `tfFullyCanonicalSig` 플래그를 설정해야 합니다. 이는 트랜잭션 서명이 완전히 정규화되어야 함을 의미합니다. 완전히 정규화된 서명을 사용하면 트랜잭션 처리 과정에서 일어날 수 있는 [특정 유형의 공격](https://xrpl.org/partial-payments.html#partial-payments-exploit)을 방지할 수 있습니다.

### 리플링 (Rippling)

리플링(Rippling)은 XRP Ledger에서 발생하는 고유한 프로세스로, 같은 통화를 가지고 있는 두 개의 신뢰선(trust lines) 간에 잔액이 전달되는 것을 의미합니다.

예를 들어, Alice가 Bob에게 USD 10을 송금하려 하지만, Alice와 Bob 사이에 직접적인 신뢰선이 없을 경우, XRP Ledger는 Alice와 Bob 사이에 다른 경로를 찾을 수 있습니다. Alice는 Charlie에게 USD 10을 송금하고, Charlie는 그 USD 10을 Bob에게 송금할 수 있습니다. 이렇게 되면 Alice는 Bob에게 원하는 USD 10을 성공적으로 전달했으며, 이 프로세스를 '리플링'이라고 합니다.

이런 리플링 과정은 돈을 보내는 사람과 받는 사람 사이에 여러 단계를 거칠 수 있으며, 이런 단계를 거치면서 각각의 신뢰선을 통해 중간 잔액이 전달됩니다.

리플링은 효과적인 토큰의 흐름을 가능하게 하여 통화 간에 유동성을 제공하고, 결제 네트워크의 전반적인 효율성을 향상시킵니다. 그러나 이 기능은 신중하게 사용해야 합니다. 왜냐하면 잘못 설정된 경우 의도치 않게 잔액이 변경될 수 있기 때문입니다.

XRP Ledger 계정은 "No Ripple" 플래그를 설정하여 특정 신뢰선에서 리플링을 방지할 수 있습니다. 이 플래그를 설정하면 해당 신뢰선이 리플링에 참여하지 않고, 직접적인 거래만 가능하게 됩니다. 이는 통제되지 않은 자산 이동을 방지하는 데 도움이 될 수 있습니다.

리플링에 대한 이해는 XRP Ledger의 기능을 올바르게 이해하고 활용하는 데 중요합니다. 이러한 메커니즘이 가지는 잠재력과 함께 그에 따른 위험성도 인지하고 있어야 합니다.

## 코드 구현

크로스 통화 결제를 사용하여 XRP를 USD로 결제하는 예시를 코드로 보여드리겠습니다.

```python
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.transactions import Payment
from xrpl.wallet import generate_faucet_wallet
from xrpl.clients import JsonRpcClient
from xrpl.transaction import (
    autofill_and_sign,
    submit_and_wait,
)

JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)

# 지갑을 생성하거나 기존의 지갑을 불러옵니다.
my_wallet = generate_faucet_wallet(client=client, debug=True)

# SendMax 필드를 포함하는 결제를 생성합니다.
# 이 예제에서는 최대 50 USD를 이용해 30 EUR를 결제하려고 합니다.
my_payment = Payment(
    account=my_wallet.classic_address,
    amount=IssuedCurrencyAmount(
        currency="EUR",
        issuer="rEuLyBCvcw4CFmzv8RepSiAoNgF8tTGJQC",
        value="30",
    ),
    destination="rPT1Sjq2YGrBMTttX4GZHjKu9dyfzbpAYe",
    send_max=IssuedCurrencyAmount(
        currency="USD",
        issuer="rMH4UxPrbuMa1spCBR98hLLyNJp4d8p3tM",
        value="50",
    ),
)

result = submit_transaction(client=client, wallet=my_wallet, transaction=my_payment)

print(result)
```
