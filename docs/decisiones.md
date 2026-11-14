# Decisiones

Una decisión por línea, con fecha AAAA-MM-DD.

2026-11-13 · Corrección L9 (auditoría paso 7): `agents/arbitro.md:32` ahora nombra la skill como `pit-lane:gauntlet`, con prefijo.

2026-11-14 · Paso 10 · APROBADO por Gerardo · R-01: las fuentes externas suben a L, no a XL, salvo que el costo del error también sea alto (`skills/pit-lane/SKILL.md`). Contradecía la fila "muchas o externas" de la sección 6.3 del diseño; ya actualizada (ver la línea RESUELTO).
2026-11-14 · Paso 10 · APROBADO por Gerardo · R-39/H10: en modo A el Jefe de pits lanza siempre `pit-lane:arbitro`; en modo B lo siguen lanzando los mecánicos (`SKILL.md`, `references/modos-de-ejecucion.md`, `references/plantillas.md`, 3 agentes mecánico). Es la salida que prevé H10 en el diseño.
2026-11-14 · Paso 10 · APLICADO por recomendación delegada de Gerardo · `agents/arbitro.md` y plantilla de contrato: las fuentes externas llevan una comprobación ejecutable (curl o lista de Drive); sin ella, NO VERIFICABLE (R-35).
2026-11-14 · Paso 10 · RESUELTO · Contradicción R-01 con la sección 6.3: se actualizó `docs/analisis-y-diseno.md` (fila de fuentes, excepción y descripción de L).
2026-11-14 · Paso 10 · APLICADO a pedido de Gerardo · R-30 (freno): el piloto reportó que `~/.claude/pit-lane-uso.json` no existía. El script funciona a mano, pero la status line no lo corre en la app de escritorio (H3 falla). El Jefe de pits lee el uso con `get_usage` de la app (probado: devuelve "5-hour limit" en %); el archivo queda como respaldo; si ninguno responde, freno manual. No hace falta un mod.

2026-11-14 · Paso 10 · APROBADO por Gerardo · Plantilla de contrato (`references/plantillas.md` y sección 6.5 del diseño): se añaden INSTRUCCIONES ORIGINALES (literales, numeradas) y un criterio de completitud para que corregir no recorte lo pedido. Son dos añadidos ✚ más (siete en total).
2026-11-14 · Paso 10 · APLICADO · Mejoras a `skills/gauntlet/`: Gerardo las aprobó y se aplicaron en un chat aparte (ver las cinco líneas "APROBADO por Gerardo · gauntlet" siguientes). Reemplaza la línea "NO APLICADO" de verificación por tipo para prompts.
2026-11-14 · APROBADO por Gerardo · gauntlet · Verificación por tipo "instrucciones o prompts": §12 nueva en `references/verificacion-por-tipo.md` (repaso en orden de ejecución; un criterio que nunca puede pasar es fallo del entregable) y mención en `SKILL.md`.
2026-11-14 · APROBADO por Gerardo · gauntlet · Pasabilidad del listón: `SKILL.md`, Fase 0 paso 4; cada criterio debe poder pasar con lo que existirá al auditar, o se corrige o elimina antes de pedir aprobación.
2026-11-14 · APROBADO por Gerardo · gauntlet · Instrucciones originales y completitud: `SKILL.md`, Fase 0 (paso 3 y paso 4); el pedido va literal y numerado (P1, P2…) y el listón lleva criterio de completitud. Gerardo aprobó después añadirlo también a `skills/gauntlet/references/plantillas.md` (sección INSTRUCCIONES ORIGINALES, fila de completitud, línea de veto y un ejemplo de criterio).
2026-11-14 · APROBADO por Gerardo · gauntlet · Protección contra recorte al corregir: `SKILL.md` (Reglas del loop) y `agents/arbitro.md` (Límites); el árbitro reporta contenido desaparecido como observación fuera del listón, sin bloquear.
2026-11-14 · APROBADO por Gerardo · gauntlet · Fuentes externas verificables: `SKILL.md` (Fase 0 paso 4) y `agents/arbitro.md` (Cómo auditas, paso 3); sin comprobación ejecutable (curl o lista de Drive), NO VERIFICABLE.

## Cierre del paso 10: respuestas de Gerardo a la sección 10 del diseño y a "Revisa tú"

2026-11-14 · CONFIRMADO por Gerardo · Decisiones 2, 3 y 4 de la sección 10: dos skills, aprobación en dos tiempos solo para XL, modos A y B en la v1 (C a evaluar, D fuera). Decisión 1 y 5 ya estaban cerradas (plan Pro verificado con `get_usage`).
2026-11-14 · Decisión 6 · Gerardo reemplaza a mano su gauntlet de cuenta, en otro chat, con la versión ajustada de este repo. No es trabajo de Pit Lane.
2026-11-14 · RH1 y RH2 · Gerardo confirma que el flujo encaja con su día a día y que el costo le sirve.
2026-11-14 · RH3 · La tablet queda DESCARTADA. El equipo "Mi Portátil" de Drive no es su laptop actual. Consecuencia: en D1 y D2 (proyecto Cerebro) los pasos de la tablet y el prompt 10 de la tablet ya no aplican, y con ellos los pendientes "la tablet sube sin pull" y "sesión en la nube sube a main".

## Marcadores [CONFIRMAR] del informe (L6): los cuatro confirmados por Gerardo

2026-11-14 · CONFIRMADO por Gerardo · `references/enrutamiento.md:29` · Regla 6 (la columna de esfuerzo es hipótesis): queda sin ID; es una nota de calibración, no una regla de comportamiento.
2026-11-14 · CONFIRMADO por Gerardo · `references/enrutamiento.md:31` · Regla 7 (plan Pro, Fable fuera): "Fable va fuera". Sigue sin ID en la sección 6.14; queda como regla de enrutamiento confirmada.
2026-11-14 · CONFIRMADO por Gerardo · `references/modos-de-ejecucion.md:100` · Modos C y D: sin pasos definidos; el C queda por evaluar (H7) y el D está fuera de la v1.
2026-11-14 · CONFIRMADO por Gerardo · `references/plantillas.md:108` · Formato de `estado.md`: se acepta la propuesta tal cual (funcionó en todo el piloto).
