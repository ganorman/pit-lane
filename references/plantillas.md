# Plantillas de Pit Lane

Contrato, encargo y `estado.md`. El resumen de auditoría y la bitácora no se repiten aquí: se usan las de `skills/gauntlet/references/plantillas.md` (secciones 2 y 3).

Estructura de carpetas de un trabajo L o XL:

```
proyectos/<área>/AAAA-MM-DD_Tema/
├── entrada/
├── entregables/
└── pit-lane/
    ├── contrato.md
    ├── datos-maestros.md
    ├── estado.md             ← una línea por encargo; solo la escribe el Jefe de pits
    ├── encargos/E01-….md
    └── auditorias/           ← E01.md, E02.md… (una por encargo: la lleva el Jefe de pits en modo A y el mecánico en modo B) y coherencia.md (el Jefe de pits)
```

---

## 1. Contrato — `pit-lane/contrato.md`

Es el contrato de gauntlet completo, con siete añadidos (marcados con ✚). Antes de aprobar, Gerardo lee INSTRUCCIONES ORIGINALES y el LISTÓN: es su único veto. Lo aprueba Gerardo; al aprobarse, el listón queda congelado y solo Gerardo lo cambia (R-05). En M, L y XL nada se construye sin contrato aprobado (R-03). Una aprobación por tarea; dos en XL (R-08).

```markdown
# Contrato — [trabajo] — tamaño [M | L | XL]
Aprobado: AAAA-MM-DD   ← lo escribe el Jefe de pits cuando Gerardo aprueba
## TAREA            qué, para quién, qué debe incluir
## INSTRUCCIONES ORIGINALES ✚  el pedido de Gerardo, literal y numerado (P1, P2…), sin resumir
## FRONTERA ✚       qué no se toca y qué no se debe hacer
## MÉTODO           fuentes (rutas), skills que se usan, modo, modelo y esfuerzo del árbitro, rondas máx. 3
## LISTÓN           ID | se exige (PASA / NO PASA) | método | evidencia esperada
                    + listón base B1…B6 que aplique
                    + completitud ✚: cada punto P1, P2… aparece en el entregable, o su ausencia es una
                      decisión anotada y vetable; corregir un criterio no elimina contenido pedido
                      (lo no verificable se marca pendiente, no se borra)
                    + pasabilidad (gauntlet, Fase 0 paso 4): cada criterio puede pasar con lo que existirá
                      al auditar (archivos, fuentes y herramientas del árbitro); si no, se corrige o se elimina
                      antes de pedir la aprobación
                    + criterios de revisión humana (el árbitro no bloquea por ellos)
                    + fuentes externas: cada una con su comprobación ejecutable (curl o lista de Drive)
                    + criterios de coherencia entre entregables (solo L y XL) ✚
## ENTREGABLE       archivos, formato, restricciones
## DATOS MAESTROS ✚ ruta del archivo único con cifras, fechas, nombres y precios compartidos
## PLAN ✚           solo L y XL: tabla de encargos (ver sección 2) con modelo y esfuerzo
## PRESUPUESTO ✚    mecánicos simultáneos máx. 2 · freno de gasto
## Decisiones tomadas (vétalas si no te sirven)
```

Reglas que el contrato hace cumplir:
- **TAREA y ambigüedades.** Ambigüedad crítica: hasta 4 preguntas con opción recomendada. Ambigüedad menor: se decide y se anota en "Decisiones tomadas" (R-04).
- **FRONTERA.** El contrato declara qué no se toca ni se debe hacer (R-06).
- **LISTÓN.** Cada criterio es binario, con método y evidencia esperada (R-05).
- **DATOS MAESTROS.** Lo compartido vive en `datos-maestros.md`; los encargos lo citan, no lo copian (R-07).
- **LISTÓN de coherencia (L y XL).** Un criterio por cada dato maestro que aparece en más de un entregable (R-29).
- **Criterios de revisión humana.** Un NO VERIFICABLE bloquea igual que un NO PASA, salvo que el contrato lo marque aquí como revisión humana (R-35).
- **PRESUPUESTO.** Máximo 2 mecánicos por oleada (R-14).

---

## 2. Encargo — `pit-lane/encargos/E01-nombre.md`

Un archivo por encargo, con esta plantilla (R-10). Fusiona el brief de Superpowers, la tarjeta de ECC, el archivo de encargo de la Colmena y la bitácora de gauntlet.

```markdown
# E01 — [nombre]
Estado: pendiente | en curso | en auditoría | terminado | espera decisión
Modelo: sonnet · Esfuerzo: medium · Modo: subagente | sesión
Árbitro: sonnet · medium   (opus · high si sale a terceros, se proyecta en público o es difícil de revertir)
Depende de: — | E0x
## Objetivo
## Entradas                 rutas (incluye normas y datos-maestros.md)
## Superficie de escritura  únicas rutas que puede crear o modificar
                            (en modo B incluye su bitácora: pit-lane/auditorias/E01.md)
## Frontera                 qué no tocar ni decidir
## Listón aplicable         IDs, con su método; incluye los IDs B del listón base
                            que apliquen a este entregable
## Decisiones ya tomadas
## Qué devolver             estado (HECHO | HECHO CON DUDAS | BLOQUEADO | FALTA CONTEXTO),
                            auditoría (aprobada en ronda N | con pendientes | pendiente),
                            rutas, decisiones propias, en ≤15 líneas
## Avance                   [fecha hora] hecho … / sigue …      ← lo escribe el mecánico
## Qué no funcionó y por qué                                     ← lo escribe el mecánico
```

Reglas que el encargo hace cumplir:
- **Modelo y esfuerzo.** Cada encargo y cada despacho los declaran siempre (R-12). Detalle en `references/enrutamiento.md`.
- **Superficie de escritura.** Cada encargo declara la suya; dos encargos corren en paralelo solo si sus superficies no se solapan (R-11).
- **Qué devolver.** El mecánico prueba sobre el archivo real y devuelve uno de los cuatro estados en 15 líneas o menos (R-16).
- **Avance y Qué no funcionó.** El mecánico actualiza "Estado", "Avance" y "Qué no funcionó" en su propio encargo (R-17).

### Línea de arranque (todo mecánico)

Todo mecánico arranca con esta línea (R-15):

> Tu encargo está en `<ruta>`. Léelo entero antes de nada y sigue desde donde se quedó.

---

## 3. Estado — `pit-lane/estado.md`

Una línea por encargo. Solo lo escribe el Jefe de pits, y lo hace leyendo los encargos (R-18). Usa los tres grupos de la Colmena: **trabajando**, **esperan tu decisión**, **terminados** (R-18).

```markdown
# Estado — [trabajo] — actualizado [AAAA-MM-DD hh:mm]

## Trabajando
- E01 — [nombre] — [modelo · esfuerzo] — [en qué va]

## Esperan tu decisión
- E02 — [nombre] — [qué se necesita decidir]

## Terminados
- E03 — [nombre] — [auditoría: aprobada en ronda N | con pendientes]
```

**[CONFIRMAR]** El documento fija los tres grupos y "una línea por encargo", pero no el contenido exacto de cada línea ni el encabezado. Los campos de arriba son una propuesta de esta plantilla.

Reglas que usan `estado.md`:
- Tras un corte, el Jefe de pits lee `estado.md` y los encargos antes de confiar en lo que recuerda (R-20).
- Un mecánico bloqueado pasa a "Esperan tu decisión" (R-19). Detalle en `references/modos-de-ejecucion.md`.
