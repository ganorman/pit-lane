# Modos de ejecución

Cómo se lanzan los mecánicos. Origen: secciones 8, 9 y 10 del diseño (`docs/diseno.md`). Los agentes se nombran con prefijo: `pit-lane:mecanico`, `pit-lane:mecanico-experto`, `pit-lane:mecanico-auxiliar`, `pit-lane:arbitro`.

## Tabla

| Modo | Qué es | Cuándo | Cómo se fija modelo y esfuerzo | Estado |
|---|---|---|---|---|
| **A. Subagentes** | Mecánicos dentro de la sesión del Jefe de pits | Encargos de menos de una hora; lectura y análisis; funciona también en el chat | Parámetros del despacho o definición del agente | **v1** |
| **B. Sesiones paralelas** | Cada mecánico es una sesión completa de la pestaña Code; el Jefe de pits las lista, lee y les escribe | Trabajos largos; cuando quieres entrar a la sesión de un mecánico a corregir | Selector de cada sesión. La sesión la abres tú y pegas la línea de arranque | **v1** |
| **C. Projects** | Coordinador con hilos, en la nube o en tu equipo | Trabajo de días que debe seguir con el equipo apagado | Ajustes del proyecto | Evaluar en el piloto si tu cuenta lo tiene |
| **D. Agent teams** | Líder con compañeros y lista de tareas compartida | — | Se nombra el modelo al crear cada compañero | Fuera: experimental, sin reanudación |
| **E. Bahías externas** | Un encargo lo ejecuta una IA de otro proveedor (Codex, Antigravity) en una carpeta aislada; el Jefe de pits integra y audita en Claude | 3 o más encargos independientes y alguno de rutina, o probar una skill o un prompt en otro modelo (R-47) | Selector de la herramienta externa; el modelo y el razonamiento van en el despacho (R-49, R-50) | **v1.3** |

Los modos C y D no se usan en la v1. El modo C queda por evaluar (hipótesis H7: si tu cuenta tiene Projects); el D está fuera por ser experimental.

---

## Reglas comunes a los modos A y B

- Cada encargo y cada despacho declaran modelo y esfuerzo (R-12). Ver `references/enrutamiento.md`.
- Topes por oleada (R-14): hasta 2 mecánicos Claude y hasta 2 externos del modo E (1 por herramienta), 4 en total. Los mecánicos expertos corren solo en Claude: 1, o 2 si no hay otro mecánico Claude trabajando. El Jefe de pits despacha por oleadas.
- Dos encargos corren en paralelo solo si sus superficies de escritura no se solapan (R-11).
- Todo mecánico arranca con la línea estándar (R-15): *"Tu encargo está en `<ruta>`. Léelo entero antes de nada y sigue desde donde se quedó."*
- Un mecánico recibe su archivo de encargo, las normas y los datos maestros; no recibe la conversación del Jefe de pits.
- Lectores y árbitros no cargan `CLAUDE.md` ni `AGENTS.md`: lo que necesiten de esas reglas va escrito en el contrato o en el encargo (R-40).
- El Jefe de pits no construye entregables de tamaño L ni XL (R-37).
- El Jefe de pits no lee entregables completos: los mecánicos devuelven 15 líneas o menos y una ruta (R-16, R-31).
- Freno de gasto: al 80 % de la ventana de 5 horas, o con la palabra "freno", no se despacha nada nuevo; cada mecánico escribe su avance y se detiene (R-30).

---

## Modo A — Subagentes

Cumple el requisito de que el Jefe de pits despache tras la aprobación del usuario.

