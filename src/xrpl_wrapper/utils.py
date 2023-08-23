import logging
import json
from typing import NewType, Callable

from xrpl.models.transactions import AccountSetAsfFlag
from xrpl.core.addresscodec import (
    classic_address_to_xaddress,
    is_valid_xaddress,
    is_valid_classic_address,
)

# Custom types
Address = NewType("Address", str)

# Public server URLs
TESTNET_URL = "https://s.altnet.rippletest.net:51234"
PUBLIC_MAINNET_URL = "https://s1.ripple.com:51234"

# Enums
AccountSetFlag = AccountSetAsfFlag


def function_name_to_pretty(func: Callable) -> str:
    """
    함수 이름을 문자열로 변환합니다.

    Args:
        func (Callable): 변환할 함수입니다.

    Returns:
        str: 변환된 문자열입니다.
    """
    return " ".join(word.capitalize() for word in func.__name__.split("_"))


def to_classic_address(address: Address) -> Address | None:
    """
    X-주소를 클래식 주소로 변환합니다.
    만약 주소가 이미 클래식 주소라면 그대로 반환합니다.
    만약 주소가 유효하지 않다면 None을 반환합니다.

    Args:
        address: 변환할 X-주소입니다.

    Returns:
        클래식 주소입니다.
    """
    if is_valid_xaddress(address):
        return Address(
            classic_address_to_xaddress(address, tag=None, is_test_network=True)
        )

    if is_valid_classic_address(address):
        return address

    return None


class Logger:
    def __init__(self, log_file: str) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s\n%(message)s\n")
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def log(self, message: str | dict) -> None:
        if isinstance(message, dict):
            message = json.dumps(message, indent=4)
        self.logger.info(message)
