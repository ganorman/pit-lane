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

2026-11-14 · APROBADO por Gerardo · gauntlet V2.1 · Plantilla de contrato de gauntlet: la línea "Árbitro:" de MÉTODO declara modelo y esfuerzo (antes solo el modo); cubre el tamaño M y la gauntlet de la cuenta.
2026-11-14 · APROBADO por Gerardo · gauntlet V2.1 · Árbitro por defecto: opus · high si el entregable sale a terceros, se proyecta en público o es difícil de revertir; sonnet · medium en el resto. Reemplaza "cuando el error es costoso" en `skills/gauntlet/SKILL.md`, `references/plantillas.md` (encargo) y sección 6.6 del diseño.
2026-11-14 · APROBADO por Gerardo · gauntlet V2.1 · Descripción de gauntlet: el trabajo con varios entregables remite a `pit-lane:pit-lane` (si es código, superpowers).
2026-11-14 · APROBADO por Gerardo · gauntlet V2.1 · Fuentes externas: la comprobación puede ser curl o WebFetch, según las herramientas del árbitro; los adjuntos largos se citan por nombre o ruta en INSTRUCCIONES ORIGINALES, no se copian.
2026-11-14 · APROBADO por Gerardo · V2.1 · Contrato de Pit Lane (`references/plantillas.md` y sección 6.5): el LISTÓN incluye la pasabilidad de gauntlet; el encargo (sección 6.6) exige que "Listón aplicable" incluya los IDs B que apliquen. Cierra el hueco que dejaba omitir la Fase 0 de gauntlet.
2026-11-14 · APROBADO por Gerardo · V2.1 · `agents/lector-ejecucion.md`: instrucción 4, pasabilidad de cada criterio e IDs B por encargo (bajo R-23).
2026-11-14 · APROBADO por Gerardo · V2.1 · AGENTS.md regla 4: `skills/gauntlet/` es la única fuente de gauntlet; la copia de la cuenta de claude.ai se exporta desde aquí y reemplaza la V1.

2026-11-14 · Corrección tras revisar V2.1 · `agents/lector-ejecucion.md`: la descripción del frontmatter va entre comillas porque `claude plugin validate` fallaba al parsearla (contiene ": "). Sin cambio de contenido.

2026-11-14 · APROBADO por Gerardo · paso 11b · `agents/*.md`: `description` del frontmatter entre comillas en los 7 agentes; el `: ` sin comillas rompía el parseo YAML en `claude plugin validate` (con el error, el agente cargaría sin `model` ni `effort`). Validación: pasa.

## Cierre del paso 10: respuestas de Gerardo a la sección 10 del diseño y a "Revisa tú"

2026-11-14 · CONFIRMADO por Gerardo · Decisiones 2, 3 y 4 de la sección 10: dos skills, aprobación en dos tiempos solo para XL, modos A y B en la v1 (C a evaluar, D fuera). Decisión 1 y 5 ya estaban cerradas (plan Pro verificado con `get_usage`).
2026-11-14 · Decisión 6 · Gerardo reemplaza a mano su gauntlet de cuenta, en otro chat, con la versión ajustada de este repo. No es trabajo de Pit Lane.
2026-11-14 · RH1 y RH2 · Gerardo confirma que el flujo encaja con su día a día y que el costo le sirve.
2026-11-14 · RH3 · La tablet queda DESCARTADA. El equipo "Mi Portátil" de Drive no es su laptop actual. Consecuencia: en D1 y D2 (proyecto Cerebro) los pasos de la tablet y el prompt 10 de la tablet ya no aplican, y con ellos los pendientes "la tablet sube sin pull" y "sesión en la nube sube a main".

## Marcadores [CONFIRMAR] del informe (L6): los cuatro confirmados por Gerardo

2026-11-14 · CONFIRMADO por Gerardo · `references/enrutamiento.md`, Reglas, punto 6 · Regla 6 (la columna de esfuerzo es hipótesis): queda sin ID; es una nota de calibración, no una regla de comportamiento.
2026-11-14 · CONFIRMADO por Gerardo · `references/enrutamiento.md`, Reglas, punto 7 · Regla 7 (plan Pro, Fable fuera): "Fable va fuera". Sigue sin ID en la sección 6.14; queda como regla de enrutamiento confirmada.
2026-11-14 · CONFIRMADO por Gerardo · `references/modos-de-ejecucion.md`, sección "Modos C y D" · Modos C y D: sin pasos definidos; el C queda por evaluar (H7) y el D está fuera de la v1.
2026-11-14 · CONFIRMADO por Gerardo · `references/plantillas.md`, sección 3 · Formato de `estado.md`: se acepta la propuesta tal cual (funcionó en todo el piloto).

2026-11-14 · Manual de uso en `docs/manual-de-uso.md`, pedido por Gerardo. Documento nuevo fuera del contrato de AGENTS.md, solo para lectura; se versiona con la revisión integral (ver abajo).

## Revisión integral del repo (2026-11-14): 14 hallazgos, todos aprobados por Gerardo ("Sí, todas")