1. El usuario aprueba contrato, plan y enrutamiento (R-08).
2. El Jefe de pits escribe `pit-lane/contrato.md`, `pit-lane/datos-maestros.md` y un archivo por encargo en `pit-lane/encargos/` (R-10).
3. Comprueba que ninguna variable de entorno anule el enrutamiento (R-38).
4. Lanza los mecánicos por oleadas de hasta 2 (R-14), como subagentes, con el agente que corresponda según la tabla de enrutamiento (`pit-lane:mecanico`, `pit-lane:mecanico-experto` o `pit-lane:mecanico-auxiliar`) y con el modelo y el esfuerzo del plan escritos en el despacho (R-12). El despacho contiene la línea de arranque (R-15).
5. Cada mecánico construye, prueba sobre el archivo real y devuelve uno de los cuatro estados más "auditoría: pendiente", en 15 líneas o menos (R-16).
6. Por cada encargo, el Jefe de pits lanza `pit-lane:arbitro` con el modelo y el esfuerzo de la línea "Árbitro:" del encargo, lleva la bitácora, devuelve los fallos al mecánico y repite hasta aprobar o llegar a 3 rondas (R-24, R-39; ver "Quién lanza cada auditoría").
   - **Los fallos van al mismo mecánico** (R-46): el Jefe de pits continúa el subagente que construyó, con SendMessage y el ID del agente, y le pasa la tabla de fallos. El mecánico conserva lo que ya leyó y probó, así que no vuelve a empezar de cero. Solo se lanza un mecánico nuevo si el anterior ya no responde o si R-27 obliga a subir de modelo; ese mecánico nuevo retoma desde "Avance" (R-17, R-20).
   - **El árbitro, en cambio, es nuevo en cada ronda** (R-24): la independencia la necesita quien juzga, no quien corrige.
   - **Disputa exprés** (R-46): si lo único pendiente son disputas y el entregable no cambió desde la ronda auditada, el Jefe de pits lanza un árbitro nuevo solo para los criterios disputados. No es una ronda completa ni consume una de las 3. Si el entregable cambió, la ronda siguiente es completa, como siempre.
7. El Jefe de pits actualiza `estado.md` leyendo los encargos (R-18).

**Escalada en el modo A** (R-27): si un criterio falla dos rondas seguidas, el Jefe de pits relanza el encargo con el modelo de un nivel superior y un enfoque distinto. Aquí sí se lanza un mecánico nuevo, porque cambia el modelo.

**Si continuar al mecánico no funciona** (hipótesis H11): si SendMessage no llega al subagente o este ya no recuerda el encargo, el Jefe de pits vuelve a lanzar uno nuevo con la línea de arranque (R-15) y lo anota en la bitácora.

**Cómo se entera el Jefe de pits de que un mecánico terminó:** el resultado vuelve solo.

---

## Modo B — Sesiones paralelas

Cumple el requisito solo a medias: las sesiones las abre el usuario, con instrucciones exactas del Jefe de pits. No se confirmó que Claude pueda crear sesiones en la app de escritorio.

1. El usuario aprueba contrato, plan y enrutamiento (R-08).
2. El Jefe de pits escribe `contrato.md`, `datos-maestros.md` y los archivos de encargo (R-10), y comprueba las variables de entorno (R-38).
3. Para cada mecánico de la oleada (hasta 2, R-14), el Jefe de pits le da al usuario cuatro cosas: el **nombre de la sesión**, el **modelo**, el **esfuerzo** y la **línea de arranque** con la ruta del encargo (R-12, R-15).
4. El usuario abre cada sesión de la pestaña Code, pone el modelo y el esfuerzo en su selector y pega la línea de arranque.
5. Cada mecánico construye y prueba como en el modo A, pero pasa él mismo el loop de `pit-lane:gauntlet`: lanza `pit-lane:arbitro` con el modelo y el esfuerzo de la línea "Árbitro:" de su encargo y lleva su bitácora (R-39). Devuelve el estado y el resultado de la auditoría en 15 líneas o menos (R-16).
6. El Jefe de pits lista las sesiones, lee su actividad y les escribe cuando haga falta.

**Escalada en el modo B** (R-27): el Jefe de pits le indica al usuario el modelo que debe poner en el selector de esa sesión.

**Cómo se entera el Jefe de pits de que un mecánico terminó:**
- Pide el aviso de inactividad de la sesión de cada mecánico, si la herramienta lo permite (`notify_when_idle`; hipótesis H4: no se confirmó que esté disponible entre sesiones de la app de escritorio).
- Si no se puede, relee los encargos cada vez que el usuario pide estado o avisa "terminó E0x".

**Ajuste pequeño y localizado:** se le pide directo al mecánico (R-22). Pasarlo por el Jefe de pits procesa el contexto dos veces.

---

## Modo E — Bahías externas

Un encargo lo ejecuta la IA de otro proveedor, en la misma máquina y el mismo proyecto. El mecánico externo trabaja en una **bahía**: una carpeta aislada con sus instrucciones, su encargo, copias de lo que necesita y una única carpeta de salida. La integración y la auditoría siguen en Claude. Del bloque de reglas comunes valen R-11, R-12, R-14, R-30, R-31, R-37 y R-40; la línea de arranque (R-15) la reemplaza el texto del despacho (R-49).

