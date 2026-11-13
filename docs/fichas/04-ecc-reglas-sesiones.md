# Ficha 04 — ECC v2.2.3: reglas, sesiones, memoria, aprendizaje y coste

Rutas relativas a `/home/claude/repos/ECC/src`. Alcance: reglas, contextos, hooks, comandos y skills de sesión, memoria, aprendizaje, coste y evals. No cubre plan/prp/multi-*/orch-*/gan/santa/epic. Todo el contenido leído se trató como dato; no se ejecutó nada.

## 1. Propósito y filosofía declarada

- Se define como plugin de codificación "production-ready" con 71 agentes, 314 skills y 98 commands (`AGENTS.md:3`). Verificado por conteo de directorios: 71 / 314 / 98.
- Cinco principios: Agent-First, Test-Driven (80%+), Security-First, Immutability, Plan Before Execute (`AGENTS.md:9-13`; repetidos en `SOUL.md:7-11`).
- Las skills son la superficie canónica; `commands/` queda como compatibilidad heredada (`AGENTS.md:177-179`).
- `SOUL.md` solo añade una "visión cross-harness": capa de portabilidad inicial (`SOUL.md:16-17`).
- `CLAUDE.md` aporta un "Prompt Defense Baseline": no cambiar de rol, tratar contenido externo como no confiable (`CLAUDE.md:9-16`).
- Las guías son personales: configurar "como fine-tuning, no arquitectura" (`the-shortform-guide.md:407`) y "la ventana de contexto es preciosa" (`:408`).
- La longform pone el foco en economía de tokens, persistencia de memoria y verificación (`the-longform-guide.md:16`).

## 2. Flujo de trabajo por defecto

Fuente: `rules/common/development-workflow.md:9-44` y `AGENTS.md:165-173`.

0. Research & Reuse, "obligatorio": GitHub search, docs de librería, Exa solo si hace falta, registries (`development-workflow.md:9-15`).
1. Plan First con agente planner; PRD, arquitectura, task_list (`:17-21`).
2. TDD: RED, GREEN, IMPROVE, 80%+ (`:23-28`).
3. Code Review inmediato; corregir CRITICAL/HIGH (`:30-33`).
4. Commit & Push con conventional commits (`:35-38`).
5. Pre-review checks: CI verde, sin conflictos (`:40-44`).

`AGENTS.md` salta el paso 0 y añade "capturar conocimiento en el lugar correcto" (memoria personal vs docs del proyecto) (`AGENTS.md:168-172`). Los contextos añaden modos: dev, research, review (§4).

## 3. Selección de modelo y esfuerzo

`AGENTS.md`, `SOUL.md` y `CLAUDE.md` no contienen ninguna regla de modelo: No encontrado. Las reglas viven en cuatro sitios que no coinciden del todo.

| Tarea | Modelo | Esfuerzo | Fuente |
|---|---|---|---|
| Exploración/búsqueda | Haiku | no definido | `the-longform-guide.md:118` |
| Ediciones simples | Haiku | no definido | `the-longform-guide.md:119` |
| Docs | Haiku | no definido | `the-longform-guide.md:124` |
| Implementación multi-archivo | Sonnet | `medium` recomendado | `the-longform-guide.md:120`; `docs/token-optimization.md:19` |
| Revisión de PRs | Sonnet | no definido | `the-longform-guide.md:122` |
| Orquestar multi-agente | Sonnet | no definido | `rules/common/performance.md:12` |
| Arquitectura compleja | Opus | `high` + Plan Mode | `the-longform-guide.md:121`; `rules/common/performance.md:49-50` |
| Seguridad | Opus | no definido | `the-longform-guide.md:123` |
| Debug complejo | Opus | no definido | `the-longform-guide.md:125` |
| Research y análisis | Opus | no definido | `rules/common/performance.md:18` |
| Subagentes (por defecto) | Haiku vía env | n/a | `docs/token-optimization.md:20,36` |
| Observer de aprendizaje | Haiku | n/a | `skills/continuous-learning-v2/agents/observer.md:4` |
| Resumen LLM en pre-compact | Haiku (configurable) | n/a | `scripts/lib/llm-summary.js:24-25` |

