---
sidebar_position: 3
author: wonj1012
---

# Hooks 고급

이번 장에서는 Hooks에 대해 더 자세히 알아보겠습니다.

## 1. Hook 생애 주기 (Life Cycle)

설명 추가

### 1.1. 생성 (Creation)

Hook을 생성하고, 계정에 연결하기 위해서는 다음의 세 단계를 거쳐야 합니다. 먼저, Hook 코드를 작성하고 WASM 바이트코드로 컴파일합니다. 그 다음, SetHook 트랜잭션에 원하는 Hook parameter를 입력하여 해당 Hook을 계정에 연결할 수 있습니다. 자세한 절차는 다음과 같습니다.

#### 1.1.1. Hook 컴파일

1. **컴파일 절차**

   - Hook는 컴파일 시 `.wasm` 이진 파일로 저장됩니다.
   - Hook를 컴파일하기 위해 `wasmcc`를 사용할 수 있고, `wasm2wat` 도구를 사용하여 이진 형식을 사람이 읽을 수 있는 웹어셈블리 형식으로 변환할 수 있습니다.

2. **컴파일 중 중요한 사항**

   - Hook는 Hooks API에서만 함수를 가져와야 합니다. 그리고 반드시 `cbak` 및 `hook` 함수만 내보내야 합니다.
   - 대부분의 웹어셈블리 컴파일러는 링킹을 위해 추가 export를 생성합니다. 이런 불필요한 export가 있으면 유효한 Hook도 거부될 위험이 있습니다.
   - Hook를 컴파일 한 후 **Hook Cleaner Utility**를 사용하여 불필요한 export를 제거해야 합니다.

#### 1.1.2. Hook 매개변수 (Parameters)

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

#### 1.1.3. SetHook 트랜잭션

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

   각 대응하는 Hook은 `HookDefinition` 객체에 대한 참조를 포함합니다. 웹어셈블리 바이트코드는 네트워크에 부하를 주므로, 중복 제거를 위해 같은 Hook은 하나의 HookDefinition 객체를 참조합니다. `Reference Counting`은 해당 객체를 참조하는 계정의 수를 나타냅니다.

4. **Hook 기본값**

   HookDefinition이 생성될 때 사용자가 제공한 초기 파라미터, 네임스페이스, 권한이 포함됩니다. 이 값들은 Hook 기본값이 됩니다. 어떤 Hook이 이 Hook Definition을 참조하면 기본값을 사용하게 됩니다. 그러나 SetHook 트랜잭션에서 이 참조를 생성하는 경우나 후속 업데이트 작업에서 명시적으로 기본값을 재정의할 수 있습니다.

5. **HookSet 작업**

   총 여섯 가지 작업이 가능합니다: No Operation, Create, Update, Delete, Install 및 Namespace Delete. 각 작업은 HookSet 객체의 필드의 포함 또는 생략에 따라 지정됩니다. 이것은 처음에는 혼란스러울 수 있지만, 몇 가지 예를 통해 직관적으로 이해할 수 있습니다.

트랜잭션의 작성, 제출, 처리 방법에 대한 구체적인 지침은 XRPL 문서에서 찾을 수 있습니다.

### 1.2. 실행 (Execution)

#### 1.2.1. HookOn 필드

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

#### 1.2.2. Chaining

XRPL의 Hook은 "하나의 작업만 수행하고 그 작업을 정말 잘 해야 한다"는 원칙에 따라 설계되었습니다. 복잡한 로직을 수행해야 하는 경우, 'Hook Chaining' 기능을 통해 한 계정에 여러 Hook을 순차적으로 연결하고, 각각의 Hook이 하나의 작업을 전문적으로 처리할 수 있습니다.

**체인 구성 및 실행**

