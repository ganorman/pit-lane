# Ficha 01 — Superpowers (obra, v7.0.2) y versión adaptada del usuario

Rutas relativas a `/home/claude/repos/superpowers/src`. Versión del usuario: `usuario-superpowers/SKILL.md`.

## 1. Propósito y alcance declarado
- Biblioteca de skills que se activan solas para que el agente no se lance a escribir código: primero pregunta qué quiere la persona (`README.md:38`), luego diseño, plan y ejecución con subagentes (`README.md:40-44`). Dice: "Mandatory workflows, not suggestions" (`README.md:324`).
- Alcance: núcleo claramente software (git, tests, ramas). Pero `skills/brainstorming/SKILL.md:3` declara que aplica "in software or out of it (a talk, a business, a renovation)", y `skills/brainstorming/SKILL.md:245-248` permite escribir el diseño en "a sensible place" fuera de un repo. El resto de skills asume código (ver apartado 13).
- Versión usuario: modo "para proyectos complejos" que incluye "documento complejo, estrategia o flujo de trabajo" (`usuario-superpowers/SKILL.md:4`).

## 2. Flujo paso a paso
| # | Fase | Skill | Entra | Sale |
|---|---|---|---|---|
| 0 | Arranque | using-superpowers (inyectada por hook, `hooks/session-start:49`) | cualquier mensaje | invocar skills aplicables antes de responder (`skills/using-superpowers/SKILL.md:20`) |
| 1 | Entender e intercambiar | brainstorming | petición vaga | enfoques elegidos (`skills/brainstorming/SKILL.md:28-29`) |
| 2 | Diseño escrito | brainstorming | enfoque elegido | doc de diseño aprobado (`skills/brainstorming/SKILL.md:30-32`) |
| 3 | Aislamiento | using-git-worktrees | diseño aprobado | worktree + línea base de tests verde (`README.md:312`; `skills/using-git-worktrees/SKILL.md:121-132`) |
| 4 | Plan | writing-plans | diseño | `docs/superpowers/plans/YYYY-MM-DD-<feature>.md` (`skills/writing-plans/SKILL.md:16`) |
| 5 | Elegir ejecutor | writing-plans (handoff) | plan | "Subagent-driven" o "Native" (`skills/writing-plans/SKILL.md:191-192`) |
| 6 | Ejecución | subagent-driven-development o executing-plans (+ test-driven-development) | plan + spec | commits + ledger (`skills/subagent-driven-development/SKILL.md:313`) |
| 7 | Revisión por tarea | requesting-code-review / task-reviewer-prompt | diff de la tarea | veredicto spec + calidad (`skills/subagent-driven-development/task-reviewer-prompt.md:16-19`) |
| 8 | Revisión final de rama | code-reviewer.md | rama completa | hallazgos; una sola tanda de arreglos (`skills/subagent-driven-development/references/final-review.md:18-31`) |
| 9 | Cierre | finishing-a-development-branch | rama verde | merge / PR / mantener (`skills/finishing-a-development-branch/SKILL.md:55-65`) |

Transversales: systematic-debugging ante fallos (`skills/systematic-debugging/SKILL.md:24-30`), verification-before-completion antes de afirmar éxito (`skills/verification-before-completion/SKILL.md:17`), receiving-code-review al recibir feedback. Brainstorming ya trae un atajo: si todo está en la petición, "Do it, and say what you did" (`skills/brainstorming/SKILL.md:22-24`).

## 3. Puntos de validación humana
Paradas fijas en un proyecto completo (mínimo 5; 4 si "hay una sola vía sensata", porque entonces enfoque y diseño se aprueban juntos, `skills/brainstorming/SKILL.md:34-36`):
1. Elegir enfoque (`skills/brainstorming/SKILL.md:156-167`).
2. Aprobar el doc de diseño: HARD-GATE, "Nothing gets built until your human partner approves" (`skills/brainstorming/SKILL.md:269-271`).
3. Consentir el worktree si no hay preferencia previa (`skills/using-git-worktrees/SKILL.md:41-45`).
4. Revisar el plan y elegir ejecutor (`skills/writing-plans/SKILL.md:184-194`).
5. Elegir opción de cierre; la decisión es de la persona (`skills/finishing-a-development-branch/SKILL.md:78-82`).

