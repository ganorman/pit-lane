# Pit Lane — diseño

**Versión 1.3 · noviembre 2026**
Autor: Gerardo Alberto Norman, con Claude. Estado: v1 en uso. Este documento es la fuente de verdad del repo: si algo del repo lo contradice, gana este documento (AGENTS.md). Las decisiones fechadas que lo modificaron están en `docs/decisiones.md`.

> **Nombre.** Pit Lane toma su nombre de la parada en pits de la Fórmula 1: un equipo de especialistas que trabaja en paralelo, cada uno en lo suyo, y nadie suelta el carro hasta que todo está verificado. El **Jefe de pits** planifica y coordina; los **mecánicos** ejecutan; el **árbitro** verifica.

## 0. Resumen

1. Pit Lane es una forma de trabajar con Claude en trabajos serios: primero un contrato con un listón verificable, después el trabajo repartido en encargos que corren en paralelo, y al final una auditoría hecha por alguien que no construyó.
2. Ataca dos fallos: declarar "listo" sin que nadie ajeno lo haya verificado sobre el archivo real, y gastar el modelo más caro en trabajo que no lo necesita.
3. La ceremonia es proporcional: el tamaño de la tarea (S, M, L, XL) decide cuántas fases corren.
4. Cabe en **2 skills, 7 agentes y 5 archivos de referencia**, y no depende de ningún plugin externo: el proceso para código y especificaciones de software es propio (sección 13).
5. Desde la v1.3, un encargo de rutina puede ejecutarlo una IA de otro proveedor (modo E, sección 8); la integración y la auditoría siguen en Claude.

---

## 1. Principios

1. **Contrato antes de construir.** Nada se genera sin TAREA, LISTÓN y ENTREGABLE aprobados.
2. **Ceremonia proporcional.** El tamaño de la tarea decide cuántas fases corren.
3. **Una aprobación, luego de corrido.** Solo detienen el trabajo: algo irreversible, algo sensible, algo que sale a terceros, o un plan roto.
4. **El encargo vive en un archivo.** La conversación es volátil; el archivo es la verdad.
5. **Cada dato tiene un solo dueño.** Lo compartido vive en un archivo de datos maestros; los encargos lo citan, no lo copian.
6. **Paralelo solo si no chocan las escrituras.**
7. **El modelo menos potente que alcance, siempre declarado.** Se sube de nivel solo cuando el inferior falla.
8. **Quien construye no se audita.** Árbitro nuevo, sin el razonamiento del constructor, sobre el archivo real. Un revisor que no corrió no cuenta como aprobación.
9. **Topes en todo.** Rondas, mecánicos simultáneos y gasto.

## 2. Flujo

```
F0 TRIAGE      → tamaño S / M / L / XL (una línea, vetable)
F1 CONTRATO    → tarea, frontera, listón, entregable, datos maestros, decisiones tomadas
F2 PLAN        → encargos con superficie de escritura, dependencias, modelo y esfuerzo
                 (L: revisión del plan por el lector de ejecución · XL: por los tres lectores)
══ APROBACIÓN ══ El usuario aprueba contrato + plan + enrutamiento   (XL: contrato y plan por separado)
F3 DESPACHO    → el Jefe de pits escribe los archivos y lanza los mecánicos por oleadas
F4 EJECUCIÓN   → cada mecánico: construir → probar → informe de ≤15 líneas → estado
F5 AUDITORÍA   → árbitro nuevo por ronda contra el listón; máx. 3 rondas   (= gauntlet)
F6 CIERRE      → entregables, resumen de auditoría, "revisa tú", candidatos a norma
```

## 3. Triage

Se evalúan seis señales y **gana el nivel más alto** que alcance cualquiera. El Jefe de pits lo declara en una línea y el usuario puede vetarlo. Excepción (decisión 2026-11-14, piloto): las fuentes externas por sí solas suben a L, no a XL; llegan a XL solo si el costo del error también es alto.

| Señal | S | M | L | XL |
|---|---|---|---|---|
| Entregables | 1 | 1 con varias partes | 2 a 5 | más de 5, o el diseño es un entregable |
| Fuentes a cotejar | 0 a 1 | 2 a 3 | varias, o externas | muchas |
| Dependencia entre partes | ninguna | interna | datos compartidos | cadenas de dependencia |
| Costo del error | bajo, reversible | se proyecta o se usa | sale a terceros | difícil de revertir |
| Duración estimada | minutos | menos de 1 hora | horas | días |
| Ambigüedad | ninguna | 1 elección | varias | preguntas abiertas |

| Tamaño | Qué corre |
|---|---|
| **S** | Se hace y se dice qué se hizo. Sin contrato |
| **M** | Es gauntlet: contrato corto en el chat (listón de 5 a 8, sin bloque PLAN), la sesión construye y lanza el árbitro, loop de hasta 3 rondas con el árbitro que fije MÉTODO (por defecto Opus 5.5, alto, si sale a terceros, se proyecta en público o es difícil de revertir; Sonnet 5.5, medio, en el resto), bitácora junto al entregable. Sin carpeta `pit-lane/` |
| **L** | Contrato, plan con encargos revisado por el lector de ejecución, mecánicos en paralelo, auditoría de cada encargo lanzada por el Jefe de pits en modo A (por su mecánico en modo B) y auditoría de coherencia entre entregables lanzada por el Jefe de pits |
| **XL** | Como L, más revisión del plan con tres lectores y aprobación en dos tiempos |

## 4. Roles

| Rol | Qué hace | Qué recibe | Qué no recibe |
|---|---|---|---|
| **Usuario** | Fija el objetivo, aprueba el contrato, decide lo irreversible, valida al final | — | — |
| **Jefe de pits** | Triage, contrato, plan, enrutamiento, despacho, estado, propagación de cambios, integración de las bahías externas, auditoría de coherencia, cierre | Todo | No construye entregables de tamaño L o XL; copiar la salida de una bahía es integrar, no construir (R-37, R-51) |
| **Mecánico** | Un encargo de principio a fin: construye, prueba y pasa su entregable por el loop de auditoría. En modo B lanza él el árbitro; en modo A lo lanza el Jefe de pits (decisión 2026-11-14, H10) | Su archivo de encargo, las normas, los datos maestros | La conversación del Jefe de pits |
| **Mecánico externo** (modo E) | Un encargo de rutina o estándar ligero en una IA de otro proveedor: construye, prueba y deja su informe en "Avance". No audita | Su bahía: `AGENTS.md` (instrucciones neutrales), `ENCARGO.md`, `entrada/` de solo lectura | La conversación, las reglas de Claude y cualquier archivo fuera de la bahía |
| **Subagente** | Una búsqueda o lectura acotada para un mecánico | La pregunta | Todo lo demás |
| **Lector** (antes de construir) | Busca huecos en el plan o el diseño | Solo el documento y lo que este enlaza | La conversación, ni `CLAUDE.md` ni `AGENTS.md` (R-40) |
| **Árbitro** (después de construir) | Intenta rechazar el entregable con evidencia | Contrato, rutas de entregables y fuentes (las web, como copia guardada, R-42), fallos previos | El plan y el razonamiento del constructor, ni `CLAUDE.md` ni `AGENTS.md` (R-40) |

