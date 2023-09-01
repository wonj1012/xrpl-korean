---
sidebar_position: 3
author: wonj1012
---

# XRPL DEX 샘플 프로젝트

## 1. 라이브러리 및 모듈 임포트

XRP Ledger를 사용하기 위해 필요한 라이브러리와 모듈을 불러옵니다.

```python
import os
from decimal import Decimal

from xrpl.models.currencies import (
    IssuedCurrency,
    XRP,
)
from xrpl.utils import (
    drops_to_xrp,
    get_balance_changes,
    xrp_to_drops,
)

from account import XrplAccount
from transaction import XrplTransaction
from request import XrplRequest
from utils import Logger
```

## 2. 스크립트 실행 디렉토리 설정

스크립트의 현재 위치를 기반으로 로그 파일과 지갑 정보와 같은 다른 리소스의 경로를 찾기 위해 사용됩니다.

```python
DIR = os.path.dirname(__file__)
```

로그 파일의 위치를 위해서 현재 스크립트의 디렉토리를 설정합니다.

## 3. 메인 함수 정의 및 초기화

메인 함수를 시작하면서 필요한 XRPL 계정과 로그 기록 도구를 준비합니다.

```python
def main():
    account = XrplAccount(
        wallet_path=os.path.join(DIR, "wallets", "dex_account.json"),
        create=False,
    )

    logger = Logger(os.path.join(DIR, "logs", "dex_scenario.log"))
```

## 4. 원하는 거래 조건 설정

거래하려는 화폐와 그에 대한 가격, 그리고 지불할 화폐와 그 가격을 설정합니다.

```python
    # TST 코인을 25개 사려고 합니다.
    we_want = {
        "currency": IssuedCurrency(
            currency="TST", issuer="rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd"
        ),
        "value": "25",
    }

    # XRP를 10개로 교환하려고 하고, 최대 15%의 교환 비용까지 지불하려고 합니다.
    # 저희가 원하는 비율보다 15% 비싸다면 (비율이 높다면) 거래를 진행하지 않습니다.
    we_spend = {
        "currency": XRP(),
        # 25 TST * 10 XRP per TST * 15% 교환 비용
        "value": xrp_to_drops(25 * 10 * 1.15),
    }

    # taker는 25 TST를 10 XRP로 교환하려고 합니다.
    # "Quality"는 TakerPays / TakerGets로 정의됩니다.
    # "Quality" 숫자가 작을수록 offer된 교환 비율이 taker에게 더 유리합니다.
    proposed_quality = Decimal(we_spend["value"]) / Decimal(we_want["value"])
```

## 5. XRPL 오더북 조회

특정 화폐 쌍에 대한 offer을 XRPL의 오더북에서 검색합니다.

```python
orderbook_info = XrplRequest.get_orderbook_info(
    client=account.client,
    taker_gets=we_want["currency"],
    taker_pays=we_spend["currency"],
)
logger.log("오더북 정보")
logger.log(orderbook_info)
```

- 이 코드는 XRPL의 오더북에서 특정 화폐 쌍에 대한 정보를 가져옵니다. 여기서 `we_want["currency"]`는 원하는 화폐, `we_spend["currency"]`는 지불할 화폐를 나타냅니다.

## 6. 오더북 `offer` 분석

오더북에서 받아온 offer을 분석하여 원하는 조건에 부합하는 offer이 있는지 확인합니다.

```python
offers = orderbook_info.get("offers", [])
want_amt = Decimal(we_want["value"])
running_total = Decimal(0)

if len(offers) == 0:
    logger.log("매칭 오더북에 offer이 없습니다. 즉시 실행될 가능성이 낮습니다.")
```

- 오더북에서 가져온 offer을 분석합니다.
- `offers`에는 오더북의 offer 목록이 들어 있습니다.
- `want_amt`는 원하는 화폐의 금액을 나타냅니다.

## 7. `offer` 목록 순회하며 조건 확인하기

```python
else:
        for o in offers:
            if Decimal(o["quality"]) <= proposed_quality:
                logger.log(
                    f"일치하는 제안이 발견되었고, {o.get('owner_funds')} "
                    f"{we_want['currency']}로 자금이 마련되었습니다."
                )
                running_total += Decimal(o.get("owner_funds", Decimal(0)))
                if running_total >= want_amt:
                    logger.log("전체 제안이 즉시 체결될 가능성이 높습니다.")
                    break
            else:
                logger.log("나머지 주문은 너무 비쌉니다.")
                break
```

- offer 목록을 순회하며 각 offer의 `quality`가 원하는 `quality`보다 낮은지 확인합니다.
- 만약 offer의 품질이 원하는 품질보다 낮다면, 그 offer의 자금을 `running_total`에 더합니다.

## 8. offer 총 합계 로깅

조건에 부합하는 offer의 총합을 로그에 기록합니다.

```python
logger.log(f"총 일치: {min(running_total, want_amt)} {we_want['currency']}")
        if 0 < running_total < want_amt:
            logger.log(
                f"나머지 {want_amt - running_total} {we_want['currency']} "
                "주문장 상단에 배치될 가능성이 있습니다."
            )
```

- 오더북의 offer 중 일부 또는 전체가 원하는 금액에 도달하는지 확인하고, 이에 따라 로그를 출력합니다.

## 9. 두 번째 오더북 정보 조회