Citas útiles: "Default to Sonnet for 90% of coding tasks" (`the-longform-guide.md:127`). Regla de escalada: pasar a Opus si el primer intento falló, la tarea abarca 5+ archivos, decisiones de arquitectura o código crítico de seguridad (mismo párrafo, `:127`). Orquesta el Claude principal ("your orchestrator (main Claude)", `the-shortform-guide.md:78`).

Esfuerzo: en modelos adaptativos se controla con `/effort`, `--effort` o `CLAUDE_CODE_EFFORT_LEVEL`; `MAX_THINKING_TOKENS` positivo se ignora (`rules/common/performance.md:35-42`; `docs/token-optimization.md:41`). `/model-route` solo devuelve modelo, confianza, motivo y fallback; no recomienda esfuerzo (`commands/model-route.md:19-24`).

**Contradicciones internas**
1. Haiku para "pair programming y code generation" (`performance.md:7`) frente a Haiku solo en ediciones simples y Sonnet para multi-archivo (`longform:119-120`).
2. Seguridad en Opus (`longform:123`), pero `agents/security-reviewer.md:5` declara `model: sonnet` (archivo fuera del alcance, citado solo por esto).
3. Reviews en Sonnet (`longform:122`; `token-optimization.md:61`) frente a "deep review" en Opus (`model-route.md:17`).
4. Sonnet cubre "~80%" de tareas (`token-optimization.md:34`) o "90%" (`longform:127`).
5. Ahorro de Haiku: "3x" (`performance.md:5`), "3-4x" (`cost-aware-llm-pipeline/SKILL.md:42`), pero la tabla de la misma skill da 1x vs 2x (`:160-161`).
6. Opus para "research" (`performance.md:18`) frente a Haiku para exploración (`longform:118`) y subagentes Haiku por defecto.

## 4. Gestión de contexto

- Evitar el último 20% de la ventana en refactors grandes, features multi-archivo y debug de interacciones; ediciones simples y docs toleran más (`rules/common/performance.md:22-31`; `AGENTS.md:197`).
- `strategic-compact` sugiere `/compact` con dos señales: tokens reales (160k en ventana 200k, 250k en 1M, repetir cada +60k) y conteo de herramientas (50, luego cada 25) (`skills/strategic-compact/SKILL.md:36-37`). Admite que el conteo es "weak proxy" (`:39`).
- Tabla de decisión: compactar tras Research→Plan, Plan→Implementación, Debug→siguiente feature y tras un enfoque fallido; no a mitad de implementación (`:82-89`).
- Qué sobrevive: CLAUDE.md, archivos, memoria, git; se pierde razonamiento intermedio y preferencias dichas de palabra (`:95-101`). Advertencia: la lista de tareas puede no existir, así que "escribe el plan a un archivo antes de compactar" (`:103-115`).
- Monitor de contexto (dentro del dispatcher PostToolUse): aviso con 35% restante, crítico con 25% (`scripts/hooks/ecc-context-monitor.js:18-19`; registro en `scripts/hooks/posttooluse-dispatcher.js:51`). El aviso dice "evitar empezar trabajo complejo nuevo" (`ecc-context-monitor.js:142`); el crítico ordena no guardar estado de forma autónoma (`:135`). Esto contradice el consejo de ejecutar `/save-session` antes del límite (`commands/save-session.md:12`) si lo hace el agente solo.
- MCPs: con demasiados, 200k pueden quedar en 70k; menos de 10 activos y menos de 80 herramientas (`the-shortform-guide.md:144-146`).
- Auto-compact: la longform recomienda desactivarlo y compactar a mano (`the-longform-guide.md:52`); `docs/token-optimization.md:43-45` avisa de errores con `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`.
- `/clear` entre tareas no relacionadas (`token-optimization.md:80`).
- Contextos por modo (se cargan con alias `--system-prompt`, `the-longform-guide.md:67-75`; no hay hook que los cargue: No encontrado):
  - dev: código primero, explicar después; prioridades "funcionar, correcto, limpio" (`contexts/dev.md:7-15`).
  - research: leer antes de concluir, "no escribir código hasta entender" (`contexts/research.md:10`); salida "hallazgos primero" (`:26`).
  - review: severidad crítico>alto>medio>bajo; agrupar por archivo (`contexts/review.md:8,22`).