Tres lectores, cada uno con una mirada distinta:
- **Lector ingenuo**: parafrasea primero; si no puede, es un bloqueo.
- **Lector crítico**: supuestos sin respaldo, riesgos sin mitigar, alternativas no consideradas (incluidas no construir y reutilizar lo que ya existe).
- **Lector de ejecución**: pasos vagos y decisiones que el encargo deja al ejecutor.

## 5. Contrato

Es el contrato de gauntlet completo, con siete añadidos (marcados con ✚; INSTRUCCIONES ORIGINALES y completitud, decisión 2026-11-14):

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
                    + fuentes externas (gauntlet, Fase 0 paso 4): cada página web guardada en entrada/fuentes/
                      con su índice (URL y fecha de consulta), o la lista de Drive; el árbitro coteja contra la
                      copia; sin copia ni comprobación ejecutable, NO VERIFICABLE (R-42, decisión 2026-11-17)
                    + criterios de coherencia entre entregables (solo L y XL) ✚
## ENTREGABLE       archivos, formato, restricciones
## DATOS MAESTROS ✚ ruta del archivo único con cifras, fechas, nombres y precios compartidos
## PLAN ✚           solo L y XL: tabla de encargos (ver 6) con modelo y esfuerzo
## PRESUPUESTO ✚    por oleada: Claude máx. 2 · externos máx. 2 (1 por herramienta) · total 4 · freno de gasto
## Decisiones tomadas (vétalas si no te sirven)
```

Al aprobarse, el listón queda congelado: solo el usuario lo cambia.

## 6. Encargo

Un archivo por encargo en `pit-lane/encargos/E01-nombre.md`. Junta en un solo archivo lo que el mecánico necesita para trabajar sin la conversación: qué hacer, con qué, dónde puede escribir, contra qué se audita y por dónde va.

```markdown
# E01 — [nombre]
Estado: pendiente | en curso | en auditoría | terminado | espera decisión
Ejecutor: claude | codex | antigravity
Modelo: sonnet · Esfuerzo: medium · Modo: subagente | sesión | bahía
                            (externo: modelo y razonamiento del proveedor, R-50)
Árbitro: sonnet · medium   (opus · high si sale a terceros, se proyecta en público o es difícil de revertir;
                            corre siempre en Claude, R-51)
Integra en: <ruta del entregable>   ← solo modo E
Depende de: — | E0x
## Objetivo
## Entradas                 rutas (incluye normas y datos-maestros.md; si es código o una
                            especificación de software, references/software.md)
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

Arranque estándar de todo mecánico: *"Tu encargo está en `<ruta>`. Léelo entero antes de nada y sigue desde donde se quedó."* En el modo E lo reemplaza el texto del despacho externo (R-49), y la copia del encargo en la bahía deja "Avance" como última sección: el mecánico externo solo escribe ahí (R-48).

## 7. Enrutamiento de modelo y esfuerzo

| Trabajo | Modelo | Esfuerzo | Por qué |
|---|---|---|---|
| Jefe de pits: triage, contrato, plan, enrutamiento, resolver conflictos | Opus 5.5 | alto | Es trabajo de arquitectura: un error aquí se multiplica en cada encargo |
| Jefe de pits: coordinar (estado, propagar cambios, despachar oleadas) | la misma sesión | medio | Seguir el estado no exige el razonamiento del plan |
| Lector del plan | Sonnet 5.5 (crítico en XL: Opus 5.5) | medio (alto en XL) | La revisión se escala al riesgo del plan |
| Mecánico: redactar con criterio, analizar, integrar varias fuentes | Sonnet 5.5 | medio | Integrar y juzgar pide un modelo estándar, no el más caro |
| Mecánico experto: diseño difícil, decisiones con muchas dependencias | Opus 5.5 | alto | Es arquitectura, como el plan |
| Mecánico auxiliar: transcribir, convertir, formatear, inventariar, con todo especificado | Haiku 5.5 | bajo | Rutina con especificación completa: no hay nada que interpretar |
| Mecánico externo (modo E): rutina o estándar ligero | El del plan gratis del proveedor (tabla fechada en `references/enrutamiento.md`) | El del proveedor | Libera la ventana de 5 horas de Claude en encargos que no necesitan juicio |
| Subagente de búsqueda o lectura | Haiku 5.5 | bajo | Explorar y leer es barato y paralelo |
| Árbitro, error costoso | Opus 5.5 | alto | La última revisión antes de que algo salga va al más capaz |
| Árbitro, rutina | Sonnet 5.5 | medio | La revisión se escala al riesgo del entregable |

Reglas:
1. **El modelo y el esfuerzo se escriben siempre** en el encargo y en el despacho. Omitirlos hace que el mecánico herede los del Jefe de pits, que son los más caros. Antes del primer despacho se comprueba que ninguna variable de entorno anule el enrutamiento (sección 17).
2. **Haiku solo cuando el encargo lo trae todo.** Si el mecánico tiene que interpretar, el modelo barato toma dos o tres veces más turnos y termina costando más: pesa más el número de turnos que el precio por token. En la duda, Sonnet.
3. **Escalada:** un criterio que falla dos rondas seguidas pasa a un modelo un nivel superior, con enfoque distinto. En el modo A el Jefe de pits relanza el encargo con el nuevo modelo. En el modo B el Jefe de pits le indica al usuario el modelo que debe poner en el selector de esa sesión.
4. **Árbitro en modelo distinto del constructor** cuando el error es costoso y el constructor no es Opus. Si el constructor es Opus, el árbitro también lo es: la independencia la da el contexto limpio, no el modelo.
5. La columna de esfuerzo parte de una regla general: medio por defecto, alto para razonamiento profundo. El desglose por rol es **hipótesis** y se calibra midiendo rondas de auditoría por nivel.
6. **Plan Pro.** Según el artículo de soporte de Anthropic sobre los modelos Fable, en el plan Pro esos modelos no entran en los límites del plan: corren con créditos de uso, que se pagan aparte. Por eso el modelo más capaz de esta tabla es Opus 5.5 y Fable queda fuera del enrutamiento. Opus es el que más rápido gasta el límite de 5 horas, así que se reserva para el Jefe de pits, el mecánico experto y el árbitro de error costoso.
7. **Modelos externos** (R-50). La tabla de modelos externos lleva fecha de verificación; con más de 30 días, el Jefe de pits la verifica en la web antes de despachar, y si una fuente dice otra cosa, gana la fuente. Un mecánico externo equivale a un auxiliar o a un estándar ligero (redactar o resumir con poco criterio y una sola fuente), nunca a un experto. Verificación del 2026-11-21: Codex con GPT-6 Luna, velocidad estándar, en la app de escritorio de ChatGPT (el plan Free no incluye el CLI), y Antigravity, app o CLI, con Gemini 3.8 Flash y cuota semanal.

