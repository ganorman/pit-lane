# Plantillas de Pit Lane

Contrato, encargo y `estado.md`. El resumen de auditoría y la bitácora no se repiten aquí: se usan las de `skills/gauntlet/references/plantillas.md` (secciones 2 y 3).

Estructura de carpetas de un trabajo L o XL. La carpeta del trabajo es la que indique el usuario o, si no indica ninguna, el directorio de trabajo de la sesión; `entrada/` y `entregables/` son la organización sugerida y el contrato puede fijar otras rutas:

```
<carpeta del trabajo>/
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

Es el contrato de gauntlet completo, con siete añadidos (marcados con ✚). Antes de aprobar, el usuario lee INSTRUCCIONES ORIGINALES y el LISTÓN: es su único veto. Lo aprueba el usuario; al aprobarse, el listón queda congelado y solo el usuario lo cambia (R-05). En M, L y XL nada se construye sin contrato aprobado (R-03). Una aprobación por tarea; dos en XL (R-08).

```markdown
# Contrato — [trabajo] — tamaño [M | L | XL]
Aprobado: AAAA-MM-DD   ← lo escribe el Jefe de pits cuando el usuario aprueba
## TAREA            qué, para quién, qué debe incluir
## INSTRUCCIONES ORIGINALES ✚  el pedido del usuario, literal y numerado (P1, P2…), sin resumir
## FRONTERA ✚       qué no se toca y qué no se debe hacer
## MÉTODO           fuentes (rutas), skills que se usan, modo, modelo y esfuerzo del árbitro, rondas máx. 3
## LISTÓN           ID | se exige (PASA / NO PASA) | método | evidencia esperada
                    + listón base B1…B6 que aplique
                    + completitud ✚: cada punto P1, P2… aparece en el entregable, o su ausencia es una
                      decisión anotada y vetable; corregir un criterio no elimina contenido pedido
                      (lo no verificable se marca pendiente, no se borra)
                    + pasabilidad con pre-vuelo (gauntlet, Fase 0 paso 4; R-44): el método de cada criterio
                      se ejecuta una vez con las herramientas del árbitro; línea "Pre-vuelo: L1 ✔ · L2 ✘ → …";
                      un ✘ cambia de método o pasa a revisión humana antes de pedir la aprobación
                    + criterios de revisión humana (el árbitro no bloquea por ellos)
                    + fuentes externas: cada página web guardada en entrada/fuentes/ con su índice
                      LEEME.md (URL y fecha de consulta), o la lista de Drive del conector; el árbitro
                      coteja contra la copia; sin copia ni comprobación ejecutable, NO VERIFICABLE (R-35, R-42)
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
- **Pre-vuelo.** El método de cada criterio se ejecuta una vez antes de pedir la aprobación; un ✘ cambia de método o pasa a revisión humana (R-44).
- **Fuentes web.** Cada página que se use como fuente se guarda como archivo en `entrada/fuentes/`, con su índice, y el árbitro coteja contra esa copia (R-42).
- **PRESUPUESTO.** Máximo 2 mecánicos por oleada (R-14).

---

## 2. Encargo — `pit-lane/encargos/E01-nombre.md`

Un archivo por encargo, con esta plantilla (R-10). Junta en un solo archivo lo que el mecánico necesita para trabajar sin la conversación: qué hacer, con qué, dónde puede escribir, contra qué se audita y por dónde va.

```markdown
# E01 — [nombre]
Estado: pendiente | en curso | en auditoría | terminado | espera decisión
Modelo: sonnet · Esfuerzo: medium · Modo: subagente | sesión
Árbitro: sonnet · medium   (opus · high si sale a terceros, se proyecta en público o es difícil de revertir)
Depende de: — | E0x
## Objetivo
## Entradas                 rutas (incluye normas y datos-maestros.md; si es código, instrucciones
                            para otra IA o una especificación de software, la ruta absoluta de references/software.md, R-34)
## Superficie de escritura  únicas rutas que puede crear o modificar
                            (en modo B incluye su bitácora: pit-lane/auditorias/E01.md;
                            si busca fuentes en la web, incluye entrada/fuentes/, R-42)
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

Una línea por encargo. Solo lo escribe el Jefe de pits, y lo hace leyendo los encargos (R-18). Usa tres grupos, para que el usuario vea de un vistazo qué le toca: **trabajando**, **esperan tu decisión**, **terminados** (R-18).

```markdown
# Estado — [trabajo] — actualizado [AAAA-MM-DD hh:mm]

## Trabajando
- E01 — [nombre] — [modelo · esfuerzo] — [en qué va]

## Esperan tu decisión
- E02 — [nombre] — [qué se necesita decidir]

## Terminados
- E03 — [nombre] — [auditoría: aprobada en ronda N | con pendientes]
```

El documento fija los tres grupos y "una línea por encargo"; el encabezado y los campos de cada línea son los de esta plantilla, aceptados tras el piloto (decisión 2026-11-14).

Reglas que usan `estado.md`:
- Tras un corte, el Jefe de pits lee `estado.md` y los encargos antes de confiar en lo que recuerda (R-20).
- Un mecánico bloqueado pasa a "Esperan tu decisión" (R-19). Detalle en `references/modos-de-ejecucion.md`.
