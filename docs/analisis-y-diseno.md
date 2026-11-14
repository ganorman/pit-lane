# Pit Lane — metodología unificada: análisis comparativo y diseño

**Versión 0.7 · noviembre 2026**
Autor del análisis: Jefe de pits (Fable 5.2). Lectores: 4 × Sonnet 5.5, esfuerzo medio. Estado: aprobado por Gerardo; v1 construida (pasos 0 a 10), piloto hecho y ajustes de gauntlet V2.1 aplicados. La versión 0.7 incorpora las decisiones del 2026-11-14 registradas en `docs/decisiones.md`.

> **Crítico independiente (Opus 5.5, esfuerzo alto), tres rondas, el tope.** Ronda 1: RECHAZADO (2 bloqueos, 11 mayores, 8 menores). Ronda 2: APROBADO CON CORRECCIONES (4 mayores, 5 menores). Ronda 3: APROBADO CON CORRECCIONES (3 mayores, 5 menores, sin bloqueos). La versión 0.4 aplicó las correcciones de las tres rondas. **Las 8 correcciones de la ronda 3 no pasaron por una cuarta auditoría, y el cambio de nombre a Pit Lane (versión 0.5) y el ajuste al plan Pro (versión 0.6) se hicieron después.** Informes en `docs/critica-ronda1.md`, `critica-ronda2.md` y `critica-ronda3.md`.

---

> **Nombres.** El sistema se llama **Pit Lane**, por la parada en pits de la Fórmula 1: un equipo de especialistas que trabaja en paralelo, cada uno en lo suyo, y nadie suelta el carro hasta que todo está verificado. En este documento, "Colmena" (con sus términos Reina y obreras) es solo el nombre de una de las cinco fuentes. En el diseño, la Reina pasa a ser el **Jefe de pits** y las obreras, los **mecánicos**. Las fichas y los informes del crítico usan los nombres anteriores.

## 0. Resumen

1. Las cinco fuentes no compiten entre sí: cada una domina una capa distinta. Unificar es apilar capas y resolver siete contradicciones concretas (sección 4).
2. La capa más fuerte de cada una:
   - **gauntlet**: contrato con listón binario congelado y árbitro independiente sobre el archivo real.
   - **Superpowers**: reglas de enrutamiento de modelo, ledger para reanudar y ejecución sin paradas con cuatro excepciones.
   - **EGM**: revisores de contexto limpio antes de construir y reglas para discutir un hallazgo.
   - **ECC**: clasificador de tamaño, regla de superficie de escritura y archivo de traspaso con "qué no funcionó".
   - **Colmena**: topología Reina, obreras y subagentes, encargo en archivo y freno de gasto.
3. Sobre **esfuerzo de razonamiento** solo ECC da una regla, y es gruesa: medio por defecto, alto para razonamiento profundo. El desglose de esfuerzo por rol de este diseño es propuesta propia y queda como hipótesis a calibrar en el piloto.
4. La Colmena del video existe en Claude Code en tres formas documentadas (sesiones paralelas de la app de escritorio con mensajería entre sesiones, Projects y agent teams). Solo en Projects es Claude quien inicia las sesiones. El freno del 80 % no es nativo: hay que construirlo.
5. El sistema propuesto cabe en **2 skills, 7 agentes y 3 archivos de referencia**. Para software no copia a Superpowers ni a EGM: los usa como plugins instalados.
6. La construcción se reparte en 11 pasos (del 0 al 10) para otros chats, cada uno con modelo, esfuerzo y encargo (sección 8).

---

## 1. Fuentes y método

| Fuente | Versión leída | Qué se leyó |
|---|---|---|
| Superpowers (obra) | v7.0.2, commit `22f0b46`, 2026-11-03 | Las 15 skills completas y sus prompts de subagente |
| Superpowers (versión de Gerardo) | skill de cuenta, 128 líneas | Completa |
| EGM (Google) | commit `964a4f1`, 2026-11-13 | 7 skills, 10 agentes, estándares de documento, 5 diseños |
| ECC (affaan-m) | v2.2.3, commit `d2ef268`, 2026-11-06 | Núcleo metodológico: 27 comandos, 11 agentes, 21 skills de orquestación; reglas comunes, hooks, sesiones, memoria, coste |
| gauntlet (Gerardo) | skill de cuenta | `SKILL.md`, `agents/arbitro.md`, `references/plantillas.md`, índice de `verificacion-por-tipo.md` |
| Colmena | archivo adjunto (transcripción de un video, fuente única F1) | Completo |
| Documentación de Claude Code | code.claude.com, consultada el 2026-11-13 | sub-agents, agents, agent-view, agent-teams, claude-projects, desktop, cross-session-messaging, remote-control, statusline |

**Convención de citas.** `SP:`, `EGM:` y `ECC:` son rutas relativas a la raíz de cada repo, con número de línea. Las fichas completas de cada lector están en `fichas/`.

**Límites de este análisis.**
- De ECC se leyó el núcleo metodológico, no los 314 directorios de skills ni los revisores por lenguaje.
- Las fichas las escribieron lectores Sonnet; cada uno reabrió entre 9 y 16 de sus citas y el Jefe de pits comprobó otras 23 directamente.
- De la documentación oficial se leyeron las páginas citadas, algunas parcialmente por tamaño (desktop: 200 de 203 mil caracteres; sub-agents y agent-view: los primeros 100 mil).

---

## 2. Qué aporta cada fuente

| Fuente | Capa que domina | Lo que tiene y las otras no | Dónde es débil |
|---|---|---|---|
| **gauntlet** | Verificación del entregable | Listón de criterios binarios con método y evidencia, congelado al aprobarse; árbitro nuevo en cada ronda que no ve el razonamiento del constructor; métodos de verificación para 11 tipos de entregable (DOCX, PPTX, XLSX, citas bíblicas, SOP…); veredicto "no verificable" que bloquea | No planifica trabajo en paralelo, no enruta modelos, no revisa el diseño antes de construir |
| **Superpowers** | Proceso de software de principio a fin | Reglas de modelo por rol (`SP:skills/subagent-driven-development/SKILL.md:140-175`); ledger que sobrevive a la compactación (`SP:skills/executing-plans/SKILL.md:132-140`); ejecución sin paradas con solo cuatro causas para detenerse (`:39-43`); informe del ejecutor en menos de 15 líneas con cuatro estados (`SP:skills/subagent-driven-development/implementer-prompt.md:140-146`) | Casi todo asume git, tests y ramas; 4 a 5 paradas fijas; sin definición de "listo" para documentos |
| **EGM** | Revisión del diseño antes de construir | Revisores sin la conversación previa, cada uno con una persona distinta; lector ingenuo que primero parafrasea (`EGM:agents/comprehension.md:37`); reglas para discutir un hallazgo con evidencia (`EGM:skills/egm-resolve/SKILL.md:71-80`); convergencia formal (`EGM:skills/egm-review-loop/SKILL.md:169-181`); informe de deriva entre documento y código | Unas 20 paradas en un recorrido completo; no ejecuta ni verifica el entregable; sin reglas de modelo |
| **ECC** | Catálogo y operación del harness | Clasificador de tamaño "el nivel más alto gana" (`ECC:skills/orch-pipeline/SKILL.md:41-50`); paralelo solo si las superficies de escritura no chocan (`ECC:skills/parallel-execution-optimizer/SKILL.md:35-42`); archivo de sesión con sección obligatoria de lo que no funcionó (`ECC:commands/save-session.md:101-104`); meta con frontera "qué no debe hacer" (`ECC:skills/loop-design-check/SKILL.md:51-56`); veredicto Guardar/Mejorar/Absorber/Descartar para lo aprendido (`ECC:commands/learn-eval.md:95-100`) | Familias de flujo redundantes; seis contradicciones internas sobre modelos; depende de tmux, Codex, hooks y Node; casi todo es para código |
| **Colmena** | Topología de ejecución | Un solo canal con la Reina; obreras como sesiones completas para trabajos largos; propagación de un dato a quien depende de él; encargo en archivo con arranque estándar; tres estados de rendición de cuentas; freno al 80 %; criterio de cuándo hablar con la obrera directamente | Fuente única sin verificar; no define calidad, criterios ni revisión; no dice qué modelo usa cada obrera |

**Tu versión de Superpowers** ya hizo parte de la unificación: generalizó el alcance a documentos y estrategias, añadió una fase propia de criterios de calidad y marcó supuestos. Perdió lo que más valor tiene del original: persistencia, topes de loop, revisores independientes y reglas de modelo.

---

## 3. Matriz comparativa paso a paso

