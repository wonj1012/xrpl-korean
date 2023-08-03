from pprint import pprint

from account import XrplAccount
from transaction import XrplTransaction
from request import XrplRequest


def main():
    payer = XrplAccount(wallet_path="wallets/payer.json", create=True)
    payee = XrplAccount(wallet_path="wallets/payee.json", create=True)
    transaction = XrplTransaction()
    request = XrplRequest()

    transaction.create_payment_channel(
        account=payer,
        destination_address=payee.address,
        amount=100,
        settle_delay=86400,
    )

    pprint(request.get_account_channels(payer.client, payer.address))
    pprint(request.get_account_channels(payee.client, payee.address))

    # request.authorize_channel(
    #     client=payer.client, channel_id=, amount=100
    # )


if __name__ == "__main__":
    main()
