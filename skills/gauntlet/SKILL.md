---
name: gauntlet
description: Modo de trabajo exhaustivo con árbitro adversarial independiente. Primero un contrato (TAREA, LISTÓN verificable, ENTREGABLE) que el usuario aprueba; después un loop autónomo construir → probar → auditar con un subagente árbitro nuevo en cada ronda → corregir, máximo 3 rondas, verificando el archivo real y cerrando con resumen de auditoría. Úsala cuando el usuario pida explícitamente trabajo exhaustivo o a prueba de fallos — "modo gauntlet", "pásalo por el gauntlet", "hazlo a fondo", "trabajo exhaustivo", "con árbitro", "audítalo hasta que pase", "no me entregues la primera versión", "quiero esto blindado". No la uses para tareas simples, para un trabajo con varios entregables, fuentes cruzadas o mecánicos en paralelo (eso es pit-lane:pit-lane, que para código sigue su proceso de software) ni para un fact-check puntual de un texto ya hecho.
---

# GAUNTLET

El fallo más caro de una IA en trabajo serio es declarar "listo" sin haber abierto el archivo, o auditarse a sí misma con el mismo razonamiento que produjo el error. GAUNTLET lo ataca con tres piezas: un **listón** de criterios binarios con método de verificación, un **árbitro** que no participó en la construcción, y un **loop** que solo termina cuando el árbitro aprueba el resultado real o se agota el tope de rondas.

Es caro en tiempo y tokens. Úsalo cuando el error cuesta más que el proceso: exámenes, procedimientos, SOP, hojas de cálculo con fórmulas, material que se proyecta en público, código que se va a usar, análisis con cifras.

## Flujo

```
FASE 0 — CONTRATO  (se detiene: el usuario aprueba)
   ↓
FASE 1 — LOOP (autónomo, sin paradas)
   Ronda N: planificar → construir → probar → ÁRBITRO (subagente nuevo) → ¿todo PASA?
            NO → corregir → Ronda N+1   (tope: 3 rondas)
            SÍ → salir
   ↓
FASE 2 — ENTREGA + RESUMEN DE AUDITORÍA + qué debe revisar el humano
```

---

## Fase 0 — Contrato

**Si el trabajo tiene un `pit-lane/contrato.md` con la línea "Aprobado:", ese archivo es el contrato y la Fase 0 se omite.** El listón que se audita es el de los IDs del encargo en curso, y la bitácora se escribe en `pit-lane/auditorias/<ID del encargo>.md` en vez de junto al entregable. En la auditoría de coherencia, que no tiene encargo, se auditan los criterios de coherencia del contrato y la bitácora es `pit-lane/auditorias/coherencia.md`.

El contrato es el plan. Aprobarlo autoriza el loop completo sin más paradas: sustituye la regla de "mostrar cada paso y esperar validación" para esta tarea, y cumple la regla de "plan antes del documento", porque ningún archivo se genera antes de la aprobación.

1. **Reúne contexto antes de escribir nada:** fuentes que dio el usuario, skills que aplican al entregable (docx, pptx, xlsx y las que el usuario tenga para ese tipo de trabajo), y las reglas permanentes del usuario (`~/.claude/pit-lane-liston-base.md` si existe, memoria, `CLAUDE.md` o `AGENTS.md`, preferencias).
2. **Clasifica las ambigüedades.**
   - **Crítica**: cambia qué se entrega, para quién, o produce algo irreversible (enviar, borrar, publicar). → Pregúntala ahora, máximo 4 preguntas, con opciones y una recomendada.
   - **Menor**: cualquier otra. → Decide, y anótala en el contrato como "Decisión tomada" para que el usuario pueda vetarla al aprobar.