Clasificación: **U** único (solo una fuente lo tiene bien resuelto), **E** equivalente (varias hacen lo mismo; se fusionan), **C** contrapuesto (se contradicen; hay que elegir).

| # | Paso | Superpowers | EGM | ECC | gauntlet | Colmena | Tipo | Más fuerte |
|---|---|---|---|---|---|---|---|---|
| 1 | Decidir cuánta ceremonia merece la tarea | Atajo "hazlo y di qué hiciste" (`SP:skills/brainstorming/SKILL.md:22-24`) y dos tamaños vetables, cambio pequeño o proyecto (`:209-224`) | No | Clasificador por señales | Solo por petición explícita | Trabajo largo frente a tarea rápida | E | ECC |
| 2 | Entender el pedido | Una pregunta a la vez, 2 a 3 enfoques | Interrogatorio y 7 lentes en paralelo | 4 fases con puertas; "TBD" en vez de inventar | Ambigüedad crítica (≤4 preguntas con opción recomendada) o menor (decisión anotada) | No | C | gauntlet |
| 3 | Criterios de éxito antes de construir | Dispersos en el plan | Estándares de documento | Rúbricas y meta con frontera | Listón binario congelado | No | E | gauntlet |
| 4 | Aprobación humana | 4 a 5 paradas fijas | ≈20 | 2 puertas | 1 (el contrato) | Decisiones puntuales y validación final | C | gauntlet y ECC |
| 5 | Revisar el diseño con contexto limpio | 1 lector ("builder check") | 5 etapas, 8 revisores, sintetizador | Revisor adversarial en `blueprint` | No | No | U | EGM |
| 6 | Partir en tareas | Tareas con archivos, interfaces y pasos | Regla "cero decisiones al ejecutor" | Matriz de carriles | Plan interno por ronda | Un archivo de encargo por trabajo | E | SP + Colmena |
| 7 | Elegir modelo por tarea | Regla por rol; siempre explícito | Hereda el de la sesión | Reglas contradictorias | No | No | U | Superpowers |
| 8 | Elegir esfuerzo por tarea | No (solo para Codex) | No | Medio por defecto, alto para razonamiento profundo (`ECC:rules/common/performance.md:48-50`; `ECC:docs/token-optimization.md:35`) | No | No | U | ECC (regla gruesa, sin desglose por rol) |
| 9 | Despachar en paralelo | Solo problemas independientes; nunca ejecutores en paralelo (`SP:skills/subagent-driven-development/SKILL.md:235`) | Revisores en paralelo, etapas en serie | Solo si no chocan las escrituras | No | La Reina abre obreras | C | ECC (regla) + Colmena (forma) |
| 10 | Mantener sincronizado un dato compartido | Restricciones globales en el plan | No | Notas compartidas | No | La Reina propaga el cambio | E | Colmena |
| 11 | Persistir y reanudar | Ledger; confiar en él antes que en la memoria | Informes; sin archivo de estado | Archivo de sesión de 10 secciones | Bitácora | Encargo y estado en archivo | E | SP + ECC |
| 12 | Prueba del constructor | Evidencia fresca antes de afirmar | No | Loop de verificación (código) | Comprobaciones sobre el archivo real, por tipo | "La Reina revisa la miel" | E | gauntlet |
| 13 | Auditoría independiente del entregable | Revisor por tarea y revisor final (código) | No | Dos revisores aislados (`ECC:skills/santa-method/SKILL.md:79-82`) con rúbrica de pasa o falla (`:126-128`) | Árbitro nuevo por ronda | No | E | gauntlet |
| 14 | Tope de rondas | 5 por tarea; sube de modelo en la 4 | 5, y 2 limpias seguidas | 3 (santa); 15 (GAN) | 3 | No | C | gauntlet |
| 15 | Discutir un hallazgo | Verificar antes de aceptar | Solo con evidencia legible por el revisor | Verificador adversarial | Disputa registrada, la resuelve el árbitro siguiente | No | E | gauntlet + EGM |
| 16 | Hacer visibles las decisiones autónomas | "Rulings" listados al final | Solo elige el autor | "TBD" | "Decisiones tomadas" vetables | No | E | gauntlet |
| 17 | Cuidar el contexto | Artefactos en archivo, briefs por tarea | El sintetizador devuelve solo un resumen | Compactar en cambio de fase (`ECC:skills/strategic-compact/SKILL.md:82-89`) | Detalle en bitácora | Separar en sesiones | E | SP + ECC |
| 18 | Frenar el gasto | Modelo mínimo suficiente | No | Avisos informativos, sin freno | Tope de rondas | Parar al 80 % con cierre ordenado | U | Colmena |
| 19 | Entregar y cerrar | Menú de cierre de rama | PR humano | Puerta antes del commit | Entregable, resumen de auditoría y "revisa tú" | Miel en la carpeta; validación final del usuario | E | gauntlet |
| 20 | Aprender del trabajo | Skills probadas con tests | No | Veredicto de 4 salidas; "instincts" | No | Normas comunes actualizadas | E | ECC + tu `AGENTS.md` |
| 21 | Supervisar sin interrumpir | No | No | Estado de loops | No | Chat lateral, control remoto, 3 estados | U | Colmena |
| 22 | Detectar deriva después de entregar | No | Informe de deriva | No | No | No | U | EGM (fuera de la v1) |

---

## 4. Contradicciones y cómo las resuelvo

| # | Conflicto | Posiciones | Resolución | Por qué |
|---|---|---|---|---|
| C1 | **Cuántas veces se detiene** | Superpowers 4 a 5; EGM ≈20; ECC 2; gauntlet 1 | **Una aprobación** (contrato con plan y enrutamiento). Excepción: tamaño XL lleva dos (contrato, luego plan). Fuera de eso, solo se detiene por las cuatro causas de Superpowers | Es tu decisión registrada en `memoria/MEMORIA.md` (entrada del 2026-11-07: un solo punto de validación por tarea). La propia Superpowers ejecuta sin parar una vez aprobado el plan. Las ≈20 paradas de EGM son un conteo del lector (ficha 02, apartado 3), no un dato que EGM declare |
| C2 | **Quién orquesta** | ECC: Sonnet orquesta y Haiku ejecuta (`ECC:rules/common/performance.md:5-18`). Superpowers admite un orquestador de gama media. Tú pides el modelo más capaz arriba | Separar **planificar** de **coordinar**. Planifica el modelo más capaz con esfuerzo alto. Coordinar (seguir estado, propagar un cambio) no lo necesita | Planificar y enrutar es una tarea de arquitectura, y para esas Superpowers también manda el modelo más capaz (`SP:skills/subagent-driven-development/SKILL.md:148`). El valor por defecto de Projects va en la misma línea: coordinador en esfuerzo bajo, hilos en alto |
| C3 | **Ejecutores en paralelo** | Superpowers lo prohíbe; la Colmena vive de eso | Paralelo **solo** entre encargos cuya superficie de escritura no se solapa; en serie cuando comparten archivo | La prohibición de Superpowers es por conflictos en un mismo código. El ejemplo de la Colmena son tres entregables separados. La regla de ECC cubre los dos casos |
| C4 | **Tope de rondas** | 3 (gauntlet, santa), 5 (Superpowers, EGM), 15 (GAN) | **3 rondas.** Si un criterio falla dos seguidas, se cambia de enfoque y se sube un nivel de modelo | Tu decisión registrada en `memoria/MEMORIA.md` (entrada del 2026-10-14: tope de 3 rondas). De Superpowers se toma la subida de modelo, no las cinco rondas |
| C5 | **Qué se vuelve a auditar** | Superpowers re-revisa solo el arreglo; gauntlet re-audita todo el listón | Todo el listón en cada ronda | Con 5 a 12 criterios cuesta poco y detecta regresiones |
| C6 | **Cómo se pregunta** | Superpowers y EGM: una pregunta por turno, varios turnos. gauntlet: un solo bloque de hasta 4 | Un bloque de hasta 4 preguntas críticas con opción recomendada; lo menor se decide y se anota | Menos paradas. De Superpowers se conserva presentar 2 o 3 enfoques solo cuando hay una elección real de diseño |
| C7 | **Qué modelo redacta y analiza** | ECC: escribir documentos va a Haiku (`ECC:the-longform-guide.md:124`) y research y análisis a Opus (`ECC:rules/common/performance.md:18`). Superpowers: piso de gama media para quien trabaja desde una descripción en prosa (`SP:skills/subagent-driven-development/SKILL.md:164-170`) | **Sonnet** para redactar con criterio y para analizar; Haiku solo si el encargo trae el texto ya decidido; Opus solo para diseño difícil | Tu trabajo principal son documentos, y un documento con criterio no es "estructura simple". El modelo barato toma más turnos cuando tiene que interpretar, y eso cuesta más que el precio por token. Es la contradicción de enrutamiento que más te afecta |

