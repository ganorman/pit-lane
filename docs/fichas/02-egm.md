# Ficha 02 — Elephant-Goldfish Model (EGM, Google)

Rutas relativas a `/home/claude/repos/elephant-goldfish-model/src`. Los números de línea son de cada archivo.

## 1. Propósito y alcance declarado
- Plugin para asistentes de IA: el Elephant (contexto) redacta, los Goldfish (sin la conversación previa) revisan y la persona decide (`README.md:16-18`).
- Alcance: el flujo de borrador y revisión "targets software specifications". Para otros documentos hay que elegir revisores y estándares con `/egm-review-loop`. Bootstrap y drift "apply to software codebases" (`README.md:20`).
- Es Spec-Driven Development: el entregable es una especificación aprobada; el código se pide después (`docs/getting_started.md:5-6`, `:79-82`).

## 2. Flujo paso a paso
| # | Fase / skill | Entra | Sale |
|---|---|---|---|
| 1 | `egm-brainstorm`: interrogatorio abierto, luego enjambre de 7 lentes (`skills/egm-brainstorm/SKILL.md:104-180`) | idea cruda | `concepts_brief.md` (`:181-210`) |
| 2 | `egm-draft`: sección por sección (`skills/egm-draft/SKILL.md:141-250`) | `concepts_brief.md` o `discussion_summary.md` (`:146-155`) | `design_draft.md`, luego `<DESIGN_DIR>/<FEATURE>.md` (`:309-312`) y `SITEMAP.md` si existe (`:306-307`) |
| 3 | `egm-review` interactivo, etapas 5→9 (`skills/egm-review/SKILL.md:164-166`) | doc de diseño | `zoom_out_report.md`, `comprehension_report.md`, `critic_report.md`, `intermediate_zoom_out_report.md`, `implementation_readiness_report.md` (`:287-303`) |
| 3a | Etapas 7 y 9 vía `egm-review-loop` (`:373-376`, `:400-405`) | hallazgos | `goldfish_review_report.md` (`skills/egm-review-loop/SKILL.md:152`) |
| 4 | `egm-resolve`: clasifica y aplica ediciones (`skills/egm-resolve/SKILL.md:54-82`) | lista de hallazgos | doc editado, informe marcado `Status: resolved` (`:184`) |
| 5 | Revisión humana por PR (`docs/getting_started.md:75-77`) | spec | spec aprobada |
| 6 | Implementar: sin skill, "tell AI to build" (`docs/getting_started.md:79-82`) | spec | código |
| 7 | `egm-drift-report`, recomendado semanal (`docs/getting_started.md:98`) | carpeta de diseños + código | `{YYYY-MM-DD}_DRIFT_REPORT.md` (`skills/egm-drift-report/SKILL.md:47`) |
| — | `egm-bootstrap` (aparte): README por directorio, de hojas a raíz (`docs/getting_started.md:124-133`) | árbol de código | `README.md` o `EGM.md` (`skills/egm-bootstrap/SKILL.md:44-47`) |

Modo "consolidado": ejecuta las 5 etapas sin parar y escribe `consolidated_review_report.md` (`skills/egm-review/SKILL.md:280-313`). En ese modo la etapa 7 usa el sintetizador, no el review-loop, así que no hay resolución (`:294-296`). Quién corrige después: No encontrado.

## 3. Puntos de validación humana
Mínimo fijo en el recorrido interactivo completo (conteo mío, derivado):
- **Brainstorm: 4.** Compuerta de preparación (`egm-brainstorm/SKILL.md:127-155`), respuesta a objeciones (`:217-218`), alineación con el brief (`:224-225`), compuerta de traspaso (`:226-246`). Además, preguntas abiertas en varios turnos (`:110-116`).
- **Draft: 6.** Consenso de contexto (`egm-draft/SKILL.md:163`), 4 aprobaciones de sección (`:87-139`, pasos 2-5), carpeta destino (`:277-298`). Condicionales: contradicciones brief vs borrador (`:257-275`) y elecciones de arquitectura, hasta 3 opciones sin recomendar (`:63-72`).
- **Review: ≥10.** Compuerta de preset (`egm-review/SKILL.md:128-131`), 5 compuertas de etapa (`:236-251`) y la compuerta de `egm-resolve` en cada ronda de las etapas 7 y 9 (`egm-resolve/SKILL.md:110-134`). El review-loop exige dos rondas limpias seguidas (`egm-review-loop/SKILL.md:173`). Puede haber hasta 2 preguntas de intake (`egm-review/SKILL.md:84-100`).
- **Total ≈ 20 paradas** sin contar turnos de clarificación ni rondas extra. Cada compuerta admite una sola pregunta (`resources/execution_instructions.md:24-27`). El agente debe quedarse inactivo hasta que la persona responda (`egm-resolve/SKILL.md:131-133`).
- La persona aprueba: hipótesis, cada sección, qué correcciones se aplican (auto accept, desglose, comentarios) y el paso a la siguiente etapa.

