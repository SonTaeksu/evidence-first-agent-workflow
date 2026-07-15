# Capability Detection

| Capability | Detection | Present Path | Absent Path | Unknown Rule |
|---|---|---|---|---|
| shared-api-client | file/import/config evidence | reuse existing | use approved stack adapter | block implementation |
| generated-client | generated folder/build metadata | use generated client | use approved manual contract | block contract invention |
| authentication-provider | configuration and middleware evidence | integrate existing provider | approved default | block security changes |
| runtime-sdk-version | manifest/tool output | use detected version | use confirmed supported version | block version-sensitive API |

Every capability used by a feature must be recorded in Project Map and repeated in Gate Analysis.
