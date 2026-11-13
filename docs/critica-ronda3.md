## Informe del crítico — Ronda 3
**Veredicto global:** APROBADO CON CORRECCIONES. No hay bloqueos. Quedan 3 hallazgos mayores, todos corregibles editando texto.

### Fallos de la ronda 2
| Hallazgo | Estado | Evidencia |
|---|---|---|
| 1. Dueño de F5 | CORREGIDO | 178, 187, 294, 307, 388, 491 |
| 2. Enrutamiento del árbitro | CORREGIDO | 482; L8 en 497 (discrepancia nueva: hallazgo 1) |
| 3. Prefijos y vía de carga | CORREGIDO | 394, 435-436, 494, 500, 503, 522, 534. Coincide con plugins/create |
| 4. Listón del paso 7 | CORREGIDO en sus dos causas | L7 en 497; 488. Hay causas nuevas: hallazgo 3 |
| 5. IDs faltantes | CORREGIDO | 384-387; 373 |
| 6. README para Haiku | CORREGIDO | 479 |
| 7. Índice de git | CORREGIDO | 462, 482-491 |
| 8. Ruta de `uso.json` | CORREGIDO | 322, 469, 488 |
| 9. Precisiones | CORREGIDO | 203, 125, 515 |

### Hallazgos nuevos

**1. [MAYOR] Paso 2, ajuste 3 (482) · Dos fuentes para el modelo del árbitro.**
- **Qué hay:** el ajuste 3 toma modelo y esfuerzo "que fije el contrato en MÉTODO". El encargo (228), la 6.10 (307) y el paso 5 (491) los toman de la línea `Árbitro:` del encargo.
- **Consecuencia:** pongamos un encargo `opus · high` dentro de un contrato `sonnet · medium`. La obrera recibe dos órdenes contrarias. Si sigue a la skill, viola R-12 y R-36, y eso afecta a R5.
- **Corrección:** cambiar "los que fije el contrato en MÉTODO" por "los de la línea «Árbitro:» del encargo en curso; si no hay encargo, los del contrato en MÉTODO".

**2. [MAYOR] Paso 2 (482), 7 (436) y decisión 6 (534) · "Sin colmena, como hoy" es falso.**
- **Qué hay:** los ajustes 2 (reintento) y 3 (modelo declarado, Sonnet medio por defecto) cambian el comportamiento también sin colmena.
- **Consecuencia:** el ejecutor tiene que elegir, y las dos opciones fallan:
  - Si los condiciona a que haya colmena, el tamaño M (que no tiene `colmena/`) lanza el árbitro sin modelo. Eso contradice 177 y viola R-12.
  - Si no los condiciona, las frases de la 436 y la 534 son falsas.
- **Corrección:**
  - Paso 2: cambiar "Sin colmena, la skill debe seguir comportándose como hoy." por "El ajuste 1 aplica solo si existe `colmena/contrato.md`; los ajustes 2 y 3 aplican siempre."
  - 436 y 534: "sin colmena, solo cambia que el árbitro sale con modelo y esfuerzo declarados y se reintenta una vez".

**3. [MAYOR] Paso 7, L1 y L6 (497) · El listón vuelve a fallar por construcción.**
- **L1:** la sección 7 lista `docs/auditoria-gauntlet.md` (430). Ese archivo lo escribe el propio paso 7, que no hace commit, y no está en la superficie del paso 8 (473). `git ls-files` no lo incluye, así que L1 da NO PASA.
- **L6:** falla aunque los pasos 1 a 6 estén bien, por dos vías:
  - `docs/critica-ronda1.md:85`, que trae el zip, contiene el marcador CONFIRMAR entre corchetes, y `decisiones.md` nace vacío (479).
  - El paso 3 lista sus marcadores "al final de tu respuesta" (485), no en `decisiones.md`, que está fuera de su superficie.
- **Corrección:**
  - L1: "…los de la sección 7, salvo `docs/auditoria-gauntlet.md`, más `.gitignore` si existe".
  - L6: "Todo marcador CONFIRMAR fuera de `docs/` aparece en el informe con archivo y línea". El paso 8 los pasa a `decisiones.md`.

**4. [MENOR] Ajuste 1 (482) · La auditoría de coherencia queda fuera.** El listón y la bitácora son "del encargo en curso", y la auditoría de coherencia no tiene encargo. **Corrección:** añadir "en la auditoría de coherencia, los criterios de coherencia del contrato y `colmena/auditorias/coherencia.md`" (como en 294 y 307).

**5. [MENOR] 6.7 (257, 264), R-36 (386) y pasos 6-7 · El árbitro puede tener el mismo modelo que el constructor.**
- Con una obrera experta (Opus) y un error costoso, la tabla da un árbitro Opus, y la regla 4 exige un modelo distinto.
- El paso 7 audita en Opus alto lo que el paso 6 construyó en Opus alto.
- **Corrección:** en la regla 4, "cuando el error es costoso y el constructor no es Opus". Otra opción: árbitro Fable 5.2 alto para un constructor Opus.

**6. [MENOR] Paso 5 (491) · El campo `tools` está sin decidir.**
- Según sub-agents, una lista `tools` sin `Agent` impide lanzar subagentes, así que restringirlo en las obreras anula la vía principal de R-39.
- En el árbitro, sin Bash no puede correr `verificar_office.py`.
- **Corrección:** "En las obreras no declares `tools`, o incluye `Agent`. En los lectores: Read, Grep y Glob. En el árbitro: también Bash".

**7. [MENOR] L9 (497) choca con el paso 5.**
- El paso 5 manda escribir `name: obrera` sin prefijo y remitir a "la skill gauntlet" (491).
- `skills/gauntlet/SKILL.md` contiene `name: gauntlet`.
- **Corrección:** añadir a L9 "fuera de los campos `name` del frontmatter y de las rutas de archivo".

**8. [MENOR] Paso 8 (500) · El chat no puede ejecutar `/reload-plugins` ni ver `/plugin`.** **Corrección:** "pídeme que ejecute `/reload-plugins` y `/agents` y que te pegue la salida". `claude plugin validate .` y `plugin list` sí corren en la terminal.

### Sin defecto
- Fase 0, "Auditar" y "Reglas del loop" existen en gauntlet (`SKILL.md:27`, `:70` y `:81`).
- Las reglas R-01 a R-39 están en las secciones que les atribuye la 6.14.
- Las superficies de la sección 8 coinciden con el árbol de la 7.
- Ningún paso usa archivos de un paso posterior o paralelo.
- Los modelos de la sección 8 cumplen la 6.7.
- El dueño de cada auditoría es el mismo en 6.3, 6.4, 6.10, R-39 y el paso 5.

### Cobertura
| Requisito | Veredicto | Sección |
|---|---|---|
| R2 | CUMPLE | 6, 7 |
| R4 | CUMPLE | 6.6, 6.7 |
| R5 | CUMPLE A MEDIAS: el modelo del árbitro tiene dos fuentes (hallazgo 1) | 6.8, 6.10, paso 2 |
| R6 | CUMPLE | 7 |
| R7 | CUMPLE A MEDIAS: el paso 2 es ambiguo y el paso 7 falla por construcción (hallazgos 2 y 3) | 8 |
| R8 | CUMPLE | 6.1, 6.14, 8, 10 |
