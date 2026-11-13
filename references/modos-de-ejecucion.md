# Modos de ejecución

Cómo se lanzan los mecánicos. Origen: secciones 6.8, 6.9 y 6.10 del documento de diseño. Los agentes se nombran con prefijo: `pit-lane:mecanico`, `pit-lane:mecanico-experto`, `pit-lane:mecanico-auxiliar`, `pit-lane:arbitro`.

## Tabla

| Modo | Qué es | Cuándo | Cómo se fija modelo y esfuerzo | Estado |
|---|---|---|---|---|
| **A. Subagentes** | Mecánicos dentro de la sesión del Jefe de pits | Encargos de menos de una hora; lectura y análisis; funciona también en el chat | Parámetros del despacho o definición del agente | **v1** |
| **B. Sesiones paralelas** | Cada mecánico es una sesión completa de la pestaña Code; el Jefe de pits las lista, lee y les escribe | Trabajos largos; cuando quieres entrar a la sesión de un mecánico a corregir | Selector de cada sesión. La sesión la abres tú y pegas la línea de arranque | **v1** |
| **C. Projects** | Coordinador con hilos, en la nube o en tu equipo | Trabajo de días que debe seguir con el equipo apagado | Ajustes del proyecto | Evaluar en el piloto si tu cuenta lo tiene |
| **D. Agent teams** | Líder con compañeros y lista de tareas compartida | — | Se nombra el modelo al crear cada compañero | Fuera: experimental, sin reanudación |

Los modos C y D no se usan en la v1. El modo C queda por evaluar en el piloto (hipótesis H7); el D está fuera por ser experimental.

---

## Reglas comunes a los modos A y B

- Cada encargo y cada despacho declaran modelo y esfuerzo (R-12). Ver `references/enrutamiento.md`.
- Máximo 2 mecánicos por oleada (R-14). El Jefe de pits despacha por oleadas.
- Dos encargos corren en paralelo solo si sus superficies de escritura no se solapan (R-11).
- Todo mecánico arranca con la línea estándar (R-15): *"Tu encargo está en `<ruta>`. Léelo entero antes de nada y sigue desde donde se quedó."*
- Un mecánico recibe su archivo de encargo, las normas y los datos maestros; no recibe la conversación del Jefe de pits.
- El Jefe de pits no construye entregables de tamaño L ni XL (R-37).
- El Jefe de pits no lee entregables completos: los mecánicos devuelven 15 líneas o menos y una ruta (R-16, R-31).
- Freno de gasto: al 80 % de la ventana de 5 horas, o con la palabra "freno", no se despacha nada nuevo; cada mecánico escribe su avance y se detiene (R-30).

---

## Modo A — Subagentes

Cumple el requisito de que el Jefe de pits despache tras la aprobación de Gerardo.

1. Gerardo aprueba contrato, plan y enrutamiento (R-08).
2. El Jefe de pits escribe `pit-lane/contrato.md`, `pit-lane/datos-maestros.md` y un archivo por encargo en `pit-lane/encargos/` (R-10).
3. Comprueba que ninguna variable de entorno anule el enrutamiento (R-38).
4. Lanza los mecánicos por oleadas de hasta 2 (R-14), como subagentes, con el agente que corresponda según la tabla de enrutamiento (`pit-lane:mecanico`, `pit-lane:mecanico-experto` o `pit-lane:mecanico-auxiliar`) y con el modelo y el esfuerzo del plan escritos en el despacho (R-12). El despacho contiene la línea de arranque (R-15).
5. Cada mecánico construye, prueba sobre el archivo real y pasa su entregable por el loop de `pit-lane:gauntlet`, lanzando él mismo a `pit-lane:arbitro` (ver "Quién lanza cada auditoría").
6. Cada mecánico devuelve uno de los cuatro estados más el resultado de la auditoría, en 15 líneas o menos (R-16).
7. El Jefe de pits actualiza `estado.md` leyendo los encargos (R-18).

**Escalada en el modo A** (R-27): si un criterio falla dos rondas seguidas, el Jefe de pits relanza el encargo con el modelo de un nivel superior y un enfoque distinto.

**Cómo se entera el Jefe de pits de que un mecánico terminó:** el resultado vuelve solo.

