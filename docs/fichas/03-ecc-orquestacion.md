# Ficha 03 — ECC v2.2.3: orquestación, planificación y loops

Rutas relativas a `/home/claude/repos/ECC/src`. Todos los archivos pedidos existen (ninguno "No encontrado"). Nota: el repo se encontró en esa ruta; el directorio de trabajo por defecto era otro.

## 1. Propósito y alcance declarado
- Es software casi por completo: planes con archivos y tests, TDD, PRs, commits convencionales (`skills/orch-pipeline/SKILL.md:73`, `commands/prp-implement.md:20-30`).
- Excepciones generales: `council` (decisiones, `skills/council/SKILL.md:16`), `santa-method` (también contenido y compliance, `skills/santa-method/SKILL.md:16-22`), `loop-design-check` (agnóstico), `operator-approval-loop` (mensajes a contrapartes, `skills/operator-approval-loop/SKILL.md:13-17`) y `chief-of-staff` (triage de email/Slack, `agents/chief-of-staff.md:17`).
- Principio común declarado: el handoff es un archivo, no la conversación (`docs/PLAN-PRD-PATTERN.md:5`; `skills/orch-pipeline/SKILL.md:108`).

## 2. Flujos paso a paso

| Familia | Fases (entrada → salida) |
|---|---|
| **plan / plan-prd** | 1 FRAME, 2 GROUND, 3 DECIDE, 4 GENERATE (`commands/plan-prd.md:29-67`) → `.claude/prds/X.prd.md`. Luego `/plan` (restate, riesgos, fases, CONFIRM; `commands/plan.md:14-17`) → `.claude/plans/X.plan.md` o plan inline. Luego `tdd-workflow` → `/pr` (`docs/PLAN-PRD-PATTERN.md:27-50`). |
| **PRP (legado)** | `prp-prd`: 8 fases con 4 gates (`commands/prp-prd.md:37-352`). `prp-plan`: DETECT, PARSE, EXPLORE, RESEARCH, DESIGN, ARCHITECT, GENERATE (`commands/prp-plan.md:18-206`). `prp-implement`: DETECT, LOAD, PREPARE, EXECUTE, VALIDATE (5 niveles), REPORT, OUTPUT (`commands/prp-implement.md:18-291`). |
| **feature-dev** | 7 fases: Discovery, Exploration (`code-explorer`), Preguntas, Arquitectura (`code-architect`), Implementación, Review (`code-reviewer`), Resumen (`commands/feature-dev.md:9-48`). |
| **multi-* (dual-model)** | `multi-plan`: contexto → análisis Codex ∥ Antigravity → cruce → plan (`commands/multi-plan.md:74-226`). `multi-execute`: leer plan → prototipo diff → Claude refactoriza → auditoría dual (`commands/multi-execute.md:115-272`). `multi-workflow`: Research, Ideation, Plan, Execute, Optimize, Review (`commands/multi-workflow.md:124-189`). |
| **orch-*** | Fases 0 Intake, 1 Research, 2 Plan (GATE 1), 3 Scaffold (solo MVP), 4 TDD, 5 Review, 6 Commit (GATE 2) (`skills/orch-pipeline/SKILL.md:60-74`). Cinco operaciones: add-feature, change-feature, fix-defect, refine-code, build-mvp (`:25-31`). `/orch-review` es el port nativo de la Fase 5 (`commands/orch-review.md:8-11`). |
| **GAN** | Setup, Planner (`spec.md` + `eval-rubric.md`), bucle Generator → Evaluator, resumen (`commands/gan-build.md:16-73`). `gan-design` omite planner (`commands/gan-design.md:12`). |
| **santa** | Rúbrica → 2 reviewers en paralelo → veredicto NICE/NAUGHTY → fix → repetir; push solo con NICE (`commands/santa-loop.md:31-172`). |
| **epic-*** | decompose / claim / validate / review sobre un issue de GitHub vía `scripts/github-coordination.js` (`commands/epic-decompose.md:9-18`; `commands/epic-review.md:9-18`). |
| **loops** | `loop-start` (sequential, continuous-pr, rfc-dag, infinite; `commands/loop-start.md:13`) con 5 pasos (`:18-24`); `loop-status`; `loop-operator`. Patrones en `skills/autonomous-loops/SKILL.md:30-37`. |

