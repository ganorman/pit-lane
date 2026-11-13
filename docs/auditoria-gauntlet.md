# Auditoría del repo — paso 7

Fecha: 2026-11-13 · Commit auditado: `1a260f6` (paso 6: skill) · Fuente de verdad: `docs/analisis-y-diseno.md`
Método: `skills/gauntlet/agents/arbitro.md`. Listón L1 a L9 del encargo del paso 7 (sección 8), congelado.

## Informe del árbitro — Ronda 1

**Veredicto global:** RECHAZADO
**Modo:** independiente (sesión nueva con contexto limpio; no es un subagente)

| ID | Criterio | Veredicto | Evidencia |
|---|---|---|---|
| L1 | `git ls-files` = archivos de la sección 7 (salvo `docs/auditoria-gauntlet.md`, más `.gitignore` si existe) | PASA | `git ls-files` devuelve 31 archivos. La sección 7 lista 32; sin `docs/auditoria-gauntlet.md` quedan 31, y coinciden uno a uno: raíz (4), `.claude-plugin/plugin.json`, `skills/pit-lane/SKILL.md`, `skills/gauntlet/` (5), `agents/` (7), `references/` (3), `scripts/` (2), `docs/` (analisis-y-diseno, critica-ronda1..3, decisiones, `fichas/01..04`). No hay `.gitignore` ni archivos de más. |
| L2 | Cada ID R-01 a R-39 aparece en `skills/pit-lane/SKILL.md` o en `references/` | PASA | Búsqueda de `R-NN` por ID: los 39 aparecen al menos una vez en `skills/pit-lane/SKILL.md` (skill = 1 o 2 por ID) y ninguno falta. Detalle de líneas en la tabla de L4. |
| L3 | `model` y `effort` de cada agente = sección 7 | PASA | `mecanico` sonnet/medium · `mecanico-experto` opus/high · `mecanico-auxiliar` haiku/low · `lector-ingenuo`, `lector-critico`, `lector-ejecucion` sonnet/medium · `arbitro` opus/high (líneas 4-5 de cada `agents/*.md`). Coinciden con la sección 7, líneas 416 a 422. |
| L4 | El texto que cita cada regla no dice lo contrario de la sección 6 | PASA | Tabla "L4 — cita por regla", más abajo. Ninguna cita contradice la sección 6. Tres citas son discutibles y van como observaciones (O1 a O3). |
| L5 | `AGENTS.md` < 100 líneas; `skills/pit-lane/SKILL.md` < 250 | PASA | `wc -l`: `AGENTS.md` 77 · `skills/pit-lane/SKILL.md` 133. |
| L6 | Todo `[CONFIRMAR]` fuera de `docs/` aparece aquí con archivo y línea | PASA | `git ls-files \| grep -v '^docs/' \| xargs grep -n '\[CONFIRMAR\]'` → 5 apariciones, todas listadas en "L6 — marcadores", más abajo. |
| L7 | La prosa de los pasos 1 a 6 está en español latinoamericano | PASA | Leí completos `README.md`, `AGENTS.md`, `plugin.json` (`description`), `skills/pit-lane/SKILL.md`, `references/*.md`, `agents/*.md`, `scripts/LEEME.md` y los tres ajustes de `skills/gauntlet/SKILL.md`. Sin voseo peninsular (vosotros, habéis, podéis), sin léxico peninsular (ordenador, fichero, coger, móvil). La única coincidencia, "vale el modo degradado" (`SKILL.md:125`), es el verbo *valer* y está tomado de la sección 6.10.7. Los términos técnicos van en inglés (status line, plugin, frontmatter). |
| L8 | `git diff` paso 0 → actual en `skills/gauntlet/` = solo los tres ajustes del paso 2 | PASA | `git diff 1f7be7e HEAD --stat -- skills/gauntlet/` → solo `SKILL.md`, 5 inserciones y 0 borrados. Bloques: (1) Fase 0, línea 29: contrato `pit-lane/contrato.md` con "Aprobado:", bitácora por encargo y de coherencia; (2) paso 4 "Auditar", línea 78: modelo y esfuerzo declarados y `pit-lane:arbitro`; (3) "Reglas del loop", línea 87: reintento único y "árbitro no ejecutado". `git log -- skills/gauntlet/` → solo `1f7be7e` y `05a6958`. |
| L9 | Ninguna skill ni agente nombra un agente o la skill gauntlet sin `pit-lane:` | NO PASA | `agents/arbitro.md:32`: "El del `arbitro.md` de la skill gauntlet." Nombra la skill gauntlet sin prefijo, y no es un campo `name` ni una ruta de archivo. |