```python
if running_total == 0:
        logger.log("총량이 0입니다")
        logger.log("두 번째 주문장 정보 요청 중...")
        orderbook2_info = XrplRequest.get_orderbook_info(
            client=account.client,
            taker=account.address,
            ledger_index="current",
            taker_gets=we_spend["currency"],
            taker_pays=we_want["currency"],
            limit=10,
        )

        logger.log("주문장2:")
        logger.log(orderbook2_info)

        # TakerGets/TakerPays가 반대이기 때문에 quality는 역수입니다.
        # 1 / proposed_quality로도 계산할 수 있습니다.
        offered_quality = Decimal(we_want["value"]) / Decimal(we_spend["value"])

        tally_currency = we_spend["currency"]
        if isinstance(tally_currency, XRP):
            tally_currency = f"{tally_currency}의 드롭"
```

- 첫 번째 오더북에서 원하는 offer을 찾지 못한 경우, 두 번째 오더북에서 정보를 가져옵니다.

## 10. 두 번째 오더북의 offer 정보 처리

```python
offers2 = orderbook2_info.get("offers", [])
        running_total2 = Decimal(0)
        if len(offers2) == 0:
            logger.log("주문장에 유사한 제안이 없습니다. 우리 제안이 첫 번째일 것입니다.")
        else:
            for o in offers2:
                if Decimal(o["quality"]) <= offered_quality:
                    logger.log(
                        f"기존 제안이 발견되었고, {o.get('owner_funds')} "
                        f"{tally_currency}로 자금이 마련되었습니다."
                    )
                    running_total2 += Decimal(o.get("owner_funds", Decimal(0)))
                else:
                    logger.log("나머지 주문은 우리 제안보다 아래에 배치될 것입니다.")
                    break

            logger.log(
                f"우리 제안은 적어도 {running_total2} " f"{tally_currency} 아래에 배치될 것입니다."
            )
            if 0 < running_total2 < want_amt:
                logger.log(
                    f"나머지 {want_amt - running_total2} {tally_currency} "
                    "주문장 상단에 배치될 가능성이 있습니다."
                )
```

- 두 번째 오더북에서 가져온 offer을 처리합니다. 첫 번째 오더북에서의 처리와 유사한 로직을 사용하되, 품질 계산이 조금 다릅니다.

요약하면, 이 코드는 XRPL의 오더북에서 특정 화폐 쌍에 대한 offer 정보를 가져와 원하는 금액에 도달할 수 있는지, 그리고 어떤 offer이 원하는 품질 조건에 부합하는지를 분석합니다.

## 10. OfferCreate 트랜잭션 전송

```python
result = XrplTransaction.create_offer(
    account=account,
    taker_gets=we_spend["value"],
    taker_pays=we_want["currency"].to_amount(we_want["value"]),
)
```

- XRPL에서 `OfferCreate` 트랜잭션을 전송하여 offer을 생성합니다. 이제 판매자는 `we_spend["value"]` 만큼의 자금을 지불하고 `we_want["currency"]` 화폐를 얻기를 원합니다.

## 11. 잔액 변동 확인

```python
balance_changes = get_balance_changes(result["meta"])
logger.log("잔액 변동:")
for change in balance_changes:
    logger.log(dict(change))
```

- 트랜잭션 결과에서 잔액의 변동 사항을 확인하고 로그에 출력합니다.

## 12. XRPL 금액을 문자열 변환

XRPL에서의 금액(혹은 drop)을 보기 좋게 문자열로 변환하는 함수입니다.

```python
def amt_str(amt) -> str:
    if isinstance(amt, str):
        return f"{drops_to_xrp(amt)} XRP"
    else:
        return f"{amt['value']} {amt['currency']}.{amt['issuer']}"
```

-

## 13. OfferCreate 트랜잭션 결과 분석

트랜잭션 결과에서 "AffectedNodes" 항목을 순회하여 결과를 분석합니다.

```python
offers_affected = 0
for affnode in result["meta"]["AffectedNodes"]:
    ...
```

## 14. 거래 결과 분석

트랜잭션 결과의 메타 데이터를 분석하여 영향을 받은 노드와 offer의 상태를 확인하고 로깅합니다.

```python
if "ModifiedNode" in affnode:
    if affnode["ModifiedNode"]["LedgerEntryType"] == "Offer":
        # 일반적으로 Offer 유형의 ModifiedNode는
        # 이전 Offer가 이 Offer에 의해 부분적으로 소비되었음을 나타냅니다.
        offers_affected += 1
    elif "DeletedNode" in affnode:
        if affnode["DeletedNode"]["LedgerEntryType"] == "Offer":
            # 제거된 Offer는 완전히 소비되었거나,
            # 만료되거나 또는 자금이 부족한 것으로 확인되었을 수 있습니다.
            offers_affected += 1
    elif "CreatedNode" in affnode:
        if affnode["CreatedNode"]["LedgerEntryType"] == "RippleState":
            logger.log("Trust line을 생성했습니다.")
        elif affnode["CreatedNode"]["LedgerEntryType"] == "Offer":
            offer = affnode["CreatedNode"]["NewFields"]
            logger.log(
                f"{offer['Account']}의 소유인 Offer가 생성되었습니다. "
                f"TakerGets={amt_str(offer['TakerGets'])} 및 "
                f"TakerPays={amt_str(offer['TakerPays'])}."
            )
logger.log(f"일치하는 Offer {offers_affected}개 수정 또는 제거")
```

## 16. 잔액 확인

검증된 원장에서 주소의 잔액을 확인합니다.

```python
logger.log("검증된 원장의 주소 잔액 가져오기...")
balances = XrplRequest.get_trust_lines(
    client=account.client,
    address=account.address,
    ledger_index="validated",
)

logger.log(balances)

logger.log("성공적으로 주문을 생성했습니다!")
```

## 17. 실행

스크립트가 실행되면 main 함수를 호출하여 앞서 정의한 모든 작업을 수행합니다.

```python
if __name__ == "__main__":
    main()
```
