# Hooks Advanced

이번 장에서는 Hooks에 대해 더 자세히 알아보겠습니다.

## 1. Hook 생애 주기 (Life Cycle)

설명 추가

### 1.1. 생성 (Creation)

Hook을 생성하고, 계정에 연결하기 위해서는 다음의 세 단계를 거쳐야 합니다. 먼저, Hook 코드를 작성하고 WASM 바이트코드로 컴파일합니다. 그 다음, SetHook 트랜잭션에 원하는 Hook parameter를 입력하여 해당 Hook을 계정에 연결할 수 있습니다. 자세한 절차는 다음과 같습니다.

#### 1.1.1 Hook 컴파일

1. **컴파일 절차**

   - Hook는 컴파일 시 `.wasm` 이진 파일로 저장됩니다.
   - Hook를 컴파일하기 위해 `wasmcc`를 사용할 수 있고, `wasm2wat` 도구를 사용하여 이진 형식을 사람이 읽을 수 있는 웹어셈블리 형식으로 변환할 수 있습니다.

2. **컴파일 중 중요한 사항**

   - Hook는 Hooks API에서만 함수를 가져와야 합니다. 그리고 반드시 `cbak` 및 `hook` 함수만 내보내야 합니다.
   - 대부분의 웹어셈블리 컴파일러는 링킹을 위해 추가 export를 생성합니다. 이런 불필요한 export가 있으면 유효한 Hook도 거부될 위험이 있습니다.
   - Hook를 컴파일 한 후 **Hook Cleaner Utility**를 사용하여 불필요한 export를 제거해야 합니다.

#### 1.1.2 Hook 매개변수 (Parameters)

1. **Hook 매개변수 정의**

   - Hook 개발자는 Hook에 설치 시간 매개변수(Hook 매개변수라고 함)를 사용할 수 있습니다.
   - 이러한 매개변수는 키-값 쌍으로 설정되며, 실행 시간 동안 Hook에 의해 검색될 수 있습니다.
   - `ParameterName`(키) 및 `ParameterValue`는 각각 최대 32 바이트와 128 바이트의 길이로 설정됩니다.

2. **매개변수 설정**

   - `SetHook` 트랜잭션은 설치된 Hook 당 최대 16개의 Hook 매개변수를 정의할 수 있습니다.
   - Hook 매개변수 배열은 아래에 표시된 대로 각 Hook의 Hook 배열 내에서 선택적으로 정의됩니다.

3. **기본 매개변수**

   - Hook를 처음 설정하는 사용자는 Hook 매개변수를 정의하여 해당 Hook의 기본 매개변수가 될 수 있습니다.
   - 이후 동일한 `HookDefinition`을 참조하는 모든 사용자는 기본적으로 원래 설정된 Hook 매개변수를 받게 됩니다.
   - 후속 사용자는 설치에 대한 기본 매개변수를 재정의하는 자체 매개변수를 지정할 수 있습니다.

4. **Hook 내에서의 매개변수 사용**

   - 매개변수는 해당 Hook에 설정된 후 `hook_param`을 사용하여 읽을 수 있습니다.
   - `Hook Chain`에 여러 Hook가 설치되어 있으면 `hook_param_set`을 사용하여 동일한 계정의 체인에서 더 아래에 있는 Hook의 Hook 매개변수를 수정할 수 있습니다.

#### 1.1.3 SetHook 트랜잭션

SetHook 트랜잭션은 XRPL 계정에 Hook를 설정하거나 수정하는 데 사용됩니다. 이 트랜잭션을 사용하여 개발자는 원하는 계정에 웹어셈블리 바이트코드 형식의 Hook를 연결할 수 있습니다. 이 트랜잭션은 간단해 보이지만 복잡한 기능을 갖고 있습니다.

