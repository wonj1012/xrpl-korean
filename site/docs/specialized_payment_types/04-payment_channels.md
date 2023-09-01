---
sidebar_position: 4
author: wonj1012
---

# 결제 채널 (Payment Channels)

결제 채널은 "비동기" XRP 결제를 매우 작은 단위로 나누고 나중에 결제할 수 있는 고급 기능입니다.

결제 채널의 XRP는 일시적으로 예약됩니다. 송신자는 채널에 대한 *청구(Claims)*를 생성하고, 수신자는 XRP 원장 거래를 보내거나 새 원장 버전이 [합의](https://xrpl.org/consensus.html)에 의해 승인되기를 기다리지 않고 확인합니다. (이것은 일반적인 트랜잭션이 합의에 의해 승인되는 패턴과 별개로 발생하므로 _비동기_ 과정입니다.) 수신자는 언제든지 청구를 *인출(redeem)*하여 그 청구에 의해 승인된 XRP 금액을 받을 수 있습니다. 이러한 청구를 결정하는 것은 표준 XRP 원장 거래를 사용하며, 이는 일반적인 합의 과정의 일부입니다. 이 단일 거래는 더 작은 청구에 의해 보장된 여러 거래를 포함할 수 있습니다.

청구는 개별적으로 확인되지만 나중에 일괄로 결제될 수 있기 때문에, 결제 채널을 통해 트랜잭션을 참가자들이 이러한 청구의 디지털 서명을 생성하고 확인하는 능력에만 제한되는 속도로 진행할 수 있게 됩니다. 이 제한은 주로 참가자들의 하드웨어 속도와 서명 알고리즘의 복잡성에 기반하고 있습니다. 최대 속도를 얻기 위해선, XRP 원장의 기본적인 secp256k1 ECDSA 서명보다 빠른 Ed25519 서명을 사용하세요. 연구는 2011년의 상품 하드웨어에서 초당 Ed25519 100,000개 이상의 서명을 생성하고 초당 70,000개 이상을 확인할 수 있는 능력을 [증명했습니다](https://ed25519.cr.yp.to/ed25519-20110926.pdf).

## 왜 결제 채널을 사용해야 하는가

결제 채널을 사용하는 과정은 항상 두 당사자, 즉 지불자와 수취인을 포함합니다. 지불자는 XRP 원장을 사용하는 개인이나 기관으로, 수취인의 고객입니다. 수취인은 상품이나 서비스에 대한 대가로 XRP를 받는 개인이나 사업체입니다.

결제 채널은 본질적으로 어떤 것을 구매하고 판매할 수 있는지에 대해 지정하지 않습니다. 그러나 결제 채널에 적합한 상품과 서비스의 유형은 다음과 같습니다:

- 디지털 아이템처럼 거의 즉시 전송될 수 있는 것들
- 거래 처리 비용이 가격의 비싼 부분을 차지하는 저렴한 것들
- 정확한 수량이 미리 알려지지 않고 대량으로 구매하는 것들

## 결제 채널의 생애주기

다음 다이어그램은 결제 채널의 생애주기를 요약한 것입니다.

![paychan-flow](./img/paychan-flow.svg)

## 결제 채널의 JSON 표현

```json
{
  "Account": "rBqb89MRQJnMPq8wTwEbtz4kvxrEDfcYvt",
  "Destination": "rf1BiGeXwwQoi8Z2ueFYTEXSwuJYfV2Jpn",
  "Amount": "4325800",
  "Balance": "2323423",
  "PublicKey": "32D2471DB72B27E3310F355BB33E339BF26F8392D5A93D3BC0FC3B566612DA0F0A",
  "SettleDelay": 3600,
  "Expiration": 536027313,
  "CancelAfter": 536891313,
  "SourceTag": 0,
  "DestinationTag": 1002341,
  "DestinationNode": "0000000000000000",
  "Flags": 0,
  "LedgerEntryType": "PayChannel",
  "OwnerNode": "0000000000000000",
  "PreviousTxnID": "F0AB71E777B2DA54B86231E19B82554EF1F8211F92ECA473121C655BFC5329BF",
  "PreviousTxnLgrSeq": 14524914,
  "index": "96F76F27D8A327FC48753167EC04A46AA0E382E6F57F32FD12274144D00F1797"
}
```

## 결제 채널 관련 트랜잭션 및 리퀘스트 타입

### 트랜잭션 (Transaction)

- **[PaymentChannelCreate](https://xrpl.org/paymentchannelcreate.html)**

  지불 채널을 생성하고 XRP로 자금을 제공합니다. 이 트랜잭션을 보내는 주소가 지불 채널의 "출처 주소"가 됩니다.

  ```json
  {
    "Account": "rf1BiGeXwwQoi8Z2ueFYTEXSwuJYfV2Jpn",
    "TransactionType": "PaymentChannelCreate",
    "Amount": "10000",
    "Destination": "rsA2LpzuawewSBQXkiju3YQTMzW13pAAdW",
    "SettleDelay": 86400,
    "PublicKey": "32D2471DB72B27E3310F355BB33E339BF26F8392D5A93D3BC0FC3B566612DA0F0A",
    "CancelAfter": 533171558,
    "DestinationTag": 23480,
    "SourceTag": 11747
  }
  ```

- **[PaymentChannelClaim](https://xrpl.org/paymentchannelclaim.html)**

  XRP 지불 채널에서 XRP를 청구하거나, 지불 채널의 만료일을 조정하거나, 둘 다 할 수 있습니다. 이 거래는 트랜잭션 발신자의 지정된 채널에서의 역할에 따라 다르게 사용될 수 있습니다.

  채널의 출처 주소는 다음과 같은 작업을 수행할 수 있습니다:

  1. 채널에서 목적지로 XRP를 청구서와 함께 또는 없이 보낼 수 있습니다.
  2. 채널의 SettleDelay가 지난 후에 채널의 만료를 설정할 수 있습니다.
  3. 보류 중인 만료 시간을 지울 수 있습니다.
  4. 채널을 즉시 닫을 수 있으며, 이 경우 청구를 먼저 처리하거나 처리하지 않을 수 있습니다. 채널에 잔여 XRP가 있는 경우 출처 주소는 채널을 즉시 닫을 수 없습니다.

  채널의 목적지 주소는 다음과 같은 작업을 수행할 수 있습니다:

  1. 서명된 청구서를 사용하여 채널로부터 XRP를 수령할 수 있습니다.
  2. 청구서를 처리한 후에 채널을 즉시 닫을 수 있으며, 이 경우 미청구 XRP를 채널의 출처로 환불합니다.

  이 트랜잭션을 보내는 어떤 주소든지, 이전 렛저의 마감 시간보다 만료 또는 CancelAfter 시간이 더 오래된 채널을 닫을 수 있습니다. 트랜잭션의 내용과는 상관없이 유효하게 구성된 PaymentChannelClaim 트랜잭션은 이 효과를 가집니다.

  ```json
  {
    "Channel": "C1AE6DDDEEC05CF2978C0BAD6FE302948E9533691DC749DCDD3B9E5992CA6198",
    "Balance": "1000000",
    "Amount": "1000000",
    "Signature": "30440220718D264EF05CAED7C781FF6DE298DCAC68D002562C9BF3A07C1E721B420C0DAB02203A5A4779EF4D2CCC7BC3EF886676D803A9981B928D3B8ACA483B80ECA3CD7B9B",
    "PublicKey": "32D2471DB72B27E3310F355BB33E339BF26F8392D5A93D3BC0FC3B566612DA0F0A"
  }
  ```

- **[PaymentChannelFund](https://xrpl.org/paymentchannelfund.html)**

  지불 채널에 XRP를 추가하고, 필요하다면 채널의 만료 시간을 업데이트합니다. 지불 채널의 출처 주소만 이 트랜잭션을 사용할 수 있습니다.

  ```json
  {
    "Account": "rf1BiGeXwwQoi8Z2ueFYTEXSwuJYfV2Jpn",
    "TransactionType": "PaymentChannelFund",
    "Channel": "C1AE6DDDEEC05CF2978C0BAD6FE302948E9533691DC749DCDD3B9E5992CA6198",
    "Amount": "200000",
    "Expiration": 543171558
  }
  ```

### 리퀘스트 (Request)

- **[channel_authorize](https://xrpl.org/channel_authorize.html)**

  지불자는 `channel_authorize` 메소드를 사용하여 생성한 서명(signature)는 수취인이 XRP를 인출하는데 필요한 권한을 부여합니다. 이 서명은 수취인에게 전송되어야 합니다.

  하지만 단순히 서명만을 보내는 것이 아니라, XRP Ledger에서의 `Payment Channel Claim` 트랜잭션을 제출하는데 필요한 몇 가지 정보도 함께 보내야 합니다. 이러한 정보에는 다음이 포함됩니다:

  1. `channel_id`: 결제 채널의 고유한 식별자입니다.
  2. `signature`: `channel_authorize` 메소드에 의해 생성된 서명입니다.
  3. `public_key`: 결제 채널을 만든 계정의 공개 키입니다.
  4. `amount`: 인출하려는 XRP 금액입니다.

  이 정보들을 수취인에게 제공하면, 수취인은 이를 사용하여 XRP Ledger에 `Payment Channel Claim` 트랜잭션을 제출하고, 지정된 금액의 XRP를 인출할 수 있습니다.

- [channel_verify](https://xrpl.org/channel_verify.html)

  `channel_verify` 메소드는 수취인이 결제 채널에서 특정 양의 XRP를 인출할 수 있는 서명의 유효성을 검사합니다. 보안성을 확보하고, 부정행위를 방지하기 위한 목적으로, 자금의 인출에 직접적으로 영향을 끼치지는 않습니다.

## 결제 채널 사용 시나리오

```python
import os

from account import XrplAccount
from transaction import XrplTransaction
from request import XrplRequest
from utils import Logger

DIR = os.path.dirname(__file__)


def main():
    # 0. 지불자와 수취인의 지갑을 연결합니다.
    payer = XrplAccount(
        wallet_path=os.path.join(DIR, "wallets", "payer.json"),
        create=True,
    )
    payee = XrplAccount(
        wallet_path=os.path.join(DIR, "wallets", "payee.json"),
        create=True,
    )

    # 트랜잭션과 리퀘스트를 위한 객체를 생성합니다.
    transaction = XrplTransaction()
    request = XrplRequest()
    # 결과 확인을 위해 로거를 생성합니다. (로그 파일은 logs 디렉토리에 저장됩니다.)
    logger = Logger(os.path.join(DIR, "logs", "channel_scenario.log"))

    # 1. 지불자: 채널 생성
    # 지불자가 채널을 생성하면 입력한 금액만큼의 XRP가 지갑으로부터 빠져나와 채널에 예치됩니다.
    result = transaction.create_payment_channel(
        account=payer,
        destination_address=payee.address,
        amount=500,
        settle_delay=86400,
        public_key=payee.wallet.public_key,
    )
    logger.log(result)

    # 지불자와 수취인 모두 채널의 공개키를 저장합니다. (이 공개키는 수취인이 청구서를 검증할 때 사용합니다.)
    channel_public_key = result["PublicKey"]

    # 2. 수취인: 채널 확인
    # 수취인은 지불자가 생성한 채널을 확인합니다.
    # 채널은 단방향이므로 수취인은 지불자의 계정 주소를 통해 채널을 확인합니다.
    result = request.get_account_channels(payee.client, payer.address)
    logger.log(result)

    channel_id = result["channels"][-1]["channel_id"]

    # 3. 지불자: 청구서에 서명
    # 지불자가 본인 지갑의 비밀키로 청구서에 서명합니다.
    result = request.authorize_channel(
        client=payer.client,
        channel_id=channel_id,
        amount=100,
        secret=payer.wallet.seed,
    )
    logger.log(result)
    # 서명 결과를 저장합니다. (이 서명 결과를 지불자가 수취인에게 전송해야 합니다. Off-ledger로 전송합니다.)
    signature = result["signature"]

    # 4. 지불자: 청구서를 수취인에게 전송
    # 필요한 정보들을 전부 포함시켜 청구서를 만듭니다.
    # Off-ledger로 청구서를 수취인에게 전송 합니다. (XRP Ledger에는 기록되지 않습니다.)
    invoice = {
        "channel_id": channel_id,
        "signature": signature,
        "amount": 100,
        "public_key": channel_public_key,
    }
    logger.log(invoice)

    # 5. 수취인: 청구서 확인
    # 수취인은 청구서를 확인하고, 청구서에 포함된 서명을 청구서의 공개키로 검증합니다.
    result = request.verify_channel(client=payee.client, **invoice)
    logger.log(result)

    # 6. 수취인: 상품 또는 서비스 제공
    # Off-ledger 또는 on-ledger로 상품 또는 서비스를 제공합니다.

    # 7. 원하는대로 3-6단계 반복합니다.

    # 8. 수취인: XRP 상환
    # 거래가 완료되면, 수취인은 인증된 금액에 대한 청구를 상환합니다.
    # 청구서는 누적된 금액을 포함하고 있으므로, 3~6단계가 여러번 진행됐어도 마지막 청구서만 claim하면 됩니다.
    # redeem_payment_channel은 내부에서 PaymentChannelClaim 트랜잭션을 생성합니다.
    result = transaction.redeem_payment_channel(
        account=payee, balance=invoice["amount"], **invoice
    )
    logger.log(result)

    # 9. 지불자: 채널 닫기 요청
    # 채널을 닫으면 채널에 남아있는 XRP가 지불자에게 돌아갑니다.
    # close_payment_channel은 내부에서 채널을 닫는 플래그를 포함한 PaymentChannelClaim 트랜잭션을 생성합니다.
    result = transaction.close_payment_channel(account=payer, channel_id=channel_id)
    logger.log(result)

    # 10. 지불자(또는 누군가): 만료된 채널 닫기
    # 만약 채널이 닫히지 않고 만료되었다면 아무나 (지불자나 수취인 말고도 정말 아무나) 채널을 닫을 수 있습니다.
    # result = transaction.close_payment_channel(account=payee, channel_id=channel_id)
    # logger.log(result)

    # 채널 닫혔는지 확인
    result = request.get_account_channels(payer.client, payer.address)
    logger.log(result)


if __name__ == "__main__":
    main()

```