3. **Escribe el contrato** con la plantilla de `references/plantillas.md`: TAREA, MÉTODO, LISTÓN, ENTREGABLE, rondas máximas y modo del árbitro. Tras TAREA añade la sección **INSTRUCCIONES ORIGINALES**: el pedido del usuario copiado literal y numerado (P1, P2…), sin resumir. Los adjuntos y documentos pegados largos no se copian: se citan por nombre o ruta y se numera lo que el usuario pide sobre ellos. El usuario lee esa sección y el listón antes de aprobar, porque es su único veto.
4. **Valida el listón antes de presentarlo.** Cada criterio debe tener:
   - **Qué se exige**, en forma que admita solo PASA o NO PASA.
   - **Método**: cómo se comprueba (comando, render, conteo, cotejo con la fuente X).
   - **Evidencia esperada**: qué debe mostrar el árbitro para dar PASA.

   Reescribe o elimina cualquier criterio vago ("profesional", "claro", "bonito", "completo"). Si el usuario da una referencia ("al nivel de X"), tradúcela a 2–4 rasgos observables de X. Entre 5 y 12 criterios específicos más el listón base: con menos de 5 la auditoría no discrimina; con más de 12, el loop se diluye en detalles.

   Antes de presentarlo, comprueba además tres cosas:
   - **Pasabilidad, con pre-vuelo ejecutado.** Cada criterio debe poder pasar con lo que existirá cuando se audite: los archivos, las fuentes y las herramientas que tendrá el árbitro (Read, Grep, Glob y Bash; no tiene WebFetch). Razonarlo no basta: ejecuta una vez el método de cada criterio con esas herramientas, sobre un archivo de prueba o sobre lo que ya exista. Comprueba que el comando existe y corre, que Microsoft Office está disponible si el método usa `--render` o `--recalcular`, y que cada fuente tiene su copia guardada o un paso del plan que la crea. Anota el resultado en el contrato en una sola línea, por ejemplo `Pre-vuelo: L1 ✔ · L2 ✔ · L5 ✘ (sin Office) → revisión humana`. Un criterio con ✘ cambia de método o pasa a revisión humana antes de pedir la aprobación; nunca se presenta un ✘ sin ese ajuste. Un criterio que exige algo que nada va a crear se corrige o se elimina.
   - **Fuentes externas.** Cada página web que use el entregable se guarda como archivo antes de auditar (en `fuentes/` junto al entregable; con Pit Lane, en `entrada/fuentes/`), con un índice `fuentes/LEEME.md`: archivo → URL → fecha de consulta. El árbitro coteja contra esa copia, que no cambia entre rondas. Las de Drive se citan con la lista tal como la devuelve el conector. Sin copia ni comprobación ejecutable (curl o WebFetch), el árbitro marca el criterio NO VERIFICABLE y lo dice.
   - **Completitud.** El listón lleva un criterio que exige que cada punto P1, P2… de INSTRUCCIONES ORIGINALES aparezca en el entregable, o que su ausencia sea una decisión anotada y vetable en "Decisiones tomadas". Método: tabla punto → ubicación en el entregable. Cuenta entre los 5 y 12 criterios.
5. **Presenta el contrato en el chat y detente.** Hasta la aprobación, el contrato vive solo en el chat: no crees ningún archivo, ni siquiera la bitácora. Solo una aprobación explícita arranca la Fase 1. Si pide cambios, ajusta y vuelve a presentar.
   - **Excepción: aprobación anticipada.** Si el usuario ya dijo en su pedido que aprueba de antemano o que arranques sin preguntar, no te detengas. Crea la bitácora con el contrato completo, muéstralo al inicio de tu respuesta para que pueda revisarlo, y sigue con el loop. Las ambigüedades críticas pasan a ser decisiones anotadas, salvo las irreversibles, que siguen deteniendo el trabajo.
6. **Al aprobarse, el listón queda congelado.** Solo el usuario lo cambia. Ni el constructor ni el árbitro añaden criterios a mitad del loop: así se evita mover la portería.

### Listón base (va en todo contrato, según aplique)

Son las reglas que valen para todo entregable. Inclúyelas en el contrato marcando cuáles aplican; no hace falta que el usuario las repita.

B1, B3, B4 y B6 toman su valor de las reglas permanentes del usuario: el archivo `~/.claude/pit-lane-liston-base.md` si existe (formato en `references/liston-base-ejemplo.md`), su memoria y su `CLAUDE.md` o `AGENTS.md`. Escribe en el contrato el valor concreto (por ejemplo "B1: es-MX"), porque el árbitro solo lee el contrato. Si el usuario no fijó un valor, B1 y B6 usan el idioma de su pedido, y B3 y B4 no aplican.