## 8. Modos de ejecución

| Modo | Qué es | Cuándo | Cómo se fija modelo y esfuerzo | Estado |
|---|---|---|---|---|
| **A. Subagentes** | Mecánicos dentro de la sesión del Jefe de pits | Encargos de menos de una hora; lectura y análisis; funciona también en el chat | Parámetros del despacho o definición del agente | **v1** |
| **B. Sesiones paralelas** | Cada mecánico es una sesión completa de la pestaña Code; el Jefe de pits las lista, lee y les escribe | Trabajos largos; cuando quieres entrar a la sesión de un mecánico a corregir | Selector de cada sesión. La sesión la abres tú y pegas la línea de arranque | **v1** |
| **C. Projects** | Coordinador con hilos, en la nube o en tu equipo | Trabajo de días que debe seguir con el equipo apagado | Ajustes del proyecto | Por evaluar si tu cuenta lo tiene (H7) |
| **D. Agent teams** | Líder con compañeros y lista de tareas compartida | — | Se nombra el modelo al crear cada compañero | Fuera: experimental, sin reanudación |
| **E. Bahías externas** | Un encargo lo ejecuta una IA de otro proveedor (Codex, Antigravity) en una carpeta aislada del mismo proyecto; el Jefe de pits integra y audita en Claude | 3 o más encargos independientes y alguno de rutina, o probar una skill o un prompt en otro modelo (R-47) | Selector de la herramienta externa; el despacho los escribe (R-49) | **v1.3** |

**Cuánto cumple cada modo el requisito de que el Jefe de pits despache tras tu aprobación:**
- **Modo A: lo cumple.** El Jefe de pits lanza los mecánicos con el modelo y el esfuerzo del plan.
- **Modo B: a medias.** Las sesiones las abres tú, con instrucciones exactas del Jefe de pits (nombre de la sesión, modelo, esfuerzo y línea de arranque). No está confirmado que Claude pueda crear sesiones en la app de escritorio.
- **Modo C: lo cumple**, y es el único en que Claude inicia sesiones completas. Depende de que tu cuenta tenga Projects (H7).
- **Modo E: a medias, como el B.** Abres tú la herramienta externa en la bahía y pegas el texto del despacho; el aviso de fin es manual ("terminó E0x").

**Modo E en breve** (pasos en `references/modos-de-ejecucion.md`):
- **Bahía** (R-48): `pit-lane/bahias/E0x-<herramienta>/` con `AGENTS.md` (copia de `references/mecanico-externo.md`, instrucciones válidas para cualquier IA, sin subagentes ni reglas de Claude), `ENCARGO.md` (copia del encargo; el ejecutor solo escribe en "Avance"), `entrada/` (copias de solo lectura) y `salida/` (lo único escribible). Si el proyecto usa git, la bahía puede ser un worktree. Antes de despachar, el Jefe de pits toma un inventario con el hash de cada archivo de la carpeta del trabajo.
- **Despacho** (R-49): un bloque fijo por encargo, con ID, herramienta, modelo y razonamiento; la carpeta; el texto que se pega, y el aviso "terminó E0x". Una corrección vuelve con el mismo formato.
- **Integración y auditoría** (R-51): con "terminó E0x", el Jefe de pits lee el informe de "Avance", compara el inventario, copia `salida/` al entregable y lanza el árbitro en Claude, como en el modo A. Si un criterio falla dos rondas seguidas, el encargo pasa a un mecánico Claude (R-27).

## 9. Estado y reanudación

Una carpeta por trabajo: la que indique el usuario o, si no indica ninguna, el directorio de trabajo de la sesión. Dentro va `pit-lane/`; `entrada/` y `entregables/` son la organización sugerida y el contrato puede fijar otras rutas:

```
<carpeta del trabajo>/
├── entrada/
├── entregables/
└── pit-lane/
    ├── contrato.md
    ├── datos-maestros.md
    ├── estado.md             ← una línea por encargo; solo la escribe el Jefe de pits
    ├── encargos/E01-….md
    ├── bahias/E03-codex/     ← solo modo E: AGENTS.md · ENCARGO.md · entrada/ · salida/ (R-48)
    └── auditorias/           ← E01.md, E02.md… (la lleva el Jefe de pits en modos A y E y el mecánico en modo B), inventarios del modo E y coherencia.md (el Jefe de pits)
```

- `estado.md` usa tres grupos: **trabajando**, **esperan tu decisión**, **terminados**.
- Tras cualquier corte: el Jefe de pits lee `estado.md` y los encargos **antes** de confiar en lo que recuerda, y reanuda cada mecánico en su última línea de avance.
- Cambio de un dato compartido: se edita `datos-maestros.md`, el Jefe de pits busca qué encargos lo citan y avisa solo a esos mecánicos.
- Ajuste pequeño y localizado: se le pide directo al mecánico. Pasarlo por el Jefe de pits procesa el contexto dos veces.
- **Quién escribe qué.** El mecánico actualiza "Estado", "Avance" y "Qué no funcionó" en su propio encargo. El Jefe de pits es el único que escribe `estado.md`, y lo hace leyendo los encargos.
- **Cómo se entera el Jefe de pits de que un mecánico terminó.** En el modo A, el resultado vuelve solo. En el modo E, el usuario avisa "terminó E0x". En el modo B, el Jefe de pits pide el aviso de inactividad de la sesión de cada mecánico si la herramienta lo permite (H4); si no, relee los encargos cada vez que el usuario pide estado o avisa "terminó E0x".
- **Mecánico bloqueado o sin contexto.** El Jefe de pits resuelve con el contrato y los datos maestros si alcanza. Si no, pasa el encargo a "esperan tu decisión", detiene también los encargos que dependen de él y sigue despachando los independientes. Al resolverse, se relanza con el mismo modelo.