**Solapes** (el repo los admite): `plan-prd` vs `prp-prd` y `/plan` vs `/prp-plan` (`docs/PLAN-PRD-PATTERN.md:70,149-154`); `/plan` vs `/multi-plan` (`commands/plan.md:2`); `epic-*` declara alias `/plan`, `/prp-plan`, `/orch-add-feature`, `/prp-implement`, `/quality-gate`, `/code-review` (`commands/epic-decompose.md:20-23`, `commands/epic-claim.md:22-26`, `commands/epic-validate.md:20-22`, `commands/epic-review.md:20-23`); `autonomous-loops` está superseded por `continuous-agent-loop` (`skills/autonomous-loops/SKILL.md:10-13`); santa-loop, gan-evaluator, orch-review y council-multi-model hacen "segunda opinión" por vías distintas.

## 3. Puntos de validación humana

| Flujo | Se detiene en | La persona aprueba |
|---|---|---|
| `/plan` | Tras el plan (`commands/plan.md:112,179`) | Plan, con "yes/modify" o botón en plan-canvas (`:114-117`) |
| `plan-prd` | Cada fase es una puerta (`commands/plan-prd.md:27,46`) | Respuestas y "skip" explícito |
| `feature-dev` | Tras preguntas y tras arquitectura (`commands/feature-dev.md:25,31`) | Diseño |
| `orch-*` | GATE 1 tras Plan; GATE 2 antes de commit; entre gates fluye sin parar (`skills/orch-pipeline/SKILL.md:80-85`) | Task list; resumen de diff y mensajes |
| `multi-plan` | Termina la respuesta tras guardar el plan (`commands/multi-plan.md:226`) | Copia manual de `/ccg:execute` |
| `multi-workflow` | Confirmación tras cada fase; para si score < 7 (`commands/multi-workflow.md:106-107`) | Cada fase |
| `gan-build` | Solo muestra el spec; no pide aprobación (`commands/gan-build.md:26`) | Nada intermedio (inferencia: no hay gate) |
| `santa-loop` | Escalación tras 3 rondas, sin push (`commands/santa-loop.md:159-170`) | Revisión manual |
| `loop-design-check` | La celda "done" la voltea un humano (`skills/loop-design-check/SKILL.md:75,110`) | Aceptación final |
| `claude-devfleet` | Muestra el plan antes de despachar (`skills/claude-devfleet/SKILL.md:34,106`) | Plan |

## 4. Roles y agentes
- **Orquestador**: la sesión principal ("Orchestrator", `commands/multi-workflow.md:28`); en santa, la sesión corrige lo marcado (`commands/santa-loop.md:150-152`).
- **Planificador**: `planner` (solo Read/Grep/Glob, `agents/planner.md:4`), `architect`, `gan-planner` (escribe spec y rúbrica, `agents/gan-planner.md:104-108`).
- **Generador**: `gan-generator` lee spec y feedback (`agents/gan-generator.md:26-28`); "No auto-evalúa" (`:29`).
- **Evaluador**: `gan-evaluator` prueba la app viva y lee rúbrica, spec y estado del generador (`agents/gan-evaluator.md:44-49`); `agent-evaluator` puntúa 5 ejes sin rehacer la tarea (`agents/agent-evaluator.md:21,27`).
- **Revisores**: `code-reviewer`, `silent-failure-hunter`, `spec-miner` (extrae specs de código existente, `agents/spec-miner.md:27`).
- **Ocultamiento deliberado**: santa — reviewers sin ver al otro (`skills/santa-method/SKILL.md:79-82`) y frescos cada ronda (`:204`); council — voces externas reciben "solo la pregunta y el contexto relevante" (`skills/council/SKILL.md:53`); dev-team — resumen ≤150 palabras, no el archivo crudo (`skills/dev-team/SKILL.md:70-71`); council-multi-model — directorio temporal vacío, sin herramientas (`skills/council-multi-model/SKILL.md:105-109`); multi-*: modelos externos sin escritura (`commands/multi-plan.md:19`).

## 5. Artefactos y persistencia