```JavaScript
{
    Account: "r4GDFMLGJUKMjNhhycgt2d5LXCdXzCYPoc",
    TransactionType: "SetHook",
    Fee: "2000000",
    Hooks:
    [
        {
            Hook: {
                CreateCode: fs.readFileSync('accept.wasm').toString('hex').toUpperCase(),
                HookOn: '0000000000000000',
                HookNamespace: addr.codec.sha256('accept').toString('hex').toUpperCase(),
                HookApiVersion: 0
            }
        }
    ]
}
```

1. **트랜잭션 구조**

   SetHook 트랜잭션의 주요 내용은 `Hooks` 배열입니다. 이 배열은 계정에 설치된 Hook Chain을 반영합니다. 배열의 위치 0은 Hook Chain의 위치 0에 해당하고, 위치 3은 위치 3에 해당합니다.

2. **HookSet 객체와 대응하는 Hook**

   Hooks 배열의 각 항목은 HookSet 객체로, 계정의 Hook Chain에 있는 해당 Hook을 대응하는 Hook이라고 합니다.

3. **HookDefinition**

   각 대응하는 Hook은 HookDefinition 객체에 대한 참조를 포함합니다. 이 객체는 웹어셈블리 바이트코드의 중복 제거를 위한 참조 카운트 된 레저 객체입니다. 같은 Hook를 사용하는 두 사용자는 동일한 HookDefinition을 가리킵니다.

4. **Hook 기본값**

   HookDefinition이 생성될 때 사용자가 제공한 초기 파라미터, 네임스페이스, 권한이 포함됩니다. 이 값들은 Hook 기본값이 됩니다. 어떤 Hook이 이 Hook Definition을 참조하면 기본값을 사용하게 됩니다. 그러나 SetHook 트랜잭션에서 이 참조를 생성하는 경우나 후속 업데이트 작업에서 명시적으로 기본값을 재정의할 수 있습니다.

5. **HookSet 작업**

   총 여섯 가지 작업이 가능합니다: No Operation, Create, Update, Delete, Install 및 Namespace Delete. 각 작업은 HookSet 객체의 필드의 포함 또는 생략에 따라 지정됩니다. 이것은 처음에는 혼란스러울 수 있지만, 몇 가지 예를 통해 직관적으로 이해할 수 있습니다.

트랜잭션의 작성, 제출, 처리 방법에 대한 구체적인 지침은 XRPL 문서에서 찾을 수 있습니다.

### 1.2. 실행 (Execution)

#### 1.2.1 HookOn 필드

**개요**

`HookOn` 필드는 특정 트랜잭션 유형에 대한 후크의 실행 여부를 지정하는데 사용됩니다.

**핵심 내용**

- **HookOn 필드 구조**

  - `HookOn`은 256비트 무부호 정수로 구성됩니다.
  - 각 비트는 특정 트랜잭션 유형에서 후크가 실행될지 여부를 나타냅니다. 대부분의 비트는 active low 상태이지만 22번째 비트만 active high 상태입니다.
  - `ttHOOK_SET`는 22번째 비트에 대응하며, 기본값이 0일 때는 SetHook 트랜잭션에 반응하지 않습니다.

- **비트 넘버링 방식**

  - 최하위 비트: 비트 0 (가장 오른쪽)
  - 최상위 비트: 비트 63 (가장 왼쪽)

- **예제 코드**

  - 후크를 완전히 비활성화:

  ```c
  ~(1ULL << 22) /* 모든 비트는 1, 22번째 비트만 0 */
  ```

  - `ttPAYMENT`만 활성화하고 나머지는 비활성화:

  ```c
  ~(1ULL << 22) & ~(1ULL)
  ```

  - `ttHOOK_SET` 제외 모든 것에서 활성화:

  ```c
  0
  ```

  - `ttHOOK_SET` 및 다른 모든 트랜잭션 유형에서 활성화:

  ```c
  (1ULL << 22)
  ```

**추가 리소스**

- 후크의 실행 여부를 쉽게 계산하려면 [HookOn Calculator](https://xrpl-hooks.readme.io/docs/hookon-field#hookon-calculator)를 참조하세요.

#### 1.2.2 Chaining
