## Informe del crítico — Ronda 1
**Veredicto global:** RECHAZADO (se puede corregir en una ronda: el diseño se sostiene; lo que falla es el plan de construcción y algunos datos)

### Citas comprobadas
28 comprobadas · 26 correctas · 2 con problema

Comprobé las 20 citas explícitas del documento y 8 más que respaldan celdas de las tablas: `SP:skills/using-superpowers/references/claude-code-tools.md:18-22`, `SP:…/fix-loop.md:20-34`, `SP:skills/executing-plans/SKILL.md:55-58`, `SP:skills/brainstorming/SKILL.md:106`, `ECC:the-longform-guide.md:116-127`, `ECC:rules/common/performance.md:48-50`, `ECC:docs/token-optimization.md:19,35`, `ECC:skills/santa-method/SKILL.md:179,204`.

Citas con problema:
1. `EGM:docs/getting_started.md:71-73` (C1). La línea dice que `/egm-review` "will provide *a lot* of feedback by design. Take what you think is relevant". Habla de **volumen de hallazgos**, no de **paradas**. No respalda que "las ≈20 paradas" sean un costo que EGM reconozca.
2. `ECC:skills/santa-method/SKILL.md:79-82` (sección 2 y fila 13). Esas líneas sostienen el aislamiento y que la rúbrica es la misma para los dos revisores. Que la rúbrica sea binaria está en `:101-102` y `:128`. El dato es cierto, pero la línea está desfasada.

Gauntlet (SKILL.md, arbitro.md, plantillas.md, verificacion-por-tipo.md con 11 tipos), la versión de Superpowers del usuario (128 líneas) y la Colmena coinciden con lo que afirma el documento.

### Hallazgos

**[BLOQUEO] Sección 8, Paso 5 · No dice de dónde copiar gauntlet.** El encargo pide "Copia mi skill de cuenta `gauntlet`", pero en el PC personal un chat nuevo de Claude Code solo tiene el repo. Las skills de cuenta están sincronizadas en una ruta interna (`~/.claude/skills/synced/<uuid>/gauntlet/`) que el encargo no da y el paso 0 no copia. Sin esa ruta, el chat tiene que buscarla o inventarla. **Corrección:** en el paso 0, que Gerardo descargue la carpeta `gauntlet/` a `entrada/gauntlet/` (o a una ruta fija), y que el encargo del paso 5 cite esa ruta.

**[BLOQUEO] Sección 8, Paso 8 · Nadie instala el plugin.** El paso 8 dice "Usa la skill `colmena`", pero ningún paso instala `.claude-plugin/plugin.json` en Claude Code ni enlaza `skills/` a `~/.claude/skills`. Además, el paso 1 crea `plugin.json` sin marketplace. **Corrección:** añadir un paso 7b (lo hace Gerardo, o Haiku con esfuerzo bajo) con el comando exacto de instalación local y una prueba de que la skill aparece.

**[MAYOR] Sección 8, orden de los pasos 7, 8 y 9.** El piloto (8) corre sobre el repo sin las correcciones de la auditoría (7), porque esas correcciones se aplican recién en el 9. Así el piloto mide errores que ya se conocían. **Corrección:** aplicar las correcciones del paso 7 antes del 8 (paso 7b), y dejar el 9 solo para lo que salga del piloto.

**[MAYOR] Sección 8, el listón del paso 7 falla por construcción.**
- L1 ("ningún archivo de más") choca con `scripts/LEEME.md`, que crea el paso 6 y no figura en la sección 7.
- L6 exige `docs/decisiones.md`, que recién se crea en el paso 9.
- L2 ("cada regla de 6.1 a 6.12") no es binario mientras no exista la lista de reglas.

**Corrección:** añadir `LEEME.md` a la sección 7 (o meterlo en `modos-de-ejecucion.md`), crear `decisiones.md` en el paso 1, y numerar las reglas de 6.x (R1…Rn) para que L2 sea un conteo.

**[MAYOR] Sección 8, "escriben en carpetas distintas" es falso.**
- El paso 5 escribe `references/verificacion-por-tipo.md`, mientras el paso 2 declara "solo `references/`".
- El paso 5 escribe `scripts/verificar_office.py` y el paso 6 escribe en "solo `scripts/`".
- El paso 4 depende de `skills/gauntlet/agents/arbitro.md` "si ya existe", que lo crea el paso 5, que corre en paralelo: el resultado depende de cuál termine primero.

Los archivos son distintos, así que el choque real es pequeño, pero la regla 6.1-6 se mide por superficie declarada. **Corrección:** declarar superficies por archivo, y poner el paso 4 después del 5 (o darle a 4 la ruta de origen de `arbitro.md`).

