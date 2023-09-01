---
sidebar_position: 2
author: wonj1012
---

# 계정

이 챕터에서는 XRP Ledger의 계정과 지갑을 생성하고 관리하는 방법을 소개합니다.

## XRP Ledger 암호화 방식

XRP Ledger의 계정은 다른 블록체인에서와 마찬가지로 암호학적 원리를 기반으로 합니다. 이는 계정의 주소를 생성하고, 트랜잭션을 서명하고, 계정의 소유권을 증명하는 등의 작업에 사용됩니다. 이러한 작업은 모두 암호화 알고리즘을 통해 이루어지며, 이 알고리즘은 대칭 키 암호화와 비대칭 키 암호화 두 가지로 구분됩니다. XRP Ledger에서는 비대칭 키 암호화를 사용합니다.

### 대칭 키 알고리즘

대칭 키 알고리즘은 암호화와 복호화에 같은 키를 사용하는 암호화 방식입니다. 이 키는 암호화된 데이터를 복호화하는 데 사용되며, 이 키를 알지 못하는 사람은 암호화된 데이터를 복호화할 수 없습니다. 대칭 키 암호화의 가장 큰 문제점은 키 교환 문제입니다. 암호화와 복호화에 같은 키를 사용하므로, 이 키를 안전하게 교환해야 하는 문제가 있습니다.

<!-- ![symmetric-key-encryption]() -->

### 비대칭 키 알고리즘

비대칭 키 알고리즘, 또는 퍼블릭 키 암호화는 암호화와 복호화에 사용되는 두 개의 키가 서로 다른 암호화 방식입니다. 이 두 키 중 하나는 공개 키(public key), 다른 하나는 비밀 키(private key) 또는 개인 키라고 합니다. 이들 키는 쌍으로 작동하며, 한 키로 암호화된 데이터는 오직 그에 상응하는 다른 키로만 복호화할 수 있습니다.

비대칭 키 암호화의 가장 큰 장점은 키 교환 문제를 해결한다는 것입니다. 대칭 키 암호화에서는 암호화와 복호화에 같은 키를 사용하므로, 이 키를 안전하게 교환해야 하는 문제가 있습니다. 하지만 비대칭 키 암호화에서는 공개 키를 자유롭게 배포할 수 있으므로, 이러한 문제가 발생하지 않습니다.

예를 들어, A가 B에게 암호화된 메시지를 보내려 할 때, A는 B의 공개 키를 사용하여 메시지를 암호화합니다. 이렇게 암호화된 메시지는 B의 비밀 키로만 복호화할 수 있으므로, 메시지의 안전성이 보장됩니다.

<!-- ![asymmetric-key-encryption]() -->

## XRP Ledger 계정 생성 원리

XRP Ledger의 비대칭 키 생성은 Elliptic Curve Cryptography(ECC) 기반입니다. 이는 매우 큰 두 개의 소수의 곱을 인수분해하는 것이 사실상 불가능하기 때문에 강력한 보안을 제공합니다.

XRP Ledger에서의 키 생성은 다음과 같은 원리로 이루어집니다.

<!-- ![cryptographic-keys](../img/account_and_transaction/cryptographic-keys.svg) -->

여기에서 시드, 비공개 키는 타인에게 노출되어서는 안되고 보안을 위해 안전하게 보관되어야 합니다. 그에 반해 공개 키, 계정 ID, 주소는 타인에게 노출되어도 안전합니다.

### 키 생성 과정

1. **시드 생성**

   사용자는 임의의 시드를 선택하거나 생성합니다. XRP Ledger에서는 암호학적으로 안전한 난수 생성기를 사용해 16바이트의 임의의 데이터를 생성해서 원시 시드로 사용합니다. 원시 시드는 Base58Check 인코딩을 통해 다시 s로 시작하는 29자리의 문자열로 변환됩니다.

   ```python
   from xrpl.core.keypairs import generate_seed

   # Generate a seed
   seed = generate_seed()

   # Print seed
   print(f"seed: {seed}")
   ```

   ```python
   seed: sEdTAmewybtGPwEqGaCGC2KBBJN77gV
   ```