2026-11-14 · APROBADO por Gerardo · gauntlet · `skills/gauntlet/scripts/verificar_office.py`: la salida se fuerza a UTF-8. En Windows, con la salida redirigida (como la corre el árbitro), el "⚠" de las alertas rompía el script con UnicodeEncodeError, salida 1 y ALERTAS vacía. Probado con un DOCX con "PVDC" y en-US: antes se caía, ahora reporta las 3 alertas.
2026-11-14 · APROBADO por Gerardo · gauntlet · `verificar_office.py`: un tipo no soportado, o un PDF sin `--render`, ahora deja una alerta en vez de "ninguna"; un XLSX sin `xl/workbook.xml` ya no se cae y lo avisa; las diapositivas o notas ilegibles se saltan.
2026-11-14 · APROBADO por Gerardo · Diseño 6.4 (fila Mecánico), 6.10 (paso 0) y 6.14 (R-39) alineados con la decisión R-39/H10 ya aprobada: en modo A el Jefe de pits lanza los árbitros; en modo B, el mecánico. Se corrige la errata "lanzal Jefe".
2026-11-14 · APROBADO por Gerardo · `references/modos-de-ejecucion.md`: pasos 5 y 6 del modo A sin repetición; el modo B y la tabla de R-39 dicen que el árbitro usa la línea "Árbitro:" del encargo (no el modelo del mecánico, R-36); se quita el resto anterior a H10.
2026-11-14 · APROBADO por Gerardo · Árbitro de tamaño M: `skills/pit-lane/SKILL.md` (tabla de tamaños) y diseño 6.3 dicen "el que fije MÉTODO" en vez de "árbitro de rutina"; queda igual que gauntlet V2.1.
2026-11-14 · APROBADO por Gerardo · Lectores de XL: `agents/lector-critico.md` pasa a opus · high y `agents/lector-ingenuo.md` a sonnet · high, porque solo corren en XL y la tabla 6.7 fija esos valores para XL; `lector-ejecucion` sigue en sonnet · medium (en XL el despacho declara high). Diseño, sección 7, actualizado.
2026-11-14 · APROBADO por Gerardo · Los cuatro marcadores [CONFIRMAR] ya confirmados se reemplazan por la nota de confirmación en `references/`. Las líneas de arriba citan secciones en vez de números de línea.
2026-11-14 · APROBADO por Gerardo · Fuentes externas en el contrato: `references/plantillas.md` y diseño 6.5 dicen "curl o WebFetch, o la lista de Drive", como gauntlet V2.1.
2026-11-14 · APROBADO por Gerardo · Diseño versión 0.7: cabecera con el estado real y sección 7 con `.gitattributes` y `docs/manual-de-uso.md`. AGENTS.md: pasos 0 a 10 hechos, cambios posteriores vía decisiones, hipótesis validadas.
2026-11-14 · APROBADO por Gerardo · `scripts/LEEME.md`: se juntan las dos secciones sobre la app de escritorio en una, con el orden del freno (get_usage, archivo, manual).
2026-11-14 · APROBADO por Gerardo · `.gitattributes` nuevo (`* text=auto eol=lf`) para que no se mezclen finales de línea.
2026-11-14 · APROBADO por Gerardo · `agents/mecanico-auxiliar.md`: R-13 en orden en la lista de reglas.
2026-11-14 · APROBADO por Gerardo · `README.md` con instalación, tabla de uso y ejemplo; `docs/manual-de-uso.md` sin ruta personal, con la auditoría de coherencia y la aclaración de que `agents/arbitro.md` es un envoltorio, no una copia.
2026-11-14 · Auditoría de la revisión: `pit-lane:arbitro` (opus · high, R-36) APROBADO en ronda 1, 11 de 11 criterios. Se aplican cinco de sus observaciones: R-39 en `SKILL.md` incluye el caso del mecánico de modo B que no puede lanzar subagentes; nota en la sección 8 del diseño (los encargos son registro histórico; vale la sección 6); `verificar_office.py` avisa de las diapositivas o notas ilegibles; `LEEME.md` recupera "o el archivo no se actualiza"; el manual dice "oleadas de hasta 2". Las demás quedan como están, por ejemplo: "gauntlet" sin prefijo en `references/` es anterior y está fuera del alcance de la regla 3.

## Evaluación externa de Gerardo (2026-11-15): seis puntos

2026-11-15 · Puntos 1 (README corto) y 2 (carga del plugin, H9) ya cubiertos por la revisión del 2026-11-14; H9 se cumple en el equipo de Gerardo, y para otros equipos el manual indica `CLAUDE_CODE_PLUGIN_DIRS`. Puntos 4 (contenido personal) y 6 (depende de Claude Code): quedan como están mientras el repo sea privado; separar las reglas personales y añadir un `marketplace.json` queda para cuando se decida compartirlo.
2026-11-15 · APROBADO por Gerardo · Punto 3 (dependencias externas) y 6: `README.md` con una sección "Requisitos" (Claude Code y versión, plan Pro, Superpowers y EGM opcionales según R-34, y herramientas de `verificar_office.py`).
2026-11-15 · APROBADO por Gerardo · Punto 5 (riesgo de desincronía de `arbitro.md`): `agents/arbitro.md` deja de repetir instrucciones del método; conserva solo lo propio del agente (la ruta, sus herramientas sin WebFetch ni Drive y el "no ejecutado" sin ruta). El método queda solo en `skills/gauntlet/agents/arbitro.md` (regla 2 de AGENTS.md).
