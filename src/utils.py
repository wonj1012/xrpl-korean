from typing import NewType, Dict, Any, Callable

from xrpl.models.transactions import AccountSetAsfFlag
from xrpl.core.addresscodec import (
    classic_address_to_xaddress,
    is_valid_xaddress,
    is_valid_classic_address,
)

# Custom types
Address = NewType("Address", str)
Result = NewType("Result", Dict[str, Any])

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
        return classic_address_to_xaddress(address, tag=None, is_test_network=True)

    if is_valid_classic_address(address):
        return address

    return None