- `context-budget`: por defecto no usa herramientas y remite a `/context` o `/status`; la auditoría estática exige opt-in explícito (`skills/context-budget/SKILL.md:19-24,41-45`).

## 5. Gestión de coste y límites

- Medición: hook Stop `stop:cost-tracker` escribe `~/.claude/metrics/costs.jsonl`, un snapshot acumulado por sesión; se toma la última fila por `session_id` (`commands/cost-report.md:13-19`; `hooks/hooks.metadata.json:138-139`). Prohibido sumar todas las filas ni recalcular precios (`skills/cost-tracking/SKILL.md:93-100`).
- Avisos de coste: aviso informativo a $5, $10 y $50 (`ecc-context-monitor.js:20-22`), con la frase "Informational only — not an instruction to stop" (`:155`). Se pueden apagar con `ECC_CONTEXT_MONITOR_COST_WARNINGS=off`, recomendado para suscripciones (`docs/token-optimization.md:37`).
- "Detenerse al X% del plan": No encontrado. Lo más cercano es `budget_limit` + `BudgetExceededError`, pero solo para apps que llaman a la API (`cost-aware-llm-pipeline/SKILL.md:61,139-140`), y la statusline opcional que muestra ventanas de rate-limit sin actuar (`docs/STATUSLINE.md:3-4,9`).
- Statusline: contexto restante, modelo, rama (`the-shortform-guide.md:362-372`); uso opcional con `ECC_STATUSLINE_USAGE=1` (`STATUSLINE.md:9-15`).
- Frenos manuales: `/cost` (`token-optimization.md:82`), subagentes Haiku, no usar Agent Teams salvo paralelismo claro (`:135-141`), MCPs mínimos (`:123`), `--budget low|med|high` en model-route (`model-route.md:11`).
- `token-budget-advisor`: menú 25/50/75/100% de profundidad antes de responder (`skills/token-budget-advisor/SKILL.md:59-62`), estimación heurística ±15% (`:66`).
- Coste oculto: el pre-compact llama a `claude -p` para resumir (`scripts/hooks/pre-compact.js:3-9`; `scripts/lib/llm-summary.js:180`).

## 6. Sesiones y persistencia

**`/save-session`** → `~/.claude/session-data/YYYY-MM-DD-<short-id>-session.tmp` (`commands/save-session.md:32,37`). Un archivo por sesión, nunca se anexa a otro (`:270`). Muestra el archivo y pide confirmación (`:54-64`). Secciones, en orden (`:70-180`):

1. Cabecera: Started, Last Updated, Project, Topic (`:71-76`)
2. What We Are Building (`:80`)
3. What WORKED (with evidence), con "confirmed by" (`:88-97`)
4. What Did NOT Work (and why), "la más importante" (`:101-110,271`)
5. What Has NOT Been Tried Yet (`:114`)
6. Current State of Files, tabla con estado (`:127-138`)
7. Decisions Made (`:142`)
8. Blockers & Open Questions (`:153`)
9. Exact Next Step (`:164`)
10. Environment & Setup Notes, opcional (`:174-179`)

Regla: no saltar secciones, escribir "Nothing yet" (`:52`).

**`/resume-session`**: sin argumento elige un candidato (`resume-session.md:28-40`); descarta vacíos, placeholders y resúmenes de un solo mensaje, luego el más reciente (`:52-68`); lee entero, presenta briefing fijo con "WHAT NOT TO RETRY" (`:78-104`), no toca archivos y espera al usuario (`:106-108`); avisa si pasaron más de 7 días o faltan archivos (`:123-127`).

**`/checkpoint`**: ejecuta `/verify quick`, hace stash o commit y añade una línea a `.claude/checkpoints.log` (`checkpoint.md:17-23`); `verify` compara archivos, tests, cobertura y build (`:31-46`); `clear` conserva los últimos 5 (`:78`). `/verify` no existe en `commands/`: No encontrado.

