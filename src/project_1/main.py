from os import path

from src.project_1.interface import Interface

WALLET_PATH = path.join(path.dirname(__file__), "..", "wallets")


def main():
    """
    메인 함수입니다.
    """
    interface = Interface()
    interface.run()


if __name__ == "__main__":
    main()
