---
sidebar_position: 1
author: wonj1012
---

# 개발환경 설정

이 챕터에서는 XRP Ledger와 상호작용하는 어플리케이션을 개발하기 위한 파이썬 개발환경 설정 방법을 안내합니다.

## xrpl-py 라이브러리

xrpl-py 라이브러리는 파이썬으로 만들어진 도구로, XRP Ledger와 편하게 소통할 수 있게 해줍니다.

XRP Ledger와 상호작용하면서 겪게 되는, 예를 들어 데이터의 직렬화나 거래 서명 같은 어려운 문제들을 파이썬 방식의 간단한 방법과 모델로 제공합니다.

이를 통해 XRP Ledger의 트랜잭션과 핵심 서버 API(rippled) 객체를 쉽게 다룰 수 있게 도와줍니다.

## 사전 요구사항

- Python 3.7 이상
- pip (Python 패키지 관리자)

## xrpl-py 설치

1. **[xrpl-py](https://xrpl-py.readthedocs.io/en/latest/index.html) 라이브러리 설치**

   xrpl-py 라이브러리를 설치하기 위해, 터미널을 열고 아래의 pip 명령을 실행하세요.

   ```shell
   pip install xrpl-py
   ```

2. **설치 확인**

   설치가 정상적으로 이루어졌는지 확인하기 위해, Python 인터프리터를 실행하고 다음의 코드를 입력하세요.

   ```python
   import xrpl
   print(xrpl.__version__)
   ```

   이 코드는 설치된 xrpl-py의 버전을 출력할 것입니다. 이렇게 함으로써 xrpl-py가 정상적으로 설치되었음을 확인할 수 있습니다.

## 개발환경 설정 완료!

이제 xrpl-py를 사용하여 XRP Ledger와 상호작용하는 Python 애플리케이션을 개발할 수 있습니다. 더 많은 정보를 얻기 위해서는 [xrpl-py 공식 문서](https://xrpl-py.readthedocs.io/en/latest/)를 참고하세요.

## XRP Ledger와의 연결

XRP Ledger와 상호작용하는 방법은 크게 두 가지가 있습니다:

1. **직접 rippled 서버 운영**

   자신의 노드를 운영하여 블록체인 네트워크에 직접 참여할 수 있습니다. 하지만 이 방법은 많은 리소스를 필요로 하고, 기술적인 어려움이 따릅니다. 상용 환경에서는 직접 rippled 서버를 운영하는 것이 권장됩니다.

2. **퍼블릭 rippled 서버 이용**

   테스트 단계나 리소스가 제한적인 경우, 퍼블릭 rippled 서버를 이용하는 것이 편리합니다. 이 방법은 빠른 개발과 테스트를 가능하게 하지만, 실제 상용 환경에서는 보안 및 안정성 문제로 인해 사용을 권장하지 않습니다.

이 가이드에서는 퍼블릭 rippled 서버를 이용하는 것을 추천합니다.

### 직접 rippled 서버 운영

1. **rippled 서버 설치**

   XRPL을 직접 호스팅하기 위해선, 먼저 rippled 서버를 설치해야 합니다. 서버 설치에 관한 자세한 가이드는 [여기](https://xrpl.org/install-rippled.html)에서 찾아볼 수 있습니다. rippled 서버는 리눅스 기반 시스템에서 가장 잘 동작하며, 서버의 성능과 안정성을 위해 충분한 하드웨어 사양이 필요합니다.

2. **서버 구성**

   rippled 서버가 설치된 후, rippled 서버를 설정하여 네트워크와 연결하고 필요한 옵션을 구성해야 합니다. 설정에 관한 자세한 내용은 [여기](https://xrpl.org/configure-rippled.html)에서 확인할 수 있습니다.

3. **Python 애플리케이션과의 연결**

   xrpl-py에서 제공하는 `JsonRpcClient` 클래스를 사용하여 rippled 서버와 연결할 수 있습니다. 이를 위해서는 rippled 서버의 IP 주소와 포트 번호가 필요합니다. 다음은 연결 예제입니다.

   ```python
   from xrpl.clients import JsonRpcClient
   JSON_RPC_URL = "http://<your-rippled-server>:5005/"
   client = JsonRpcClient(JSON_RPC_URL)
   ```

   이제 `client` 객체를 이용하여 XRP Ledger와 상호작용할 수 있습니다.

### 퍼블릭 rippled 서버 사용하기

1. **퍼블릭 rippled 서버 선택**

   XRPL에 연결하면서 자원을 절약하려면 퍼블릭 rippled 서버를 사용하는 것이 좋습니다. Ripple에서는 `https://s.altnet.rippletest.net:51234` 등의 테스트 네트워크를 제공하며, 다른 퍼블릭 rippled 서버를 찾아볼 수 있는 [리스트](https://xrpl.org/public-servers.html)도 제공합니다.

   **테스트 네트워크(testnet)이란**: 실제 네트워크(mainnet)와 동일한 기능을 가진 실험 환경입니다. 테스트넷에서 사용되는 암호화폐는 실제 가치가 없는 토큰으로, 실험을 할 때 자산 손실의 위험 없이 다양한 테스트를 수행할 수 있습니다.

2. **Python 애플리케이션과의 연결**

   직접 rippled 서버를 운영하는 것과 동일한 방식으로, xrpl-py의 Client 클래스를 사용해 퍼블릭 rippled 서버에 연결할 수 있습니다. 아래는 그 예시입니다.

   ```python
   from xrpl.clients import JsonRpcClient
   JSON_RPC_URL = "http://s.altnet.rippletest.net:51234/"
   client = JsonRpcClient(JSON_RPC_URL)
   ```

   이제 `client` 객체를 사용해 XRP Ledger와 상호작용할 수 있습니다.

이제 xrpl-py를 사용해 XRP Ledger와 상호작용하는 애플리케이션 개발 준비가 모두 완료되었습니다. 각 연결 방식에는 특별한 장단점이 있으니, 사용자의 요구사항과 사용 가능한 리소스에 따라 적합한 방법을 선택하세요.

## 클라이언트 연결 확인하기

Python 애플리케이션에서 xrpl-py의 Client 클래스를 사용하여 rippled 서버와 연결한 후에는, 연결이 제대로 이루어졌는지 확인하는 테스트를 수행할 수 있습니다. XRP Ledger의 서버 정보를 요청하여 이를 확인하는 방법을 아래에 안내하겠습니다.

1. **서버 정보 요청 코드 작성**

   XRP Ledger에는 서버 상태 정보를 요청하는 `ServerInfo` 요청이 있습니다. 이를 사용해 클라이언트가 서버와 제대로 연결되었는지 확인해 보겠습니다. 아래 코드는 서버 정보를 출력하는 방법입니다.

   ```python
   from xrpl.clients import JsonRpcClient
   from xrpl.models.requests import ServerInfo

   JSON_RPC_URL = "http://s.altnet.rippletest.net:51234/"
   client = JsonRpcClient(JSON_RPC_URL)

   response = client.request(ServerInfo())
   ```

   위 코드에서 `JSON_RPC_URL`부분은 사용하려는 서버의 URL로 수정해야 합니다. 위 예시에서는 퍼블릭 테스트넷을 사용했습니다.

2. **테스트 실행 및 결과 확인**

   위 Python 코드를 실행하면, 서버 정보가 출력됩니다. 만약 서버와의 연결에 문제가 있다면, 클라이언트는 오류 메시지를 반환할 것입니다.

   `server_info` 메서드로 반환된 정보에는 서버 로드, 피어 수, 서버 상태 등의 다양한 데이터가 포함됩니다. 이를 통해 서버가 정상적으로 작동하고 있는지 확인할 수 있습니다.

   ```python
   print(response.result)
   ```

   ```python
   {'info': {'build_version': '1.11.0-rc3',
             'complete_ledgers': '39324437-39635691',
             'hostid': 'POW',
             'initial_sync_duration_us': '208323551',
             'io_latency_ms': 1,
             'jq_trans_overflow': '0',
             'last_close': {'converge_time_s': 2, 'proposers': 6},
             'load_factor': 1,
             'network_id': 1,
             'peer_disconnects': '44979',
             'peer_disconnects_resources': '755',
             'peers': 78,
             'pubkey_node': 'n9MwV33AoZvuVUketM4JB7qAAJre5SpgMjZxsQ7gpE1JMpU4jzxv',
             'server_state': 'full',
             'server_state_duration_us': '3134061552461',
             'state_accounting': {'connected': {'duration_us': '203217293',
                                                'transitions': '2'},
                                  'disconnected': {'duration_us': '1098223',
                                                   'transitions': '2'},
                                  'full': {'duration_us': '3134061552461',
                                           'transitions': '1'},
                                  'syncing': {'duration_us': '4007993',
                                              'transitions': '1'},
                                  'tracking': {'duration_us': '40',
                                               'transitions': '1'}},
             'time': '2023-Jul-20 04:52:11.539658 UTC',
             'uptime': 3134269,
             'validated_ledger': {'age': 3,
                                  'base_fee_xrp': 1e-05,
                                  'hash': '3DC0B6E22052FF2DEF38ED25EAE363CB1C27FC4221CD13A32FBCB565E43A7BB7',
                                  'reserve_base_xrp': 10,
                                  'reserve_inc_xrp': 2,
                                  'seq': 39635691},
             'validation_quorum': 5}}
   ```