| ID | Criterio | Aplica a |
|---|---|---|
| B1 | Idioma del archivo declarado = el idioma del usuario (por ejemplo es-MX), no el que trae la plantilla (suele ser en-US), en estilos y texto | DOCX, PPTX, XLSX |
| B2 | Fecha del documento = mes y año reales de creación, nunca de plantilla | Todo documento fechado |
| B3 | Nombres de empresa, producto o persona escritos como los fija el usuario; ninguna aparición de las formas que prohíbe | Contenido que los nombra |
| B4 | Sin mezclar marcas que el usuario mantiene separadas (por ejemplo, la personal con la de su empresa) | Documentos con marca |
| B5 | Ninguna fecha, cita, cifra o nombre inventado: cada uno es rastreable a una fuente o queda marcado como pendiente | Todo |
| B6 | Idioma y variante de redacción del usuario; los términos técnicos, como se usan en su oficio | Todo texto |

Si el usuario tiene más reglas permanentes (en ese archivo, en su memoria o en su `CLAUDE.md` o `AGENTS.md`), súmalas como B7, B8…

---

## Fase 1 — Loop

### Cada ronda

1. **Planificar.** En la ronda 1, el plan completo de construcción. En las siguientes, solo el plan de corrección de los criterios que fallaron.
2. **Construir.** En la ronda 1, guarda primero las páginas web que uses como fuente (ver "Fuentes externas" en la Fase 0). Sigue las skills del tipo de entregable. GAUNTLET no reemplaza las skills de cada formato (docx, pptx, xlsx…): las envuelve.
3. **Probar.** El constructor corre sus propias comprobaciones sobre el archivo real (ver `references/verificacion-por-tipo.md` y `scripts/verificar_office.py`). Esta prueba es necesaria pero no basta: es el constructor revisando su propia obra.
4. **Auditar.** Lanza un **subagente árbitro nuevo** y dile que lea primero `agents/arbitro.md` (con la ruta absoluta de la carpeta de esta skill, `${CLAUDE_SKILL_DIR}`, para que también encuentre `references/` y `scripts/`). Pásale solo esto:
   - el contrato aprobado (listón con métodos y evidencias);
   - las rutas de los archivos entregables;
   - las rutas de las fuentes originales, para cotejar datos;
   - desde la ronda 2: la tabla de fallos de la ronda anterior (ID, hallazgo) y las disputas registradas.

   Al lanzar el árbitro se declaran siempre modelo y esfuerzo: los de la línea "Árbitro:" del encargo en curso; si no hay encargo, los que fije el contrato en MÉTODO; y si el contrato no los fija, Opus con esfuerzo alto cuando el entregable sale a terceros, se proyecta en público o es difícil de revertir, y Sonnet con esfuerzo medio en el resto. Si el agente `pit-lane:arbitro` está disponible, se lanza ese agente. No carga `CLAUDE.md` ni `AGENTS.md`: lo que necesite de esas reglas (los valores del listón base, cómo correr las pruebas) va escrito en el contrato.

   **No le pases** el plan, el razonamiento del constructor ni un "esto es lo que hice". Un árbitro que lee las justificaciones del constructor tiende a aceptarlas; eso es justo lo que se quiere evitar.
5. **Decidir.**
   - Todos los criterios PASA → sal del loop. Ninguna versión sale sin al menos una auditoría, pero una primera versión que la pasa puede entregarse: rehacerla por regla solo produce cambios cosméticos. Esto vale también en modo degradado, siempre que el resumen lo declare.
   - Algún NO PASA → corrige esos criterios y vuelve al paso 1.
   - Si lo único que no pasa son criterios escalados o defectuosos (ver "Escalar" y "Criterio defectuoso" en las reglas del loop), sal del loop: los decide el usuario.

### Reglas del loop