| Flujo | Archivo | Formato |
|---|---|---|
| plan-prd / plan | `.claude/prds/*.prd.md`, `.claude/plans/*.plan.md` | Markdown con tabla de milestones (`commands/plan-prd.md:112-115`) |
| PRP | `.claude/PRPs/{prds,plans,reports,plans/completed}` | MD; plan archivado al terminar (`commands/prp-implement.md:283-284`) |
| multi-plan | `.claude/plan/<feature>.md` (+ `-v2`) con SESSION_IDs | MD (`commands/multi-plan.md:209,241`) |
| GAN | `gan-harness/{spec,eval-rubric,generator-state,build-report}.md`, `feedback/feedback-NNN.md` | MD (`commands/gan-build.md:96-100`) |
| loop-start | Runbook en `.claude/plans/` (`commands/loop-start.md:23`); snapshots `index.json` por sesión (`commands/loop-status.md:66-69`) | MD/JSON |
| tmux/worktrees | `.orchestration/<session>/{task,handoff,status}.md` (`skills/dmux-workflows/SKILL.md:170`) | MD |
| Kanban | Tarjeta JSON con owner, state, branch, merge_gate, handoff (`skills/team-agent-orchestration/SKILL.md:45-61`) | JSON |
| blueprint | `plans/<proyecto>.md` autocontenido (`skills/blueprint/SKILL.md:27`) | MD |
| spec-miner | `openspec/specs/<cap>/spec.md` con bloques Requirement/Invariant (`agents/spec-miner.md:99`) | MD + comentarios `<!-- key: value -->` |
| aprobación de envíos | Libro SQLite con hash y epoch (`skills/operator-approval-loop/SKILL.md:100-103`) | SQL |
| council, dev-team | No guardan nada por defecto (`skills/council/SKILL.md:157`; `skills/dev-team/SKILL.md:170`) | — |

## 6. Verificación y calidad

| Mecanismo | "Terminado" significa | Tope |
|---|---|---|
| `verification-loop` | 6 fases PASS/FAIL: build, tipos, lint, tests (80%), grep de seguridad, diff (`skills/verification-loop/SKILL.md:23-125`); "target acceptance" se reporta aparte (`:99-103`) | — |
| `quality-gate` | Solo formatter de un archivo; excluye lint y tipos (`commands/quality-gate.md:12-26`) | — |
| `santa-loop` | Ambos reviewers PASS en cada criterio de la rúbrica (`commands/santa-loop.md:50,63`) | 3 rondas (`:159`) |
| `gan-build` | Score ponderado ≥ umbral 7.0 (`commands/gan-build.md:8,57`) | 15 iteraciones; plateau si it≥3 sin mejora en 2 (`:7,61`) |
| `gan-evaluator` | Escala 1-10 con calibración (`agents/gan-evaluator.md:115-122`); fórmula 0.3/0.2/0.3/0.2 (`:126`); declara el modo realmente logrado (`:38-42`) | — |
| `orch-review` | Verdict APPROVE/CHANGES_REQUESTED; todo CRITICAL/HIGH pasa por verificador adversarial; falla cerrada (`commands/orch-review.md:76-78,104-108`) | — |
| `code-reviewer` | Cita línea, modo de fallo concreto; cero hallazgos es válido (`agents/code-reviewer.md:39-74`) | Confianza >80% (`:33`) |
| `agent-evaluator` | 5 ejes 1-5; score <5 exige evidencia (`agents/agent-evaluator.md:21-22`) | — |
| `multi-workflow` | Requisitos puntuados 0-10; <7 detiene (`commands/multi-workflow.md:130-133`) | — |

Evidencia aceptada: salidas de comandos, tests, líneas citadas, capturas; "mirar si se ve bien" es el anti-patrón (`skills/loop-design-check/SKILL.md:104`).

## 7. Modelos y esfuerzo

| Agente | `model:` | Cita |
|---|---|---|
| planner | opus | `agents/planner.md:5` |
| architect | opus | `agents/architect.md:5` |
| spec-miner | opus | `agents/spec-miner.md:4` |
| chief-of-staff | sonnet | `agents/chief-of-staff.md:5` |
| loop-operator | sonnet | `agents/loop-operator.md:5` |
| gan-planner / generator / evaluator | sonnet | `agents/gan-planner.md:5`, `gan-generator.md:5`, `gan-evaluator.md:5` |
| agent-evaluator | sonnet | `agents/agent-evaluator.md:5` |
| code-reviewer | sonnet | `agents/code-reviewer.md:5` |
| silent-failure-hunter | sonnet | `agents/silent-failure-hunter.md:4` |

