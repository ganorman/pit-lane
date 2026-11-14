# Decisiones

Una decisión por línea, con fecha AAAA-MM-DD.

2026-11-13 · Corrección L9 (auditoría paso 7): `agents/arbitro.md:32` ahora nombra la skill como `pit-lane:gauntlet`, con prefijo.

2026-11-14 · Paso 10 · APROBADO por Gerardo · R-01: las fuentes externas suben a L, no a XL, salvo que el costo del error también sea alto (`skills/pit-lane/SKILL.md`). Contradice la fila "muchas o externas" de la sección 6.3 del diseño, que no se editó: queda por actualizar.
2026-11-14 · Paso 10 · APROBADO por Gerardo · R-39/H10: en modo A el Jefe de pits lanza siempre `pit-lane:arbitro`; en modo B lo siguen lanzando los mecánicos (`SKILL.md`, `references/modos-de-ejecucion.md`, `references/plantillas.md`, 3 agentes mecánico). Es la salida que prevé H10 en el diseño.
2026-11-14 · Paso 10 · APLICADO por recomendación delegada de Gerardo · `agents/arbitro.md` y plantilla de contrato: las fuentes externas llevan una comprobación ejecutable (curl o lista de Drive); sin ella, NO VERIFICABLE (R-35).
2026-11-14 · Paso 10 · NO APLICADO · verificación por tipo para prompts/instrucciones en `skills/gauntlet/`: es skill de Gerardo (regla 4 de AGENTS.md); queda como pendiente hasta su aprobación expresa.
2026-11-14 · Paso 10 · RESUELTO · Contradicción R-01 con la sección 6.3: se actualizó `docs/analisis-y-diseno.md` (fila de fuentes, excepción y descripción de L).
2026-11-14 · Paso 10 · APLICADO a pedido de Gerardo · R-30 (freno): el piloto reportó que `~/.claude/pit-lane-uso.json` no existía. El script funciona a mano, pero la status line no lo corre en la app de escritorio (H3 falla). El Jefe de pits lee el uso con `get_usage` de la app (probado: devuelve "5-hour limit" en %); el archivo queda como respaldo; si ninguno responde, freno manual. No hace falta un mod.

## Pendientes de Gerardo (marcadores [CONFIRMAR] del informe, L6)

2026-11-13 · PENDIENTE [CONFIRMAR] · `references/enrutamiento.md:29` · Regla 6 (la columna de esfuerzo es hipótesis): el documento no asigna ID de la sección 6.14 a esta regla; queda sin ID.
2026-11-13 · PENDIENTE [CONFIRMAR] · `references/enrutamiento.md:31` · Regla 7 (plan Pro, Fable fuera): tampoco tiene ID en la sección 6.14.
2026-11-13 · PENDIENTE [CONFIRMAR] · `references/modos-de-ejecucion.md:100` · El documento no define pasos concretos para los modos C y D; la referencia solo recoge su fila de la tabla.
2026-11-13 · PENDIENTE [CONFIRMAR] · `references/plantillas.md:108` · Formato de `estado.md`: los campos de cada línea y el encabezado son una propuesta, no están en el documento.