### Cuándo (R-47)

- Hay **3 o más encargos independientes y alguno es de rutina**, o hace falta **probar una skill o un prompt en otro modelo**. Fuera de eso no compensa: armar la bahía, integrar y auditar cuesta más que lo que se ahorra.
- Solo encargos de nivel auxiliar o estándar ligero (R-50). Un encargo de `pit-lane:mecanico-experto` no va nunca a una bahía.
- El encargo declara `Ejecutor:` con la herramienta, y en "Modelo" el modelo y el razonamiento del proveedor (`references/plantillas.md`, sección 2).
- Antes de despachar, si la tabla de modelos externos de `references/enrutamiento.md` tiene más de 30 días, el Jefe de pits la verifica en la web (R-50).

### Armar la bahía (R-48)

Una carpeta por encargo externo: `<carpeta del trabajo>\pit-lane\bahias\E0x-<herramienta>\`.

| Pieza | Qué es | Cómo la deja el Jefe de pits |
|---|---|---|
| `AGENTS.md` | Copia de `references/mecanico-externo.md` | Solo lectura |
| `ENCARGO.md` | Copia del encargo de `pit-lane/encargos/`, con "Avance" como **última** sección | Escribible: el ejecutor solo escribe en "Avance" |
| `entrada\` | Copias de lo que el encargo necesita (datos maestros, fuentes, plantillas), nunca los originales | Solo lectura |
| `salida\` | Lo único que el ejecutor puede escribir. `salida\_borrador\` es para sus archivos de trabajo y no se integra | Vacía |

1. Copia las piezas y marca como solo lectura `AGENTS.md` y todo `entrada\`: `Get-ChildItem <bahía>\entrada -Recurse -File | ForEach-Object { $_.IsReadOnly = $true }`, y lo mismo con `AGENTS.md`.
2. Guarda una copia de `ENCARGO.md` tal como se despacha en `pit-lane/auditorias/E0x-encargo-despacho.md`.
3. Toma el **inventario antes**: el hash de cada archivo de la carpeta del trabajo, fuera de `pit-lane\auditorias\`.
   ```powershell
   $t = '<carpeta del trabajo>'
   Get-ChildItem $t -Recurse -File | Where-Object { $_.FullName -notlike "$t\pit-lane\auditorias\*" } |
     Get-FileHash | Select-Object Hash, @{n='Ruta'; e={ $_.Path.Substring($t.Length) }} |
     Export-Csv "$t\pit-lane\auditorias\E0x-inventario-antes.csv" -NoTypeInformation
   ```
- **Variante con git.** Si el proyecto usa git y el encargo necesita el repositorio entero como entrada, la bahía puede ser un worktree (`git worktree add <bahía> -b bahia/E0x`). `AGENTS.md`, `ENCARGO.md` y `salida\` van en su raíz (si el proyecto ya tiene `AGENTS.md`, el del worktree se reemplaza y ese cambio nunca se confirma), el resto del repositorio hace de `entrada\` y el control del paso "Integrar" es `git status --porcelain` dentro del worktree.

### Despachar (R-49)

El Jefe de pits le da al usuario un bloque por encargo, con la plantilla de `references/plantillas.md`, sección 4: ID, herramienta, modelo y razonamiento; la ruta absoluta de la bahía; el texto que se pega; y el aviso de fin. El usuario abre la herramienta en esa carpeta, pone el modelo y el razonamiento en su selector y pega el texto. Cada despacho cuenta para los topes de R-14 hasta que se integra.

### Aviso de fin

No hay aviso automático entre proveedores. El usuario escribe **"terminó E0x"**. Si pide el estado antes, el Jefe de pits lee la sección "Avance" de cada bahía.

### Integrar (R-51)

Con "terminó E0x":
1. Lee el informe final de "Avance" (15 líneas o menos). No lee el entregable completo (R-31).
2. Toma el **inventario después** con el mismo comando (archivo `E0x-inventario-despues.csv`) y compara:
   ```powershell
   Compare-Object (Import-Csv "$t\pit-lane\auditorias\E0x-inventario-antes.csv") (Import-Csv "$t\pit-lane\auditorias\E0x-inventario-despues.csv") -Property Ruta, Hash
   ```
   Solo pueden aparecer `salida\` y `ENCARGO.md` de las bahías despachadas, las superficies de escritura de los encargos Claude de la misma oleada y los archivos del Jefe de pits (`estado.md`, `encargos/`). En `ENCARGO.md`, todo lo anterior a "Avance" debe ser idéntico a `E0x-encargo-despacho.md`. Cualquier otro cambio se anota en la bitácora como **escritura fuera de la bahía**, se muestra al usuario y cuenta como un fallo de H12.
3. Copia `salida\` (sin `_borrador\`) a la ruta de la línea "Integra en:" del encargo, y pasa al encargo de `pit-lane/encargos/` el estado, el "Avance" y el "Qué no funcionó" del informe (R-17, R-18). Copiar la salida es integrar, no construir (R-37): el Jefe de pits no cambia una palabra del entregable.

### Auditar (R-51)

El Jefe de pits lanza `pit-lane:arbitro` **en Claude**, sobre el entregable integrado, con el modelo y el esfuerzo de la línea "Árbitro:" del encargo, y lleva la bitácora en `pit-lane/auditorias/E0x.md`, como en el modo A (R-24, R-39). El árbitro corre siempre en Claude, nunca en la herramienta externa. Como el constructor no es Opus, si el error es costoso el árbitro es Opus (R-36).

- **Corrección.** Los fallos vuelven a la bahía: el Jefe de pits agrega a `ENCARGO.md`, justo antes de "Avance", la sección "Fallos de la auditoría — ronda N" con la tabla de fallos, renueva la copia de despacho y el inventario antes, y le da al usuario el mismo formato de despacho (R-49).
- **Escalada** (R-27). Si un criterio falla dos rondas seguidas, el encargo pasa a Claude: `pit-lane:mecanico` en modo A, que retoma desde `salida\` y el "Avance".
- **Freno** (R-30). Con el freno activo tampoco se despachan bahías: su auditoría corre en Claude. La cuota de la herramienta externa es aparte; si se acaba, el ejecutor escribe su avance y se detiene.

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
| L y XL, modo A | El Jefe de pits lanza el árbitro de cada encargo (`pit-lane:arbitro`, con el modelo y el esfuerzo de la línea "Árbitro:" del encargo) | `pit-lane/auditorias/E0x.md`, la lleva el Jefe de pits |
| L y XL, modo B | Cada mecánico lanza el árbitro de su encargo (`pit-lane:arbitro`, con el modelo y el esfuerzo de la línea "Árbitro:" del encargo, no los suyos) | `pit-lane/auditorias/E0x.md`, la lleva el mecánico |
| L y XL, modo E | El Jefe de pits, en Claude, sobre el entregable integrado (R-51) | `pit-lane/auditorias/E0x.md`, la lleva el Jefe de pits |
| L y XL, coherencia entre entregables | El Jefe de pits, cuando todos los encargos terminaron | `pit-lane/auditorias/coherencia.md` |

- En modo A el Jefe de pits lanza siempre los árbitros: no se cuenta con que un subagente lance a otro (hipótesis H10, decisión 2026-11-14). En modo B, si un mecánico no puede lanzar subagentes, devuelve "auditoría: pendiente" y la lanza el Jefe de pits (R-39).
- La auditoría de coherencia lleva un criterio por cada dato maestro que aparece en más de un entregable (R-29).
- Un árbitro nuevo por ronda, sin el razonamiento del constructor, sobre todo el listón, máximo 3 rondas (R-24).
- Un árbitro que falló o no corrió se reintenta una vez; si vuelve a fallar se registra "no ejecutado", nunca "sin hallazgos" (R-25).
- Sin subagentes (por ejemplo, en un chat que no los tenga): modo degradado de gauntlet, y el resumen empieza con **AUDITORÍA NO INDEPENDIENTE** (R-26).

## Tras un corte (R-20)

El Jefe de pits lee `estado.md` y los encargos **antes** de confiar en lo que recuerda, y reanuda cada mecánico en su última línea de avance. Si cambia un dato compartido, edita `datos-maestros.md` y avisa solo a los mecánicos cuyos encargos lo citan (R-21).

## Modos C y D

Sin pasos concretos en la v1: esta referencia solo recoge su fila de la tabla. El C queda por evaluar (H7) y el D está fuera (decisión 2026-11-14).