**[MAYOR] Sección 8, el paso 1 se contradice.** Pide "Crea exactamente esa estructura de carpetas" y también "ni carpetas vacías". **Corrección:** que cada paso cree sus propias carpetas.

**[MAYOR] Resumen punto 3, fila 8 y regla 6.7-5 · "Ninguna fuente define esfuerzo" es falso para ECC.**
- `ECC:rules/common/performance.md:48-49` manda "For complex tasks requiring deep reasoning: Choose a higher supported effort level, such as `/effort high`".
- `ECC:docs/token-optimization.md:11,35` recomienda `medium` por defecto, "Adjust it for task complexity".

Es una regla gruesa, pero existe, y coincide con la tabla 6.7. **Corrección:** fila 8, columna ECC: "medium por defecto, high para razonamiento profundo"; más fuerte: ECC (parcial). En 6.7, citar ECC como origen; la parte propia es solo el desglose por rol.

**[MAYOR] Sección 5, "se puede imponer por configuración" omite una precedencia.** La doc oficial (sub-agents, "Choose an effort level") dice que `CLAUDE_CODE_EFFORT_LEVEL` "takes precedence over both" (el parámetro por invocación y el campo `effort`). Y ECC recomienda justamente fijar esa variable en `settings.json` (`ECC:docs/token-optimization.md:19`). Si está fijada, toda la columna de esfuerzo se ignora sin aviso. **Corrección:** decirlo en la sección 5 y en la regla 6.7-1, y que el paso 6 o el piloto verifique que la variable no está definida.

**[MAYOR] Sección 4 · Contradicción que el documento no vio: el modelo para documentos y análisis.**
- ECC asigna "Writing docs → Haiku" (`ECC:the-longform-guide.md:124`) y "Research and analysis → Opus" (`ECC:rules/common/performance.md:18`).
- El diseño manda redactar y analizar a Sonnet, con la regla de Superpowers de un piso de gama media para trabajo en prosa (`SP:skills/subagent-driven-development/SKILL.md:166-167`).

Para un usuario cuyo trabajo principal son documentos, este es el conflicto de enrutamiento más relevante. **Corrección:** añadir C7 con la resolución (Superpowers gana porque el turn count pesa más que el precio del token, `:164-170`) y su porqué.

**[MAYOR] Sección 6.5 · La plantilla de contrato pierde el bloque MÉTODO de gauntlet.** La plantilla original (`gauntlet/references/plantillas.md:15-20,31`) incluye las rutas de las **fuentes**, las skills que se usan, el modo del árbitro y los criterios de "revisión humana". En la 6.5 no hay un campo para las fuentes, y la 6.10-2 depende de pasárselas al árbitro. El paso 5 hace que gauntlet tome `colmena/contrato.md` como su contrato, así que heredaría ese hueco. Además, el texto dice "cuatro bloques añadidos" y marca cinco con ✚. **Corrección:** conservar MÉTODO (fuentes, skills, modo del árbitro, revisión humana) y corregir el conteo.

**[MAYOR] Sección 6, la obrera bloqueada no tiene flujo.** Los estados BLOQUEADA y FALTA CONTEXTO existen (6.6), pero no se dice:
- quién atiende el bloqueo;
- si cuenta como "espera tu decisión" en `estado.md`;
- si frena la oleada o los encargos que dependen de ella;
- con qué modelo se relanza.

**Corrección:** una regla en 6.9: la Reina resuelve con los datos maestros si puede; si no, pasa el encargo a "espera tu decisión", lo detiene junto con los que dependen de él, y la siguiente oleada sigue con los independientes.

**[MAYOR] Secciones 6.8 y 6.9, la Reina no se entera de que una obrera en sesión aparte terminó.**
- En el modo B nada avisa a la Reina, y `estado.md` "solo lo escribe la Reina".
- No está dicho quién actualiza el campo "Estado" del encargo.

La doc oficial ofrece el mecanismo: `SendMessage` con `notify_when_idle`, un aviso cuando la otra sesión queda inactiva, en sesiones de la misma máquina, desde v2.1.236 (página cross-session-messaging, "Get a notice when another session goes idle"). **Corrección:**
- La obrera actualiza "Estado" y "Avance" en su encargo.
- La Reina se suscribe con `notify_when_idle` a cada obrera.
- Respaldo: la Reina lee los encargos cuando Gerardo pide estado.

