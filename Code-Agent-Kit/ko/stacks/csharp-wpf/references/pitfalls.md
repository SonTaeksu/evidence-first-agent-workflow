# Pitfall — WPF (.NET Framework 4.7.2+)

여기 있는 것들은 모두 기술 자체의 속성이고 어떤 Project와도 무관하게 확인할 수
있습니다. 한 가지 공통점 때문에 모아 두었습니다. **실패가 조용하거나, 오류
Message가 원인이 아닌 다른 것을 가리킨다는 점입니다.** 실패가 스스로를 알리는
Stack이라면 이런 목록이 필요 없습니다.

## Binding 실패는 조용하다

`Path`의 철자가 틀려도 Exception도 Compiler 오류도 나지 않습니다. Control이 빈 채로 Rendering될 뿐입니다. `PresentationTraceSources.DataBindingSource`를 Warning으로 올리거나, Test에서 Binding된 값을 Assert하십시오. 오류가 없다는 것만으로 'Binding이 동작한다'고 결론짓지 마십시오.

## DataContext는 지정되는 것이 아니라 상속된다

`DataContext`를 명시하지 않은 Control은 부모의 것을 상속합니다. Visual Tree에서 Element를 옮기면 무엇에 Binding되는지가 조용히 달라집니다.

## UI Thread 밖에서의 Collection 갱신

`ObservableCollection`은 호출한 Thread에서 변경 알림을 냅니다. 그런데 WPF는 UI Thread를 요구합니다. `Dispatcher`를 통해 Marshal하십시오.

## Resource 조회 순서

Key는 해당 Element에서 바깥으로, 그다음 Application, 그다음 Theme 순으로 해석됩니다. 서로 다른 수준에 같은 Key를 가진 Resource가 둘 있으면 Element가 어디에 놓였는지에 따라 다르게 해석됩니다.

## Framework Version별 동작

4.7.2, 4.8, 4.8.1은 DPI 처리와 일부 기본 Style이 다릅니다. 기억하지 말고 Version을 조회하십시오. 권위는 Project File의 Target Framework에 있습니다.