Paradas variables: preguntas y "playback" de 200-300 palabras que alternan (`skills/brainstorming/SKILL.md:192-200`); una ronda de preguntas tras el builder check (`skills/brainstorming/SKILL.md:263-266`); oferta del visual companion (`skills/brainstorming/SKILL.md:302-306`); línea base roja (`skills/using-git-worktrees/SKILL.md:130`); confirmar rama base (`skills/finishing-a-development-branch/SKILL.md:48-51`); escribir "discard" para borrar (`skills/finishing-a-development-branch/SKILL.md:143-146`).
Durante la ejecución NO hay paradas: "Do not pause to check in" (`skills/executing-plans/SKILL.md:27-30`), salvo cuatro causas: operación irreversible, acción sensible de seguridad, efecto externo (merge/push/publicar) o plan roto (`skills/executing-plans/SKILL.md:39-43`).

## 4. Roles y agentes
| Rol | Función | Contexto que recibe | Oculto a propósito |
|---|---|---|---|
| Controlador/orquestador | coordina, mantiene ledger, no arregla código | plan y spec | "never inherit your session's context" aplica a subagentes (`skills/subagent-driven-development/SKILL.md:10`) |
| Implementer | una tarea por subagente | ruta del brief, una línea de contexto, interfaces previas (`skills/subagent-driven-development/SKILL.md:209-215`) | historial de la sesión; no resúmenes acumulados (`skills/subagent-driven-development/SKILL.md:220-224`); no puede lanzar subagentes (`skills/subagent-driven-development/implementer-prompt.md:50-60`) |
| Task reviewer | veredicto spec + calidad | brief, informe, diff, restricciones globales (`skills/subagent-driven-development/SKILL.md:271-273`) | trata el informe como "unverified claims" (`skills/subagent-driven-development/task-reviewer-prompt.md:64-67`); no se le dice qué ignorar (`skills/subagent-driven-development/SKILL.md:285-290`) |
| Re-reviewer | verifica ADDRESSED/NOT ADDRESSED solo sobre el diff del arreglo (`skills/subagent-driven-development/re-review-prompt.md:55-62`) | hallazgos, brief, diff de arreglo | código no tocado |
| Final reviewer | revisión de rama | paquete de revisión, líneas de minors/parked (`skills/subagent-driven-development/references/final-review.md:6-16`) | historial |
| Builder check | subagente que lee el diseño sin poder hablar con el autor (`skills/brainstorming/builder-check-prompt.md:5-8`) | solo el documento | la conversación |

Reglas de reporte: el implementer devuelve estado en menos de 15 líneas (`skills/subagent-driven-development/implementer-prompt.md:140-146`) con cuatro estados (`skills/subagent-driven-development/implementer-prompt.md:142`). El prompt de `code-reviewer.md` no trae campo `model` (`skills/requesting-code-review/code-reviewer.md:8-10`), a diferencia de los otros (`skills/subagent-driven-development/implementer-prompt.md:8-9`).

