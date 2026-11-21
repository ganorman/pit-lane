# Plantillas GAUNTLET

## 1. Contrato (Fase 0)

```markdown
# Contrato GAUNTLET — [nombre corto del trabajo]

## TAREA
[Qué se va a hacer, en una o dos frases.]
Es para: [usuario o audiencia, y en qué contexto lo va a usar].
Debe incluir:
- [...]
- [...]

## INSTRUCCIONES ORIGINALES
El pedido del usuario, literal y numerado, sin resumir (los adjuntos largos se citan por nombre o ruta, no se copian):
- P1. [...]
- P2. [...]

## MÉTODO
Loop autónomo: planificar → construir → probar → árbitro → corregir.
Árbitro: subagente nuevo por ronda | pase separado (AUDITORÍA NO INDEPENDIENTE) · modelo [opus | sonnet] · esfuerzo [high | medium]
  (opus · high si sale a terceros, se proyecta en público o es difícil de revertir; sonnet · medium en el resto).
Rondas máximas: 3.
Skills que se usan: [docx, pptx, xlsx, las propias del usuario…].
Fuentes: [rutas; las páginas web, guardadas en `fuentes/` con su índice `fuentes/LEEME.md` (URL y fecha de consulta)].

## LISTÓN
Referencia de calidad: [estándar o ejemplo, traducido a rasgos observables].

| ID | Se exige (PASA / NO PASA) | Método de verificación | Evidencia esperada |
|---|---|---|---|
| L1 | ... | ... | ... |
| L2 | ... | ... | ... |
| Ln | Completitud: cada punto P1, P2… aparece en el entregable, o su ausencia es una decisión anotada en "Decisiones tomadas" | Tabla punto → ubicación en el entregable | Tabla completa; cada punto ausente remite a su decisión |

Listón base aplicable: B1 (idioma: [es-XX]), B2, B5, B6 ([idioma y variante de redacción])  (B3/B4 no aplican porque … | B3: [nombre exigido / formas prohibidas])
Criterios de revisión humana (el árbitro no bloquea por ellos): [ID, o "ninguno"].
Pre-vuelo (método de cada criterio ejecutado una vez con las herramientas del árbitro): L1 ✔ · L2 ✔ · … [un ✘ solo aparece con su ajuste: "→ otro método" o "→ revisión humana"]

## ENTREGABLE
- Archivos: [nombre.ext, ruta]
- Formato y estructura: [...]
- Restricciones: [...]
- No usar: [...]
- Al final: resumen de auditoría + bitácora `auditoria-gauntlet.md`.

## Decisiones tomadas (vétalas si no te sirven)
- [Ambigüedad menor] → [decisión] — [por qué]

Lee INSTRUCCIONES ORIGINALES y el LISTÓN antes de aprobar: es tu único veto.

**¿Apruebas el contrato?** El loop arranca con tu aprobación y no se detiene hasta entregar.
```

### Ejemplos de criterios: mal y bien

| Mal (vago) | Bien (verificable) |
|---|---|
| El examen es de buena calidad | Cada pregunta tiene exactamente 4 opciones y una sola correcta según la clave · Método: conteo en el DOCX y cotejo con la clave · Evidencia: tabla pregunta → opciones → clave |
| Las fórmulas funcionan | Tras recalcular, ninguna celda devuelve #REF!, #DIV/0!, #VALUE! o #NAME? y ninguna fórmula queda sin valor · Método: `verificar_office.py archivo.xlsx --recalcular` (recalcula una copia con Excel) · Evidencia: sección "Recálculo" sin alerta, `celdas_con_error: 0` y `formulas_sin_valor_cacheado: 0` |
| Las citas son correctas | Cada cita coincide palabra por palabra con la edición que fija el contrato · Método: cotejo cita por cita · Evidencia: tabla cita → texto de la edición → coincide sí/no |
| Que esté todo lo que pedí | Cada punto P1…Pn del pedido aparece en el entregable, o su ausencia está anotada en "Decisiones tomadas" · Método: cotejo punto por punto contra INSTRUCCIONES ORIGINALES · Evidencia: tabla punto → ubicación o decisión |
| Que se vea profesional | Ninguna diapositiva tiene texto que se salga del cuadro ni fuente menor de 18 pt · Método: render a PDF (`--render`) + inspección de cada página con la herramienta de lectura · Evidencia: lista de diapositivas revisadas |
| Al nivel de un SOP de la planta | Tiene propósito, alcance, responsables, EPP, pasos numerados con puntos de LOTO y registro de revisión · Método: buscar cada sección · Evidencia: título de sección encontrado por cada rasgo |

---

## 2. Bitácora — `auditoria-gauntlet.md`

```markdown
# Bitácora GAUNTLET — [trabajo] — [AAAA-MM-DD]

## Contrato
Aprobado el [fecha] · Listón: L1–Ln + [B…] · Rondas máx: 3 · Árbitro: [modo]

## Decisiones
- [AAAA-MM-DD] [decisión] — [por qué]

## Ronda 1
Construido: [archivos/versión]
Pruebas del constructor: [qué corrió y resultado]
Informe del árbitro: [pegar el informe completo]
Correcciones planificadas: [...]

## Ronda 2
...

## Disputas
- [ID] constructor dice … / árbitro dice … / resolución …

## Escalados
- [ID] hallazgo … / prueba fuera del alcance del árbitro … / decisión del usuario …
```

---

## 3. Resumen de auditoría (Fase 2, en el chat)

```markdown
## Resumen de auditoría GAUNTLET
[Si aplica, primera línea: **AUDITORÍA NO INDEPENDIENTE**]

**Resultado:** APROBADO en ronda N de M | ENTREGADO CON PENDIENTES tras M rondas

| Ronda | Rechazó | Errores encontrados | Corregido |
|---|---|---|---|
| 1 | L2, L5 | [hallazgo concreto, una línea] | sí |
| 2 | — | — | — |

**Pendientes:** [criterios que no pasaron, con el porqué] | ninguno
**Disputas:** [resumen] | ninguna
**Escalados:** [criterio, hallazgo y la prueba que debes confirmar] | ninguno
**Fuera del listón (observaciones):** [lo que el árbitro vio y no bloqueaba]
**Revisa tú:** [lista corta de lo que solo un humano puede confirmar]

Detalle completo: `auditoria-gauntlet.md`
```
