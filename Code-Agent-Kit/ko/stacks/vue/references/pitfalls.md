# Pitfall — Vue.js

모두 기술 자체의 성질이며 Project와 무관하게 확인할 수 있습니다. 한데 모은 이유는 한 가지 특징
때문입니다. **실패가 조용하거나, Error Message가 원인이 아닌 다른 것을 가리킵니다.** 실패가 스스로
드러나는 Stack에는 이런 목록이 필요 없습니다.

## Destructuring은 Reactivity를 잃습니다

`const { count } = reactive(state)`는 갱신되지 않는 평범한 값을 내놓습니다. `toRefs`를 쓰거나 객체를 그대로 유지합니다. Error는 없습니다 — UI가 그냥 바뀌지 않습니다.

## `ref` 대 `reactive`

`ref`는 Script에서 `.value`가 필요하고 Template에서는 필요 없습니다. `reactive`는 둘 다 필요 없지만 재할당할 수 없습니다. 둘을 섞는 것이 한 번 Render된 뒤 갱신되지 않는 값의 가장 흔한 원인입니다.

## 안정적 Key 없는 `v-for`

Index Key는 순서 변경 후 Component State가 다른 항목에 재사용되게 만듭니다. 증상은 Error가 아니라 엉뚱한 행에 나타나는 State입니다.

## Watcher Flush 시점

`watch`는 기본적으로 Render 전에 실행되므로 그 안에서 DOM을 읽으면 이전 Frame이 보입니다. `flush: 'post'` 또는 `nextTick`이 필요합니다.

## Vue 2의 배열 및 Property 제약

Vue 2에서는 Index 대입과 새 Property 추가가 Reactive하지 않습니다. Vue 3에서는 Reactive합니다. Version을 건너뛴 답은 둘 중 하나에서 틀립니다.