## 5. Artefactos y persistencia
- Diseño: `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`, commiteado (`skills/brainstorming/SKILL.md:245-246`).
- Plan: `docs/superpowers/plans/...`, con cabecera obligatoria (Goal, Architecture, Tech Stack, Spec, Global Constraints, Review Focus) (`skills/writing-plans/SKILL.md:54-87`) y tareas con Files/Interfaces/pasos con checkbox (`skills/writing-plans/SKILL.md:94-138`).
- Workspace por plan: `<repo>/.superpowers/sdd/<plan-basename>/`, git-ignorado, con ledger, briefs, informes y paquetes de revisión (`skills/executing-plans/SKILL.md:125-131`).
- Ledger `progress.md`: primera línea `# SDD ledger — plan: <ruta>` y líneas `Task <N>: complete (...)` (`skills/executing-plans/SKILL.md:132-140`; `skills/subagent-driven-development/SKILL.md:313`).
- Retomar tras interrupción: confiar en ledger y `git log` antes que en la memoria (`skills/executing-plans/SKILL.md:136-138`); reanudar en la primera tarea sin línea "complete"; fix-round a medias se continúa en la siguiente ronda (`skills/subagent-driven-development/references/resuming.md:6-9`). Ambos ejecutores comparten ledger y pueden intercambiarse (`skills/executing-plans/SKILL.md:121-123`).
- Los "Ruling:" se recogen en el mensaje final antes de borrar el workspace (`skills/subagent-driven-development/references/final-review.md:35-42`).
- Skills de scripts: `task-done` solo registra si los tests pasan (`skills/executing-plans/scripts/task-done:41-48`).

## 6. Verificación y calidad
- "Terminado" por tarea (inline): tests nombrados existen y corrieron, última corrida verde, cada línea `Expected:` comparada con salida real, cada desvío con `Ruling:` (`skills/executing-plans/SKILL.md:211-219`).
- Evidencia válida: salida fresca de comando, no "should pass" (`skills/verification-before-completion/SKILL.md:20,42`); "Agent completed" exige diff de VCS, no el informe del agente (`skills/verification-before-completion/SKILL.md:47`). TDD exige ver el test fallar antes (`skills/test-driven-development/SKILL.md:113-128`).
- Bucle de arreglos (modo subagentes): máximo 5 rondas por tarea; 1-3 reanudan al implementer, 4-5 usan uno nuevo en modelo superior (`skills/subagent-driven-development/references/fix-loop.md:20-34`). Al tope, el controlador adjudica y deja ledger (`skills/subagent-driven-development/references/fix-loop.md:59-77`).
- Revisión final: UNA tanda de arreglos con un solo subagente, UNA re-revisión acotada, "no second fix wave" (`skills/subagent-driven-development/references/final-review.md:18-29`). En modo inline, una sola pasada de arreglos con test rojo→verde y sin re-revisión (`skills/executing-plans/SKILL.md:279-287`).
- Depuración: tras 3 arreglos fallidos, parar y cuestionar la arquitectura (`skills/systematic-debugging/SKILL.md:191-196`).
- Severidad: se reclasifica por efecto, no por silencio del spec (`skills/executing-plans/SKILL.md:267-271`); el reviewer lista "Declined to judge" (`skills/requesting-code-review/code-reviewer.md:43-48`).

## 7. Modelos y esfuerzo
| Regla | Cita (≤15 palabras) | Paráfrasis |
|---|---|---|
| Mínimo suficiente | "Use the least powerful model that can handle each role" (`skills/subagent-driven-development/SKILL.md:142`) | Gastar lo mínimo por rol |
| Tareas mecánicas | "use a fast, cheap model" (`skills/subagent-driven-development/SKILL.md:144`) | Spec clara, 1-2 archivos |
| Integración | "use a standard model" (`skills/subagent-driven-development/SKILL.md:146`) | Multi-archivo/depuración |
| Arquitectura y revisión final | "use the most capable available model" (`skills/subagent-driven-development/SKILL.md:148`) | La rama completa va al modelo más potente (`skills/subagent-driven-development/SKILL.md:149-150`) |
| Revisores | elegir por tamaño/riesgo del diff; re-revisiones pequeñas en gama baja-media (`skills/subagent-driven-development/SKILL.md:152-155`) | |
| Escalada | rondas 4-5: un nivel por encima del que se atascó (`skills/subagent-driven-development/SKILL.md:157-158`) | |
| Especificar siempre | "Always specify the model explicitly when dispatching a subagent" (`skills/subagent-driven-development/SKILL.md:160`) | Omitirlo hereda el modelo caro |
| Turnos vs precio | "Turn count beats token price" (`skills/subagent-driven-development/SKILL.md:164`) | Reviewers e implementers con prosa: mínimo gama media (`skills/subagent-driven-development/SKILL.md:166-167`); si el plan trae el código completo, gama barata (`skills/subagent-driven-development/SKILL.md:168-170`) |
| Sesión inline | sesión de gama media vale; el modelo top solo en la revisión final (`skills/executing-plans/SKILL.md:55-58`) | |
| Orquestador barato | un subagente orquestador en gama media, opt-in (`skills/using-superpowers/references/claude-code-tools.md:18-22`) | |
Nivel de razonamiento: No encontrado en las skills de Claude Code; solo `reasoning_effort` en `skills/using-superpowers/references/codex-tools.md:65-68`.