---

## 5. La Colmena frente a la documentación oficial

| Afirmación del video | Veredicto | Qué dice la documentación |
|---|---|---|
| Hay una función que trabaja con archivos locales y trabajos largos, en la pestaña Code de la app de escritorio | **Verificado** | Sesiones de Claude Code en la app de escritorio |
| La Reina abre sesiones obreras | **Parcial** | Están documentadas tres formas de que un Claude coordine sesiones: (a) en la app de escritorio, Claude puede listar las otras sesiones de la pestaña Code, leer su actividad y enviarles mensajes; no confirmé que pueda **crearlas**; (b) **Projects**, en beta pública para Pro y Max: una conversación coordinadora que inicia "hilos" en la nube o en tu computadora por Remote Control; (c) **agent teams**, experimental y desactivado por defecto. No pude identificar cuál usa el video |
| Cada obrera despliega subagentes | **Verificado** | Subagentes con contexto propio; anidan hasta 3 niveles por defecto |
| Normas comunes en `cloud.md` | **Verificado** | Es `CLAUDE.md` |
| Control remoto con `/rc` y sesiones visibles en el móvil | **Verificado** | `/remote-control` o `/rc`; aparecen en la sección Code de la app móvil; en la app de escritorio hay un ajuste para conectar las sesiones nuevas |
| La Reina vigila el porcentaje del plan y frena al 80 % | **No nativo** | El porcentaje de las ventanas de 5 horas y 7 días llega al script de la *status line* (página statusline). La app de escritorio muestra el uso del plan en el anillo junto al selector de modelo (página desktop). No encontré que el modelo pueda leerlo por sí mismo, ni que el script de status line corra dentro de la app (hipótesis H3). En Projects, un hilo que alcanza el límite espera y continúa solo cuando se renueva |
| Al volver el límite, la Reina reactiva todo | **Viable** | Depende de los archivos de encargo y estado, que son del método, no de la herramienta |
| 23 trabajos largos en 2,5 días | **No verificable** | Anécdota de la fuente |
| "Chat lateral" | **Sin verificar** | No lo busqué a fondo |

**Lo que sí se puede imponer por configuración** (y por eso el enrutamiento no queda en buenas intenciones):
- Un subagente acepta `model` (`sonnet`, `opus`, `haiku`, `fable`) y `effort` (`low` a `max`) en su definición y en cada invocación. La invocación gana a la definición. El parámetro de esfuerzo por invocación requiere Claude Code v2.1.292 o posterior.
- En la app de escritorio cada sesión tiene su selector de modelo y de esfuerzo.
- En Projects hay ajustes separados de modelo y esfuerzo para el coordinador y para los hilos.

**Lo que puede anular el enrutamiento sin avisar.** La variable `CLAUDE_CODE_EFFORT_LEVEL` tiene prioridad sobre el esfuerzo de la invocación y sobre el de la definición del agente. Si está fijada en `settings.json` (ECC recomienda fijarla, `ECC:docs/token-optimization.md:14-19`), toda la columna de esfuerzo se ignora. Lo mismo pasa con el modelo si está fijada `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`, sola o junto con `CLAUDE_CODE_SUBAGENT_MODEL`. El paso 4 de la construcción comprueba que no lo estén.

**Aviso de cierre entre sesiones.** La mensajería entre sesiones permite que una sesión pida un aviso cuando otra de la misma máquina queda inactiva (`notify_when_idle`, v2.1.236 o posterior). No confirmé que esté disponible entre sesiones de la app de escritorio (hipótesis H4).

**Advertencias para tu equipo (Windows).** En agent teams, el modo de paneles divididos no funciona en Windows Terminal. La mensajería entre sesiones requiere v2.1.234 o posterior en Windows nativo. Una sesión en WSL 2 y una en Windows nativo no se ven entre sí.

---

## 6. Diseño unificado

Desde aquí se usan los nombres de Pit Lane: **Jefe de pits** (la Reina de la fuente Colmena) y **mecánicos** (las obreras).

### 6.1 Principios

1. **Contrato antes de construir.** Nada se genera sin TAREA, LISTÓN y ENTREGABLE aprobados. *(gauntlet, Superpowers)*
2. **Ceremonia proporcional.** El tamaño de la tarea decide cuántas fases corren. *(ECC)*
3. **Una aprobación, luego de corrido.** Solo detienen el trabajo: algo irreversible, algo sensible, algo que sale a terceros, o un plan roto. *(gauntlet, Superpowers, tu `AGENTS.md`)*
4. **El encargo vive en un archivo.** La conversación es volátil; el archivo es la verdad. *(Colmena, Superpowers, ECC)*
5. **Cada dato tiene un solo dueño.** Lo compartido vive en un archivo de datos maestros; los encargos lo citan, no lo copian. *(tu `AGENTS.md`, Colmena)*
6. **Paralelo solo si no chocan las escrituras.** *(ECC)*
7. **El modelo menos potente que alcance, siempre declarado.** Se sube de nivel solo cuando el inferior falla. *(Superpowers, ECC)*
8. **Quien construye no se audita.** Árbitro nuevo, sin el razonamiento del constructor, sobre el archivo real. Un revisor que no corrió no cuenta como aprobación. *(gauntlet, EGM, ECC)*
9. **Topes en todo.** Rondas, mecánicos simultáneos y gasto. *(gauntlet, Colmena)*

### 6.2 Flujo

```
F0 TRIAGE      → tamaño S / M / L / XL (una línea, vetable)
F1 CONTRATO    → tarea, frontera, listón, entregable, datos maestros, decisiones tomadas
F2 PLAN        → encargos con superficie de escritura, dependencias, modelo y esfuerzo
                 (L: revisión del plan por el lector de ejecución · XL: por los tres lectores)
══ APROBACIÓN ══ Gerardo aprueba contrato + plan + enrutamiento   (XL: contrato y plan por separado)
F3 DESPACHO    → el Jefe de pits escribe los archivos y lanza los mecánicos por oleadas
F4 EJECUCIÓN   → cada mecánico: construir → probar → informe de ≤15 líneas → estado
F5 AUDITORÍA   → árbitro nuevo por ronda contra el listón; máx. 3 rondas   (= gauntlet)
F6 CIERRE      → entregables, resumen de auditoría, "revisa tú", candidatos a norma
```

### 6.3 Triage

Se evalúan seis señales y **gana el nivel más alto** que alcance cualquiera. El Jefe de pits lo declara en una línea y Gerardo puede vetarlo. Excepción (decisión 2026-11-14, piloto): las fuentes externas por sí solas suben a L, no a XL; llegan a XL solo si el costo del error también es alto.

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
| **M** | Es gauntlet tal como lo usas hoy: contrato corto en el chat (listón de 5 a 8, sin bloque PLAN), la sesión construye y lanza el árbitro, loop de hasta 3 rondas con el árbitro que fije MÉTODO (por defecto Opus 5.5, alto, si sale a terceros, se proyecta en público o es difícil de revertir; Sonnet 5.5, medio, en el resto; decisión 2026-11-14, gauntlet V2.1), bitácora junto al entregable. Sin carpeta `pit-lane/` |
| **L** | Contrato, plan con encargos revisado por el lector de ejecución, mecánicos en paralelo, auditoría de cada encargo lanzada por el Jefe de pits en modo A (por su mecánico en modo B, decisión 2026-11-14) y auditoría de coherencia entre entregables lanzada por el Jefe de pits |
| **XL** | Como L, más revisión del plan con tres lectores y aprobación en dos tiempos |

### 6.4 Roles

| Rol | Qué hace | Qué recibe | Qué no recibe |
|---|---|---|---|
| **Gerardo** | Fija el objetivo, aprueba el contrato, decide lo irreversible, valida al final | — | — |
| **Jefe de pits** | Triage, contrato, plan, enrutamiento, despacho, estado, propagación de cambios, auditoría de coherencia, cierre | Todo | No construye entregables de tamaño L o XL |
| **Mecánico** | Un encargo de principio a fin: construye, prueba y pasa su entregable por el loop de auditoría. En modo B lanza él el árbitro; en modo A lo lanza el Jefe de pits (decisión 2026-11-14, H10) | Su archivo de encargo, las normas, los datos maestros | La conversación del Jefe de pits |
| **Subagente** | Una búsqueda o lectura acotada para un mecánico | La pregunta | Todo lo demás |
| **Lector** (antes de construir) | Busca huecos en el plan o el diseño | Solo el documento y lo que este enlaza | La conversación |
| **Árbitro** (después de construir) | Intenta rechazar el entregable con evidencia | Contrato, rutas de entregables y fuentes, fallos previos | El plan y el razonamiento del constructor |

