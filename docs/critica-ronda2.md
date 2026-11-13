## Informe del crítico — Ronda 2
**Veredicto global:** APROBADO CON CORRECCIONES. No quedan bloqueos. Hay 4 hallazgos mayores, todos de integración entre la skill, gauntlet, el plugin y el plan. Se corrigen editando texto y no obligan a rediseñar.

### Fallos de la ronda 1
| Hallazgo | Estado | Evidencia |
|---|---|---|
| Paso 5 no dice de dónde copiar gauntlet | CORREGIDO | 434, 446: el zip trae `skills/gauntlet/` |
| Nadie instala el plugin | CORREGIDO | 442, 486 (ver hallazgo nuevo 3) |
| Orden 7→8→9 | CORREGIDO | 441-444 |
| Listón del paso 7 falla por construcción | CORREGIDO en sus 3 causas | `LEEME.md` en 412; `decisiones.md` en el paso 1 (435); IDs R-xx (341-378). Aparecen causas nuevas (hallazgo 4) |
| "Escriben en carpetas distintas" | CORREGIDO | Superficies por archivo (450-460); `arbitro.md` ya viene en el zip |
| Paso 1 se contradice | CORREGIDO | 465 |
| ECC sí define esfuerzo | CORREGIDO | 19, 74, 261 |
| Precedencia de `CLAUDE_CODE_EFFORT_LEVEL` | CORREGIDO | 125, 257, 474, H8 |
| Falta C7 | CORREGIDO | 102 |
| Contrato sin MÉTODO; conteo de añadidos | CORREGIDO | 205; los ✚ son 5, igual que el texto (199) |
| Obrera bloqueada sin flujo | CORREGIDO | 299, R-19 |
| La Reina no se entera del cierre | CORREGIDO | 297-298, 127 |
| El modo B no cumple R5 | CORREGIDO | 272-275 |
| M: "una auditoría"; PLAN solo L y XL | CORREGIDO | 177, 212 |
| Escalada sin dueño en el modo B | CORREGIDO | 259 |
| Modo degradado | CORREGIDO | 309 |
| Fila 1: Superpowers también clasifica tamaño | CORREGIDO | 67; `SP:…brainstorming/SKILL.md:22-24` y `:209-224` comprobadas |
| Paso con "Sonnet, bajo" | CORREGIDO | Tabla 432-444. Queda un resto en H2 (501): ver hallazgo 9 |
| Fechas de C1 y C4 | CORREGIDO | 96, 99 citan `memoria/MEMORIA.md` (no se audita) |
| "9 pasos" | CORREGIDO | 22: "11 pasos (del 0 al 10)" |
| Anillo de uso | CORREGIDO | 115, fuente nueva (ver disputa) |

Las dos citas con problema de la ronda 1 también quedaron bien: C1 (`fichas/02-egm.md:30`) y la fila 13 (`santa-method:79-82`, `:126-128`).

### Disputa
**Anillo de uso: a favor del autor.** La página desktop, sección "Check usage", dice: "Both layouts have the usage ring next to the model picker. Click it to see your plan usage, which is shared across all your Claude Code surfaces." La línea 115 queda bien sustentada.

### Citas nuevas o cambiadas
Todas correctas:
- C7: `the-longform-guide.md:124`, `performance.md:18` y `SP:…subagent-driven-development/SKILL.md:164-170`.
- Fila 8: `performance.md:48-49`, `token-optimization.md:35`. Sección 5: `token-optimization.md:14-19`.
- Documentación oficial: `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` (v2.1.257), `notify_when_idle` (v2.1.236), valores por defecto y límite de Projects, `rate_limits`.
- R-09 coincide con `SP:executing-plans/SKILL.md:39-43`.

### Hallazgos nuevos

**1. [MAYOR] 6.2, 6.4, 6.9 y pasos 2 y 6 · Nadie es dueño de F5 y la bitácora es compartida.**
- **Qué hay:** ningún rol lanza la auditoría. La 6.4 no se la asigna ni a la Reina ni a la obrera. Las tres cosas siguientes chocan:
  - La 6.9 prevé un solo `colmena/auditoria-gauntlet.md` por trabajo.
  - En L, la auditoría va por entregable (178).
  - Gauntlet escribe la bitácora "junto al entregable" (`gauntlet/SKILL.md:104`).
- **Por qué importa:** si cada obrera corre su loop, varias escriben el mismo archivo y eso viola R-11. El paso 6 tendrá que decidir algo que el diseño no decidió.
- **Corrección:**
  - En la 6.4, que la obrera corra su loop gauntlet y el árbitro lo lance ella.
  - Una bitácora por encargo: `colmena/auditorias/E0x.md`, dentro de su superficie de escritura.
  - La Reina lanza solo la auditoría de coherencia.

**2. [MAYOR] 6.7, 7 y paso 2 · El enrutamiento del árbitro no está conectado.**
- **Qué hay:** gauntlet lanza "un subagente árbitro nuevo" sin modelo ni esfuerzo (`gauntlet/SKILL.md:70`). Los dos ajustes del paso 2 (468) no tocan eso, y el paso 6 solo "remite a skills/gauntlet para la auditoría (F5)" (480).
- **Consecuencias:**
  - El árbitro hereda el modelo de quien lo lanza. Eso viola R-12 y las filas 253-254 (Opus alto o Sonnet medio).
  - `agents/arbitro.md` (405) no lo usa nadie.
- **Corrección:** un tercer ajuste en el paso 2: "si hay contrato de colmena, lanza el árbitro como agente `colmena:arbitro`, con el modelo y el esfuerzo que fija el contrato". Ajustar L8 a "tres ajustes".

