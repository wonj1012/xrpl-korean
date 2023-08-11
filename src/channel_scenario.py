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