**`/sessions`**: list/load/alias/info sobre el mismo almacén (`sessions.md:7,11`).

**Automático (hooks)**: Stop guarda estado tras cada respuesta (`hooks.metadata.json:128-129`) con formato distinto: cabecera con Worktree (`scripts/hooks/session-end.js:161-165`) y secciones Tasks, Files Modified, Tools Used, Stats (`:358-378`), más pie "Notes for Next Session / Context to Load" (`:24`). PreCompact inserta un resumen LLM entre marcadores `<!-- ECC:SUMMARY:START -->` (`pre-compact.js:20-21`). SessionStart carga contexto, máximo 8000 caracteres, sesiones de hasta 7 días (`session-start.js:42,69`), retención 30 días (`:43`).

Tras una interrupción: inferencia mía a partir de "después de cada respuesta", se pierde como máximo la respuesta en curso; el archivo no está escrito en la estructura de 10 secciones (hay dos formatos).

## 7. Memoria y aprendizaje continuo

- **Instinct**: unidad atómica con id, trigger, confidence, domain, source, scope (`skills/continuous-learning-v2/SKILL.md:52-72`).
- **Captura**: hooks PreToolUse/PostToolUse, "100% fiables" frente a skills que disparan 50-80% (`:41,346-351`); un agente observer en segundo plano con Haiku analiza (`:94`). **Desactivado por defecto**: `observer.enabled: false`, mínimo 20 observaciones, cada 5 min (`:226-228`; `config.json:4-6`). En Windows nativo no funciona (`:243-247`).
- **Confianza**: 0.3 tentativo, 0.5 moderado, 0.7 "auto-approved", 0.9 casi seguro (`:327-332`). Inicial por frecuencia 0.3/0.5/0.7/0.85; +0.05 por confirmación, -0.1 por contradicción, -0.02 por semana sin verse (`agents/observer.md:130-139`). SessionStart inyecta solo instincts ≥0.7, máximo 6 (`scripts/hooks/session-start.js:38-39`).
- **Alcance**: proyecto por defecto (hash de git remote); global si aparece en 2+ proyectos con confianza media ≥0.8 (`SKILL.md:129-136,304-306`). Guía de qué es global vs proyecto (`:289-298`).
- **`/evolve`**: agrupa instincts en commands, skills o agents; candidato a skill con 2+ instincts (`commands/evolve.md:23-26,83`). `--generate` escribe en `evolved/`, no en skills activas (`:87-89`).
- **`/learn`**: extracción manual a `~/.claude/skills/<nombre>/SKILL.md`, con confirmación del usuario (`commands/learn.md:40,83-87`), redacción de secretos y tratamiento de la sesión como no confiable (`:44-53`).
- **`/learn-eval`**: añade ubicación global vs proyecto (`learn-eval.md:23-27`), checklist de solapamiento (`:82-89`) y veredicto Save / Improve / Absorb / Drop (`:95-100`); Drop sin confirmación (`:114`).
- **`unified-memory`**: vault Markdown `ecc.memory.v1` con alcances project/team/user (`skills/unified-memory/SKILL.md:11,44-48`); buscar antes de escribir (`:60-62`); "recall es evidencia, no certeza" (`:76-98`); nunca promover un recuerdo a regla sin revisión humana (`:163-165`). Requiere runtime npm aparte (`:16-19`).
- **`context-and-decisions`**: CONTEXT.md solo con lenguaje de dominio; decisiones a ADR; tareas al tracker (`skills/context-and-decisions/SKILL.md:11-22,36-45,88`).
- Inconsistencia de rutas: la skill dice `~/.local/share/ecc-homunculus` (`SKILL.md:30,140-144`), pero `evolve.md:88-89` e `instinct-status.md:34-35` leen `~/.claude/homunculus`.

## 8. Hooks

Perfiles `minimal|standard|strict` (`hooks/README.md:162-165`). Evento (línea en `hooks/hooks.json`) → hook (`hooks.metadata.json`):