## 10. Verificación y auditoría

0. **Quién lanza cada auditoría.** En M, la sesión que construye. En L y XL, modo A, el Jefe de pits lanza el árbitro de cada encargo (`pit-lane:arbitro`, con el modelo y el esfuerzo de la línea "Árbitro:" del encargo) y lleva su bitácora en `pit-lane/auditorias/E0x.md`: no se cuenta con que un subagente lance a otro (decisión 2026-11-14, H10). En modo B, cada mecánico lanza el árbitro de su encargo con esos mismos valores y lleva su bitácora; si no puede lanzar subagentes, devuelve "auditoría: pendiente" y la lanza el Jefe de pits. En modo E, el Jefe de pits lanza el árbitro en Claude sobre el entregable integrado (R-51): el árbitro nunca corre en la herramienta externa. La auditoría de coherencia la lanza el Jefe de pits cuando todos los encargos terminaron, con bitácora en `pit-lane/auditorias/coherencia.md`.
1. **El mecánico prueba** su entregable sobre el archivo real, con el método por tipo de gauntlet. Es necesario y no basta.
2. **Árbitro nuevo por ronda**, con el contrato, las rutas y las fuentes. Veredictos: PASA, NO PASA, NO VERIFICABLE y DEFECTUOSO. NO VERIFICABLE bloquea salvo que el contrato lo marque como revisión humana; DEFECTUOSO sigue el punto 14.
3. **Coherencia entre entregables** (L y XL): un criterio del listón por cada dato maestro que aparece en más de un entregable.
4. **Un árbitro que falló o no corrió** se reintenta una vez; si vuelve a fallar se registra "no ejecutado", nunca "sin hallazgos".
5. **Disputas:** el constructor registra su objeción con evidencia que el árbitro pueda abrir; "fue intencional" no es evidencia. La resuelve un árbitro nuevo y el usuario la ve en el resumen. Si lo único pendiente son disputas y el entregable no cambió, es una disputa exprés: un árbitro nuevo resuelve solo esos criterios, sin ronda completa y sin consumir una de las 3 (R-46).
6. **Tope:** 3 rondas. Al tope se entrega con los pendientes a la vista.
7. **Sin subagentes** (por ejemplo, en un chat que no los tenga): vale el modo degradado de gauntlet, un pase separado sobre el archivo real, y el resumen empieza con **AUDITORÍA NO INDEPENDIENTE**.
8. **Render de documentos de Office.** Para los criterios visuales, `verificar_office.py --render` exporta el DOCX, PPTX o XLSX a PDF con Microsoft Office, y el árbitro lo lee página por página con su herramienta de lectura; `--recalcular` recalcula una copia de un XLSX con Excel. Sin Office ni alternativa, esos criterios son NO VERIFICABLE (decisión 2026-11-15).
9. **Revisores sin las instrucciones del proyecto** (R-40). Lectores y árbitro corren con `omitClaudeMd`: no cargan `CLAUDE.md` ni `AGENTS.md`. Lo que necesiten de esas reglas va en el contrato o en el encargo.
10. **Escalar** (R-41). Si la prueba del constructor existe pero no está en ningún archivo que el árbitro pueda abrir, el hallazgo no se disputa ni se corrige: queda NO PASA marcado ESCALADO, no cuenta para seguir el loop y va primero en "revisa tú".
11. **Fuentes web guardadas** (R-42). Cada página que se use como fuente se guarda como archivo antes de auditar, con un índice de URL y fecha de consulta; el árbitro coteja contra esa copia.
12. **Corregir no es rellenar** (R-43). Nada se agrega a un entregable o al contrato solo para que un revisor lo apruebe. En el plan y los encargos, el contexto que le falta a un lector le falta al mecánico, y se agrega.
13. **Pre-vuelo del listón** (R-44). Antes de pedir la aprobación, quien redacta el contrato ejecuta una vez el método de cada criterio con las herramientas del árbitro y anota el resultado en la línea "Pre-vuelo:". Un ✘ cambia de método o pasa a revisión humana antes de aprobar. En L y XL va antes de los lectores.
14. **Criterio defectuoso** (R-45). El árbitro marca DEFECTUOSO un criterio que admite dos lecturas con veredictos opuestos, o que no puede pasar con lo que existe ni con lo que el contrato hará existir, y lo demuestra con evidencia. Sale del loop como un ESCALADO: no cuenta para seguir el loop ni para R-27 y va primero en "revisa tú". Solo el árbitro lo declara, y solo el usuario cambia el criterio, porque el listón sigue congelado.
15. **Mecánico vivo entre rondas** (R-46). En el modo A, el Jefe de pits devuelve los fallos al mismo mecánico continuando su subagente; solo lanza uno nuevo si ya no responde o si R-27 sube el modelo. El árbitro sigue siendo nuevo en cada ronda. Depende de H11.

## 11. Frenos

| Freno | Regla | Cómo se cumple |
|---|---|---|
| Rondas | Máximo 3 | Contrato |
| Mecánicos simultáneos | Por oleada, hasta 2 mecánicos Claude (plan Pro) y hasta 2 externos (1 por herramienta), 4 en total; expertos solo en Claude: 1, o 2 si no hay otro mecánico Claude trabajando (R-14) | Contrato; el Jefe de pits despacha por oleadas |
| Gasto | Al 80 % de la ventana de 5 horas no se despacha nada nuevo, tampoco a una bahía, porque su auditoría corre en Claude; cada mecánico escribe su avance y se detiene | El Jefe de pits lee el uso con `get_usage` de la app de escritorio; de respaldo, `~/.claude/pit-lane-uso.json`, que escribe el script de status line cuando Claude Code corre en la terminal; si ninguno responde, el freno lo activas tú con la palabra "freno" |
| Cuota externa | La de cada proveedor (en Antigravity, semanal); si se acaba, el mecánico externo escribe su avance y se detiene | `references/mecanico-externo.md` |
| Contexto del Jefe de pits | Los mecánicos devuelven ≤15 líneas y una ruta; el Jefe de pits no lee entregables completos | Formato del encargo |
| Compactación | Solo al cambiar de fase, con el estado ya escrito | Regla del flujo |