Reglas de selección:
- `model-route`: haiku para cambios mecánicos, sonnet por defecto, opus para arquitectura y requisitos ambiguos (`commands/model-route.md:15-17`). `agentic-engineering` repite la regla y añade "Escalate model tier only when lower tier fails" (`skills/agentic-engineering/SKILL.md:141`).
- santa-loop: Reviewer A fijo en `opus`; B es Codex, luego Gemini (`-m gemini-2.5-pro`), Antigravity, o Claude (`commands/santa-loop.md:67,86-96,125`). Sin diversidad real se registra que "comparten familia de modelo" (`:139`).
- GAN: planner/generator/evaluator sonnet por defecto, subibles con `GAN_*_MODEL=opus` (`skills/gan-style-harness/SKILL.md:80,93,110`); `gan-build.md` no menciona esas variables.
- `blueprint`: reviewer adversarial con el "strongest model" (`skills/blueprint/SKILL.md:28`).
- Ralphinho: Plan/Code Review/Final Review en Opus, implementar en Codex (`skills/autonomous-loops/SKILL.md:465-474`).
- `council-multi-model`: solo acepta Codex CLI 0.146.0 exacto (`skills/council-multi-model/SKILL.md:105`).
- Nivel de razonamiento (effort/thinking): No encontrado. `council`, `dev-team`: sin modelo declarado.

## 8. Paralelismo y orquestación
- **Regla general**: paralelo para operaciones independientes (`rules/common/agents.md:38`), con contrato de cierre: quien delega recoge y entrega, nada de fire-and-forget (`:55-57`).
- **Subagentes en proceso**: team-builder (máx. 5, `skills/team-builder/SKILL.md:130`), dev-team (4 fijos, `skills/dev-team/SKILL.md:90`), council (3 voces, `skills/council/SKILL.md:85`).
- **Worktrees + tmux**: `orchestrate-worktrees.js` crea un worktree-rama por worker y un pane por worker (`skills/dmux-workflows/SKILL.md:167-173`); `multi-workflow` lo recomienda cuando se necesita estado git aislado (`commands/multi-workflow.md:112`). dmux: "mantén menos de 5-6 panes" (`skills/dmux-workflows/SKILL.md:111`).
- **DevFleet**: DAG de misiones, auto-merge, 3 agentes concurrentes por defecto (`skills/claude-devfleet/SKILL.md:36-40,75`); conflicto de merge queda en la rama del agente (`:111`).
- **Carriles**: `parallel-execution-optimizer` define la matriz Lane | ¿paralelo? | superficie de escritura | riesgo | verificación (`skills/parallel-execution-optimizer/SKILL.md:35-40`) y "solo paralelo si las superficies de escritura no chocan" (`:42`). Aviso: `docs/LANE-RULES.md` usa "lane" para otra cosa (workers codex del sistema Ito: una tarea, una rama, un PR, no lanzar subagentes; `docs/LANE-RULES.md:13,19`).
- **Anti-choque**: un owner por tarjeta, sin escrituras solapadas sin integrador (`skills/team-agent-orchestration/SKILL.md:67`); cola de merge con expulsión y contexto de conflicto (`skills/autonomous-loops/SKILL.md:478-508`); descomposición con mínimo solape de archivos (`:437`).
- **Monitoreo/reanudación**: `loop-status` CLI sobre transcripts (`commands/loop-status.md:17-19`); escalar si no hay progreso en 2 checkpoints, trazas idénticas, deriva de coste o conflictos (`agents/loop-operator.md:41-45`); estado "carry-forward" por registro verificado (`skills/parallel-execution-optimizer/SKILL.md:115-119`); SQLite reanudable en Ralphinho (`skills/autonomous-loops/SKILL.md:538`); `SHARED_TASK_NOTES.md` entre iteraciones (`:273`).

## 9. Gestión de contexto y coste
- Contexto fresco por paso con `claude -p` (`skills/autonomous-loops/SKILL.md:72`); sesión nueva tras cambio de fase, compactar tras hitos (`skills/agentic-engineering/SKILL.md:39-43`).
- spec-miner: muestrear, expandir máx. 15 archivos, diferir el resto (`agents/spec-miner.md:57-68`).
- Antigravity limitado a contexto <32k tokens (`commands/multi-execute.md:182`).
- Costes citados: santa 2-3x la generación (`skills/santa-method/SKILL.md:300`); muestreo 10-15% en lotes (`:246`); GAN ~14-22x el costo del agente solo (`skills/gan-style-harness/SKILL.md:264-272`); dedup antes de verificar redujo 11 hallazgos a 4 (`workflows/README.md:20`).
- Registrar por tarea modelo, tokens, reintentos, tiempo (`skills/agentic-engineering/SKILL.md:134-139`).

