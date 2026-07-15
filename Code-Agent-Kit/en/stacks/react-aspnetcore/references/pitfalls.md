# React and ASP.NET Core Verified Pitfalls

| Incorrect Assumption | Verified Rule | Evidence | Failure Stage |
|---|---|---|---|
| Frontend and backend can change contracts independently | update both contracts and tests together | sample API and tests | runtime |
| Adding a second HTTP client is harmless | reuse detected project API entry point | `frontend/src/api.ts` | architecture |
| Build PASS proves UI fidelity | run screen, color, and E2E gates separately | workflow tools | rendered/runtime |
| Sample in-memory repository implies production data policy | owner confirmation is required before database adoption | capability rules | architecture |