## 8. Paralelismo y orquestación
- Permitido: 2+ problemas independientes sin estado compartido; varios `Agent` en la misma respuesta (`skills/dispatching-parallel-agents/SKILL.md:36-40,66-77`). Tras volver: revisar conflictos y correr la suite completa (`skills/dispatching-parallel-agents/SKILL.md:161-167`).
- Prohibido: fallos relacionados, estado compartido, depuración exploratoria (`skills/dispatching-parallel-agents/SKILL.md:129-134`); "Never dispatch multiple implementation subagents in parallel" (`skills/subagent-driven-development/SKILL.md:235`).
- Aislamiento: worktree en `.worktrees/` verificando que esté ignorado (`skills/using-git-worktrees/SKILL.md:80-88`); herramienta nativa antes que `git worktree add` (`skills/using-git-worktrees/SKILL.md:53-57`); workspace de ledger separado por plan (`skills/executing-plans/SKILL.md:125-131`).
- Agrupar ediciones pequeñas del mismo tipo en un solo despacho (`skills/subagent-driven-development/references/batching.md:5-11`).
- Espera de subagentes: tramos acotados de 5-10 min con reconciliación (`skills/subagent-driven-development/SKILL.md:187-196`).

## 9. Gestión de contexto y coste
- Todo lo que se pega o imprime "stays resident"; entregar artefactos como archivos (`skills/subagent-driven-development/SKILL.md:183-185`); diff en archivo, no en el contexto del controlador (`skills/subagent-driven-development/SKILL.md:261-266`).
- Narrar una línea como máximo entre llamadas (`skills/executing-plans/SKILL.md:24-25`); salida larga de tests a archivo (`skills/executing-plans/SKILL.md:167-169`).
- La compactación no sobrevive: ledger como memoria (`skills/subagent-driven-development/SKILL.md:108-111`); el fallo más caro observado fue re-despachar tareas completas (`skills/subagent-driven-development/SKILL.md:109-111`).
- Los briefs son la única fuente de requisitos: no pegar el plan entero (`skills/subagent-driven-development/SKILL.md:214-215`).
- Seguridad de contexto al leer transcripciones: medir antes de leer (`skills/diagnosing-superpowers/references/context-safety.md:8-14`).
- Tres modos de coste: subagentes (más minucioso), inline (más barato, `skills/writing-plans/SKILL.md:191-192`), orquestador de gama media (`skills/using-superpowers/references/claude-code-tools.md:28-29`).

