# Código y especificaciones de software

Proceso propio de Pit Lane para tres tipos de entregable: **código** (scripts, programas, automatizaciones, macros), **instrucciones para otra IA** (skills, prompts, agentes) y **especificaciones de software** (documentos de diseño que otro va a implementar). Aplica cuando el encargo lo indica (R-34). Todo lo demás del flujo sigue igual: contrato, listón, encargos, auditoría.

El porqué de fondo: un documento se puede leer y juzgar; el código hay que ejecutarlo, y una especificación falla cuando alguien intenta construirla. Por eso cada parte pide evidencia que solo existe al ejecutar.

---

## 1. Código

### Antes de empezar
1. **Rama aparte.** El mecánico trabaja en una rama de git propia (o en una copia de trabajo aislada), nunca directo en la rama principal. Si el proyecto no usa git, trabaja en una copia de la carpeta. *Por qué:* un intento fallido se descarta entero, sin dejar restos en lo que ya funcionaba.
2. **Línea base verde.** Antes de cambiar nada, corre las pruebas que ya existen y anota el resultado en "Avance". Si ya fallaban, se anota cuáles: no son fallos del encargo. *Por qué:* sin línea base no se sabe si un fallo lo trajo el cambio o ya estaba.

### Construir: primero la prueba, después el código
3. **Prueba que falla primero.** Por cada comportamiento que exige el listón, el mecánico escribe una prueba ejecutable, la corre y **ve que falla** por la razón esperada. Solo después escribe el código mínimo que la hace pasar, y la vuelve a correr. *Por qué:* una prueba que nunca falló no demuestra nada; puede pasar aunque el código no haga lo pedido.
4. **Código sin prueba no entra.** Si escribió código antes de su prueba, lo descarta y empieza por la prueba. Excepción: lo que no se puede probar en ese entorno (macros de Office, VBA, integraciones sin entorno de prueba) va al listón como revisión humana (R-35).
5. **Ordenar al final.** Con todas las pruebas en verde, puede reorganizar el código sin cambiar el comportamiento, y corre todo de nuevo.

### Cuando algo falla
6. **Causa raíz antes que arreglo.** Ante un fallo: reproducirlo, leer el error completo, formular una hipótesis, comprobarla con un cambio mínimo, y recién ahí arreglar. Nada de cambiar cosas "a ver si pasa". *Por qué:* un arreglo sin causa tapa el síntoma y el fallo vuelve en otra parte.
7. **Tres arreglos fallidos, se para.** Si tres intentos seguidos no arreglan el mismo fallo, el mecánico deja de arreglar, escribe en "Qué no funcionó" lo que probó y devuelve BLOQUEADO: el problema probablemente es de diseño, no de detalle (R-19). En la auditoría rige además R-27.

### Revisión
8. **El árbitro audita el código real.** Lee el diff completo de la rama (`git diff` contra la rama principal), corre las pruebas él mismo y aplica la verificación por tipo de `pit-lane:gauntlet` (código y scripts). El informe del mecánico no es evidencia: lo es la salida del comando (R-16, R-24).
9. **Verificar el hallazgo antes de corregir.** Cuando el árbitro marca un fallo, el mecánico primero lo reproduce. Si se reproduce, lo corrige con una prueba que lo atrape. Si no se reproduce, abre una disputa con la salida que lo demuestra (R-28). No se acepta un hallazgo solo por cortesía ni se corrige "por si acaso".
10. **Revisión final de la rama** (L y XL). La auditoría de coherencia corre la batería completa de pruebas con todos los encargos integrados, porque dos encargos que pasan por separado pueden romperse juntos (R-29).

### Cierre
11. **Opciones, no acciones.** Al terminar, el Jefe de pits le presenta al usuario las opciones: integrar la rama en local, abrir un pull request o dejar la rama para después. Integrar a la rama principal, hacer push o publicar son acciones que salen a terceros o son difíciles de revertir: esperan su decisión (R-09). Nunca se fuerza una operación de git (`--force`) ni se borra una rama sin su aprobación.

### Skills, prompts y agentes
12. Si el entregable son instrucciones que otra IA va a ejecutar (una skill, un prompt, un agente), se aplica el mismo principio de la prueba que falla primero, con un subagente nuevo como banco de pruebas:
    - **Antes de escribir**, el mecánico corre el caso de prueba sin las instrucciones nuevas (o con la versión anterior) y anota en "Avance" qué hizo mal el subagente. Ese fallo observado es lo que las instrucciones tienen que corregir.
    - **Después de escribir**, corre el mismo caso con un subagente nuevo y comprueba que el fallo desapareció sin romper lo que ya funcionaba.
    - El listón incluye esa prueba real, además de la verificación por tipo de instrucciones de `pit-lane:gauntlet`, y el árbitro compara lo que hizo el subagente con lo que el listón exige.

    *Por qué:* leer un prompt no revela cómo lo interpreta otro modelo; ejecutarlo sí. Y unas instrucciones que nunca se vieron fallar sin ellas no demuestran que hagan falta ni que funcionen.

---

## 2. Especificaciones de software

### Plantilla mínima
Toda especificación lleva estas secciones; el listón exige cada una (R-05):

| Sección | Qué responde |
|---|---|
| Problema | Qué está mal hoy, para quién, con qué evidencia |
| Estado actual | Cómo se resuelve hoy y qué código existente toca (rutas reales) |
| Propuesta | Qué se construye, con interfaces, datos y comportamiento observable |
| Alternativas | Al menos dos descartadas, incluida "no construir" o "reutilizar lo que ya existe", con el porqué |
| Riesgos | Qué puede fallar y cómo se mitiga o se detecta |
| Cómo se mide | Qué prueba o dato demuestra que funcionó |
| Fuera de alcance | Qué no se hace en esta versión |

### Revisión antes de aprobar
1. **Cero decisiones al implementador.** `pit-lane:lector-ejecucion` lee la especificación como quien la va a construir: cada paso que deja una decisión abierta es un hallazgo (R-23).
2. **Cotejo contra el código.** Si la especificación nombra código existente (archivos, funciones, tablas, comandos), el lector comprueba en el repositorio que existe y hace lo que el documento dice. Una referencia inexistente o equivocada es un hallazgo mayor. *Por qué:* una especificación escrita sobre un código imaginado no se puede construir.
3. **¿Hace falta construirlo?** `pit-lane:lector-critico` (en XL) busca si algo que ya existe resuelve el problema, si la propuesta es más grande de lo necesario y si optimiza algo que todavía no duele. *Por qué:* lo más barato de mantener es lo que no se construyó.
4. En XL, `pit-lane:lector-ingenuo` parafrasea primero; si no puede parafrasear una parte, es un bloqueo.

Los hallazgos se resuelven con evidencia que el lector pueda abrir; no se contesta una falta de comprensión diciendo "es obvio" (R-28).