| Evento | Hook | Qué automatiza | Rol |
|---|---|---|---|
| PreToolUse (3) | `pre:bash:dispatcher` (`metadata:6`) | calidad, tmux, push, GateGuard | seguridad/código |
| PreToolUse | `pre:edit-write:gateguard-fact-force` (`:46-47`) | niega la primera edición de cada archivo hasta presentar hechos | seguridad; fricción alta |
| PreToolUse | `pre:config-protection` (`:36-37`) | bloquea cambios a configs de linter | código |
| PreToolUse | `pre:edit-write:suggest-compact` (`:21-22`) | sugiere compactar | **esencial al método** |
| PreToolUse | `pre:observe:continuous-learning` (`:26-27`) | captura para instincts | solo si hay aprendizaje |
| PreToolUse | `pre:mcp-health-check`, `pre:write:doc-file-warning`, `pre:governance-capture` (opt-in) | salud MCP, docs, gobernanza | comodidad |
| UserPromptSubmit (102) | `prompt:hookify-runtime` (`:58`) | reglas locales de prompt | opcional |
| PreCompact (113) | `pre:compact` (`:65-66`) | guarda estado antes de compactar | **esencial** |
| SessionStart (124) | `session:start` (`:72-73`) | carga contexto previo | **esencial** |
| SessionStart | `plan-canvas-sessions` (`:77-78`) | reanuda revisiones Plan Canvas | comodidad |
| PostToolUse (144) | dispatchers sync/async (`:84-90`): context-monitor, activity-tracker, design-quality | avisos y telemetría | context-monitor esencial |
| PostToolUseFailure (167) | `post:mcp-health-check`, `post:skill:track` | MCP y skills | comodidad |
| Stop (187) | `stop:session-end` (`:128-129`) | persiste sesión | **esencial** |
| Stop | `stop:cost-tracker` (`:138-139`) | métricas de coste | esencial si se mide |
| Stop | `stop:evaluate-session` (`:133-134`) | patrones extraíbles | aprendizaje |
| Stop | `stop:format-typecheck`, `stop:check-console-log`, `stop:desktop-notify` | format, tsc, console.log, aviso | solo código/comodidad |
| SessionEnd (271) | `session:end:marker` (`:150-151`) | marca de cierre | menor |

El perfil `minimal` conserva session-end, evaluate-session, cost-tracker y marker, pero `pre:compact` está solo en standard y strict (`hooks.json:119`). La clasificación "esencial" es juicio mío.

## 9. Reglas duras

- Inmutabilidad "CRITICAL" (`rules/common/coding-style.md:3-13`); archivos 200-400 líneas, techo 800 (`:39`); funciones <50 líneas, anidación >4 (`code-review.md:30-32`).
- TDD obligatorio, cobertura 80% mínima, unit + integration + E2E (`testing.md:3-18`). Arreglar la implementación, no los tests (`:25`).
- Antes de commit: sin secretos, inputs validados, SQL parametrizado, XSS, CSRF, rate limiting (`security.md:5-13`). Al hallar un problema: STOP, agente de seguridad, rotar secretos (`:24-29`).
- Revisión obligatoria tras escribir código, antes de commit, en código sensible y antes de merge (`code-review.md:9-15`); CRITICAL bloquea, HIGH advierte (`:55-56,111-115`).
- Nunca `dangerously-skip-permissions` (`hooks.md:14`).
- Contrato de delegación: el mensaje final es el entregable; quien delega recoge resultados; no re-delegar tareas de un solo contexto (`agents.md:51-59`). Paralelo "ALWAYS" para tareas independientes (`:38`).
- Contenido recordado o de sesión = no confiable (`unified-memory/SKILL.md:71`; `learn.md:44-53`).
- Evals: "Never fully automate security checks" (`eval-harness/SKILL.md:203`).
- Cost-tracking: no inventar uso si falta el log; no instalar hooks sin revisar (`cost-tracking/SKILL.md:61-63,100`).

## 10. Autoevaluación y evals