**[MAYOR] Sección 6.8, el modo B no cumple del todo R5.** En el modo B despacha Gerardo, y "Es lo que pediste" no es cierto: R5 pide que se despache tras la aprobación. Agent view confirma que el despacho de sesiones lo inicia el usuario; Projects es el único modo donde Claude inicia hilos. **Corrección:** decirlo con franqueza: el modo A cumple R5; el modo B es semiautomático; el modo C es el que encaja con R5 si la cuenta lo tiene (H7).

**[MENOR] Tabla 6.3, tamaño M · "una auditoría" es ambiguo.** No queda claro si es una ronda o el loop de hasta 3, ni con qué árbitro. **Corrección:** "loop gauntlet de hasta 3 rondas, árbitro de rutina (Sonnet, medio)". Además, la 6.5 hace obligatorio el bloque PLAN, que en M no aplica: debe marcarse "solo L y XL".

**[MENOR] Regla 6.7-3 · La escalada no tiene dueño en el modo B.** Allí el modelo lo fija el selector de la sesión. Hay que decir que la Reina indica a Gerardo el nuevo modelo, o que relanza el encargo en modo A.

**[MENOR] 6.10 · No se menciona el modo degradado de gauntlet** ("AUDITORÍA NO INDEPENDIENTE", `gauntlet/SKILL.md:90-92`), aunque la 6.8 dice que el modo A "funciona también en el chat", donde puede no haber subagentes.

**[MENOR] Fila 1 de la matriz · Superpowers también clasifica tamaño.** Lo hace en "Size the Work": cambio pequeño o proyecto, vetable, y sube de tamaño si la tarea crece (`SP:skills/brainstorming/SKILL.md:209-224`). Hay que mencionarlo; ECC sigue siendo el más fuerte.

**[MENOR] Paso 5 · Esfuerzo no previsto en 6.7.** "Sonnet, bajo" no figura en la tabla 6.7. O es mecánico (Haiku) o requiere juicio (Sonnet, medio).

**[MENOR] Datos sin respaldo.**
- C1 y C4: "tu decisión del 7 de noviembre" y "del 14 de octubre" no se pueden comprobar con las fuentes entregadas; citar la ruta y la línea, o marcar [CONFIRMAR].
- Resumen, punto 6: dice "9 pasos" y la tabla tiene 10 (del 0 al 9).
- Sección 5: la página de status line no menciona la app de escritorio, así que "se ve en el anillo de uso de la app" no tiene sustento ahí.

### Cobertura R1–R8
| Requisito | Veredicto | Sección |
|---|---|---|
| R1 Evaluación comparativa | CUMPLE A MEDIAS: un dato falso sobre esfuerzo y una contradicción de modelos sin ver | 2, 3, 4 |
| R2 Metodología única con gauntlet | CUMPLE | 6.1–6.12, F5 |
| R3 Agente cabeza capaz, esfuerzo alto | CUMPLE | 6.4, 6.7 |
| R4 Modelo y esfuerzo por tarea | CUMPLE (el esfuerzo es hipótesis declarada y la anula `CLAUDE_CODE_EFFORT_LEVEL`) | 6.6, 6.7 |
| R5 Despacho colmena tras aprobación | CUMPLE A MEDIAS: el modo A sí; el modo B lo despacha Gerardo y sin aviso de cierre | 6.8, 6.9 |
| R6 Estructura de repo | CUMPLE (falta `LEEME.md`) | 7 |
| R7 Plan paso a paso con encargos | CUMPLE A MEDIAS: pasos 5 y 8 no ejecutables, orden 7→8→9, choques de superficie | 8 |
| R8 Preferencias permanentes | CUMPLE: XL lleva dos aprobaciones, pero se somete a decisión en 10.3 | 6.2, 7, 10 |

### Lo que está bien (máximo 5 líneas, solo lo que comprobé)
- Las citas de Superpowers sobre selección de modelo, ledger, cuatro causas de parada, informe en menos de 15 líneas y prohibición de ejecutores en paralelo son exactas.
- Las de ECC sobre el clasificador "el nivel más alto gana", superficies de escritura, "What Did NOT Work", Save/Improve/Absorb/Drop, compactación por fase y santa (3 rondas, revisores frescos) son exactas.
- Las de EGM sobre parafrasear primero, reglas de disputa, convergencia (dos rondas limpias, tope 5) y "revisor no ejecutado = ronda no limpia" son exactas.
- Gauntlet y Colmena están descritos con fidelidad a sus archivos.
- Sección 5: `model`, `effort`, v2.1.292, anidación de 3 niveles, v2.1.234 en Windows, WSL y Windows aislados entre sí, y `rate_limits`: todo confirmado en la doc oficial.