**3. [MAYOR] 7, pasos 6, 8 y 9 · Nombres con el prefijo del plugin y gauntlet duplicado.**
- **Qué dice la documentación:** en un plugin, skills y agentes llevan el nombre del plugin como prefijo ("Claude sees `reviewer` and `my-plugin:reviewer` as two subagents", página plugins/create).
- **Qué falla:**
  - El paso 6 manda nombrar los agentes "exactamente como en la sección 7" (`obrera`), pero una vez instalados se llaman `colmena:obrera`.
  - La alternativa del paso 8 (copiar a `~/.claude/skills/`) convierte la skill en `/colmena`, y el paso 9 invoca `/colmena:colmena`.
  - Quedan cargadas dos gauntlet: la de cuenta, sin cambios, y `colmena:gauntlet`. Si la Reina usa la de cuenta, la Fase 0 pide una segunda aprobación y se viola R-08.
  - "Develop without a marketplace" ofrece `--plugin-dir` (una sesión, solo terminal), `CLAUDE_CODE_PLUGIN_DIRS` o un plugin en `~/.claude/skills/`. Instalarlo de forma persistente por marketplace exige `marketplace.json`, que no está en la sección 7 ni en la superficie del paso 8.
- **Corrección:**
  - Usar los nombres con prefijo en la sección 7 y en el paso 6.
  - Fijar una sola vía de instalación: carpeta del repo como plugin en `~/.claude/skills/colmena/`, o `CLAUDE_CODE_PLUGIN_DIRS` en la configuración de usuario.
  - El paso 9 debe usar el nombre que resulte de esa vía.
  - Añadir a la sección 10 la decisión de retirar o desactivar la gauntlet de cuenta.

**4. [MAYOR] Paso 7 · El listón sigue fallando por construcción.**
- **L7 con el paso 1:** el texto de la licencia MIT está en inglés y no se debe traducir, pero L7 exige que todo lo escrito en los pasos 1 a 6 esté en español. El paso 8 "corregiría" la licencia.
- **L1 con el paso 4:** "Pruébalo" (474) escribe `colmena/uso.json` en el directorio de arranque, que es el repo (`workspace.project_dir`). Eso deja un archivo fuera de la sección 7.
- **Corrección:**
  - L7: excluir `LICENSE`, `NOTICE` y las claves de JSON y frontmatter.
  - Paso 4: probar con un JSON de ejemplo en una carpeta temporal y borrar lo generado. Otra opción: añadir `colmena/` a `.gitignore` y que L1 ignore lo ignorado.

**5. [MENOR] 6.14 (341) · "Cada regla del diseño tiene un ID" es falso.** Faltan IDs para:
- NO VERIFICABLE bloquea (304);
- árbitro en modelo distinto (260);
- la Reina no construye L ni XL (186);
- comprobar las variables de entorno antes del primer despacho (257).

Además, R-24 cita la 6.10, pero "todo el listón" está en C5 (100). Hay que añadir R-35 a R-38, o matizar la frase.

**6. [MENOR] Paso 1 · Haiku tiene que interpretar.** El README "que diga qué es el sistema" (465) obliga a resumir 533 líneas, y eso choca con R-13. **Corrección:** dar el texto del README en el encargo, o pasar el paso a Sonnet medio.

**7. [MENOR] Oleada A · El índice de git es compartido.** "Pueden correr a la vez porque sus superficies son archivos distintos" (448) no cuenta con `.git/index`. Tres commits a la vez pueden barrer archivos ajenos o chocar con `index.lock`. **Corrección:** en cada encargo, "`git add` solo de tu superficie; si hay `index.lock`, espera y reintenta".

**8. [MENOR] 6.11 y 6.9 · `uso.json` no cae donde la Reina lo busca.** La status line escribe relativo a `workspace.project_dir`, y la 6.9 pone `colmena/` dentro de `proyectos/<área>/AAAA-MM-DD_Tema/`. **Corrección:** una ruta fija común, por ejemplo `~/.claude/colmena-uso.json`.

**9. [MENOR] Precisiones.**
- La 6.5 no tiene una marca de aprobación, y el ajuste 1 del paso 2 exige un contrato "aprobado". Añadir la línea `Aprobado: AAAA-MM-DD`.
- En 125: `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` sola también anula el modelo, porque los subagentes pasan a correr con el modelo principal.
- H2 propone "Sonnet, esfuerzo bajo", que no está en la tabla 6.7.

### Cobertura R1–R8
| Requisito | Veredicto | Sección |
|---|---|---|
| R1 Evaluación comparativa | CUMPLE | 2, 3, 4 |
| R2 Metodología única con gauntlet | CUMPLE (falta definir quién es dueño de F5, hallazgo 1) | 6.1–6.14 |
| R3 Reina capaz con esfuerzo alto | CUMPLE | 6.4, 6.7 |
| R4 Modelo y esfuerzo por tarea | CUMPLE | 6.6, 6.7 |
| R5 Despacho colmena con los modelos sugeridos | CUMPLE A MEDIAS: el árbitro sale sin el modelo del plan (hallazgo 2); el modo B está declarado como semiautomático | 6.8, 6.10 |
| R6 Estructura del repo | CUMPLE (nombres con prefijo, hallazgo 3) | 7 |
| R7 Plan paso a paso con encargos | CUMPLE A MEDIAS: el listón del paso 7 falla por construcción; la vía de instalación y los nombres están sin fijar | 8 |
| R8 Preferencias permanentes | CUMPLE | 6.1, 6.14, 7, 10 |
