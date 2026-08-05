# C# Windows Forms Skeleton Source

`MinimalApp/`은 알려진 정상 출발점입니다. 관련된 최소 Pattern을 복사하십시오; Project, 구성, Manifest 내용을 기억으로 지어내지 마십시오 — 이 File들은 Schema에 민감하고 Compiler가 잡아내지 못하는 방식으로 틀리기 쉽습니다.

| File | 이 File이 고정하는 것 |
|---|---|
| `MinimalApp.csproj` | `net472`을 Target하는 SDK-style Project, `OutputType` `WinExe`, Windows Forms 직접 참조 |
| `App.config` | 4.7.2용 `supportedRuntime`과 `DpiAwareness=PerMonitorV2` Section |
| `app.manifest` | Windows 10 `supportedOS` 선언, 이것 없이는 DPI Key가 아무 효과가 없다 |
| `Program.cs` | 첫 호출인 `EnableVisualStyles`, `[STAThread]`, Entry Point에서 주입되는 Service |
| `MainForm.cs` | UI-thread Marshalling Pattern을 포함한 Behaviour만 |
| `MainForm.Designer.cs` | Designer가 생산하는 형태의 Layout만 |
| `Services/` | Form이 자기 자신 밖에 닿는 유일한 경계 |
| `screen-spec.json` | Designer-tree 검사가 비교 대상으로 삼는 선언 |

## 규칙

- Project에 복사할 때 Source와 Version을 기록합니다.
- 여기 있는 원본은 보존하고, 복사본을 수정합니다.
- Detection된 Target이 다른 Project에 `net472`을 복사하지 않습니다. 먼저 Target을 확인합니다.
- 다른 곳에서 발견한 낡은 자료의 Manifest DPI 접근을 복사하지 않습니다 — 이 Skeleton은 의도적으로 `App.config`에서 DPI를 구성합니다.
- 기밀 Skeleton은 공개 Repository에서 제외합니다. 여기 있는 것은 모두 합성 데이터입니다.

## Skeleton 자체 검증

```bash
python ../tools/extract_designer_tree.py --designer MinimalApp/MainForm.Designer.cs --output /tmp/tree.json
python ../tools/check_designer_spec.py --tree /tmp/tree.json --spec MinimalApp/screen-spec.json
```

Kit 자신의 Skeleton은 Kit 자신의 검사를 통과해야 합니다. 통과하지 못하면 Skeleton이 결함입니다.