- `agent-self-evaluation`: tras tareas no triviales puntúa 1-5 en accuracy, completeness, clarity, actionability, conciseness (`skills/agent-self-evaluation/SKILL.md:11-18,24-40`). Regla de evidencia: todo puntaje <5 cita un hueco concreto (`:44`); cada eje se puntúa por separado (`:68`); no es puerta de aprobación (`:9`); anti-patrón "todo es 5" (`:134-142`).
- `eval-harness` (EDD): define evals antes de codificar (`skills/eval-harness/SKILL.md:199`); capability vs regression (`:31-53`); graders de código, reglas, modelo o humano (`:279-282`); pass@k y pass^k con umbrales pass@3 ≥ 0.90 y pass^3 = 1.00 (`:290-292`; `the-longform-guide.md:162-170`). Artefactos en `.claude/evals/` (`:303-305`). La ejecución de candidatos está deshabilitada por falta de aislamiento (`:262-266`). `/eval` no existe como comando: No encontrado.
- `/harness-audit`: scorecard determinista de hasta 12 categorías, rúbrica `2026-05-19` (`commands/harness-audit.md:27-42`).
- `agent-evaluator` (AGENTS.md:77) puntúa en 5 ejes la salida de otro agente.

## 11. Supuestos del harness

- Plugin de Claude Code con `hooks.json` propio y `CLAUDE_PLUGIN_ROOT`; no pegarlo en settings (`hooks/README.md:29-31`). El instalador escribe `settings.json` (`:41-42`), incluso `includeCoAuthoredBy: false` (`rules/common/git-workflow.md:12`).
- Node para todos los hooks (`hooks/README.md:316`); Python3 para el CLI de instincts (`commands/evolve.md:14`); `claude -p` para resúmenes (`llm-summary.js:5`).
- Rutas fijas: `~/.claude/session-data/`, `~/.claude/skills/`, `~/.claude/metrics/`.
- Statusline por script absoluto (`STATUSLINE.md:13-15`). Las herramientas de tareas pueden faltar en modelos nuevos (`strategic-compact/SKILL.md:105-109`).
- Sólo en Linux/macOS/WSL2 funciona el observer (`continuous-learning-v2/SKILL.md:243-247`).
- **Portable**: formato de archivo de sesión y briefing (Markdown puro), tabla de compactación, modelo de instinct y veredictos de `/learn-eval`, regla de evidencia, glosario vs ADR, filosofía EDD. SOUL.md reconoce que la portabilidad real aún no existe (`SOUL.md:16-17`).
- Instalación selectiva: manifiestos de módulos y perfiles `core/developer/security/research/full` (`docs/SELECTIVE-INSTALL-ARCHITECTURE.md:546-550`); resolver intención → grafo → adaptador → estado de instalación (`:461-465`).

## 12. Fortalezas únicas

1. Sección "What Did NOT Work" obligatoria y briefing "WHAT NOT TO RETRY" (`save-session.md:101-110`; `resume-session.md:92-93,180`). Evita repetir callejones sin salida.
2. Resume con ranking que rechaza archivos placeholder y ecos de resumen (`resume-session.md:52-68`), coherente con el cuerpo vacío que genera el hook (`session-end.js:25`).
3. Compactar según fase y "escribir antes de compactar", con dos señales y umbrales (`strategic-compact/SKILL.md:36-37,82-89,113-115`).
4. Aprendizaje con confianza, decaimiento, aislamiento por proyecto y regla de promoción cuantitativa (`observer.md:136-139`; `SKILL.md:304-306`).
5. Tratar la memoria como evidencia, con handoff que separa resultado verificado de intención (`unified-memory/SKILL.md:76-98`).
6. Veredicto Absorb/Drop que frena la acumulación de skills (`learn-eval.md:95-100`); el propio archivo explica que sustituyó una rúbrica numérica (`:143-145`).
7. Mensajes de coste honestos ("informativo, no es instrucción de parar", `ecc-context-monitor.js:155`).
8. Separación glosario / decisión / estado de tareas (`context-and-decisions/SKILL.md:22,88`).

## 13. Debilidades y huecos