## 10. Reglas duras
| Ley / prohibición | Dónde |
|---|---|
| Invocar skill ante 1% de probabilidad | `skills/using-superpowers/SKILL.md:11` |
| HARD-GATE: nada se construye sin diseño aprobado | `skills/brainstorming/SKILL.md:269-271` |
| NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST; código previo se borra | `skills/test-driven-development/SKILL.md:34-37` |
| NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST | `skills/systematic-debugging/SKILL.md:17` |
| NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE | `skills/verification-before-completion/SKILL.md:17` |
| NO SKILL WITHOUT A FAILING TEST FIRST | `skills/writing-skills/SKILL.md:166` |
| Nunca review saltada "porque es simple" | `skills/requesting-code-review/SKILL.md:84-88` |
| Implementer no despacha subagentes | `skills/subagent-driven-development/implementer-prompt.md:50-52` |
| Prohibidas respuestas performativas ("You're absolutely right!") | `skills/receiving-code-review/SKILL.md:29-32` |
| Nunca `--force` en limpieza por iniciativa propia | `skills/finishing-a-development-branch/SKILL.md:178-180` |
| Nunca pre-juzgar a un reviewer ("do not flag") | `skills/subagent-driven-development/SKILL.md:285-290` |
Anti-patrón nombrado recurrente: tablas "Common Rationalizations" y "Red Flags" en casi todas las skills (p. ej. `skills/executing-plans/SKILL.md:308-323`).

## 11. Supuestos del harness
- Claude Code es el "reference harness" (`skills/using-superpowers/references/claude-code-tools.md:3-4`): subagentos (`Agent`), todos, `Skill`.
- Hook `SessionStart` (startup|clear|compact) que inyecta using-superpowers (`hooks/hooks.json:3-10`; `hooks/session-start:49`).
- Git obligatorio: SHAs, worktrees, ramas (`skills/using-git-worktrees/SKILL.md:16-33`), scripts `bash` (`skills/writing-skills/SKILL.md:161`).
- Subagentos anidados (3 niveles por defecto) para el orquestador barato (`skills/using-superpowers/references/claude-code-tools.md:13-16`).
- Sin subagentes: fallback a executing-plans con autorrevisión declarada como más débil (`skills/executing-plans/SKILL.md:255-260`).
- Un runner de tests del proyecto (`skills/using-git-worktrees/SKILL.md:121-128`).

## 12. Fortalezas únicas
- Compuerta dura de diseño antes de construir, con enfoques alternativos y revisor "builder check" que busca huecos sin hablar con el autor (`skills/brainstorming/SKILL.md:250-267`).
- Recuperación ante compactación: ledger por plan, `task-done` que solo registra si pasa, reanudación determinista (`skills/executing-plans/SKILL.md:132-140`).
- Decisiones de la IA visibles: "Rulings, not stalls" y lista exhaustiva "Rulings I made" (`skills/subagent-driven-development/SKILL.md:19-25`; `skills/subagent-driven-development/references/final-review.md:35-42`).
- Topes explícitos a los bucles (5 rondas, una tanda final, 3 arreglos en depuración) que evitan iterar sin fin.
- Aislamiento de contexto de revisores y desconfianza del informe (`skills/subagent-driven-development/task-reviewer-prompt.md:64-71`).
- Tabla de selección de modelo por rol y regla "turn count beats token price".
- Metodología para probar las propias skills con subagentes (`skills/writing-skills/SKILL.md:30-45,250-259`) y skill de autodiagnóstico de sesiones (`skills/diagnosing-superpowers/SKILL.md:15-17`).

## 13. Debilidades y huecos
- Mayoría de skills son solo para código: TDD, depuración, worktrees, finishing, revisión de diff.
- Pesada para tareas pequeñas: brainstorming ya admite el atajo (`skills/brainstorming/SKILL.md:22-24`), pero el resto del pipeline no tiene versión ligera.
- El ledger y los scripts requieren bash y git (`skills/executing-plans/scripts/task-done:20-26`).
- Sin definición de "listo" para entregables no verificables por test (documentos): No encontrado.
- Ejecución sin paradas (`skills/executing-plans/SKILL.md:27-30`): la persona solo ve los rulings al final.
- Coste alto en modo subagentes: un contexto nuevo por tarea y por revisión (`skills/writing-plans/SKILL.md:191`).
- Nivel de razonamiento: sin reglas para Claude Code (apartado 7).