### Hallazgos (solo NO PASA y NO VERIFICABLE)

- **L9** — Dónde: `agents/arbitro.md`, línea 32 (sección "Formato de salida"). · Hay: "El del `arbitro.md` de la skill gauntlet." · Debe haber: la skill nombrada con prefijo, como en la línea 15 del mismo archivo (sección 7: "La skill del Jefe de pits los llama siempre con prefijo"; `AGENTS.md`, regla de contenido 3). · Corrección: cambiar a "El del `arbitro.md` de la skill `pit-lane:gauntlet`." Es un cambio de una línea, sin tocar nada más.

### Fallos de la ronda anterior

- No aplica: es la ronda 1.

### Disputas

- No hay disputas registradas.

---

## L4 — cita por regla

Cita principal en `skills/pit-lane/SKILL.md` (S) y, cuando la hay, en `references/` (E = enrutamiento, M = modos-de-ejecucion, P = plantillas) o `agents/` (A). Veredicto: la cita no contradice la sección 6.

| ID | Línea(s) | Texto del repo (resumido) | Sección 6 |
|---|---|---|---|
| R-01 | S:40 | "Evalúa las seis señales; gana el nivel más alto… Decláralo en una línea… salvo que Gerardo lo vete" | 6.3 ✔ |
| R-02 | S:55 | "Se hace y se dice qué se hizo, sin contrato" | 6.3 ✔ |
| R-03 | S:64, P:23 | "Nada se construye sin contrato aprobado" (sección F1, para M, L y XL) | 6.1.1 ✔ |
| R-04 | S:65, P:43 | "un solo bloque de hasta 4 preguntas, cada una con opción recomendada… Ambigüedad menor: decides y lo anotas" | 4, C6 ✔ |
| R-05 | S:66, P:23, P:45 | "Listón binario… al aprobarse queda congelado y solo Gerardo lo cambia" | 6.5 ✔ |
| R-06 | S:67, P:44 | "El contrato declara la FRONTERA" | 6.5 ✔ |
| R-07 | S:68, P:46, A:25 | "contrato y encargos los citan, no los copian" | 6.1.5 ✔ (ver O1) |
| R-08 | S:87, P:23, M:35, M:53 | "Una sola aprobación… En XL, dos: primero el contrato y después el plan" | 4, C1 · 6.2 ✔ |
| R-09 | S:89 | "solo cuatro causas detienen… irreversible, sensible, sale a terceros, plan roto" | 6.1.3 ✔ |
| R-10 | S:76, P:55, M:36, M:54 | "Un encargo por archivo, con la plantilla de la sección 2" | 6.6 ✔ (ver O2) |
| R-11 | S:77, P:79, M:22, A:26 | "dos encargos corren en paralelo solo si no se solapan" | 6.1.6 · 4, C3 ✔ |
| R-12 | S:78, S:98, E:21, M:20, A:27, A:31 | "Cada encargo declara modelo, esfuerzo y la línea 'Árbitro:'" | 6.7.1 ✔ |
| R-13 | S:79, E:23, A (auxiliar):10, 27 | "`pit-lane:mecanico-auxiliar` (Haiku) solo si el encargo lo trae todo. En la duda, Sonnet" | 6.7.2 ✔ |
| R-14 | S:81, P:49, M:21, M:38, M:55 | "oleadas de 2 mecánicos como máximo" | 6.11 ✔ |
| R-15 | S:99, P:87, M:23, A:14 | Línea de arranque, textual | 6.6 ✔ |
| R-16 | S:106, P:80, M:26, M:40, A:29, A:46 | "prueba sobre el archivo real… devuelve HECHO, HECHO CON DUDAS, BLOQUEADO o FALTA CONTEXTO… en 15 líneas o menos" | 6.6 · 6.10.1 ✔ |
| R-17 | S:107, P:81, A:40 | "actualiza 'Estado', 'Avance' y 'Qué no funcionó' en su propio encargo" | 6.9 ✔ |
| R-18 | S:108, P:93, M:41, A:40 | "Solo tú escribes `estado.md`, leyendo los encargos, en tres grupos" | 6.9 ✔ |
| R-19 | S:109, M:70-76, A:41 | "resuelve con el contrato y los datos maestros… si no, pasa el encargo a 'esperan tu decisión', detén los que dependen… relánzalo con el mismo modelo" | 6.9 ✔ (ver O3) |
| R-20 | S:115, P:111, M:96 | "lee `estado.md` y los encargos antes de confiar en lo que recuerdas" | 6.9 ✔ |
| R-21 | S:110, M:96 | "edita `datos-maestros.md`… avisa solo a esos mecánicos" | 6.9 ✔ |
| R-22 | S:111, M:66 | "ajuste pequeño y localizado… directo al mecánico" | 6.9 ✔ |
| R-23 | S:83, A (lectores):24 | "en L, `pit-lane:lector-ejecucion`; en XL, además… ingenuo y… crítico" | 6.3 · 6.2 ✔ |
| R-24 | S:123, M:90, A:30-33, arbitro:20, 25 | "Árbitro nuevo en cada ronda, sin el plan ni el razonamiento del constructor, sobre todo el listón, máximo 3 rondas" | 6.10.2, 6.10.6 · 4, C4-C5 ✔ |
| R-25 | S:124, M:91, A:34, arbitro:28 | "se reintenta una vez; si vuelve a fallar, se registra 'no ejecutado', nunca 'sin hallazgos'" | 6.10.4 ✔ |
| R-26 | S:125, M:92 | "modo degradado… el resumen empieza con AUDITORÍA NO INDEPENDIENTE" | 6.10.7 ✔ |
| R-27 | S:112, E:24-26, M:43, M:60, A:36 | "cambio de enfoque y un nivel más de modelo. En el modo A relanzas tú…; en el B le dices a Gerardo" | 6.7.3 ✔ |
| R-28 | S:126, A:37, arbitro:27 | "evidencia que el árbitro pueda abrir; 'fue intencional' no lo es" | 6.10.5 ✔ |
| R-29 | S:69, S:122, P:47, M:89 | "un criterio de coherencia por cada dato maestro que aparece en más de un entregable" | 6.10.3 ✔ |
| R-30 | S:113, M:27, A:42, `scripts/LEEME.md`:3, 32 | "80 % o más en la ventana de 5 horas, o Gerardo dice 'freno'… si el archivo no existe… el freno es solo manual" | 6.11 ✔ |
| R-31 | S:114, M:26 | "No leas entregables completos… Compacta solo al cambiar de fase y con `estado.md` ya escrito" | 6.11 ✔ |
| R-32 | S:131 | "rutas de los entregables, resumen de auditoría… y la lista 'revisa tú'" | 6.12 ✔ |
| R-33 | S:132 | "guardar, mejorar una existente, absorber en otra o descartar. Gerardo aprueba" | 6.12 ✔ |
| R-34 | S:82 | "código o una especificación de software… plugin Superpowers (código) o EGM (especificación)" | 6.13 ✔ |
| R-35 | S:70, S:127, P:48, A:35, arbitro:26 | "NO VERIFICABLE bloquea igual que un NO PASA, salvo… revisión humana" | 6.10.2 ✔ |
| R-36 | S:80, E:27 | "modelo distinto del constructor cuando el error es costoso y el constructor no es Opus; si el constructor es Opus, el árbitro también" | 6.7.4 ✔ |
| R-37 | S:100, M:25 | "No construyas entregables de L ni XL" | 6.4 ✔ |
| R-38 | S:96, E:22, E:41-46, M:37, M:54 | "comprueba que `CLAUDE_CODE_EFFORT_LEVEL`, `CLAUDE_CODE_SUBAGENT_MODEL` y `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` no estén fijadas… no las cambies" | 6.7.1 · 5 ✔ |
| R-39 | S:121, M:80-88, A:38-39 | "en M, tú; en L y XL, cada mecánico lanza `pit-lane:arbitro`… Tú lanzas la de coherencia y la de cualquier mecánico que devuelva 'auditoría: pendiente'" | 6.10.0 ✔ |

