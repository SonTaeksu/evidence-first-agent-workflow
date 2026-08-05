# C# Windows Forms Communication 및 Data Contract

- **단일 진입점**: Form은 자기 자신 밖에 있는 모든 것에 주입된 Service Interface 하나를 통해서만 접근합니다. Reference Skeleton에서는 `IGreetingService`입니다. Form은 직접 Connection을 열거나, HTTP Client를 호출하거나, File을 읽지 않습니다.
- **Request Mapping**: Form은 Primitive나 자신이 소유한 Request Type을 전달합니다. Control 인스턴스나 Event Argument를 경계 너머로 전달하지 않습니다.
- **Response Mapping**: Service는 Data를 반환하며, Control이나 `Form`을 반환하지 않습니다. 표시를 위한 Formatting은 Form에서 이루어집니다.
- **Error Contract**: Service는 Typed Exception을 발생시키거나 결과 값을 반환합니다. 사용자가 무엇을 보는지는 Form이 결정합니다. UI를 그대로 둔 채 삼켜진 Exception은 결함입니다.
- **Authentication 전파**: `authentication-provider` Capability로 결정됩니다. `unknown`인 동안에는 Credential 처리를 추가하지 않습니다.
- **Generated-client Ownership**: Service Reference나 Generated Proxy가 있으면, 재생성 명령을 기록하고 Generated File을 수기 편집하지 않습니다.

## UI Thread 경계

이 Contract는 가장 자주 깨지므로, Guideline이 아니라 규칙으로 명시합니다.

```text
service or background work   ConfigureAwait(false)
→ no control access
→ marshal through Control.Invoke / BeginInvoke
→ form code                  ConfigureAwait(true)
→ control access
```

- Control은 자신을 만든 Thread에 묶여 있습니다. 다른 Thread에서 안전하게 호출할 수 있는 것은 `Invoke`, `BeginInvoke`, `EndInvoke`, `CreateGraphics`뿐이며, `CreateGraphics`는 Handle이 존재한 이후에만 안전합니다.
- 다른 Thread에서 Control을 건드리면 *Cross-thread operation not valid* 메시지와 함께 `InvalidOperationException`이 발생합니다. Debugger 아래서는 항상 발생하고 Production에서도 발생할 수 있으므로, Test되지 않은 경로는 안전한 경로가 아닙니다.
- `InvokeRequired`는 Marshal이 필요 없을 때와 Control의 Handle이 아직 존재하지 않을 때 모두 `false`를 반환합니다. Background Thread에서는 `IsHandleCreated`도 확인해야 합니다. 그렇지 않으면 Message Pump가 없는 Thread에서 Handle이 생성되어 Application이 불안정해집니다.
- `CheckForIllegalCrossThreadCalls`로 검사를 끄지 않습니다. 그것은 결함을 고치는 게 아니라 숨기는 것입니다.

## Contract 변경

Service Interface 변경은 같은 변경 안에서 Interface, 구현, Form 호출 지점, Unit Test, Feature `current.md`를 함께 갱신합니다. 한쪽만 바뀐 Contract는 부분 성공이 아니라 불완전한 변경입니다.