2. **비공개 키 생성**

   앞에서 생성한 원시 시드를 사용하여 타원곡선 DSA (Elliptic Curve Digital Signature Algorithm, ECDSA)를 통해 비공개 키를 생성합니다. 비공개 키를 생성하는 과정은 타원곡선의 기본 점(G)을 원시 시드(s)번 곱하는 것으로, 이 연산을 통해 타원곡선 위의 새로운 점(P)이 얻어지게 됩니다. 즉, 비공개 키는 기본적으로 타원곡선 위의 한 점입니다.

3. **공개 키 생성**

   비공개 키를 사용하여 공개 키를 생성합니다. 공개 키는 비공개 키(타원곡선 위의 점)에 타원곡선의 기본 점을 곱하여 얻어집니다. 이렇게 생성된 공개 키는 비밀 키를 알지 못하는 다른 사람들이 메시지를 암호화하거나 디지털 서명을 검증하는 데 사용될 수 있습니다.

   ```python
   from xrpl.core.keypairs import derive_keypair

   # Derive a keypair from a seed
   public_key, private_key = derive_keypair("sEdTAmewybtGPwEqGaCGC2KBBJN77gV")

   print(f"public key: {public_key}\nprivate key: {private_key}")
   ```

   ```python
   public key: EDBB2431197ECED939BE4552A583A5D060F5BC0AF9BD5D480A34BFD6787FAE83B1
   private key: EDD3FDF904528CC68CABB645BE19BFB34FE1854D8DD52214AE516338354E3A7F53
   ```

4. **계정 ID 생성**

   공개 키는 다시 계정 ID로 해시됩니다. 이 계정 ID는 공개 키의 SHA-256 해시이며, 이 해시의 첫 20바이트만 사용됩니다.

5. **XRP Ledger 주소 생성**

   계정 ID는 최종적으로 XRP Ledger 주소로 변환됩니다. 이 변환은 Base58Check 인코딩을 사용하며, 이는 주소의 첫 글자가 'r'로 시작하게 만듭니다. 이 인코딩 방식은 오류 감지 기능을 내장하고 있어, 주소를 잘못 입력했을 때 이를 감지할 수 있게 합니다.

   ```python
   from xrpl.core.keypairs import derive_classic_address

   address = derive_classic_address(
       public_key="EDBB2431197ECED939BE4552A583A5D060F5BC0AF9BD5D480A34BFD6787FAE83B1"
   )

   print(f"address: {address}")
   ```

   ```python
   address: rpifos5x2NQXRW1fxc2uK5WuuZtoWdDh4L
   ```

이러한 과정을 통해 XRP Ledger에서 사용할 수 있는 지갑이 생성됩니다. 하지만 실제 지갑 생성 시에는 직접 이 과정을 따라할 필요는 없고, 모든 과정이 자동으로 사용자의 기기에서 안전하게 이루어지게 됩니다.

### 지갑 활성화