## 10. Reglas duras
- No escribir código antes de confirmar plan (`commands/plan.md:179`); no commit antes de GATE 2 (`commands/orch-add-feature.md:34`).
- "Never invent plausible-sounding requirements": usar `TBD` (`commands/plan-prd.md:23`).
- Plan PRP: parar y preguntar si hay ambigüedad (`commands/prp-plan.md:82-89`).
- Santa: solo arreglar lo marcado; push solo con NICE; tope 3 (`commands/santa-loop.md:151,170,210`).
- GAN: evaluador solo critica, generador arregla (`skills/gan-style-harness/SKILL.md:256`).
- Loops: parada explícita antes de empezar y tests verdes (`commands/loop-start.md:26-30`); 4 condiciones de veto antes de construir un loop (`skills/loop-design-check/SKILL.md:37-42`); cinco modos de fallo (`:101-107`); builder no edita criterios de aceptación (`:85`).
- Anti-patrones nombrados: "Agent soup", "Board theater", "Invisible work" (`skills/team-agent-orchestration/SKILL.md:97-101`); "Rubber stamping" (`skills/santa-method/SKILL.md:273`); "Silent skipping" (`skills/search-first/SKILL.md:181`).
- Enviar a contrapartes: nunca sin aprobación sobre el texto exacto; aprobación vieja no libera texto reescrito (`skills/operator-approval-loop/SKILL.md:8-10,88-89`).
- Review debe fallar cerrado, nunca APPROVE limpio si no corrió (`commands/orch-review.md:106-108`).

## 11. Supuestos del harness
- Claude Code con Agent/Task, `claude -p`, y la herramienta Workflow nativa (`workflows/README.md:3`).
- tmux + git worktrees (jj en Ralphinho, `skills/autonomous-loops/SKILL.md:524`), `gh` CLI, Node scripts de ECC.
- Codex CLI, Gemini CLI, `ccg-workflow` + `codeagent-wrapper` (`commands/multi-plan.md:9`), ace-tool MCP opcional (`:80`), Playwright MCP (`agents/gan-evaluator.md:4`), DevFleet MCP en puerto 18801 (`skills/claude-devfleet/SKILL.md:21`).
- Navegador para plan-canvas (`commands/plan-canvas.md:19-21`).

## 12. Fortalezas únicas
1. `loop-design-check`: meta-diseño de loops — meta decidable, frontera ("qué NO debe hacer"), juez independiente, humano voltea "done" (`skills/loop-design-check/SKILL.md:51-56,75,85`).
2. Santa: rúbrica binaria, reviewers frescos y aislados, tope y escalación, métricas de first-pass (`skills/santa-method/SKILL.md:79-82,204,290-296`).
3. Orch: clasificador de tamaño por señales con "mayor tier gana" y solo dos gates (`skills/orch-pipeline/SKILL.md:41-50,76-85`).
4. Honestidad operativa: reportar el modo de evaluación realmente logrado (`agents/gan-evaluator.md:38-42`), canal de búsqueda omitido (`skills/search-first/SKILL.md:181`), review incompleto no es aprobación (`workflows/README.md:53`).
5. Aprobación vinculada al texto exacto con hash/epoch (`skills/operator-approval-loop/SKILL.md:44-49`).
6. `plan-orchestrate` falla cerrado cuando un comando no puede llevar el alcance del paso (`skills/plan-orchestrate/SKILL.md:47-53`).
7. `code-reviewer`: "pre-report gate" y permiso para cero hallazgos (`agents/code-reviewer.md:39-74`).
8. `dynamic-workflow-mode`: separar quién-puede-leer/escribir/publicar del alcance de entidades (`skills/dynamic-workflow-mode/SKILL.md:31-50`).