## 14. Aplicable a trabajo no-software
- **Se trasladan casi tal cual:** compuerta de aprobación antes de producir (`skills/brainstorming/SKILL.md:269-271`); preguntas una a una y playback por trozos (`skills/brainstorming/SKILL.md:99-207`); enfoques alternativos con recomendación; builder check con dominio cambiado (el prompt trae `[DOMAIN]`, `skills/brainstorming/builder-check-prompt.md:5-6`); evidencia antes de afirmar (`skills/verification-before-completion/SKILL.md:17`); ledger de progreso y "Rulings"; reviewers con contexto limpio que desconfían del informe; recibir feedback verificando antes de implementar (`skills/receiving-code-review/SKILL.md:12`).
- **Hay que adaptar:** plan en tareas de 2-5 min con interfaces (`README.md:314`) a secciones de un documento o módulos de una hoja; "tests" a criterios de aceptación revisables (checklist línea a línea, `skills/verification-before-completion/SKILL.md:48`); aislamiento (worktree) a copia de trabajo/versión del archivo; reviewer de código a reviewer de contenido; menú de cierre a "entregar / revisar / guardar".
- **No aplican:** worktrees, ramas y merge, TDD literal (`skills/test-driven-development/SKILL.md:34-37`), depuración con instrumentación, paquetes de diff por SHA.

## 15. Diferencias entre original y versión adaptada
| Aspecto | Original | Usuario |
|---|---|---|
| Estructura | 15 skills + scripts y prompts | 1 skill de 128 líneas |
| Fases | brainstorming, worktree, plan, ejecución, review, cierre | 5 fases: entender, planificar, criterios, ejecutar, revisar (`usuario-superpowers/SKILL.md:19-87`) |
| Aprobación humana | HARD-GATE y 5+ paradas | Sin parada obligatoria: solo preguntar si falta información crítica (`usuario-superpowers/SKILL.md:28`) |
| Preguntas | una a la vez, Socrático, en conversación | lista de datos faltantes y supuestos marcados "[Supuesto: ...]" (`usuario-superpowers/SKILL.md:28`) |
| Criterios de calidad | dispersos (Global Constraints, Review Focus, `skills/writing-plans/SKILL.md:70-87`) | fase propia (`usuario-superpowers/SKILL.md:45-52`) |
| Revisión | subagentes frescos, dos pasadas y final | autorrevisión en dos niveles, spec y calidad (`usuario-superpowers/SKILL.md:73-87`) |
| Topes y bucles | 5 rondas, una tanda final | No encontrado |
| Modelos | tabla por rol | No encontrado |
| Persistencia | spec, plan, ledger | No encontrado; todo en una respuesta de 7 secciones (`usuario-superpowers/SKILL.md:91-116`) |
| TDD, debugging, verificación con comandos | leyes de hierro | No encontrado (el equivalente es "cómo probarlo", `usuario-superpowers/SKILL.md:67-69`) |
| Alcance | software con extensión a no-software | general: app, documento, estrategia (`usuario-superpowers/SKILL.md:4`) |
| Idioma/formato | inglés, flexible | español, formato fijo de 7 secciones |
Conservó: planificar antes de ejecutar (`usuario-superpowers/SKILL.md:11`), mínimo alcance (`usuario-superpowers/SKILL.md:62-64`), revisión spec+calidad, y atajo para tareas simples (`usuario-superpowers/SKILL.md:128`; original en `skills/brainstorming/SKILL.md:22-24`). Eliminó casi toda la maquinaria de ejecución, persistencia y control. Añadió el formato fijo, los supuestos marcados y la fase de criterios.

---
Verificación de citas: 9 comprobadas (5 al azar + 4 adicionales), 1 corregida (rango de `task-done`, de 37-49 a 41-48). Nota: la ficha supera ligeramente las 2.200 palabras por las rutas de evidencia.