## L6 — marcadores `[CONFIRMAR]` fuera de `docs/`

| # | Archivo:línea | Texto |
|---|---|---|
| 1 | `AGENTS.md:41` | Regla de contenido 1: "si falta algo, se marca **[CONFIRMAR]**…". Es la definición del marcador, no un pendiente. Se lista por completitud. |
| 2 | `references/enrutamiento.md:29` | Regla 6 (la columna de esfuerzo es hipótesis): "El documento no asigna ID de la sección 6.14 a esta regla; queda sin ID." |
| 3 | `references/enrutamiento.md:31` | Regla 7 (plan Pro, Fable fuera): "Esta regla tampoco tiene ID en la sección 6.14." |
| 4 | `references/modos-de-ejecucion.md:100` | "El documento no define pasos concretos para los modos C y D; esta referencia solo recoge su fila de la tabla." |
| 5 | `references/plantillas.md:108` | Formato de `estado.md`: los campos de cada línea y el encabezado son una propuesta, no están en el documento. |

Los pendientes de Gerardo son los marcadores 2 a 5. Ninguno está registrado todavía en `docs/decisiones.md`; según el encargo, eso lo hace el paso 8.

---

## Observaciones fuera del listón (no bloquean)

- **O1 — R-07 extendido a los entregables.** Dónde: `agents/mecanico.md:25`, `agents/mecanico-experto.md:25` y `agents/mecanico-auxiliar.md:25`. Dicen: "Los datos compartidos se leen de `datos-maestros.md`; no los copies al entregable por tu cuenta (R-07)". R-07 se refiere a los **encargos** ("los encargos lo citan, no lo copian"). La sección 6.10.3 da por hecho que los datos maestros **sí** aparecen en los entregables, y por eso existe la auditoría de coherencia. "Por tu cuenta" atenúa el choque, pero un mecánico literal podría dejar fuera de un informe una cifra que debía incluir. Sugerencia: "no los copies a tu encargo ni los cambies; en el entregable, úsalos tal como están en `datos-maestros.md`".
- **O2 — ID mal asignado.** Dónde: línea 28 de los tres mecánicos: "Construye el entregable siguiendo las skills que indique el encargo (R-10)". R-10 es "un archivo por encargo, con la plantilla de 6.6". No contradice nada, pero la cita no corresponde a la instrucción. Sugerencia: quitar el ID o citar R-34 si se refiere a Superpowers o EGM.
- **O3 — Quién pasa un encargo a "esperan tu decisión".** Dónde: línea 41 de los tres mecánicos: el mecánico "deja 'Estado' en `espera decisión`". En 6.9 es el Jefe de pits quien primero intenta resolver y solo después pasa el encargo a "esperan tu decisión". Como `estado.md` se escribe leyendo los encargos (R-18), el encargo podría aparecer como "espera decisión" antes de que el Jefe de pits intente resolverlo. El texto añade "El Jefe de pits lo resuelve", así que no hay contradicción literal.
- **O4 — Tensión interna del diseño: lectores en XL.** La sección 7 fija `lector-critico` en sonnet/medium. La sección 6.7 dice "Lector del plan: Sonnet 5.5 (crítico en XL: Opus 5.5) · medio (alto en XL)". El lector crítico solo se usa en XL (R-23; su propio `description`), así que su frontmatter nunca coincide con su único uso y depende de que el despacho lo sobrescriba. Tampoco está claro si "alto en XL" aplica a los tres lectores o solo al crítico. `skills/pit-lane/SKILL.md:83` remite a `references/enrutamiento.md` para fijarlos, lo que lo cubre en la práctica. Esto lo decide Gerardo, no el paso 8.
- **O5 — Menciones de gauntlet sin prefijo en `references/`.** `references/plantillas.md:23` ("el contrato de gauntlet completo"), `references/plantillas.md:55` ("la bitácora de gauntlet") y `references/modos-de-ejecucion.md:92` ("modo degradado de gauntlet"). `references/` no es una skill ni un agente, así que queda fuera de L9 y de la regla 3 de `AGENTS.md`. Aun así, la skill remite a estos archivos, y conviene unificarlo con `pit-lane:gauntlet`.
- **O6 — `skills/pit-lane/SKILL.md:18`** dice "nunca la skill `gauntlet` sin prefijo". Esa mención sin prefijo es **correcta**: nombra la skill de cuenta (otra skill, sección 7, "Dos gauntlet cargadas") justamente para prohibirla. No cuenta como fallo de L9.
- **O7 — Decisiones no registradas.** `docs/decisiones.md` no tiene entradas. Hay al menos dos decisiones tomadas en los pasos 3 a 6 que no estaban escritas en el diseño: el modo A "por defecto" (`skills/pit-lane/SKILL.md:93`; el diseño marca A y B como v1 sin elegir uno) y el formato de las líneas de `estado.md` (marcador 5 de L6). `AGENTS.md`, "Cómo se hace un cambio", punto 4, pide registrarlas.
- **O8 — Interpretación de L9 aplicada.** Las palabras de rol con tilde ("árbitro", "mecánico", "lector") se tomaron como nombres de rol, no como nombres de agente (`arbitro`, `mecanico`…), igual que las usa la sección 6. Si Gerardo quiere que también cuenten, habría que revisar todos los agentes y la skill.