## 12. Cierre y aprendizaje

Entrega: los entregables, el resumen de auditoría y la lista "revisa tú".

Aprendizaje: el Jefe de pits propone candidatos a norma y da a cada uno un veredicto: **guardar**, **mejorar una existente**, **absorber en otra** o **descartar**. El usuario aprueba. Una corrección que se repite se convierte en propuesta de cambio a la skill.

## 13. Código y especificaciones de software

Cuando un entregable es código, instrucciones para otra IA (skill, prompt, agente) o una especificación de software, el encargo sigue `references/software.md` (R-34). Es el proceso propio de Pit Lane para estos casos, y no requiere ningún plugin externo:

- **Código:** rama aparte con línea base de pruebas verde; por cada comportamiento, una prueba que se ve fallar antes de escribir el código; causa raíz antes de cualquier arreglo, y tres arreglos fallidos detienen el encargo; el árbitro audita el diff y corre las pruebas él mismo; cada hallazgo se reproduce antes de corregirlo; la auditoría de coherencia corre la batería completa con todo integrado; el cierre presenta opciones (integrar, pull request o dejar la rama) y nada sale sin la decisión del usuario. 
- **Instrucciones para otra IA:** el mismo principio con un subagente nuevo como banco de pruebas: el caso se corre primero sin las instrucciones (o con la versión anterior) y se anota el fallo; después se escriben y el mismo caso debe pasar.
- **Especificación:** plantilla mínima (problema, estado actual, propuesta, alternativas, riesgos, cómo se mide, fuera de alcance); cero decisiones al implementador; cotejo de cada referencia a código existente contra el repositorio; y la pregunta de si hace falta construirlo o ya existe algo que lo resuelve.

*Por qué:* un documento se juzga leyéndolo; el código hay que ejecutarlo, y una especificación falla cuando alguien intenta construirla. Por eso cada paso pide evidencia que solo existe al ejecutar.

## 14. Qué queda fuera y por qué

| Fuera de la v1 | Motivo | Alternativa |
|---|---|---|
| Revisión de diseño en varias etapas con muchos revisores | Demasiadas paradas para el valor que agrega | Tres lectores de contexto limpio |
| Hooks y un observador en segundo plano que aprende solo | Complejidad alta; un observador así no funciona bien en Windows nativo | Aprendizaje con aprobación humana al cierre |
| Puntajes numéricos de calidad | El mismo agente se califica y un número no dice qué falla | Listón binario |
| Agent teams | Experimental | Modos A y B |
| Informe de deriva entre documentos y código | Útil solo cuando haya documentos vivos que mantener | Candidato a v2 |

## 15. Reglas numeradas

Las reglas que el repo implementa tienen un ID. La skill y los archivos de referencia las citan por ID.

| ID | Regla | Sección |
|---|---|---|
| R-01 | Triage con seis señales; gana el nivel más alto; se declara en una línea vetable | 3 |
| R-02 | Tamaño S: sin contrato; se hace y se dice qué se hizo | 3 |
| R-03 | En M, L y XL nada se construye sin contrato aprobado | 1 |
| R-04 | Ambigüedad crítica: hasta 4 preguntas con opción recomendada. Ambigüedad menor: decisión anotada | 16 |
| R-05 | Listón binario, con método y evidencia; congelado al aprobarse | 5 |
| R-06 | El contrato declara la frontera | 5 |
| R-07 | Lo compartido vive en `datos-maestros.md`; los encargos lo citan, no lo copian | 1 |
| R-08 | Una aprobación por tarea; dos en XL | 16 |
| R-09 | Tras aprobar, solo cuatro causas detienen: irreversible, sensible, sale a terceros, plan roto | 1 |
| R-10 | Un archivo por encargo, con la plantilla de la sección 6 | 6 |
| R-11 | Cada encargo declara su superficie de escritura; paralelo solo sin solape | 1 |
| R-12 | Cada encargo y cada despacho declaran modelo y esfuerzo | 7 |
| R-13 | Haiku solo con el encargo completo; en la duda, Sonnet | 7 |
| R-14 | Topes por oleada: hasta 2 mecánicos Claude y hasta 2 externos (1 por herramienta), 4 en total; expertos solo en Claude: 1, o 2 si no hay otro mecánico Claude trabajando | 11 |
| R-15 | Todo mecánico arranca con la línea estándar | 6 |
| R-16 | El mecánico prueba sobre el archivo real y devuelve uno de cuatro estados en 15 líneas o menos | 6, 10 |
| R-17 | El mecánico actualiza Estado, Avance y Qué no funcionó en su encargo | 9 |
| R-18 | `estado.md` lo escribe solo el Jefe de pits, en tres grupos | 9 |
| R-19 | Mecánico bloqueado: el Jefe de pits resuelve o pasa a "esperan tu decisión"; se detienen sus dependientes; el resto sigue | 9 |
| R-20 | Tras un corte, el Jefe de pits lee `estado.md` y los encargos antes de confiar en lo que recuerda | 9 |
| R-21 | Cambio de un dato compartido: se edita `datos-maestros.md` y se avisa solo a quien lo cita | 9 |
| R-22 | Ajuste pequeño y localizado: directo al mecánico | 9 |
| R-23 | Revisión del plan con contexto limpio antes de aprobar: L, lector de ejecución; XL, los tres lectores | 3 |
| R-24 | Auditoría con árbitro nuevo por ronda, sin el razonamiento del constructor, sobre todo el listón, máximo 3 rondas | 10, 16 |
| R-25 | Un árbitro que no corrió no cuenta como aprobación; un reintento | 10 |
| R-26 | Sin subagentes: modo degradado, declarado como AUDITORÍA NO INDEPENDIENTE | 10 |
| R-27 | Un criterio que falla dos rondas seguidas: cambio de enfoque y un nivel más de modelo | 7 |
| R-28 | Una disputa exige evidencia que el árbitro pueda abrir; la resuelve un árbitro nuevo, el de la ronda siguiente o uno exprés | 10 |
| R-29 | L y XL: un criterio de coherencia por cada dato maestro que aparece en más de un entregable | 10 |
| R-30 | Freno: al 80 % de la ventana de 5 horas, o con la palabra "freno", no se despacha; cada mecánico escribe su avance y se detiene | 11 |
| R-31 | El Jefe de pits no lee entregables completos; compacta solo al cambiar de fase y con el estado escrito | 11 |
| R-32 | Cierre: entregables, resumen de auditoría y "revisa tú" (primero ESCALADOS y DEFECTUOSOS) | 12 |
| R-33 | Aprendizaje: candidatos a norma con veredicto de cuatro salidas; aprueba el usuario | 12 |
| R-34 | Si el entregable es código, instrucciones para otra IA o una especificación de software, el encargo sigue `references/software.md` | 13 |
| R-35 | NO VERIFICABLE bloquea igual que NO PASA, salvo que el contrato lo marque como revisión humana | 10 |
| R-36 | Árbitro en modelo distinto del constructor cuando el error es costoso y el constructor no es Opus | 7 |
| R-37 | El Jefe de pits no construye entregables de tamaño L ni XL; copiar la salida de una bahía al entregable es integrar, no construir (R-51) | 4 |
| R-38 | Antes del primer despacho se comprueba que ninguna variable de entorno anule el enrutamiento | 7, 17 |
| R-39 | Dueño de cada auditoría: en M, la sesión; en L y XL, modo A, el Jefe de pits lanza el árbitro de cada encargo y lleva su bitácora; en modo B, cada mecánico lanza el suyo y lleva su bitácora (o lo lanza el Jefe de pits si el mecánico no puede lanzar subagentes); en modo E, el Jefe de pits, en Claude; el Jefe de pits lanza siempre la de coherencia | 10 |
| R-40 | Lectores y árbitro corren sin `CLAUDE.md` ni `AGENTS.md`; lo que necesiten de esas reglas va en el contrato o el encargo | 4, 10 |
| R-41 | Una prueba que el árbitro no puede abrir se escala: NO PASA marcado ESCALADO, fuera del loop y de R-27, primero en "revisa tú" | 10 |
| R-42 | Toda página web usada como fuente se guarda como archivo, con índice de URL y fecha, y el árbitro coteja contra la copia | 5, 10 |
| R-43 | Corregir no es rellenar: nada se agrega solo para el revisor; en el plan y los encargos, el contexto que falta a un lector se agrega | 10 |
| R-44 | Pre-vuelo del listón: el método de cada criterio se ejecuta una vez antes de aprobar; un ✘ cambia de método o pasa a revisión humana | 5, 10 |
| R-45 | Un criterio que el árbitro marca DEFECTUOSO, con evidencia, sale del loop como un ESCALADO; solo el usuario lo cambia | 10 |
| R-46 | Modo A: los fallos vuelven al mismo mecánico (se continúa su subagente); disputa exprés si lo único pendiente son disputas y el entregable no cambió | 8, 10 |
| R-47 | Modo E solo con 3 o más encargos independientes y alguno de rutina, o para probar una skill o un prompt en otro modelo; el encargo declara `Ejecutor:` y el modelo y el razonamiento del proveedor | 6, 8 |
| R-48 | Bahía por encargo externo: `AGENTS.md` (copia de `references/mecanico-externo.md`), `ENCARGO.md`, `entrada/` de solo lectura y `salida/`; el ejecutor escribe solo en `salida/` y en "Avance"; inventario antes de despachar | 8, 9 |
| R-49 | El despacho externo usa siempre el formato fijo de la plantilla, también para las correcciones | 8 |
| R-50 | Tabla de modelos externos fechada; con más de 30 días se verifica en la web antes de despachar; un externo es auxiliar o estándar ligero, nunca experto | 7 |
| R-51 | Con "terminó E0x": informe de "Avance", inventario comparado, `salida/` copiada al entregable y árbitro en Claude, que siempre corre en Claude | 8, 10 |