- **Un árbitro que falla o no entrega informe se reintenta una vez.** Si vuelve a fallar, la ronda se registra como "árbitro no ejecutado", nunca como aprobación.
- **Árbitro nuevo en cada ronda.** Uno que ya aprobó algo tiende a seguir aprobándolo. El nuevo recibe los fallos previos para comprobar que se corrigieron.
- **Cada ronda re-audita todo el listón**, no solo lo que falló. Una corrección puede romper lo que antes pasaba (regresión).
- **Mismo criterio falla dos rondas seguidas → cambia de enfoque**, no repitas el mismo arreglo. Anota en la bitácora qué cambió.
- **Corregir no es recortar.** Al corregir un fallo, el constructor no elimina contenido pedido para que un criterio pase. Lo que no se pueda verificar o no tenga fuente se marca como pendiente, no se borra. Si el árbitro nota que desapareció contenido respecto a la ronda anterior, lo reporta como observación fuera del listón; no bloquea, porque el listón está congelado.
- **Corregir no es rellenar.** Tampoco agregues al entregable texto que solo sirve para que el árbitro apruebe, como notas de "verificado" o explicaciones dirigidas al revisor. La evidencia va en la bitácora.
- **Tope: 3 rondas** (o lo que diga el contrato). Al llegar al tope, entrega con los pendientes a la vista. Nunca maquilles un NO PASA como PASA.
- **Disputas.** Si el constructor cree que el árbitro se equivoca, no lo ignora: registra la disputa con evidencia en la bitácora. El árbitro siguiente la resuelve, y el usuario la ve en el resumen.
- **Escalar.** Si el constructor cree que un hallazgo es erróneo pero su prueba no está en ningún archivo que el árbitro pueda abrir (una decisión verbal, una convención del equipo), no lo disputa ni lo corrige: lo escala. El criterio queda NO PASA, marcado ESCALADO en la bitácora con la prueba que el usuario debe confirmar. No cuenta para seguir el loop ni para cambiar de enfoque, y va primero en "Qué debe revisar el humano". Si el usuario lo confirma, el resumen lo registra como aprobado por el usuario, no por el árbitro.
- **Criterio defectuoso.** Si el árbitro marca un criterio DEFECTUOSO (admite dos lecturas con veredictos opuestos, o no puede pasar con lo que existe ni con lo que el contrato hará existir), ese criterio sale del loop igual que uno escalado: no cuenta para seguir el loop ni para cambiar de enfoque, y va primero en "Qué debe revisar el humano", con las dos lecturas o con lo que falta. El listón sigue congelado: el constructor no reescribe el criterio ni lo esquiva, y solo el usuario lo reescribe, lo quita o acepta una de las lecturas. Solo el árbitro puede declarar un criterio DEFECTUOSO; el constructor no.
- **Sin paradas.** Una ambigüedad menor que aparezca en el loop se decide y se anota. Solo se detiene el loop por algo irreversible o que invalide el contrato (por ejemplo, la fuente contradice la TAREA); en ese caso se presenta el problema con opciones.

### Modo degradado (sin subagentes)

Si el entorno no tiene herramienta para lanzar subagentes, el árbitro se ejecuta en un pase separado: relee `agents/arbitro.md`, abre el archivo desde el disco (no de memoria) y aplica el método de cada criterio. Es mejor que nada, pero no es independiente. El resumen debe decirlo en su primera línea: **AUDITORÍA NO INDEPENDIENTE**.

---

## Verificar, no suponer

El árbitro audita el **artefacto**, no la descripción del artefacto. Una evidencia válida es algo observable: salida de un comando, una celda con su valor, una página renderizada, un fragmento citado de la fuente. "El constructor dice que…" no es evidencia. Si un criterio no se puede verificar con las herramientas disponibles, el veredicto es **NO VERIFICABLE**, que bloquea igual que NO PASA salvo que el contrato lo haya marcado como "revisión humana".

Métodos por tipo (DOCX, PPTX, XLSX, PDF, código, web, datos, citas textuales, imágenes, instrucciones o prompts): `references/verificacion-por-tipo.md`.

## Bitácora

Lleva un solo archivo, `auditoria-gauntlet.md`, junto al entregable. Si la tarea vive en un proyecto con carpetas, va en la carpeta del entregable; si no, en el directorio de trabajo. Nace cuando se aprueba el contrato (o al arrancar con aprobación anticipada), nunca antes. Desde ese momento escríbelo mientras avanzas, no al final de memoria: decisiones tomadas, informe de cada ronda del árbitro, disputas y cambios de enfoque. El resumen final se arma desde este archivo.

## Fase 2 — Entrega

1. El entregable, en el formato del contrato.
2. El **resumen de auditoría** (plantilla en `references/plantillas.md`): rondas hechas, qué rechazó el árbitro, errores encontrados, qué se corrigió, pendientes, disputas y observaciones fuera del listón.
3. **Qué debe revisar el humano.** La lista corta de lo que ninguna máquina pudo confirmar (primero los criterios ESCALADOS y los DEFECTUOSOS; después los marcados "revisión humana", los NO VERIFICABLE y los riesgos fuera del listón). El árbitro aprueba el listón, no la intención; la revisión final sigue siendo del usuario.

Sé breve en el chat: el detalle está en la bitácora.