Tres lectores, tomados de las personas de EGM y reescritos para trabajo general:
- **Lector ingenuo**: parafrasea primero; si no puede, es un bloqueo.
- **Lector crítico**: supuestos sin respaldo, riesgos sin mitigar, alternativas no consideradas.
- **Lector de ejecución**: pasos vagos y decisiones que el encargo deja al ejecutor.

### 6.5 Contrato

Es el contrato de gauntlet completo, con siete añadidos (marcados con ✚; INSTRUCCIONES ORIGINALES y completitud, decisión 2026-11-14):

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
                    + fuentes externas (gauntlet, Fase 0 paso 4): cada una con su comprobación ejecutable
                      (curl o WebFetch, o la lista de Drive); sin ella, NO VERIFICABLE (decisión 2026-11-14)
                    + criterios de coherencia entre entregables (solo L y XL) ✚
## ENTREGABLE       archivos, formato, restricciones
## DATOS MAESTROS ✚ ruta del archivo único con cifras, fechas, nombres y precios compartidos
## PLAN ✚           solo L y XL: tabla de encargos (ver 6.6) con modelo y esfuerzo
## PRESUPUESTO ✚    mecánicos simultáneos máx. 2 · freno de gasto
## Decisiones tomadas (vétalas si no te sirven)
```

Al aprobarse, el listón queda congelado: solo Gerardo lo cambia.

### 6.6 Encargo

Un archivo por encargo en `pit-lane/encargos/E01-nombre.md`. Fusiona el brief de Superpowers, la tarjeta de ECC, el archivo de encargo de la Colmena y la bitácora de gauntlet.

```markdown
# E01 — [nombre]
Estado: pendiente | en curso | en auditoría | terminado | espera decisión
Modelo: sonnet · Esfuerzo: medium · Modo: subagente | sesión
Árbitro: sonnet · medium   (opus · high si sale a terceros, se proyecta en público o es difícil de revertir)
Depende de: — | E0x
## Objetivo
## Entradas                 rutas (incluye normas y datos-maestros.md)
## Superficie de escritura  únicas rutas que puede crear o modificar
                            (incluye su bitácora: pit-lane/auditorias/E01.md)
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

Arranque estándar de todo mecánico: *"Tu encargo está en `<ruta>`. Léelo entero antes de nada y sigue desde donde se quedó."*

### 6.7 Enrutamiento de modelo y esfuerzo

| Trabajo | Modelo | Esfuerzo | Regla de origen |
|---|---|---|---|
| Jefe de pits: triage, contrato, plan, enrutamiento, resolver conflictos | Opus 5.5 | alto | Arquitectura va al más capaz (SP) |
| Jefe de pits: coordinar (estado, propagar cambios, despachar oleadas) | la misma sesión | medio | Propuesta propia |
| Lector del plan | Sonnet 5.5 (crítico en XL: Opus 5.5) | medio (alto en XL) | Revisión escalada al riesgo (SP) |
| Mecánico: redactar con criterio, analizar, integrar varias fuentes | Sonnet 5.5 | medio | Integración y juicio van al estándar (SP) |
| Mecánico experto: diseño difícil, decisiones con muchas dependencias | Opus 5.5 | alto | Arquitectura (SP, ECC) |
| Mecánico auxiliar: transcribir, convertir, formatear, inventariar, con todo especificado | Haiku 5.5 | bajo | Trabajo de rutina con especificación completa (SP, ECC) |
| Subagente de búsqueda o lectura | Haiku 5.5 | bajo | Exploración (ECC) |
| Árbitro, error costoso | Opus 5.5 | alto | Revisión final al más capaz (SP) |
| Árbitro, rutina | Sonnet 5.5 | medio | Revisión escalada al riesgo (SP) |

Reglas:
1. **El modelo y el esfuerzo se escriben siempre** en el encargo y en el despacho. Omitirlos hace que el mecánico herede los del Jefe de pits, que son los más caros. Antes del primer despacho se comprueba que `CLAUDE_CODE_EFFORT_LEVEL` no esté fijada, porque anula el esfuerzo de todos los agentes (sección 5).
2. **Haiku solo cuando el encargo lo trae todo.** Si el mecánico tiene que interpretar, el modelo barato toma dos o tres veces más turnos y termina costando más (`SP:skills/subagent-driven-development/SKILL.md:164-170`). En la duda, Sonnet.
3. **Escalada:** un criterio que falla dos rondas seguidas pasa a un modelo un nivel superior, con enfoque distinto. En el modo A el Jefe de pits relanza el encargo con el nuevo modelo. En el modo B el Jefe de pits le indica a Gerardo el modelo que debe poner en el selector de esa sesión.
4. **Árbitro en modelo distinto del constructor** cuando el error es costoso y el constructor no es Opus. Si el constructor es Opus, el árbitro también lo es: la independencia la da el contexto limpio, no el modelo.
5. La columna de esfuerzo parte de la regla gruesa de ECC (medio por defecto, alto para razonamiento profundo). El desglose por rol es **hipótesis** propia y se calibra en el piloto midiendo rondas de auditoría por nivel.
6. **Plan Pro.** Según el artículo de soporte de Anthropic sobre los modelos Fable, en el plan Pro esos modelos no entran en los límites del plan: corren con créditos de uso, que se pagan aparte. Por eso el modelo más capaz de esta tabla es Opus 5.5 y Fable queda fuera del enrutamiento. Opus es el que más rápido gasta el límite de 5 horas, así que se reserva para el Jefe de pits, el mecánico experto y el árbitro de error costoso.

### 6.8 Modos de ejecución

| Modo | Qué es | Cuándo | Cómo se fija modelo y esfuerzo | Estado |
|---|---|---|---|---|
| **A. Subagentes** | Mecánicos dentro de la sesión del Jefe de pits | Encargos de menos de una hora; lectura y análisis; funciona también en el chat | Parámetros del despacho o definición del agente | **v1** |
| **B. Sesiones paralelas** | Cada mecánico es una sesión completa de la pestaña Code; el Jefe de pits las lista, lee y les escribe | Trabajos largos; cuando quieres entrar a la sesión de un mecánico a corregir | Selector de cada sesión. La sesión la abres tú y pegas la línea de arranque | **v1** |
| **C. Projects** | Coordinador con hilos, en la nube o en tu equipo | Trabajo de días que debe seguir con el equipo apagado | Ajustes del proyecto | Evaluar en el piloto si tu cuenta lo tiene |
| **D. Agent teams** | Líder con compañeros y lista de tareas compartida | — | Se nombra el modelo al crear cada compañero | Fuera: experimental, sin reanudación |

**Cuánto cumple cada modo tu requisito de que el Jefe de pits despache tras tu aprobación:**
- **Modo A: lo cumple.** El Jefe de pits lanza los mecánicos con el modelo y el esfuerzo del plan.
- **Modo B: a medias.** Las sesiones las abres tú, con instrucciones exactas del Jefe de pits (nombre de la sesión, modelo, esfuerzo y línea de arranque). No confirmé que Claude pueda crear sesiones en la app de escritorio.
- **Modo C: lo cumple**, y es el único en que Claude inicia sesiones completas. Depende de que tu cuenta tenga Projects (H7).

### 6.9 Estado y reanudación

Carpeta por trabajo, dentro de tu estructura actual:

```
proyectos/<área>/AAAA-MM-DD_Tema/
├── entrada/
├── entregables/
└── pit-lane/
    ├── contrato.md
    ├── datos-maestros.md
    ├── estado.md             ← una línea por encargo; solo la escribe el Jefe de pits
    ├── encargos/E01-….md
    └── auditorias/           ← E01.md, E02.md… (cada mecánico la suya) y coherencia.md (el Jefe de pits)
```