## 16. Decisiones de diseño y sus porqués

| Decisión | Por qué |
|---|---|
| **Una aprobación por tarea** (contrato con plan y enrutamiento); dos en XL. Fuera de eso, solo detienen las cuatro causas de R-09 | Decisión del autor (2026-11-07: un solo punto de validación por tarea). Cada parada extra cuesta tiempo sin agregar control: lo que importa se decide en el contrato. En XL el plan es demasiado grande para aprobarlo antes de que el contrato esté firme |
| **Separar planificar de coordinar.** Planifica el modelo más capaz con esfuerzo alto; coordina la misma sesión con esfuerzo medio | Planificar y enrutar es arquitectura y un error ahí se multiplica; seguir el estado o propagar un cambio no lo necesita. El valor por defecto de Projects va en la misma línea: coordinador con esfuerzo bajo, hilos con esfuerzo alto |
| **La severidad de un hallazgo la fija quien revisa** (lector o árbitro); el autor corrige, discute con evidencia o la muestra al usuario tal cual | Si el autor pudiera bajar la severidad, la revisión dejaría de filtrar |
| **Paralelo solo entre encargos cuya superficie de escritura no se solapa**; en serie cuando comparten archivo | Dos ejecutores sobre el mismo archivo se pisan; entregables separados pueden avanzar a la vez sin riesgo |
| **Tope de 3 rondas**; si un criterio falla dos seguidas, otro enfoque y un nivel más de modelo | Decisión del autor (2026-10-14). Pasadas tres rondas, las correcciones tienden a ser cosméticas; insistir con el mismo enfoque y el mismo modelo repite el mismo fallo |
| **Cada ronda re-audita todo el listón** | Con 5 a 12 criterios cuesta poco y atrapa regresiones: una corrección puede romper lo que antes pasaba |
| **El listón se prueba antes de aprobarlo** (pre-vuelo, R-44) | Un criterio que el árbitro no puede verificar sale NO VERIFICABLE y no se arregla editando el entregable: gasta las 3 rondas. Detectarlo antes de aprobar cuesta una ejecución por criterio |
| **Un criterio mal escrito tiene salida** (DEFECTUOSO, R-45) y el listón sigue congelado | El listón congelado impide mover la portería, pero sin esta salida un criterio ambiguo o imposible gira hasta el tope de rondas. Lo declara solo el árbitro, con evidencia, y lo decide el usuario, así que el constructor no gana una vía para esquivar un criterio |
| **Árbitro nuevo, mecánico vivo** (R-46) | La independencia la necesita quien juzga, no quien corrige. Relanzar al mecánico en cada ronda le hace leer todo de nuevo; continuarlo conserva lo que ya probó. Una disputa sola, sin cambios en el entregable, no justifica re-auditar todo el listón |
| **Preguntas en un solo bloque** de hasta 4, cada una con opción recomendada; lo menor se decide y se anota. 2 o 3 enfoques solo si hay una elección real de diseño | Un bloque ahorra paradas, y lo anotado sigue siendo vetable |
| **Sonnet redacta y analiza**; Haiku solo si el encargo trae el texto ya decidido; Opus solo para diseño difícil | Un documento con criterio no es "estructura simple". El modelo barato toma más turnos cuando tiene que interpretar, y eso cuesta más que su precio por token |
| **Listón binario**, no puntajes | Lo binario se verifica; un puntaje lo pone el mismo que construyó y no dice qué falla |
| **Dos skills** (`pit-lane` y `gauntlet`) en vez de una por fase | Menos archivos, y gauntlet sigue sirviendo sola para tareas M |
| **Modos A y B en la v1**, E desde la v1.3; C por evaluar; D fuera | A y B cubren trabajos cortos y largos con lo que la app ofrece hoy; E suma IA de otros proveedores para la rutina; C depende de la cuenta (H7); D es experimental |
| **Plan Pro**: máximo 2 mecánicos Claude simultáneos y Opus 5.5 como modelo más capaz | Más mecánicos Claude a la vez agotan antes la ventana de 5 horas; los modelos Fable corren con créditos aparte. Si se sube de plan, se puede volver a 3 mecánicos y a Fable |
| **Modo E: carriles externos en el mismo proyecto**, hasta 2 (1 por herramienta) | Los planes gratis de otros proveedores suman capacidad sin gastar la ventana de Claude en rutina. Un carril por herramienta porque cada una se abre a mano y comparte una sola cuota |
| **La bahía aísla y el inventario comprueba** | Otra IA no carga las reglas de Pit Lane ni sus permisos: sus instrucciones pueden ignorarse sin aviso. Copias de solo lectura limitan el daño y el hash antes y después hace verificable qué tocó (H12) |
| **El árbitro corre siempre en Claude**, y el externo nunca es experto | El método del árbitro, el contexto limpio y las herramientas de verificación son de Claude; el criterio difícil se queda donde el enrutamiento está garantizado por configuración |
| **Copiar la salida es integrar, no construir** (R-37, R-51) | El Jefe de pits copia sin cambiar el contenido; si hubiera que editarlo, es una corrección y vuelve a la bahía |
| **gauntlet vive en este repo** | Es la única fuente: la copia de la cuenta de claude.ai se exporta desde `skills/gauntlet/` |