---

## Modo B — Sesiones paralelas

Cumple el requisito solo a medias: las sesiones las abre Gerardo, con instrucciones exactas del Jefe de pits. No se confirmó que Claude pueda crear sesiones en la app de escritorio.

1. Gerardo aprueba contrato, plan y enrutamiento (R-08).
2. El Jefe de pits escribe `contrato.md`, `datos-maestros.md` y los archivos de encargo (R-10), y comprueba las variables de entorno (R-38).
3. Para cada mecánico de la oleada (hasta 2, R-14), el Jefe de pits le da a Gerardo cuatro cosas: el **nombre de la sesión**, el **modelo**, el **esfuerzo** y la **línea de arranque** con la ruta del encargo (R-12, R-15).
4. Gerardo abre cada sesión de la pestaña Code, pone el modelo y el esfuerzo en su selector y pega la línea de arranque.
5. Cada mecánico trabaja como en el modo A: construye, prueba, pasa el loop de `pit-lane:gauntlet` lanzando él mismo a `pit-lane:arbitro`, y devuelve el estado en 15 líneas o menos (R-16).
6. El Jefe de pits lista las sesiones, lee su actividad y les escribe cuando haga falta.

**Escalada en el modo B** (R-27): el Jefe de pits le indica a Gerardo el modelo que debe poner en el selector de esa sesión.

**Cómo se entera el Jefe de pits de que un mecánico terminó:**
- Pide el aviso de inactividad de la sesión de cada mecánico, si la herramienta lo permite (`notify_when_idle`; hipótesis H4: no se confirmó que esté disponible entre sesiones de la app de escritorio).
- Si no se puede, relee los encargos cada vez que Gerardo pide estado o avisa "terminó E0x".

**Ajuste pequeño y localizado:** se le pide directo al mecánico (R-22). Pasarlo por el Jefe de pits procesa el contexto dos veces.

---

## Mecánico bloqueado o sin contexto (R-19)

1. El Jefe de pits resuelve con el contrato y los datos maestros si alcanzan.
2. Si no alcanzan, pasa el encargo a **"esperan tu decisión"** en `estado.md`.
3. Detiene también los encargos que dependen de él.
4. Sigue despachando los encargos independientes.
5. Al resolverse, relanza el encargo **con el mismo modelo**.

---

## Quién lanza cada auditoría (R-39)

| Tamaño | Quién lanza el árbitro | Bitácora |
|---|---|---|
| M | La sesión que construye | Junto al entregable |
| L y XL | Cada mecánico lanza el árbitro de su encargo (`pit-lane:arbitro`, con el modelo y el esfuerzo del encargo) | `pit-lane/auditorias/E0x.md`, la lleva el mecánico |
| L y XL, coherencia entre entregables | El Jefe de pits, cuando todos los encargos terminaron | `pit-lane/auditorias/coherencia.md` |

- Si un mecánico no puede lanzar subagentes, devuelve "auditoría: pendiente" y la lanza el Jefe de pits (R-39). Hipótesis H10: que un mecánico lanzado como subagente pueda lanzar a su vez el árbitro se valida en el piloto, modo A.
- La auditoría de coherencia lleva un criterio por cada dato maestro que aparece en más de un entregable (R-29).
- Un árbitro nuevo por ronda, sin el razonamiento del constructor, sobre todo el listón, máximo 3 rondas (R-24).
- Un árbitro que falló o no corrió se reintenta una vez; si vuelve a fallar se registra "no ejecutado", nunca "sin hallazgos" (R-25).
- Sin subagentes (por ejemplo, en un chat que no los tenga): modo degradado de gauntlet, y el resumen empieza con **AUDITORÍA NO INDEPENDIENTE** (R-26).

## Tras un corte (R-20)

El Jefe de pits lee `estado.md` y los encargos **antes** de confiar en lo que recuerda, y reanuda cada mecánico en su última línea de avance. Si cambia un dato compartido, edita `datos-maestros.md` y avisa solo a los mecánicos cuyos encargos lo citan (R-21).

## Modos C y D

**[CONFIRMAR]** El documento no define pasos concretos para los modos C y D; esta referencia solo recoge su fila de la tabla.
