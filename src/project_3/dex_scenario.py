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

from src.xrpl_wrapper.account import XrplAccount
from src.xrpl_wrapper.transaction import XrplTransaction
from src.xrpl_wrapper.request import XrplRequest
from src.xrpl_wrapper.utils import Logger


DIR = os.path.dirname(__file__)


def main():
    account = XrplAccount(
        wallet_path=os.path.join(DIR, "wallets", "dex_account.json"),
        create=False,
    )

    logger = Logger(os.path.join(DIR, "logs", "dex_scenario.log"))

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
    # "Quality" 숫자가 작을수록 제안된 교환 비율이 taker에게 더 유리합니다.
    proposed_quality = Decimal(we_spend["value"]) / Decimal(we_want["value"])

    # 오더북(주문장) 조회하기
    orderbook_info = XrplRequest.get_orderbook_info(
        client=account.client,
        taker_gets=we_want["currency"],
        taker_pays=we_spend["currency"],
    )
    logger.log("주문장 정보")
    logger.log(orderbook_info)

    offers = orderbook_info.get("offers", [])
    want_amt = Decimal(we_want["value"])
    running_total = Decimal(0)
    if len(offers) == 0:
        logger.log("매칭 주문장에 제안이 없습니다. 즉시 실행될 가능성이 낮습니다.")
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

        logger.log(f"총 일치: {min(running_total, want_amt)} {we_want['currency']}")
        if 0 < running_total < want_amt:
            logger.log(
                f"나머지 {want_amt - running_total} {we_want['currency']} "
                "주문장 상단에 배치될 가능성이 있습니다."
            )

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

    # OfferCreate 트랜잭션 전송 --------------------------------------------------

    # 이 튜토리얼에서는 TST가 대략 10:1의 비율과 스프레드를 더해서
    # XRP에 연동되어 있다는 것을 이미 알고 있으므로,
    # TakerGets와 TakerPays 금액을 하드코딩합니다.

    result = XrplTransaction.create_offer(
        account=account,
        taker_gets=we_spend["value"],
        taker_pays=we_want["currency"].to_amount(we_want["value"]),
    )

    balance_changes = get_balance_changes(result["meta"])
    logger.log("잔액 변경:")
    for change in balance_changes:
        logger.log(dict(change))

    # XRPL 금액을 표시 문자열로 변환하기 위한 헬퍼 함수
    def amt_str(amt) -> str:
        if isinstance(amt, str):
            return f"{drops_to_xrp(amt)} XRP"
        else:
            return f"{amt['value']} {amt['currency']}.{amt['issuer']}"

    # OfferCreate 트랜잭션 결과 분석 --------------------------------------------
    offers_affected = 0
    for affnode in result["meta"]["AffectedNodes"]:
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

    # 잔액 확인 ------------------------------------------------------------
    logger.log("검증된 원장의 주소 잔액 가져오기...")
    balances = XrplRequest.get_trust_lines(
        client=account.client,
        address=account.address,
        ledger_index="validated",
    )

    logger.log(balances)

    logger.log("성공적으로 주문을 생성했습니다!")


if __name__ == "__main__":
    main()