## 17. La plataforma: qué ofrece Claude Code

Comprobado en la documentación oficial de Claude Code (code.claude.com, consultada el 2026-11-13) y en el piloto.

**Lo que se puede imponer por configuración** (por eso el enrutamiento no queda en buenas intenciones):
- Un subagente acepta `model` (`sonnet`, `opus`, `haiku`, `fable`) y `effort` (`low` a `max`) en su definición y en cada invocación. La invocación gana a la definición. El parámetro de esfuerzo por invocación requiere Claude Code v2.1.292 o posterior.
- En la app de escritorio cada sesión tiene su selector de modelo y de esfuerzo.
- En Projects hay ajustes separados de modelo y esfuerzo para el coordinador y para los hilos.
- Los subagentes anidan hasta 3 niveles por defecto, pero en el piloto no se comprobó que un mecánico lanzado como subagente pudiera lanzar al árbitro (H10).

**Lo que puede anular el enrutamiento sin avisar.** La variable `CLAUDE_CODE_EFFORT_LEVEL` tiene prioridad sobre el esfuerzo de la invocación y sobre el de la definición del agente; si está fijada en `settings.json`, toda la columna de esfuerzo se ignora. Lo mismo pasa con el modelo si está fijada `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`, sola o junto con `CLAUDE_CODE_SUBAGENT_MODEL`. Por eso R-38 las comprueba antes del primer despacho.

**Sesiones paralelas.** En la app de escritorio, Claude puede listar las otras sesiones de la pestaña Code, leer su actividad y enviarles mensajes; no está confirmado que pueda crearlas. La mensajería entre sesiones permite pedir un aviso cuando otra sesión de la misma máquina queda inactiva (`notify_when_idle`, v2.1.236 o posterior); no está confirmado entre sesiones de la app de escritorio (H4).

**Uso del plan.** El porcentaje de las ventanas de 5 horas y 7 días llega al script de status line, pero en el piloto la status line no corrió en la app de escritorio (H3 falló). La app sí expone el uso con `get_usage`, y el freno lo usa. En Projects, un hilo que alcanza el límite espera y continúa solo cuando se renueva.

**Otros.** Las normas comunes de un proyecto viven en `CLAUDE.md`. El control remoto (`/remote-control` o `/rc`) hace visibles las sesiones en la sección Code de la app móvil.

**Windows.** En agent teams, el modo de paneles divididos no funciona en Windows Terminal. La mensajería entre sesiones requiere v2.1.234 o posterior en Windows nativo. Una sesión en WSL 2 y una en Windows nativo no se ven entre sí.

## 18. Estructura del repositorio