## 13. Debilidades y huecos
- Redundancia alta entre familias (sección 2); varios alias cruzados sin semántica clara (`commands/epic-claim.md:22-26`).
- Contradicciones: `multi-plan` prohíbe Y/N y autoejecución (`commands/multi-plan.md:229-231`) pero `multi-execute` exige "Y" (`commands/multi-execute.md:21`); nombran `/ccg:execute`, no `multi-execute`. Pesos GAN: 0.3/0.2/0.3/0.2 (`agents/gan-planner.md:70-80`) vs 0.35/0.30/0.25/0.10 en `gan-design` (`commands/gan-design.md:23-27`, declarado a propósito). El skill GAN promete "sprint contract" (`skills/gan-style-harness/SKILL.md:88`) que ni `gan-generator` ni `gan-build` describen. `COMMAND-AGENT-MAP.md:26` lista `/orchestrate`, que `plan-orchestrate` prohíbe emitir (`skills/plan-orchestrate/SKILL.md:196`); y describe `/quality-gate` como pipeline (`docs/COMMAND-AGENT-MAP.md:24`) cuando es solo formatter.
- `blueprint` menciona checklist y catálogo de anti-patrones del review (`skills/blueprint/SKILL.md:28`) pero el archivo no los incluye: No encontrado.
- Dependencias externas pesadas (ccg, tmux, Codex, Playwright, DevFleet, `gh`).
- Solo código: TDD, coverage, PR, build, worktrees; `LANE-RULES` es específico de otro entorno (Mac mini, rutas, `docs/LANE-RULES.md:6,17`).
- GAN cuesta ~20x (`skills/gan-style-harness/SKILL.md:272`) y el score subjetivo depende de calibración del evaluador.

## 14. Aplicable a trabajo no-software

| Se traslada tal cual | Hay que adaptar | No aplica |
|---|---|---|
| Gate de plan antes de generar; archivo de handoff | Clasificador de tamaño (archivos → páginas/secciones/audiencia) | TDD red-green, coverage, build/lint |
| Rúbrica binaria + reviewer fresco (santa) | "Evidencia" de tests → checklist con fuentes y fechas | Worktrees, merge queue, tmux, DevFleet |
| `loop-design-check` completo | Lane matrix → "un entregable, un responsable, un archivo" | `orch-*`, `epic-*`, `prp-implement`, GAN con Playwright |
| Council / dev-team (roles de lectura, 4 lentes) | Roles PM/Arch/Dev/QA → roles del dominio | `multi-*` |
| Aprobación sobre texto exacto (operator-approval-loop, versión liviana) | `chief-of-staff`: 4 niveles de triage (`agents/chief-of-staff.md:28-53`) | Quality-gate formatter |

## 15. Los 5 patrones a extraer (por valor)
1. **Gate de plan + handoff en archivo + clasificador de tamaño**: plan aprobado antes de producir; confirmación antes de entregar; ceremonia proporcional (`skills/orch-pipeline/SKILL.md:41-85`; `docs/PLAN-PRD-PATTERN.md:20-24`).
2. **Meta decidable + frontera + juez independiente + humano cierra** (`skills/loop-design-check/SKILL.md:51-56,83-85`), con tope de 3 reintentos y escalación.
3. **Reviewer fresco y aislado con rúbrica binaria**, corrigiendo solo lo marcado, máx. 3 rondas (`skills/santa-method/SKILL.md:79-82,204`).
4. **Un responsable por entregable con superficie de escritura declarada** (versión mínima de `skills/parallel-execution-optimizer/SKILL.md:35-42` y tarjeta de `team-agent-orchestration`).
5. **Aprobación ligada al contenido exacto** (si el texto cambia, la aprobación caduca; `skills/operator-approval-loop/SKILL.md:44-49`).

**No traer**: `multi-*` y Antigravity (runtime externo, contradicciones); GAN (20x coste, orientado a UI); PRP de 8 fases (el propio repo lo declara sobredimensionado, `docs/PLAN-PRD-PATTERN.md:70`); `autonomous-loops`/Ralphinho/dmux/DevFleet (infra de código); `epic-*` (GitHub); `model-route`/`quality-gate` (formatter y tiers); `spec-miner` (OpenSpec); `LANE-RULES`; hooks de chief-of-staff (dependen de PostToolUse, fuera de alcance).

## Verificación
Se comprobaron 10 citas `ruta:línea` abriendo la línea citada (gan-build:61, orch-pipeline:85, code-reviewer:33, parallel-execution-optimizer:42, LANE-RULES:19, agentic-engineering:141, santa-loop:210, search-first:181, workflows/README:53, team-agent-orchestration:67). Las 10 coincidían con lo afirmado; se corrigieron 0.