앞에서 비공개 키와 공개 키, 계정 ID, 주소를 생성했습니다. 하지만 그것들을 생성한 것만으로 아직은 XRP Ledger에서 거래를 할 수 없습니다. XRP Ledger에서 거래를 할 수 있도록 지갑(주소)를 활성화 시키려면, 해당 지갑의 주소로 최소 10 XRP를 전송해야 합니다. 이것은 XRP Ledger의 [Reserves](https://xrpl.org/reserves.html)라는 정책으로 계정이 최소 10 XRP 이상을 보유하고 있어야만 계정이 활성화되어 거래를 할 수 있습니다. 이는 스팸 계정이나 악의적인 계정 이용으로 인한 과부화를 방지하기 위한 목적입니다.

### Destination Tag와 X-address

XRP Ledger는 분산형 디지털 자산 네트워크로, Ripple의 디지털 토큰인 XRP를 활용하는 많은 기관과 개인이 플랫폼을 사용합니다. 그러나, 이러한 모든 사용자에게 고유한 주소를 제공하는 것은 매우 비효율적일 수 있습니다. 따라서 XRP Ledger는 Destination Tag라는 특별한 개념을 도입했습니다.

Destination Tag는 정확하게 말하면 고유의 숫자 식별자로, 특정 사용자를 식별하고 거래를 추적하는 데 사용됩니다. 이는 특히 대형 거래소나 월렛 서비스와 같이 여러 사용자가 동일한 XRP 주소를 공유하는 경우에 유용합니다. Destination Tag를 통해, 서비스 제공자는 사용자 간의 거래를 더욱 정확하게 구분하고 관리할 수 있습니다.

예를 들어, 거래소 X가 단일 XRP 주소를 사용하여 모든 사용자의 자금을 관리한다고 가정해보겠습니다. 이제 사용자 A와 사용자 B가 모두 이 거래소로 XRP를 입금하려고 합니다. 두 사용자의 입금을 어떻게 구분할까요? 여기서 Destination Tag가 중요한 역할을 합니다. 사용자 A는 Destination Tag 12345를 받고, 사용자 B는 67890을 받습니다. 이제 두 사용자가 동일한 주소로 입금할 때, 거래소는 Destination Tag를 통해 누가 입금했는지 알 수 있습니다.

이와 같이, Destination Tag는 XRP Ledger의 효율성과 정확성을 향상시키는 중요한 역할을 합니다. 이는 사용자가 자신의 거래를 쉽게 추적하고, 사용자간의 거래가 혼란스럽게 얽히는 것을 방지하며, 거래소나 월렛 서비스가 효과적으로 자금을 관리하게 돕습니다.

X-address는 XRP Ledger의 주소 체계의 한 부분으로, 주소와 Destination Tag를 합친 새로운 형식의 주소입니다. 이 주소 형식은 Destination Tag를 내장하고 있어, 사용자가 주소와 Destination Tag를 별도로 입력할 필요가 없습니다. 이로 인해 사용자의 실수를 줄일 수 있으며, 편리하고 안전한 XRP Ledger 사용 경험을 제공합니다.

## 암호화 키 활용 방식

위에서 언급된 과정을 통해 생성된 암호화 키들은 XRP Ledger에서 매우 다양하게 활용됩니다. 이러한 키들의 주요 활용 방식은 아래와 같습니다.

- **디지털 서명(Digital Signature Algorithm, DSA)**

  비공개 키를 사용해 메시지를 '서명'하고, 공개 키를 사용해 서명을 검증합니다. 이 과정은 다음과 같이 진행됩니다.

  1. 서명 생성: 거래를 생성한 후, 해당 거래를 비공개 키로 서명합니다. 이는 일종의 암호화 작업으로 볼 수 있으며, 이 작업을 거치면 서명된 거래가 생성됩니다. 비공개 키는 서명 프로세스에서 사용되며, 이 키는 거래를 생성한 사용자만이 알고 있습니다. 이렇게 하면 거래의 무결성이 보장되며, 거래가 변경되지 않았음을 확인할 수 있습니다.

  2. 서명 검증: 거래를 수신한 측은 공개 키를 사용하여 서명을 검증합니다. 이 과정에서는 거래와 함께 전달된 디지털 서명과 원래 거래를 비교합니다. 공개 키를 사용하여 디지털 서명을 '복호화'하고, 복호화된 내용이 원래의 거래 내용과 일치하는지 확인합니다. 만약 일치한다면, 이는 거래가 중간에 변경되지 않았으며, 해당 비공개 키의 소유자가 거래를 생성하였음을 의미합니다.

  이렇게 비공개 키와 공개 키를 활용한 디지털 서명 시스템은 전자 거래에서의 사기를 방지하고, 정보의 무결성을 보장하며, 디지털 세계에서의 신뢰를 구축하는데 매우 중요한 역할을 합니다. XRP Ledger에서도 이러한 원리가 적용되어, 거래의 안전성과 보안을 보장하고 있습니다.

- **계정 소유권 증명**

  암호화 키는 계정의 소유권을 증명하는 데에도 사용됩니다. 각 XRP Ledger 계정은 공개 키와 그에 연결된 비공개 키로 생성됩니다. 이 비공개 키는 계정의 소유자만이 알고 있어야 합니다. 이 비공개 키로 생성된 디지털 서명은 공개 키를 통해 검증 가능하며, 이를 통해 특정 계정의 소유권을 증명할 수 있습니다. 즉, 만약 사용자가 계정의 비공개 키로 거래를 서명할 수 있다면, 그 사용자는 해당 계정의 합법적 소유자임을 증명한 것이 됩니다. 이렇게 암호화 키를 사용하는 것은 계정의 소유권을 신원을 증명하는 강력한 도구가 됩니다.

## 안전한 지갑 보관

- **안전한 온라인 지갑 사용**

  [XUMM](https://xumm.app/)은 XRP Ledger 지갑을 생성하고 관리하는 모바일 지갑 앱입니다. XRPL Labs 팀에 의해 디자인되고 개발되었습니다. XUMM은 키를 안전하게 보관하고, 키를 사용하여 거래를 서명하고, 키를 사용하여 계정을 제어하는 모든 기능을 제공합니다. 앱은 사용자 친화적인 인터페이스와 강력한 보안 기능을 결합하여 사용자가 자신의 자산을 안전하게 관리할 수 있게 해줍니다. 또한 모바일 앱이지만, QR 코드 스캔 기능을 도입해 편하고 쉽게 데스크톱에서도 사용할 수 있습니다.

  <!-- ![xumm-wallet]() -->

  XUMM의 보안 체계는 다음과 같은 주요 요소들을 포함하고 있습니다:

  - **암호화**: XUMM은 사용자의 비공개 키를 암호화하여 로컬 스토리지에 안전하게 보관합니다. 이 키는 암호화되어 있으므로, 실제 키 값을 얻으려면 사용자의 비밀번호나 PIN 코드를 알아야 합니다.

  - **사용자 인증**: XUMM은 사용자가 자신의 지갑에 접근하거나 트랜잭션을 서명할 때마다 비밀번호나 PIN 코드를 입력하도록 요구합니다. 이는 비공개 키에 대한 접근을 보호하고, 무단으로 거래가 발생하는 것을 방지하는 데 중요한 역할을 합니다.

  - **개인정보 보호**: XUMM은 사용자의 개인정보와 금융 정보를 존중합니다. 애플리케이션은 사용자의 지갑 주소나 트랜잭션 정보를 수집하지 않으며, 서버에 저장하지 않습니다. 또한, XUMM은 필요한 최소한의 데이터만을 수집하고, 이를 안전하게 암호화하여 저장합니다.

  - **디지털 서명**: XUMM은 사용자의 비공개 키를 사용하여 XRP Ledger의 트랜잭션을 서명합니다. 이 서명 과정은 사용자의 기기에서 직접 이루어지며, 비공개 키가 사용자의 기기를 벗어나지 않도록 보장합니다.

- **하드웨어 지갑 사용**

  하드웨어 지갑은 암호화폐를 보관하는데 가장 안전한 방법 중 하나입니다. 이들은 인터넷에 연결되지 않은 상태에서 키를 안전하게 보관하는 데 사용되는 물리적인 장치입니다. 이런 방식으로, 하드웨어 지갑은 온라인 해킹 공격으로부터 사용자의 자산을 보호해 줍니다. 트레저(Trezor)와 레저(Ledger)와 같은 브랜드는 이 분야에서 가장 잘 알려져 있습니다. 이들은 모두 확보된 환경에서 개인 키를 생성하고, 그 키가 장치 밖으로 나가지 않게 하는 등의 보안 기능을 제공합니다.

  <!-- ![hardware-wallet]() -->

- **비밀번호 관리자 사용**

  비밀번호 관리자는 암호화폐 사용자에게 매우 유용한 도구가 될 수 있습니다. 이러한 서비스는 사용자의 키를 안전하게 보관하며, 그것들을 암호화하여 저장합니다. 또한 사용자가 필요로 할 때마다 암호화된 키를 복호화할 수 있게 해줍니다. 그 결과, 사용자는 복잡한 비밀번호를 기억할 필요 없이 모든 자산에 대한 접근을 유지할 수 있습니다. 비밀번호 관리자는 강력한 암호화 알고리즘을 사용하여 사용자의 정보를 보호하므로, 해커가 그 정보를 이용하는 것은 극히 어렵습니다.

## Regular key와 Master key

XRP Ledger (XRPL)에서 Master Key와 Regular Key는 모두 거래를 서명할 수 있는 권한을 가지지만, 그 용도와 관리 방식에는 차이가 있습니다.

- **Master Key**

  Master Key는 계정을 생성할 때 생성되며, 계정 설정 변경, 거래 서명 등 계정의 모든 기능을 통제할 수 있는 권한을 가집니다. 또한, 계정 소유권을 증명하는 유일한 방법이므로 매우 중요합니다.

- **Regular Key**

  Regular Key는 Master Key를 대체하거나 보안을 강화하려는 목적으로 사용될 수 있습니다. Regular Key는 Master Key와 같은 권한을 가지나, Regular Key를 변경하거나 삭제하는 것이 Master Key를 변경하거나 삭제하는 것보다 더 쉽습니다. 또한, Regular Key를 사용하여 계정을 제어하면, Master Key를 안전하게 보관하면서도 일상적인 거래를 수행할 수 있습니다.

그러나, XRPL에서 Regular Key는 Master Key가 가지는 계정 설정 변경 등의 일부 권한을 대체하지 못합니다. Master Key는 계정을 삭제하거나, Regular Key를 설정하거나 변경하는 등의 권한을 가집니다. 따라서 Regular Key는 일상적인 거래를 수행하고, Master Key는 더 중요하고 민감한 작업을 수행하는 데 사용됩니다.

즉, Master Key와 Regular Key 모두 계정을 제어하는 권한을 가지지만, Master Key는 더 많은 권한과 더 높은 보안 요구 사항을 가지고 있습니다. Master Key는 또한 Regular Key를 생성하고 변경하는 데 사용되며, 이로써 Master Key의 보안을 강화하고, 일상적인 거래를 보다 안전하게 수행할 수 있습니다.

### Regular Key 설정

다음은 Regular Key를 생성하고, Master Key를 비활성화하는 과정을 보여줍니다.

1. **Regular key의 생성**

   Regular key는 공개 키와 비밀 키의 쌍으로 구성됩니다. 이 키의 생성은 전자 서명 알고리즘에 의해 이루어지며, 보통은 암호화 방법론의 일부인 elliptic-curve cryptography (ECC)를 사용합니다.

   Regular key의 생성은 보안상 매우 중요한 단계입니다. 일반적으로 이는 안전한 난수 생성기를 사용하여 이루어지며, 키 생성 프로세스의 모든 부분이 적절히 보호되어야 합니다. 생성된 비밀 키는 절대 노출되어서는 안되며, 안전하게 저장되어야 합니다.

   생성된 Regular key는 특정 계정의 새로운 인증 수단으로 사용될 수 있습니다. 이를 통해 기본적인 계정 관리를 위한 Master key의 사용을 줄이고, 계정의 보안을 강화할 수 있습니다. 이는 특히 블록체인 기술에서 중요한데, 그 이유는 한 번 생성된 키는 변경이 불가능하며, 잘못 관리되거나 노출될 경우 해당 계정의 자산이 위험에 노출되기 때문입니다.

2. **Regular key의 할당**

   생성된 Regular key는 특정 계정에 할당되어야 합니다. 이 단계는 Regular key를 해당 계정의 새로운 접근 키로 설정합니다. Regular key의 할당은 사용자의 목표에 따라 진행될 수 있으며, 트랜잭션 서명 또는 계정 관리를 위한 새로운 방법을 제공합니다.

3. **Master key의 비활성화**

   Regular key가 할당되면 Master key를 비활성화할 수 있습니다. 이는 해당 계정에 대한 모든 권한이 Regular key로 이동함을 의미합니다. 이 단계는 Regular key를 주된 계정 키로 설정하고, Master key를 더 이상 사용하지 않도록 하여 추가적인 보안 레벨을 제공합니다. 이는 특히 Master key가 위험에 노출되었거나 손실됐을 경우 유용합니다.

4. **Regular key의 업데이트 및 Master key의 재활성화**

   사용자의 필요에 따라, Regular key는 업데이트 될 수 있습니다. 이는 새로운 Regular key를 생성하고 계정에 재할당하는 과정을 포함합니다. 또한, 필요한 경우 Master key는 언제든지 재활성화 될 수 있습니다. 이는 Master key가 필요한 특정 트랜잭션을 진행하거나, Regular key를 대체하거나 삭제해야 할 때 유용합니다.

이러한 절차는 계정 보안을 강화하는 중요한 방법입니다. Regular key와 Master key를 적절히 관리하면, 암호화폐 지갑의 안전성을 크게 향상시킬 수 있습니다. 키를 관리하는 과정에서는 항상 안전하게 보관하고, 백업하는 등의 절차를 따르는 것이 중요합니다.

## 실습 프로젝트

이번 실습에서는 XRP Ledger 지갑을 생성하고, 계정을 활성화 한 후, Regular Key를 생성 및 설정하는 과정을 진행합니다.

### 지갑 생성

먼저 XRP Ledger에서 지갑을 생성해보겠습니다.

xrpl-py와 같은 라이브러리를 사용하여 직접 만들 수도 있고, [XUMM](https://xumm.app/)과 같은 지갑 앱을 사용할 수도 있습니다. XUMM 이용 가이드는 [이 링크](https://help.xumm.app/getting-started-with-xumm/installing-xumm)를 참고하세요. 이번 실습에서는 xrpl-py를 사용하여 지갑을 생성해보겠습니다. 여기서 만든 지갑은 다시 XUMM과 같은 지갑 앱에 연결할 수도 있습니다.

테스트넷에서 간단하게 이용해보려면 [`generate_faucet_wallet`](https://xrpl-py.readthedocs.io/en/latest/source/xrpl.wallet.html#xrpl.wallet.generate_faucet_wallet) 함수를 이용해도 좋습니다. 이 함수는 다음에 나오는 지갑 활성화 파트에서 다시 설명하겠습니다.

```python
from xrpl.wallet import Wallet
from xrpl.constants import CryptoAlgorithm

wallet = Wallet.create()
```

[`Wallet.create()`](https://xrpl-py.readthedocs.io/en/latest/source/xrpl.wallet.html#xrpl.wallet.Wallet.create) 메서드에는 `algorithm=CryptoAlgorithm.ED25519`와 같이 매개변수를 주어 암호화 알고리즘을 지정할 수도 있습니다. 기본값은 ED25519입니다. 암호화 알고리즘의 종류는 [여기](https://xrpl-py.readthedocs.io/en/latest/source/xrpl.html#xrpl.constants.CryptoAlgorithm)에서 확인할 수 있습니다.

지갑 정보를 확인하려면 다음과 같이 입력합니다.

```python
print(wallet)
```

```python
public_key: EDBD30AA72B8A968705D535B4C4B2843E692F68026D6D5AB44C9E06834FDB1310E
private_key: -HIDDEN-
classic_address: rGjfhcmVfrwW4DRcghhdR8ZXUViqFdpt83
```

비공개 키를 포함한 모든 정보를 확인하고 싶다면 다음과 같이 입력합니다.

```python
print(wallet.__dict__)
```

```python
{'_address': 'rshhyEKHHeW2CUBryRdFpZ5LeSh4tdN4Cq',
 'algorithm': <CryptoAlgorithm.ED25519: 'ed25519'>,
 'private_key': 'ED0DDC86B79A55C1B8BEA8BB4D27187C1C731B55FA0417E0519CB31306AC78D373',
 'public_key': 'ED8A9341F24320B8218D591A599D5B2C12D3EF750A32C0857061153AEC8E809C37',
 'seed': 'sEdTjia3fsH9AtAnmYm1rUwTHazetY2'}
```

### 지갑 저장 및 불러오기

지갑을 직접 저장하고 불러오려면 다음과 같은 방법을 사용할 수 있습니다.

```python
import json

with open(wallet_path, "w", encoding="UTF-8") as file:
    json.dump(wallet.__dict__, file)
```

위 코드는 지갑의 정보를 JSON 형식으로 파일에 저장합니다. 이를 다시 불러오려면 다음과 같이 입력합니다.

```python
import json
from xrpl.wallet import Wallet

with open(wallet_path, "r", encoding="UTF-8") as file:
    wallet_info = json.load(file)

wallet = Wallet(
    public_key=wallet_info["public_key"],
    private_key=wallet_info["private_key"],
    master_address=wallet_info["address"],
    seed=wallet_info["seed"],
    algorithm=wallet_info["algorithm"],
)
```

이렇게 하면 지갑을 다시 불러올 수 있습니다. 이 방법은 지갑을 직접 저장하고 불러오는 방법 중 하나입니다. 하지만 이 방법은 지갑의 정보를 모두 저장하므로, 보안에 취약할 수 있습니다. 따라서 실제 지갑을 저장할 때는 암호화를 하거나 다른 지갑 서비스, 하드웨어 지갑 등을 사용하는 것이 좋습니다.

### 지갑 활성화

지갑을 활성화 하려면 최소 10 XRP를 보유해야 합니다. 테스트넷에서는 무료로 테스트용 XRP를 제공하는 'Faucet' 서비스를 이용할 수 있습니다. 이 서비스를 이용하면, 테스트용 XRP가 들어있는 지갑을 생성하거나 기존 지갑에 테스트용 XRP를 전송할 수 있습니다.

- **테스트용 XRP가 들어있는 지갑 생성**

  ```python
  from xrpl.wallet import generate_faucet_wallet

  wallet = generate_faucet_wallet(client=client)
  ```

- **기존 지갑에 테스트용 XRP 전송**

  ```python
  from xrpl.wallet import generate_faucet_wallet

  wallet = generate_faucet_wallet(client=client, wallet=wallet)
  ```

### 계정 정보 확인

계정 정보를 확인하려면, XRP Ledger로 부터 계정 정보의 데이터를 요청해야 합니다.

XRP Ledger로부터 레저의 데이터를 요청하는 방법은 [`xrpl.models.requests`](https://xrpl-py.readthedocs.io/en/latest/source/xrpl.models.requests.html)에서 원하는 요청 클래스를 불러와서 내용을 채우고, [`client.request`](https://xrpl-py.readthedocs.io/en/latest/source/xrpl.clients.html#xrpl.clients.JsonRpcClient.request) 메서드에 넣어주면 됩니다.

계정 정보는 `AccountInfo` 요청 클래스를 사용하여 요청할 수 있습니다.

```python
from xrpl.models.requests import AccountInfo

response = client.request(request = AccountInfo(account=wallet.classic_address))

print(response.result)
```

```python
{'account_data': {'Account': 'r9Y5orxqCmkHDPUEX9jG2zhadz8PwNA7sg',
                  'Balance': '10000000000',
                  'Flags': 0,
                  'LedgerEntryType': 'AccountRoot',
                  'OwnerCount': 0,
                  'PreviousTxnID': 'E3A3B7B1619A618261154A9468E8F93D28AC7B813F40741D494A0ED7B9794653',
                  'PreviousTxnLgrSeq': 39662860,
                  'Sequence': 39662860,
                  'index': '173F2F53EB166A75818F3D01D9CCB7ECEF83879B99C869ADF32F5A438A657BAF'},
 'account_flags': {'defaultRipple': False,
                   'depositAuth': False,
                   'disableMasterKey': False,
                   'disallowIncomingCheck': False,
                   'disallowIncomingNFTokenOffer': False,
                   'disallowIncomingPayChan': False,
                   'disallowIncomingTrustline': False,
                   'disallowIncomingXRP': False,
                   'globalFreeze': False,
                   'noFreeze': False,
                   'passwordSpent': False,
                   'requireAuthorization': False,
                   'requireDestinationTag': False},
 'ledger_current_index': 39662862,
 'validated': False}
```

계정 정보에는 계정의 잔액, 시퀀스 번호, 플래그 등이 포함되어 있습니다. 이 정보를 통해 계정의 상태를 확인할 수 있습니다.

### Regular Key 생성

Regular Key를 생성하고, 등록하려면 Ledger에 트랜잭션을 제출해야 합니다. 트랜잭션을 제출하는 과정은 transaction 파트에서 더 자세하게 다루고 이번 실습에서는 해당 부분에 대한 설명은 간단하게 하겠습니다.

```python
from pprint import pprint

from xrpl.clients import JsonRpcClient
from xrpl.models.transactions import SetRegularKey
from xrpl.transaction import autofill_and_sign, submit_and_wait
from xrpl.wallet import generate_faucet_wallet, Wallet

# JsonRpcClient 객체 생성
client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

# master key 지갑 (원래 있던 지갑을 불러오면 됩니다. 여기서는 예시를 위해 새로운 테스트 지갑을 생성했습니다)
my_wallet = generate_faucet_wallet(client=client)

# regular key 지갑 생성
regular_key_wallet = Wallet.create()

# SetRegularKey 트랜잭션 객체 생성
set_regular_key_tx = SetRegularKey(
    account=my_wallet.classic_address,
    regular_key=regular_key_wallet.classic_address,
)

# 트랜잭션 필드 자동 채우기 및 서명
signed_tx = autofill_and_sign(
    transaction=set_regular_key_tx, client=client, wallet=my_wallet
)

# 트랜잭션 제출 및 응답 반환
response = submit_and_wait(transaction=signed_tx, client=client, wallet=my_wallet)

# 결과 출력
pprint(response.result)
```

위 코드는 Regular Key를 생성하고, 등록하는 과정을 보여줍니다.

Regular Key를 등록하려는 계정의 지갑은 `my_wallet`이며, 이 지갑의 공개와 비공개 키 쌍이 바로 Master Key 입니다.

먼저, 새로운 키 쌍을 합니다. 이를 위해 새로운 지갑(`regular_key_wallet`)을 생성하며, 이 지갑의 키 쌍이 Regular Key가 됩니다. 이 지갑의 생성은 이전에 설명한 지갑 생성 방법을 통해 진행할 수 있습니다.

다음으로 `SetRegularKey` 트랜잭션 객체를 생성합니다. 이 때, `my_wallet`의 주소와 `regular_key_wallet`의 공개 키를 트랜잭션에 포함시킵니다.

트랜잭션 서명을 위해 `sign_and_autofill` 함수를 사용하며, 이 함수는 트랜잭션에 필요한 세부 정보를 자동으로 채워넣고 서명 과정을 진행합니다.

마지막으로, `submit_and_wait` 함수를 사용하여 서명된 트랜잭션을 XRPL에 제출하고, 처리 결과를 기다립니다.

제출이 성공적으로 이루어진 경우, Regular Key가 성공적으로 등록되었음을 의미합니다. 이후부터는 `my_wallet`에 관련된 트랜잭션 서명 시, 아래의 코드와 같이 Master Key 대신 이 Regular Key를 사용하여 서명할 수 있게 됩니다. 이렇게 함으로써 Master Key는 안전하게 보관되며, 일상적인 트랜잭션 서명은 Regular Key를 통해 이루어질 수 있습니다.

```python
from xrpl.transaction import sign

# some_tx = Transaction(account=my_wallet.classic_address, ...)

signed_tx = sign(
    transaction=some_tx, wallet=regular_key_wallet, client=client
)
```