- **Hook Chain**: XRPL 계정에 설치할 수 있는 Hook의 시퀀스로, 최대 10개까지 설치 가능합니다.
- **실행 순서**: 체인의 실행은 chain position 0에서 시작하여 chain position 9에서 끝납니다. 빈 위치는 성공으로 간주되고 건너뜁니다.
- **트랜잭션 성공 조건**: 송신측과 수신측의 Hook Chain이 모두 성공적으로 실행되어야 트랜잭션이 성공합니다.

**런타임에서의 조작**

- **HookHash 확인**: `hook_hash`를 호출하여 자신의 HookHash를 알아낼 수 있습니다.
- **체인 위치 확인**: `hook_pos`를 사용하여 자신이 체인의 어떤 위치에 있는지 확인할 수 있습니다.
- **다른 Hook 제어**:
  - `hook_skip`를 사용하여 체인 내의 다른 Hook을 건너뛸 수 있습니다.
  - `hook_param_set`을 사용하여 체인 내의 다른 Hook의 매개변수를 변경할 수 있습니다.

**약한 실행 (Weak Executions)**

- **hook_again 호출**: Hook이 두 번째 '약한 실행'을 요구할 수 있습니다.
- **Weak Execution 순서**: 원래 트랜잭션이 성공적으로 적용된 후에만 약한 실행이 이루어집니다. 이러한 실행은 특정 순서(예: Account ID나 Hook 위치 등)에 따라 수행됩니다.

### 1.3. 종료 (Termination)

#### 1.3.1. Accept & Rollback

Accept와 Rollback은 hookapi의 함수들입니다. 이 두 함수를 통해, Hook은 자신이 수행한 작업을 XRPL에 안전하게 반영하거나 취소할 수 있습니다.

**Accept**

- **용도**: Hook의 실행을 '성공' 상태로 종료하고, 그 동안 Hook이 수행한 모든 상태 변화를 확정합니다.
- **동작**:
  - 상태 변화를 커밋(Commit)
  - `emit()` 트랜잭션 제출
  - 원래의 트랜잭션을 계속 진행
- **주의사항**: 만약 원래 트랜잭션이 다른 이유로 중단된다면, 'Accept'는 'Rollback'이 됩니다.

**Rollback**

- **용도**: Hook의 실행을 '실패' 상태로 종료하고, 그 동안 Hook이 수행한 모든 상태 변화를 폐기합니다.
- **동작**:
  - 모든 상태 변화 폐기
  - `emit()` 트랜잭션 폐기
  - 원래의 트랜잭션을 중지
- **주의사항**: 원래 트랜잭션은 `tecHOOK_REJECTED` 상태와 함께 실패하며, 수수료가 부과됩니다.

#### 1.3.2. HookDefinition 삭제

Hook을 설치한 계정이 없어져서 해당 HookDefinition 객체의 Reference Counting 값이 0이 되면, 해당 HookDefinition 객체는 삭제됩니다.

## 2. Advanced Hook Features

### 2.1. Ledger 데이터와의 상호작용

#### 2.1.1. Slots와 Keylets

#### 2.1.2. State Management

#### 2.1.3. Namespace

### 2.2 Emitting Transactions

### 2.3 Data representation in Hooks

- **Serialized Objects**
- **Floating Point Numbers (XFL)**

### 2.4 Hook Fees

- **Weak and Strong**
- **Hook Fees**
- **Collect Call**

## 3. Writing Your First Hook

## 4. Best Practices and Common Patterns

- Error Handling
- Efficient State Management
- Secure Coding Practices

## 5. Debugging and Testing Hooks

- **Execution Metadata**
- **Debugging Hooks**

## 6. Deployment and Production Considerations

## 7. Community and Further Resources

- Forums and Workshops: 커뮤니티 포럼 및 워크샵
- Sample Projects: 참조할 수 있는 샘플 프로젝트

## 8. Future Developments and Roadmap

- Upcoming Features: 향후 예정된 기능
- Research and Development: 연구 및 개발 방향

## 9. Conclusion