- `estado.md` usa los tres grupos de la Colmena: **trabajando**, **esperan tu decisión**, **terminados**.
- Tras cualquier corte: el Jefe de pits lee `estado.md` y los encargos **antes** de confiar en lo que recuerda, y reanuda cada mecánico en su última línea de avance.
- Cambio de un dato compartido: se edita `datos-maestros.md`, el Jefe de pits busca qué encargos lo citan y avisa solo a esos mecánicos.
- Ajuste pequeño y localizado: se le pide directo al mecánico. Pasarlo por el Jefe de pits procesa el contexto dos veces.
- **Quién escribe qué.** El mecánico actualiza "Estado", "Avance" y "Qué no funcionó" en su propio encargo. El Jefe de pits es el único que escribe `estado.md`, y lo hace leyendo los encargos.
- **Cómo se entera el Jefe de pits de que un mecánico terminó.** En el modo A, el resultado vuelve solo. En el modo B, el Jefe de pits pide el aviso de inactividad de la sesión de cada mecánico si la herramienta lo permite (H4); si no, relee los encargos cada vez que Gerardo pide estado o avisa "terminó E0x".
- **Mecánico bloqueado o sin contexto.** El Jefe de pits resuelve con el contrato y los datos maestros si alcanza. Si no, pasa el encargo a "esperan tu decisión", detiene también los encargos que dependen de él y sigue despachando los independientes. Al resolverse, se relanza con el mismo modelo.

### 6.10 Verificación y auditoría

0. **Quién lanza cada auditoría.** En M, la sesión que construye. En L y XL, modo A, el Jefe de pits lanza el árbitro de cada encargo (`pit-lane:arbitro`, con el modelo y el esfuerzo de la línea "Árbitro:" del encargo) y lleva su bitácora en `pit-lane/auditorias/E0x.md`: no se cuenta con que un subagente lance a otro (decisión 2026-11-14, H10). En modo B, cada mecánico lanza el árbitro de su encargo con esos mismos valores y lleva su bitácora; si no puede lanzar subagentes, devuelve "auditoría: pendiente" y la lanza el Jefe de pits. La auditoría de coherencia la lanza el Jefe de pits cuando todos los encargos terminaron, con bitácora en `pit-lane/auditorias/coherencia.md`.
1. **El mecánico prueba** su entregable sobre el archivo real, con el método por tipo de gauntlet. Es necesario y no basta.
2. **Árbitro nuevo por ronda**, con el contrato, las rutas y las fuentes. Veredictos: PASA, NO PASA, NO VERIFICABLE. Este último bloquea salvo que el contrato lo marque como revisión humana.
3. **Coherencia entre entregables** (L y XL): un criterio del listón por cada dato maestro que aparece en más de un entregable.
4. **Un árbitro que falló o no corrió** se reintenta una vez; si vuelve a fallar se registra "no ejecutado", nunca "sin hallazgos".
5. **Disputas:** el constructor registra su objeción con evidencia que el árbitro pueda abrir; "fue intencional" no es evidencia. La resuelve el árbitro siguiente y Gerardo la ve en el resumen.
6. **Tope:** 3 rondas. Al tope se entrega con los pendientes a la vista.
7. **Sin subagentes** (por ejemplo, en un chat que no los tenga): vale el modo degradado de gauntlet, un pase separado sobre el archivo real, y el resumen empieza con **AUDITORÍA NO INDEPENDIENTE**.

### 6.11 Frenos

| Freno | Regla | Cómo se cumple |
|---|---|---|
| Rondas | Máximo 3 | Contrato |
| Mecánicos simultáneos | Máximo 2 por oleada (plan Pro) | Contrato; el Jefe de pits despacha por oleadas |
| Gasto | Al 80 % de la ventana de 5 horas no se despacha nada nuevo; cada mecánico escribe su avance y se detiene | **Por construir:** script de *status line* que escriba el porcentaje en `~/.claude/pit-lane-uso.json`, una ruta fija que el Jefe de pits lee desde cualquier trabajo. Mientras no exista, o si no corre en la app de escritorio, el freno lo activas tú con la palabra "freno" |
| Contexto del Jefe de pits | Los mecánicos devuelven ≤15 líneas y una ruta; el Jefe de pits no lee entregables completos | Formato del encargo |
| Compactación | Solo al cambiar de fase, con el estado ya escrito | Regla del flujo |

### 6.12 Cierre y aprendizaje

Entrega: los entregables, el resumen de auditoría y la lista "revisa tú".

Aprendizaje: el Jefe de pits propone candidatos a norma y da a cada uno un veredicto: **guardar**, **mejorar una existente**, **absorber en otra** o **descartar**. Gerardo aprueba. Una corrección que se repite se convierte en propuesta de cambio a la skill.

### 6.13 Qué queda fuera y por qué

| Fuera de la v1 | Motivo | Alternativa |
|---|---|---|
| TDD, worktrees, ramas, merge | Solo aplican a código | Si el entregable es código, se usa el plugin Superpowers dentro del encargo |
| Las 5 etapas y 8 revisores de EGM | ≈20 paradas | Tres lectores; para una especificación de software, el plugin EGM que ya tienes |
| Hooks, "instincts", observador en segundo plano de ECC | Complejidad alta; el observador no funciona en Windows nativo | Aprendizaje con aprobación humana al cierre |
| GAN, multi-modelo con Codex o Gemini, DevFleet, tmux | Infraestructura externa y coste | — |
| Puntajes numéricos de calidad | El mismo agente se califica; ECC los abandonó en `learn-eval` | Listón binario |
| Agent teams | Experimental | Modos A y B |
| Informe de deriva | Útil solo cuando haya documentos vivos que mantener | Candidato a v2 |

### 6.14 Reglas numeradas

Las reglas que el repo debe implementar tienen un ID. La skill y los archivos de referencia las citan por ID, y la auditoría del repo (paso 7) comprueba que estén todas.

| ID | Regla | Sección |
|---|---|---|
| R-01 | Triage con seis señales; gana el nivel más alto; se declara en una línea vetable | 6.3 |
| R-02 | Tamaño S: sin contrato; se hace y se dice qué se hizo | 6.3 |
| R-03 | En M, L y XL nada se construye sin contrato aprobado | 6.1 |
| R-04 | Ambigüedad crítica: hasta 4 preguntas con opción recomendada. Ambigüedad menor: decisión anotada | 4 (C6) |
| R-05 | Listón binario, con método y evidencia; congelado al aprobarse | 6.5 |
| R-06 | El contrato declara la frontera | 6.5 |
| R-07 | Lo compartido vive en `datos-maestros.md`; los encargos lo citan, no lo copian | 6.1 |
| R-08 | Una aprobación por tarea; dos en XL | 4 (C1) |
| R-09 | Tras aprobar, solo cuatro causas detienen: irreversible, sensible, sale a terceros, plan roto | 6.1 |
| R-10 | Un archivo por encargo, con la plantilla de 6.6 | 6.6 |
| R-11 | Cada encargo declara su superficie de escritura; paralelo solo sin solape | 6.1 |
| R-12 | Cada encargo y cada despacho declaran modelo y esfuerzo | 6.7 |
| R-13 | Haiku solo con el encargo completo; en la duda, Sonnet | 6.7 |
| R-14 | Máximo 2 mecánicos por oleada | 6.11 |
| R-15 | Todo mecánico arranca con la línea estándar | 6.6 |
| R-16 | El mecánico prueba sobre el archivo real y devuelve uno de cuatro estados en 15 líneas o menos | 6.6, 6.10 |
| R-17 | El mecánico actualiza Estado, Avance y Qué no funcionó en su encargo | 6.9 |
| R-18 | `estado.md` lo escribe solo el Jefe de pits, en tres grupos | 6.9 |
| R-19 | Mecánico bloqueado: el Jefe de pits resuelve o pasa a "esperan tu decisión"; se detienen sus dependientes; el resto sigue | 6.9 |
| R-20 | Tras un corte, el Jefe de pits lee `estado.md` y los encargos antes de confiar en lo que recuerda | 6.9 |
| R-21 | Cambio de un dato compartido: se edita `datos-maestros.md` y se avisa solo a quien lo cita | 6.9 |
| R-22 | Ajuste pequeño y localizado: directo al mecánico | 6.9 |
| R-23 | Revisión del plan con contexto limpio antes de aprobar: L, lector de ejecución; XL, los tres lectores | 6.3 |
| R-24 | Auditoría con árbitro nuevo por ronda, sin el razonamiento del constructor, sobre todo el listón, máximo 3 rondas | 6.10, 4 (C4 y C5) |
| R-25 | Un árbitro que no corrió no cuenta como aprobación; un reintento | 6.10 |
| R-26 | Sin subagentes: modo degradado, declarado como AUDITORÍA NO INDEPENDIENTE | 6.10 |
| R-27 | Un criterio que falla dos rondas seguidas: cambio de enfoque y un nivel más de modelo | 6.7 |
| R-28 | Una disputa exige evidencia que el árbitro pueda abrir | 6.10 |
| R-29 | L y XL: un criterio de coherencia por cada dato maestro que aparece en más de un entregable | 6.10 |
| R-30 | Freno: al 80 % de la ventana de 5 horas, o con la palabra "freno", no se despacha; cada mecánico escribe su avance y se detiene | 6.11 |
| R-31 | El Jefe de pits no lee entregables completos; compacta solo al cambiar de fase y con el estado escrito | 6.11 |
| R-32 | Cierre: entregables, resumen de auditoría y "revisa tú" | 6.12 |
| R-33 | Aprendizaje: candidatos a norma con veredicto de cuatro salidas; aprueba Gerardo | 6.12 |
| R-34 | Si el entregable es código o una especificación de software, el encargo usa el plugin Superpowers o EGM | 6.13 |
| R-35 | NO VERIFICABLE bloquea igual que NO PASA, salvo que el contrato lo marque como revisión humana | 6.10 |
| R-36 | Árbitro en modelo distinto del constructor cuando el error es costoso y el constructor no es Opus | 6.7 |
| R-37 | El Jefe de pits no construye entregables de tamaño L ni XL | 6.4 |
| R-38 | Antes del primer despacho se comprueba que ninguna variable de entorno anule el enrutamiento | 6.7 |
| R-39 | Dueño de cada auditoría: en M, la sesión; en L y XL, modo A, el Jefe de pits lanza el árbitro de cada encargo y lleva su bitácora; en modo B, cada mecánico lanza el suyo y lleva su bitácora (o lo lanza el Jefe de pits si el mecánico no puede lanzar subagentes); el Jefe de pits lanza siempre la de coherencia | 6.10 |