- Tamaño: 71 agentes, 314 skills, 98 commands, repo de 111 MB (`AGENTS.md:3`; `du`). Instalar todo carga mucho y obliga a elegir perfiles.
- Redundancia y desajustes: `agents.md:26` dice 69 agentes frente a 71; `rules/README.md:8-16` omite `code-review.md` y `development-workflow.md`; `token-optimization.md:102` cita un "README" de strategic-compact que no existe (solo `SKILL.md`).
- Referencias rotas: `/verify` y `/eval` sin archivo; rutas de homunculus divergentes; dos formatos de sesión.
- Casi todo asume código: TDD, 80%, inmutabilidad, tsc, prettier, console.log, GateGuard.
- Contradicciones de modelo (§3) y precios con fecha fija en una skill (`cost-aware-llm-pipeline/SKILL.md:155-165`) que otra prohíbe copiar (`cost-tracking/SKILL.md:99`).
- Sin freno real por límite de plan; solo avisos.
- Aprendizaje automático apagado por defecto y sin efecto en Windows nativo.
- Riesgos de instalar entero: hooks que bloquean con exit 2 (`hooks/README.md:51,54`), GateGuard por cada primera edición, reglas Hookify de repos si se confía en ellas (`:185-189`), gasto extra por resúmenes LLM, inyección de hasta 8000 caracteres en cada inicio.
- `memory` MCP configurado pero sin uso (`token-optimization.md:131`).

## 14. Los 5 patrones que vale la pena extraer

1. **Archivo de traspaso con "qué funcionó con evidencia / qué falló y por qué / qué falta / decisión / bloqueo / próximo paso exacto"** y un resume que informa sin actuar (`save-session.md:70-180`; `resume-session.md:106-108`). Sirve igual para estudios, documentos y negocio.
2. **Compactar en límites de fase y escribir el estado a archivo antes** (`strategic-compact/SKILL.md:82-89,113-115`). Umbrales de referencia: 35% / 25% restante (`ecc-context-monitor.js:18-19`).
3. **Criterios de éxito definidos antes de trabajar y autochequeo con evidencia** (`eval-harness/SKILL.md:199`; `agent-self-evaluation/SKILL.md:44`). Sin puntaje numérico.
4. **Aprender con compuerta humana**: candidato → veredicto Save/Improve/Absorb/Drop → promoción solo tras repetición en 2+ contextos (`learn-eval.md:95-100`; `continuous-learning-v2/SKILL.md:304-306`).
5. **Higiene de memoria**: lo recordado es evidencia a verificar; glosario, decisiones y tareas en lugares distintos (`unified-memory/SKILL.md:76-98`; `context-and-decisions/SKILL.md:22,88`).

Mención: "el modelo más barato que alcance, escalar si el primer intento falla" (`the-longform-guide.md:109,127`). Traer el principio, no la tabla, por sus contradicciones.

**No traer**
- Roster de agentes por lenguaje y perfiles de instalación: sin sentido fuera de código.
- TDD/80%/inmutabilidad/límites de líneas: reglas de software.
- Hooks de format, tsc, console.log, notificaciones, GateGuard: comodidad o fricción.
- Dispatchers, perfiles y variables ECC_*: complejidad de mantenimiento alta.
- Observer automático por cada herramienta: apagado por defecto, no funciona en Windows, implica registrar toda la actividad.
- Vault `unified-memory`: requiere runtime npm y duplica la memoria del harness.
- Puntaje 1-5 de autoevaluación: el mismo agente se califica; ECC abandonó los puntajes numéricos en learn-eval.
- `token-budget-advisor` (±15%, una pregunta por prompt), `cost-aware-llm-pipeline` (para apps con API), pricing con fecha.

## Verificación de citas

Comprobé 10 citas reabriendo la línea citada: `ecc-context-monitor.js:135,142,155`, `the-longform-guide.md:127`, `save-session.md:12`, `hooks.json:119`, `continuous-learning-v2/SKILL.md:305-306`, `eval-harness/SKILL.md:203`, `agents.md:26` y `context-and-decisions/SKILL.md:22`. Corregí 0: todas decían lo afirmado. Los números de línea se tomaron con `cat -n` por archivo.