## 4. Roles y agentes
- **Elephant:** el contexto principal. Redacta y resuelve; se recomienda correr `egm-resolve` en la sesión que generó el documento (`egm-resolve/SKILL.md:24-28`).
- **Goldfish:** subagentes frescos, de solo lectura, que reciben el documento, el estándar y `GoldfishContext` (archivos enlazados) (`egm-review/SKILL.md:101-119`). No reciben la conversación (`docs/harnesses.md:107-111`). Los adaptadores de Claude fijan `tools: [Read, Grep, Glob]` y `omitClaudeMd: true` (`.claude-plugin/agents/design_critic.md:5-8`). La etapa 6 recibe solo el documento (`egm-review/SKILL.md:118-119`).
- **Sintetizador:** orquesta el enjambre, deduplica, normaliza enlaces y escribe el informe. Devuelve un solo mensaje corto con el estado por revisor (`agents/synthesizer.md:9-14`, `:66`).

| Agente | Persona | Qué busca (modo REVIEW) |
|---|---|---|
| `zoom_out` | Skeptical Architect | YAGNI, reinvención, optimización prematura, "weeds"; obligado a buscar código existente (`agents/zoom_out.md:44-55`) |
| `comprehension` | Lector ingenuo | Paráfrasis primero; términos sin definir; si no puede parafrasear, es Blocker (`agents/comprehension.md:37`) |
| `design_critic` | Crítico de diseño hostil | Brechas contra el estándar, supuestos sin respaldo, riesgos sin mitigar (`agents/design_critic.md:37-44`) |
| `implementation_readiness` | Tech lead | Pasos vagos; decisiones dejadas al implementador (`agents/implementation_readiness.md:37-43`) |
| `codebase_details` | Auditor pedante | Documento vs código; referencias inexistentes (`agents/codebase_details.md:38-50`) |
| `structural` | Validador de estructura | Encabezados faltantes, jerarquía, formato (`agents/structural.md:37-46`) |
| `style` | Editor técnico | Hipérbole, relleno; caveats con DROP/CALIBRATE/RELOCATE/KEEP (`agents/style.md:38-48`) |
| `inventive_catalyst` | TRIZ | Falsos compromisos, patrones con costo secundario; solo Major/Nit (`agents/inventive_catalyst.md:62-100`) |
| `synthesizer` | Compilador | Deduplicar, priorizar, escribir informe (`agents/synthesizer.md:42-66`) |
| `bootstrap_orchestrator` | Arquitecto de docs | Particiona subárboles y coordina trabajadores (`agents/bootstrap_orchestrator.md:20-30`) |

En modo BRAINSTORM cada persona cambia de lente: `zoom_out` = YAGNI, `design_critic` = costes, `comprehension` = UX, `implementation_readiness` = migración, `codebase_details` = observabilidad, `structural` = deuda técnica (`docs/designs/brainstorm.md:122-128`).

## 5. Artefactos y persistencia
- Todos son Markdown en el directorio de trabajo, o en uno indicado con la línea `EGM artifact directory:` (`docs/harnesses.md:127-128`). Si la ruta sale del directorio de trabajo, se pide confirmación (`docs/harnesses.md:130-134`).
- Se prohíbe volcar documentos largos al chat; se escribe archivo y se notifica la ruta (`egm-brainstorm/SKILL.md:40-45`).
- Retomar tras una interrupción: "Pause Review (save progress and exit)" conserva los informes (`egm-review/SKILL.md:276-278`). No existe un archivo de estado explícito (No encontrado). El reinicio se apoya en los informes y en `Step` para saltar a una etapa (`:76-78`). Al reanudar se relee el archivo para recalcular líneas (`:264-270`).
- Las plantillas de documento están en `skills/egm-draft/references/design_doc.md:1-177`. El pie `*Drafted with EGM*` aparece ahí (`:177`) y en el diseño (`docs/designs/draft.md:51`), pero no en el SKILL de draft (No encontrado).

## 6. Verificación y calidad
**Cinco etapas** (`egm-review/SKILL.md:287-303`): 5 Zoom Out + Inventive Catalyst sobre el archivo completo; 6 Comprehension; 7 Critic (`design`, `structural`, `style`); 8 Zoom Out intermedio centrado en lo añadido en 6 y 7; 9 Implementation Readiness (`implementation_readiness`, `codebase_details`, `style`).

- **Deduplicación y prioridad:** el sintetizador agrupa en Blocker/Major/Nit y deduplica (`agents/synthesizer.md:42`). En el modo consolidado hay matriz de trazabilidad (`egm-review/SKILL.md:304-309`). Cada hallazgo recibe un id `<reviewer>-<round>-<n>` (`egm-review-loop/SKILL.md:136-139`).
- **Quién decide:** el Elephant propone una categoría (PROPOSE FIX, CONTEST, ESCALATE, DECLINE) y la persona aprueba (`egm-resolve/SKILL.md:54-66`, `:110-134`). Un CONTEST debe citar evidencia que el revisor podía leer (`:71-73`). No se contesta una brecha de comprensión (`:77-79`). No se cambia la severidad (`:79-80`).
- **Rondas:** el tope es 5 rondas; converge con dos rondas limpias seguidas; "churn" detiene el ciclo y pregunta a la persona (`egm-review-loop/SKILL.md:169-181`). En `egm-review`, cada etapa admite máximo 1 re-auditoría (`egm-review/SKILL.md:271-275`).
- **Revisor fallido:** un reintento y luego "not run"; nunca cuenta como cero hallazgos (`egm-review-loop/SKILL.md:140-144`).
- **Sin subagentes de contexto limpio:** la revisión se detiene; una revisión en el mismo contexto "is not a Goldfish review" (`egm-review/SKILL.md:28`, `docs/harnesses.md:107-109`). Excepción: `egm-bootstrap` corre sus scouts en línea (`egm-bootstrap/SKILL.md:35`). Contradicción interna: `egm-review-loop/TEST.md:30` habla de iterar personas en secuencia en "degraded mode".

## 7. Modelos y esfuerzo
No encontrado: ninguna regla de selección de modelo ni nivel de razonamiento. Todos los adaptadores fijan `model: inherit`, es decir, heredan el modelo de la sesión (`.claude-plugin/agents/design_critic.md:6`; también en `.cursor-plugin/agents/*.md:4`). El texto menciona un "reasoning LLM" solo para extraer símbolos de un README viejo (`egm-bootstrap/SKILL.md:236-238`).

## 8. Paralelismo y orquestación
- Brainstorm: 7 lentes "simultaneously" para evitar sesgo secuencial (`egm-brainstorm/SKILL.md:54-56`).
- Etapa 5: `zoom_out` e `inventive_catalyst` en paralelo (`egm-review/SKILL.md:322-324`). Las etapas son estrictamente secuenciales 5→9 (`:136-140`, `:217`).
- Jerarquía: el review-loop llama al sintetizador y este lanza el enjambre en paralelo (`egm-review-loop/SKILL.md:119-125`). Sin anidación se despacha cada revisor directo (`:128-133`). Opcional: instancias A y B por revisor para más recall (`agents/synthesizer.md:40`). Claude Code anida hasta 3 niveles (`docs/harnesses.md:96`).
- Bootstrap: trabajadores en paralelo "without artificial concurrency limits" (`egm-bootstrap/SKILL.md:198-199`), con compuerta si hay más de 15 subdirectorios (`:66-68`). Cada scout lee unas 1.500 líneas (`:249-254`).
- El tope máximo de revisores simultáneos en revisión: No encontrado.

## 9. Gestión de contexto y coste
- El sintetizador existe para no contaminar el contexto raíz con "6 to 12" revisores y para evitar duplicados (`docs/designs/synthesizer.md:22-30`). Solo devuelve un resumen, no el informe (`:104-110`).
- Política "artifact-first": nada largo en el chat (`docs/designs/architecture.md:171-185`).
- Los revisores solo leen el documento y lo enlazado; los enlaces fuera del directorio de trabajo o las URL requieren aprobación (`egm-review/SKILL.md:101-117`).
- Coste en tokens o dinero: No encontrado. `getting_started.md:98` y `egm-review/SKILL.md:304-309` dan indicios, pero no hay presupuesto. El diseño reconoce que el review genera "a lot" de feedback (`docs/getting_started.md:71-73`).

## 10. Reglas duras
- Universales de todo Goldfish: solo lectura, mentalidad sin estado, sin charla (`agents/design_critic.md:9-13`).
- Elephant: cero archivos de producción; scratchpad fuera del árbol (`resources/execution_instructions.md:3-12`). Una pregunta por turno (`:24-27`). Sin resúmenes de estado (`:29-31`). Ante contradicción, cero ediciones en ese turno (`:32-37`).
- Anti-adulación: sin elogios ni disculpas, crítica primero (`egm-draft/SKILL.md:35-61`). Arquitectura la decide el autor, sin ranking ni default (`:63-72`).
- "Proposed files are not findings" (`agents/codebase_details.md:50`). Un revisor no ejecutado no es "cero hallazgos" (`egm-review-loop/SKILL.md:140-144`).
- Contribución: sin PR autónomos (`AGENTS.md:7-8`).

## 11. Supuestos del harness
- Herramienta de subagentes de contexto fresco; sin ella, se detiene (`docs/harnesses.md:107-109`). Fallback: persona genérica que lee `agents/<archivo>.md`, o despacho directo (`:103-105`).
- Instalar el plugin completo; las skills leen `agents/` y `resources/` en tiempo de ejecución (`docs/harnesses.md:24-26`).
- Los skills tienen `disable-model-invocation: true` (`skills/egm-review/SKILL.md:4`). En Claude Code no se usa la herramienta `Skill`; se lee el SKILL.md y se sigue en el mismo hilo (`docs/claude.md:20-25`).
- Límites reconocidos: Codex y Antigravity filtran `AGENTS.md` al contexto del revisor; no hay exclusión verificada (`docs/harnesses.md:148-158`). Cowork y ChatGPT Work: huecos de verificación abiertos (`:161`). Antigravity IDE independiente no soportado (`:32`). Para Claude exige 2.1.271 o posterior (`docs/claude.md:8-9`).

## 12. Fortalezas únicas
- **Estándares de documento versionados** (`resources/document_standards/*.md`): el estándar de Alternativas obligatorias, la regla Zero-Decision (`implementation-readiness-standard.md:12-18`) y la Heilmeier (`heilmeier-standard.md:13-30`).
- **Paráfrasis primero** del lector ingenuo: detecta documentos cuyas partes no conectan (`agents/comprehension.md:37`).
- **Inventive Catalyst/TRIZ:** exige verificar que exista una contradicción real y declarar costos secundarios (`agents/inventive_catalyst.md:62`, `:25`).
- **Reglas de resolución anticorrupción:** el autor no puede contestar sin evidencia legible (`egm-resolve/SKILL.md:71-83`).
- **Convergencia formal:** hallazgos "settled", rondas limpias, churn (`egm-review-loop/SKILL.md:159-181`).
- **Drift report** y **bootstrap** de contratos (`egm-drift-report/SKILL.md:34-43`; `egm-bootstrap/SKILL.md:386-405`).
- **Separación Feature/Detailed** por encabezado, que dirige a cada revisor (`egm-review/SKILL.md:186-196`).
- Registro de pruebas de aislamiento (`TESTING.md:145-151`).

## 13. Debilidades y huecos
- **No ejecuta ni verifica la implementación:** "Design-Only" (`execution_instructions.md:3-8`); la fase 5 no tiene skill (`docs/designs/architecture.md:157-159`). Los límites de escritura son convención "nothing enforces" (`:164-165`). Solo el drift report detecta divergencia, después y a mano.
- No revisa el entregable final contra la intención original; la comprobación brief vs borrador la hace el propio Elephant (`egm-draft/SKILL.md:257-275`).
- Los revisores son lectores LLM; "A review does not replace tests or human judgment" (`README.md:121`).
- Excesivo: unas 20 paradas, 10+ agentes, enjambres A/B y dos rondas limpias mínimas; el propio texto avisa de mucho feedback (`docs/getting_started.md:71-73`).
- Inconsistencias: la etapa 7 invoca a `egm-resolve` dentro del review-loop y otra vez por la compuerta (`egm-review/SKILL.md:373-396` vs `egm-review-loop/SKILL.md:146-155`). El diseño de brainstorm cita Heilmeier (`docs/designs/brainstorm.md:129-131`), pero el SKILL no la usa.
- Vocabulario de software pegado a las personas ("Senior Software Engineer", código, endpoints).

## 14. Aplicable a trabajo no-software
- **Tal cual:** disciplina de artefactos en archivo; compuertas de una pregunta; `comprehension` (lector ingenuo con paráfrasis); `style`; revisores sin contexto; reglas de `egm-resolve` (CONTEST/ESCALATE); convergencia.
- **Adaptar:** `structural` necesita una plantilla propia como estándar; `design_critic` y `zoom_out` hay que reescribirlos (hablan de QPS, código y YAGNI). Heilmeier sirve para propuestas (`heilmeier-standard.md:13-30`). `codebase_details` y `implementation_readiness` solo valen si el entregable cita datos o fuentes verificables.
- **No aplica:** `egm-bootstrap`, `egm-drift-report`, el `FeatureRange`/`DetailedRange` (depende del encabezado `## Detailed Implementation Plan`, `egm-review/SKILL.md:186-196`) y la fase de implementación.
- **Cómo funciona `egm-review-loop`:** recibe `TargetFile`, `SemanticTarget` (o `full file`), `Reviewers` y `Standards` (`egm-review-loop/SKILL.md:50-63`). Un nombre con `/` se toma como ruta propia, lo que permite revisores y rúbricas personalizados (`:77-78`). Cada ronda: relee el rango (`:109-113`), lanza el enjambre y consolida, `egm-resolve` clasifica y aplica ediciones, y la persona decide (`:146-155`). Itera hasta dos rondas limpias, 5 rondas o churn (`:169-181`). Inferencia mía: como todo se basa en archivos de texto con líneas y encabezados, un DOCX o XLSX tendría que convertirse a Markdown; el soporte directo para esos formatos: No encontrado.

## 15. Cómo se define un revisor
Archivo `agents/<nombre>.md` (ejemplo: `agents/style.md`):
1. **Frontmatter:** `name: egm-<x>`, `description`, `license` (`agents/style.md:1-5`). Adaptador por harness con `tools`, `model: inherit`, `omitClaudeMd` (`.claude-plugin/agents/design_critic.md:1-9`).
2. **`# Core Mandates (Universal Goldfish Context)`:** 3 mandatos idénticos: solo lectura, sin estado, sin charla (`:7-13`).
3. **`# Role`:** persona, tono y actitud (`:17-20`).
4. **`# Instructions`:** bifurcación `IF Mode: BRAINSTORM` / `IF Mode: REVIEW`, con pasos numerados (`:26-40`) y `### Audit Vectors` con viñetas "Nombre: definición" (`:42-48`).
5. **`# Output Format`:** lenguaje natural; cada hallazgo lleva `Severity [Blocker|Major|Nit]`, `Affected Scope` y una descripción con justificación (`:52-60`). En BRAINSTORM añade `Dimension` y `Requirement` (`:62-67`).
6. Variantes: `inventive_catalyst` añade catálogo y la salida "No false compromise detected" (`agents/inventive_catalyst.md:85`); `comprehension` antepone la paráfrasis (`agents/comprehension.md:57`).
7. Se registra en `.claude-plugin/plugin.json` (`docs/harnesses.md:83`) y se enlaza a su estándar por nombre en `Standards` (`egm-review-loop/SKILL.md:74-76`).

---
Comprobación: se reabrieron 16 citas (5 al azar y 11 adicionales de riesgo); 7 estaban desfasadas y se corrigieron (4 rangos de egm-resolve, 3 de docs/harnesses.md).