---

## 7. Estructura del repositorio

El repo es un plugin de Claude Code que vive en tu carpeta personal de skills: `~/.claude/skills/pit-lane/` (en Windows, `C:\Users\<tu usuario>\.claude\skills\pit-lane\`). Una carpeta ahí que contiene `.claude-plugin/plugin.json` se carga sola en cada sesión, sin instalarla.

```
pit-lane/
├── README.md
├── AGENTS.md                      manual, menos de 100 líneas
├── LICENSE · NOTICE               atribución a Superpowers (MIT), ECC (MIT) y EGM (Apache-2.0)
├── .gitattributes                 finales de línea LF en el repo (decisión 2026-11-14)
├── .claude-plugin/plugin.json
├── skills/
│   ├── pit-lane/SKILL.md           triage, contrato, plan, despacho, cierre
│   └── gauntlet/                  tu skill, con tres ajustes (paso 2)
│       ├── SKILL.md
│       ├── agents/arbitro.md
│       ├── references/plantillas.md
│       ├── references/verificacion-por-tipo.md
│       └── scripts/verificar_office.py
├── agents/
│   ├── mecanico.md                sonnet · medium
│   ├── mecanico-experto.md        opus · high
│   ├── mecanico-auxiliar.md       haiku · low
│   ├── lector-ingenuo.md          sonnet · high    (solo XL; tabla 6.7)
│   ├── lector-critico.md          opus · high      (solo XL; tabla 6.7)
│   ├── lector-ejecucion.md        sonnet · medium  (en XL el despacho declara high)
│   └── arbitro.md                 opus · high · envoltorio que remite a skills/gauntlet/agents/arbitro.md
├── references/
│   ├── plantillas.md              contrato, encargo, estado
│   ├── enrutamiento.md            tabla 6.7 y reglas
│   └── modos-de-ejecucion.md      tabla 6.8 y pasos por modo
├── scripts/
│   ├── uso-statusline.ps1         freno de gasto
│   └── LEEME.md                   cómo activarlo
└── docs/
    ├── analisis-y-diseno.md       este documento
    ├── critica-ronda1.md          informes del crítico, uno por ronda
    ├── critica-ronda2.md
    ├── critica-ronda3.md
    ├── auditoria-gauntlet.md      informe del paso 7
    ├── decisiones.md
    ├── manual-de-uso.md           guía corta para usarlo (decisión 2026-11-14)
    └── fichas/                    las 4 fichas de los lectores
```

- **Nombres una vez cargado.** Todo lleva el prefijo del plugin: las skills son `/pit-lane:pit-lane` y `/pit-lane:gauntlet`; los agentes son `pit-lane:mecanico`, `pit-lane:mecanico-experto`, `pit-lane:mecanico-auxiliar`, `pit-lane:lector-ingenuo`, `pit-lane:lector-critico`, `pit-lane:lector-ejecucion` y `pit-lane:arbitro`. La skill del Jefe de pits los llama siempre con prefijo.
- **Dos gauntlet cargadas.** Tu skill de cuenta `gauntlet` seguirá cargada junto a `pit-lane:gauntlet`. El Jefe de pits usa siempre `pit-lane:gauntlet`, que es la que reconoce el contrato de Pit Lane. Sin Pit Lane, los únicos cambios de la ajustada son que el árbitro sale con modelo y esfuerzo declarados y que un árbitro fallido se reintenta una vez; por eso después del piloto puedes reemplazar la de cuenta por la ajustada (decisión 6 de la sección 10).
- **Sin duplicados.** La verificación por tipo y `verificar_office.py` viven solo dentro de `skills/gauntlet/`; la skill `pit-lane` remite a ellos. El resumen de auditoría es el de gauntlet.
- El texto del repo se escribe de cero, en español. Se toman ideas y estructuras, no archivos; el `NOTICE` acredita cada fuente. No soy abogado: si el repo llega a ser público, conviene revisar las licencias con alguien que lo sea.

---

## 8. Plan de construcción

Todo se construye en **Claude Code, en tu PC personal**, abriendo la carpeta `~/.claude/skills/pit-lane/`. Cada paso es un chat nuevo: pones en el selector el modelo y el esfuerzo indicados y pegas el encargo tal cual. La fuente de verdad es este documento, que ya estará en `docs/`.

| Paso | Qué | Modelo | Esfuerzo | Depende de | Oleada |
|---|---|---|---|---|---|
| 0 | Clonar `https://github.com/ganorman/pit-lane` en `~/.claude/skills/pit-lane/` y descomprimir ahí `pit-lane-inicio.zip` | lo haces tú | — | — | — |
| 1 | Esqueleto: `plugin.json`, `LICENSE`, `NOTICE`, `README.md`, `docs/decisiones.md` | Haiku 5.5 | bajo | 0 | — |
| 2 | Tres ajustes a `skills/gauntlet/SKILL.md` | Sonnet 5.5 | medio | 1 | A |
| 3 | Los 3 archivos de `references/` | Sonnet 5.5 | medio | 1 | A |
| 4 | Script del freno de gasto y revisión de variables de entorno | Sonnet 5.5 | medio | 1 | A |
| 5 | Los 7 archivos de `agents/` | Sonnet 5.5 | medio | 2 | B |
| 6 | `skills/pit-lane/SKILL.md` y `AGENTS.md` | Opus 5.5 | alto | 3 | B |
| 7 | Auditoría del repo contra este documento | Opus 5.5 | alto | 2 a 6 | — |
| 8 | Aplicar las correcciones del paso 7 y comprobar que el plugin carga | Sonnet 5.5 | medio | 7 | — |
| 9 | Piloto con una tarea real de tamaño L | Opus 5.5 | alto | 8 | — |
| 10 | Ajustes del piloto, `docs/decisiones.md` y subida | Sonnet 5.5 | medio | 9 | — |

`pit-lane-inicio.zip` trae `docs/` (este documento, las fichas y los informes del crítico) y `skills/gauntlet/` (tu skill tal como está hoy, sin cambios).

Dentro de cada oleada los pasos pueden correr a la vez, porque sus superficies de escritura son archivos distintos. Con el plan Pro conviene correrlos de uno en uno: en paralelo se llega antes al límite de 5 horas. Comparten el índice de git, y por eso cada encargo añade al commit solo sus propios archivos.

| Paso | Superficie de escritura |
|---|---|
| 1 | `.claude-plugin/plugin.json`, `LICENSE`, `NOTICE`, `README.md`, `docs/decisiones.md` |
| 2 | `skills/gauntlet/SKILL.md` |
| 3 | `references/plantillas.md`, `references/enrutamiento.md`, `references/modos-de-ejecucion.md` |
| 4 | `scripts/uso-statusline.ps1`, `scripts/LEEME.md` (y, fuera del repo, `~/.claude/pit-lane-uso.json`) |
| 5 | `agents/*.md` |
| 6 | `skills/pit-lane/SKILL.md`, `AGENTS.md` |
| 7 | `docs/auditoria-gauntlet.md` |
| 8 | Los archivos que el informe del paso 7 señale; `docs/decisiones.md`. Su commit incluye también `docs/auditoria-gauntlet.md` |
| 10 | Los archivos que el piloto señale; `docs/decisiones.md` |

### Encargos listos para pegar

> Registro histórico de la construcción: los encargos se dejan como se ejecutaron. Donde difieren de la sección 6 (por ejemplo, el paso 5 dice que el mecánico lanza siempre su árbitro), vale la sección 6 con las decisiones de `docs/decisiones.md`.

**Paso 1 — Haiku 5.5, esfuerzo bajo**
> Antes de crear nada, haz un commit local con lo que ya hay en el repo (`docs/` y `skills/gauntlet/`) con el mensaje "paso 0: insumos". Después crea solo estos cinco archivos. (1) `.claude-plugin/plugin.json` con `"name": "pit-lane"`, `"version": "0.1.0"`, `"description": "Metodología de trabajo con Claude: Jefe de pits que planifica y enruta, mecánicos en paralelo y árbitro independiente."` y `"author": {"name": "Gerardo Alberto Norman"}`. (2) `LICENSE` con el texto estándar de la licencia MIT en inglés, titular Gerardo Alberto Norman, año 2026. (3) `NOTICE` con estas tres líneas de atribución, indicando que se tomaron ideas y no archivos: obra/superpowers (MIT), affaan-m/ECC (MIT), google/elephant-goldfish-model (Apache-2.0). (4) `README.md` con exactamente este contenido: título "# Pit Lane"; un párrafo: "Metodología de trabajo con Claude: un Jefe de pits que planifica y enruta, mecánicos que ejecutan en paralelo y un árbitro independiente que audita."; y cuatro viñetas: "Qué es y por qué: `docs/analisis-y-diseno.md`", "Cómo se trabaja en este repo: `AGENTS.md`", "Skills: `skills/pit-lane` (flujo completo) y `skills/gauntlet` (auditoría)", "Créditos: `NOTICE`". (5) `docs/decisiones.md` con el título "# Decisiones" y una línea: "Una decisión por línea, con fecha AAAA-MM-DD." No crees carpetas vacías ni ningún otro archivo. Al terminar, lista lo creado y haz un commit local "paso 1: esqueleto" que incluya solo esos cinco archivos. No hagas push.

**Paso 2 — Sonnet 5.5, esfuerzo medio**
> Trabaja solo sobre `skills/gauntlet/SKILL.md`; no toques ningún otro archivo. Lee `docs/analisis-y-diseno.md`, secciones 6.5, 6.6, 6.9 y 6.10. Aplica exactamente tres ajustes, sin reescribir nada más. (1) Al inicio de la Fase 0, añade: si el trabajo tiene un `pit-lane/contrato.md` con la línea "Aprobado:", ese archivo es el contrato; la Fase 0 se omite; el listón que se audita es el de los IDs del encargo en curso, y la bitácora se escribe en `pit-lane/auditorias/<ID del encargo>.md` en vez de junto al entregable; en la auditoría de coherencia, que no tiene encargo, se auditan los criterios de coherencia del contrato y la bitácora es `pit-lane/auditorias/coherencia.md`. (2) En "Reglas del loop", añade: un árbitro que falla o no entrega informe se reintenta una vez y, si vuelve a fallar, la ronda se registra como "árbitro no ejecutado", nunca como aprobación. (3) En el paso "Auditar", añade: al lanzar el árbitro se declaran siempre modelo y esfuerzo: los de la línea "Árbitro:" del encargo en curso; si no hay encargo, los que fije el contrato en MÉTODO; y si el contrato no los fija, Sonnet con esfuerzo medio, u Opus con esfuerzo alto cuando el error es costoso; y si el agente `pit-lane:arbitro` está disponible, se lanza ese agente. El ajuste 1 aplica solo si existe `pit-lane/contrato.md`; los ajustes 2 y 3 aplican siempre. Conserva el estilo y el idioma del archivo. Muéstrame el `git diff` de los tres ajustes y haz un commit local "paso 2: gauntlet" que incluya solo ese archivo; si git informa de un bloqueo del índice, espera unos segundos y reintenta. No hagas push.

**Paso 3 — Sonnet 5.5, esfuerzo medio**
> Lee completo `docs/analisis-y-diseno.md` y `skills/gauntlet/references/plantillas.md`. Escribe tres archivos. `references/plantillas.md`: contrato de la sección 6.5, encargo de la 6.6 con su línea de arranque, y `estado.md` con los tres grupos de la 6.9; para el resumen de auditoría remite a la plantilla de gauntlet, no la copies. `references/enrutamiento.md`: tabla y reglas de la 6.7, más la advertencia de la sección 5 sobre las variables de entorno que anulan el enrutamiento. `references/modos-de-ejecucion.md`: tabla de la 6.8 y los pasos concretos de los modos A y B, incluido cómo se entera el Jefe de pits de que un mecánico terminó, qué pasa con un mecánico bloqueado y quién lanza cada auditoría, según la 6.9 y la 6.10. Junto a cada regla escribe su ID de la sección 6.14, por ejemplo "(R-12)". Los agentes se nombran con prefijo, como en la sección 7 (`pit-lane:mecanico`). Español latinoamericano, términos técnicos en inglés. No añadas reglas que no estén en el documento; si algo falta, márcalo **[CONFIRMAR]** y lístalo al final de tu respuesta. Haz un commit local "paso 3: references" que incluya solo esos tres archivos; si git informa de un bloqueo del índice, espera unos segundos y reintenta. No hagas push.

**Paso 4 — Sonnet 5.5, esfuerzo medio**
> Lee `docs/analisis-y-diseno.md`, secciones 5 y 6.11, y la documentación de la status line de Claude Code (https://code.claude.com/docs/en/statusline). Escribe `scripts/uso-statusline.ps1`: un script de status line en PowerShell que lea el JSON de entrada y guarde `rate_limits.five_hour.used_percentage`, `rate_limits.seven_day.used_percentage` y la hora en `~/.claude/pit-lane-uso.json`, sin fallar cuando esos campos falten, y que imprima una línea corta con los dos porcentajes. Escribe `scripts/LEEME.md` con cómo activarlo en `settings.json`. Pruébalo primero con un JSON de ejemplo pasado por la entrada estándar; no dejes ningún archivo de prueba dentro del repo. No cambies mi `settings.json` sin que yo lo apruebe: dime qué línea habría que añadir y, cuando la apruebe, dime con la salida real si el script se ejecuta en la app de escritorio o solo en la terminal. Si no se ejecuta en la app, dilo sin rodeos, porque entonces el freno queda manual. Además revisa si en mi `~/.claude/settings.json` o en el entorno están definidas `CLAUDE_CODE_EFFORT_LEVEL`, `CLAUDE_CODE_SUBAGENT_MODEL` o `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`, y repórtalo sin cambiarlas. Haz un commit local "paso 4: freno" que incluya solo los dos archivos de `scripts/`; si git informa de un bloqueo del índice, espera unos segundos y reintenta. No hagas push.

**Paso 5 — Sonnet 5.5, esfuerzo medio**
> Lee `docs/analisis-y-diseno.md`, secciones 6.4, 6.6, 6.7, 6.9, 6.10 y 7, y `skills/gauntlet/SKILL.md` y `skills/gauntlet/agents/arbitro.md`. Escribe los 7 archivos de `agents/` listados en la sección 7. En el frontmatter, `name` es el nombre del archivo sin prefijo (por ejemplo `mecanico`), y `description`, `model` y `effort` siguen esa lista. No declares `tools` en los mecánicos, para que puedan lanzar subagentes; en los lectores declara `tools: Read, Grep, Glob`; en el árbitro, `tools: Read, Grep, Glob, Bash`. Estructura de cada archivo: qué recibe y qué no recibe, rol, instrucciones numeradas, formato de salida. Los tres mecánicos: leen su encargo completo; escriben solo dentro de su superficie de escritura; construyen, prueban sobre el archivo real y pasan su entregable por el loop de `pit-lane:gauntlet`, y son ellos quienes lanzan el árbitro `pit-lane:arbitro` con el modelo y el esfuerzo que diga el encargo; llevan la bitácora en `pit-lane/auditorias/<ID>.md`; actualizan "Estado", "Avance" y "Qué no funcionó" en su encargo; y devuelven uno de los cuatro estados más el resultado de la auditoría en 15 líneas o menos. Si no pueden lanzar subagentes, devuelven "auditoría: pendiente" para que la lance el Jefe de pits. Los tres lectores son de solo lectura y entregan hallazgos con severidad (bloqueo, mayor, menor), ubicación y motivo; el lector ingenuo parafrasea primero. `agents/arbitro.md` es un envoltorio corto: su cuerpo ordena leer y seguir el `agents/arbitro.md` de la skill gauntlet, cuya ruta absoluta recibe en el despacho; no copies el contenido de ese archivo. Cita los ID de regla de la sección 6.14 que cada agente cumple. Haz un commit local "paso 5: agentes" que incluya solo `agents/`; si git informa de un bloqueo del índice, espera unos segundos y reintenta. No hagas push.

**Paso 6 — Opus 5.5, esfuerzo alto**
> Lee completo `docs/analisis-y-diseno.md` y los tres archivos de `references/`. Escribe `skills/pit-lane/SKILL.md`: la skill que convierte a la sesión en Jefe de pits. Debe cubrir las fases F0 a F6 de la sección 6.2; remitir a `references/` en vez de repetir su contenido; usar `pit-lane:gauntlet` (nunca la skill `gauntlet` sin prefijo) para la auditoría y para la verificación por tipo; y nombrar a los agentes con prefijo, exactamente como en la sección 7. Cada regla de R-01 a R-39 de la sección 6.14 debe aparecer con su ID, aquí o en el archivo de `references/` al que remitas. Cabecera con `name: pit-lane` y `description` (qué hace y cuándo activarla). Explica el porqué de cada regla en una frase. Menos de 250 líneas. Después escribe `AGENTS.md` en la raíz, de menos de 100 líneas: qué es el repo, cómo está organizado y cómo se trabaja en él. No modifiques `references/`; si encuentras una contradicción entre el documento y `references/`, repórtala y detente. Haz un commit local "paso 6: skill" que incluya solo esos dos archivos; si git informa de un bloqueo del índice, espera unos segundos y reintenta. No hagas push.

**Paso 7 — Opus 5.5, esfuerzo alto**
> Eres el árbitro de una auditoría. Lee primero `skills/gauntlet/agents/arbitro.md` y sigue su método y su formato de informe. No construiste este repo y no tienes por qué defenderlo. Audita el repositorio contra `docs/analisis-y-diseno.md` con este listón congelado. (L1) Los archivos versionados (`git ls-files`) son exactamente los de la sección 7, salvo `docs/auditoria-gauntlet.md`, que escribes tú en este paso, más `.gitignore` si existe; método: comparar las dos listas. (L2) Cada ID de R-01 a R-39 aparece en `skills/pit-lane/SKILL.md` o en `references/`; método: buscar cada ID. (L3) El `model` y el `effort` del frontmatter de cada agente coinciden con la sección 7. (L4) Para cada regla R-01 a R-39, el texto del repo que la cita no dice lo contrario de la sección 6; evidencia: cita de la línea. (L5) `AGENTS.md` tiene menos de 100 líneas y `skills/pit-lane/SKILL.md` menos de 250. (L6) Todo marcador CONFIRMAR entre corchetes que haya fuera de `docs/` aparece en tu informe con archivo y línea; método: buscar el marcador. Este criterio PASA si la lista está completa, aunque no esté vacía. (L7) La prosa escrita en los pasos 1 a 6 está en español latinoamericano; quedan fuera `LICENSE`, `NOTICE`, las claves de JSON y de frontmatter, los nombres de archivo y el código. (L8) `git diff` entre el commit "paso 0: insumos" y el actual, limitado a `skills/gauntlet/`, muestra solo los tres ajustes del paso 2. (L9) Ninguna skill ni agente nombra a un agente o a la skill gauntlet sin el prefijo `pit-lane:`, fuera de los campos `name` del frontmatter, de las rutas de archivo y del contenido original de `skills/gauntlet/`. Escribe el informe en `docs/auditoria-gauntlet.md` y no corrijas nada: corregir es el paso 8.

**Paso 8 — Sonnet 5.5, esfuerzo medio**
> Lee `docs/auditoria-gauntlet.md`. Corrige solo los criterios marcados NO PASA, sin tocar nada más, y anota cada corrección en `docs/decisiones.md` (una línea con fecha). Copia también a `docs/decisiones.md` cada marcador CONFIRMAR que liste el informe, como pendiente de mi decisión. Después comprueba que el plugin carga: ejecuta en la terminal `claude plugin validate .` y `claude plugin list` y muéstrame la salida real. Pídeme que ejecute `/reload-plugins` en una sesión y que te pegue la salida, y que confirme en una sesión nueva de la app de escritorio que `/pit-lane:pit-lane` aparece y que los 7 agentes se listan con el prefijo `pit-lane:`. Si ahí no carga, no cambies nada: dime qué viste y propón la alternativa de declarar esta carpeta en la variable `CLAUDE_CODE_PLUGIN_DIRS` de mi configuración de usuario, que solo aplicarás si yo la apruebo. Haz un commit local "paso 8: correcciones y carga", que incluya también `docs/auditoria-gauntlet.md`. No hagas push.

**Paso 9 — Opus 5.5, esfuerzo alto**
> /pit-lane:pit-lane — Tarea: [una tarea real tuya de tamaño L, con sus fuentes]. Al terminar dame, además de los entregables: cuántas rondas de auditoría necesitó cada encargo, con qué modelo y esfuerzo corrió cada uno, y qué regla de la skill estorbó o faltó.

**Paso 10 — Sonnet 5.5, esfuerzo medio**
> Lee el resultado del piloto que te pego abajo. Aplica solo los ajustes que yo marque como aprobados, registra cada decisión en `docs/decisiones.md` (una línea con fecha) y haz un commit local "paso 10: ajustes del piloto". No hagas push: muéstrame el resumen de cambios y espera mi confirmación para subir.

---

## 9. Riesgos e hipótesis por validar en el piloto

| # | Hipótesis | Cómo se valida | Si falla |
|---|---|---|---|
| H1 | La tabla de esfuerzo es adecuada | Rondas de auditoría por encargo en el piloto | Subir un nivel el esfuerzo del rol que más rondas necesite |
| H2 | Haiku 5.5 acepta esfuerzo bajo y rinde en encargos de rutina | Paso 1 y un encargo de rutina del piloto | El mecánico auxiliar pasa a Sonnet, esfuerzo medio |
| H3 | El script de status line corre en la app de escritorio en Windows | Paso 4 | Freno manual |
| H4 | En la app de escritorio el Jefe de pits puede leer y escribir a las sesiones de los mecánicos, y recibir el aviso cuando quedan inactivas | Piloto, modo B | Solo modo A, más aviso manual de Gerardo ("terminó E0x") |
| H5 | Una sola aprobación basta para tamaño L | Piloto | Añadir la aprobación en dos tiempos también a L |
| H6 | Tres lectores encuentran lo que importa sin las 5 etapas de EGM | Comparar un plan XL contra el plugin EGM | Sumar el lector de estructura |
| H7 | Tu cuenta tiene Projects | Mirar la barra lateral de la pestaña Code | El modo C queda fuera |
| H8 | `CLAUDE_CODE_EFFORT_LEVEL` y `CLAUDE_CODE_SUBAGENT_MODEL` no están fijadas en tu `settings.json` | Paso 4 | Quitarlas, con tu aprobación, o aceptar que el enrutamiento por agente no aplica |
| H9 | El plugin en `~/.claude/skills/pit-lane/` carga con sus 7 agentes también en la app de escritorio | Paso 8 | Declarar la carpeta en `CLAUDE_CODE_PLUGIN_DIRS`, en la configuración de usuario |
| H10 | Un mecánico lanzado como subagente puede lanzar a su vez el árbitro | Piloto, modo A | El Jefe de pits lanza los árbitros (regla R-39) |

---

## 10. Decisiones que necesito de ti

1. **Nombre y repo: decididos.** El sistema se llama Pit Lane; el plugin, `pit-lane`; el repo es `https://github.com/ganorman/pit-lane`.
2. **Dos skills** (`pit-lane` y `gauntlet`) en vez de una por fase. Recomiendo dos: menos archivos, y gauntlet sigue sirviendo sola.
3. **Aprobación en dos tiempos solo para XL.** Recomiendo que sí.
4. **Modos A y B en la v1**, C a evaluar, D fuera.
5. **Plan de Claude: Pro.** El máximo queda en 2 mecánicos simultáneos y el Jefe de pits corre en Opus 5.5 (regla 6 de la sección 6.7). Si subes a Max, se puede volver a 3 y a Fable.
6. **Tu gauntlet de cuenta.** Mientras se construye quedan dos cargadas. Recomiendo dejar la de cuenta como está hasta el piloto y reemplazarla después por la ajustada. Sin Pit Lane, sus únicos cambios son que el árbitro sale con modelo y esfuerzo declarados y que se reintenta una vez si falla.

---

## Anexo — Fuentes web

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
