# Stack Input Requirements

A generic workflow cannot safely invent stack-specific facts. Every stack profile combines automatic detection with information supplied or confirmed by the user or project owner.

## Readiness states

| State | Meaning |
|---|---|
| ready | All required inputs are detected, confirmed, or explicitly not applicable |
| provisional | Work that does not depend on unresolved inputs may continue |
| blocked | A required unknown affects the requested implementation |

Unknown required information is written as:

```text
⟨verification required: input, owner, and verification method⟩
```

## What tools can usually detect

- package and project manifests;
- runtime or SDK version files;
- imported packages and namespaces;
- existence of shared clients, generated code, configuration, and skeletons;
- build and test commands already stored in the repository;
- framework file extensions and project layout;
- existing authentication, data-access, or UI-library references.

Detection is evidence, but a path name alone does not prove the intended organizational policy.

## What the user or project owner usually must supply or confirm

| Input | Why it is needed |
|---|---|
| Supported runtime and SDK versions | Prevent copying an example version or using an unavailable API |
| Authoritative documentation and installed artifacts | Ground facts that the model cannot infer |
| Golden skeleton or known-good framework files | Prevent invented schema, metadata, or project structure |
| Feature boundary and action model | Define what one feature means for this stack |
| Internal naming and file conventions | Prevent inconsistent artifacts |
| Communication and data contract | Define entry points, DTO/data mappings, error shapes, and generated-client ownership |
| Capability branch rules | Define what to do when shared libraries, clients, auth, ORM, or design systems are present or absent |
| Validation commands and failure signals | Convert completion into deterministic gates |
| Known pitfalls and corrected assumptions | Prevent repeated hallucinations |
| Confidentiality classification | Prevent private references and assets from entering a public repository |
| Reference UI assets and binding expectations | Validate structure, content, colors, and real-data replacement |

## Minimum stack pack

```text
stacks/<stack>/
├─ STACK.md
├─ STACK-INPUTS.md
├─ STACK-READINESS.json
├─ AGENTS.stack.md
├─ SKILL.md
├─ capability-detection.md
├─ feature-model.md
├─ artifact-contract.md
├─ communication-contract.md
├─ evidence-provenance.md
├─ references/
│  ├─ _index.md
│  ├─ pitfalls.md
│  └─ verified-facts.md
├─ skeletons/
│  └─ README.md
└─ validation/
   └─ validation-profile.md
```

## Three-layer enforcement

A capability that changes code generation appears in:

1. Project Map capability table;
2. Gate Analysis `Environment Capability Decision`;
3. stack rule that prohibits the dependent pattern until confirmed.

## Onboarding sequence

1. Copy `templates/stack-profile/`.
2. Fill `STACK-INPUTS.md`.
3. Add authoritative sources and skeletons.
4. Complete `STACK-READINESS.json`.
5. Run:

```bash
python tools/check-stack-readiness/check_stack_readiness.py \
  --stack stacks/<stack>
```

6. Resolve every blocking unknown.
7. Add the selected capabilities to Project Map.
8. Only then begin stack-dependent implementation.

The validator does not prove the framework facts are correct. It proves the required evidence and decisions have not been silently omitted.