El repo es un plugin de Claude Code que vive en tu carpeta personal de skills: `~/.claude/skills/pit-lane/` (en Windows, `C:\Users\<tu usuario>\.claude\skills\pit-lane\`). Una carpeta ahí que contiene `.claude-plugin/plugin.json` se carga sola en cada sesión, sin instalarla.

```
pit-lane/
├── README.md
├── AGENTS.md                      manual del repo, menos de 100 líneas
├── LICENSE · NOTICE
├── .gitattributes                 finales de línea LF
├── .claude-plugin/plugin.json · marketplace.json
├── skills/
│   ├── pit-lane/SKILL.md          el Jefe de pits: fases F0 a F6
│   └── gauntlet/
│       ├── SKILL.md
│       ├── agents/arbitro.md      el método del árbitro (única fuente)
│       ├── references/plantillas.md
│       ├── references/verificacion-por-tipo.md
│       ├── references/liston-base-ejemplo.md   formato del listón base personal (~/.claude/pit-lane-liston-base.md, fuera del repo)
│       └── scripts/verificar_office.py · office.ps1
├── agents/
│   ├── mecanico.md                sonnet · medium
│   ├── mecanico-experto.md        opus · high
│   ├── mecanico-auxiliar.md       haiku · low
│   ├── lector-ingenuo.md          sonnet · high    (solo XL; tabla de la sección 7)
│   ├── lector-critico.md          opus · high      (solo XL; tabla de la sección 7)
│   ├── lector-ejecucion.md        sonnet · medium  (en XL el despacho declara high)
│   └── arbitro.md                 opus · high · envoltorio que remite a skills/gauntlet/agents/arbitro.md
├── references/
│   ├── plantillas.md              contrato, encargo, estado
│   ├── enrutamiento.md            tabla de la sección 7 y reglas
│   ├── modos-de-ejecucion.md      modos A, B y E paso a paso
│   ├── mecanico-externo.md        instrucciones del mecánico para cualquier IA (modo E, R-48)
│   └── software.md                código y especificaciones de software (R-34)
├── scripts/
│   ├── uso-statusline.ps1         freno de gasto (respaldo en la terminal)
│   └── LEEME.md                   cómo activarlo
└── docs/
    ├── diseno.md                  este documento
    ├── decisiones.md              registro de decisiones fechadas
    └── manual-de-uso.md           guía corta para usarlo
```

- **Nombres una vez cargado.** Todo lleva el prefijo del plugin: las skills son `/pit-lane:pit-lane` y `/pit-lane:gauntlet`; los agentes son `pit-lane:mecanico`, `pit-lane:mecanico-experto`, `pit-lane:mecanico-auxiliar`, `pit-lane:lector-ingenuo`, `pit-lane:lector-critico`, `pit-lane:lector-ejecucion` y `pit-lane:arbitro`. La skill del Jefe de pits los llama siempre con prefijo.
- **Sin duplicados.** La verificación por tipo y `verificar_office.py` viven solo dentro de `skills/gauntlet/`; la skill `pit-lane` remite a ellos. El resumen de auditoría es el de gauntlet.
- **Texto propio.** Todo el repo está escrito de cero, en español.

## 19. Historia de la construcción

La v1 se construyó en once pasos, cada uno en un chat nuevo con su modelo y esfuerzo, y un commit local por paso:

| Paso | Qué |
|---|---|
| 0 | Insumos: el documento de diseño y gauntlet tal como estaba |
| 1 | Esqueleto: `plugin.json`, `LICENSE`, `NOTICE`, `README.md`, `docs/decisiones.md` |
| 2 | Tres ajustes a gauntlet para reconocer el contrato de Pit Lane |
| 3 | Los archivos de `references/` |
| 4 | Script del freno de gasto y revisión de variables de entorno |
| 5 | Los 7 agentes |
| 6 | `skills/pit-lane/SKILL.md` y `AGENTS.md` |
| 7 | Auditoría del repo contra el diseño |
| 8 | Correcciones de la auditoría y comprobación de que el plugin carga |
| 9 | Piloto con una tarea real de tamaño L |
| 10 | Ajustes del piloto |

Después vinieron el paso 11 (gauntlet V2.1), la revisión integral del 2026-11-14 y la versión 1.0 de este documento (2026-11-15), que lo reescribió como especificación propia e integró el proceso de software. El detalle de cada cambio está en `docs/decisiones.md` y en el historial de git.

## 20. Hipótesis

| # | Hipótesis | Cómo se valida | Si falla | Resultado |
|---|---|---|---|---|
| H1 | La tabla de esfuerzo es adecuada | Rondas de auditoría por encargo | Subir un nivel el esfuerzo del rol que más rondas necesite | Abierta: se calibra con el uso |
| H2 | Haiku 5.5 acepta esfuerzo bajo y rinde en encargos de rutina | Un encargo de rutina | El mecánico auxiliar pasa a Sonnet, esfuerzo medio | Abierta |
| H3 | El script de status line corre en la app de escritorio en Windows | Piloto | Freno manual | **Falló**: el freno lee el uso con `get_usage` (decisión 2026-11-14) |
| H4 | En la app de escritorio el Jefe de pits puede leer y escribir a las sesiones de los mecánicos, y recibir el aviso cuando quedan inactivas | Uso en modo B | Solo modo A, más aviso manual del usuario ("terminó E0x") | Abierta |
| H5 | Una sola aprobación basta para tamaño L | Uso en L | Añadir la aprobación en dos tiempos también a L | Abierta; el piloto L corrió con una |
| H6 | Tres lectores encuentran lo que importa sin una revisión en varias etapas | Comparar en un plan XL | Sumar un lector de estructura | Abierta |
| H7 | Tu cuenta tiene Projects | Mirar la barra lateral de la pestaña Code | El modo C queda fuera | Abierta |
| H8 | `CLAUDE_CODE_EFFORT_LEVEL` y `CLAUDE_CODE_SUBAGENT_MODEL` no están fijadas | R-38 en cada despacho | Quitarlas, con tu aprobación, o aceptar que el enrutamiento por agente no aplica | Se comprueba en cada trabajo |
| H9 | El plugin en `~/.claude/skills/pit-lane/` carga con sus 7 agentes también en la app de escritorio | Sesión nueva | Declarar la carpeta en `CLAUDE_CODE_PLUGIN_DIRS` | **Se cumple** en el equipo del autor; sin comprobar en otros |
| H10 | Un mecánico lanzado como subagente puede lanzar a su vez el árbitro | Piloto, modo A | El Jefe de pits lanza los árbitros | No se cuenta con ello: en modo A el Jefe de pits lanza los árbitros (decisión 2026-11-14) |
| H11 | Continuar un subagente con SendMessage conserva su contexto en Claude Code (R-46) | Prueba del 2026-11-21 y uso en modo A | Volver a relanzar al mecánico en frío, con la línea de arranque | **Se cumple** en la prueba del 2026-11-21: el subagente terminó su turno, se continuó con SendMessage y recordó el dato del primer turno. Falta confirmarlo en un encargo real |
| H12 | Codex y Antigravity siguen el `AGENTS.md` de la bahía y solo escriben en `salida/` y en "Avance" (R-48) | Prueba real con un encargo de rutina en cada herramienta, inventario antes y después (R-51) | La herramienta que escribió fuera sale del modo E hasta una nueva prueba; si las dos fallan, la bahía se arma siempre como copia descartable o worktree | **Se cumple para Antigravity** en la prueba del 2026-11-21: dos bahías con Gemini 3.8 Flash (Medium), y el inventario solo mostró cambios en `salida/` y en "Avance". **Codex sin probar.** El inventario no ve escrituras fuera de la carpeta del trabajo |

---

## Anexo — Documentación de la plataforma

- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/agents
- https://code.claude.com/docs/en/agent-view
- https://code.claude.com/docs/en/agent-teams
- https://code.claude.com/docs/en/claude-projects
- https://code.claude.com/docs/en/desktop
- https://code.claude.com/docs/en/cross-session-messaging
- https://code.claude.com/docs/en/remote-control
- https://code.claude.com/docs/en/statusline
- https://code.claude.com/docs/en/plugins
- https://code.claude.com/docs/en/plugins/create
- https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan
