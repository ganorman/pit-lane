# AGENTS.md — cómo se trabaja en Pit Lane

## Qué es

Pit Lane es un plugin de Claude Code con una metodología de trabajo: un **Jefe de pits** que hace el triage, el contrato y el plan, y enruta modelo y esfuerzo; **mecánicos** que ejecutan encargos en paralelo; y un **árbitro** independiente que audita cada entregable contra un listón binario. Es autosuficiente: no depende de ningún plugin externo, y para código y especificaciones de software tiene su propio proceso (`references/software.md`).

El repo vive en `~/.claude/skills/pit-lane/`. Como contiene `.claude-plugin/plugin.json`, se carga solo en cada sesión, sin instalarlo.

**Fuente de verdad:** `docs/diseno.md`. Si algo del repo contradice ese documento, gana el documento, y la contradicción se reporta en vez de corregirla por cuenta propia.

## Cómo está organizado

```
pit-lane/
├── README.md · AGENTS.md · LICENSE · NOTICE
├── .claude-plugin/plugin.json
├── skills/
│   ├── pit-lane/SKILL.md       el Jefe de pits: fases F0 a F6
│   └── gauntlet/               contrato, loop de auditoría, verificación por tipo
├── agents/                     mecánicos (3), lectores (3) y árbitro (envoltorio)
├── references/                 plantillas, enrutamiento, modos de ejecución y software
├── scripts/                    freno de gasto (status line) y su LEEME.md
└── docs/                       diseño, decisiones y manual de uso
```

| Pieza | Para qué |
|---|---|
| `skills/pit-lane/SKILL.md` | El flujo F0 a F6. Cita cada regla por ID y remite a `references/` para el detalle |
| `skills/gauntlet/` | La auditoría. Es lo único que contiene la verificación por tipo y `verificar_office.py` |
| `references/` | El detalle que la skill no repite: plantillas, tabla de enrutamiento, pasos de los modos A, B y E, instrucciones del mecánico externo, proceso de software |
| `agents/` | Un archivo por agente; `model` y `effort` del frontmatter según la sección 18 del diseño |
| `scripts/` | `uso-statusline.ps1` escribe el porcentaje de uso en `~/.claude/pit-lane-uso.json` |
| `docs/decisiones.md` | Registro de decisiones, una por línea, con fecha |

**Nombres una vez cargado:** todo lleva el prefijo del plugin. Las skills son `/pit-lane:pit-lane` y `/pit-lane:gauntlet`. Los agentes son `pit-lane:mecanico`, `pit-lane:mecanico-experto`, `pit-lane:mecanico-auxiliar`, `pit-lane:lector-ingenuo`, `pit-lane:lector-critico`, `pit-lane:lector-ejecucion` y `pit-lane:arbitro`.

## Cómo se trabaja en este repo

### Reglas de contenido

1. **Reglas con ID.** Las reglas del sistema son R-01 a R-51 (sección 15 del diseño). Toda regla que aparece en la skill, en `references/` o en un agente lleva su ID, por ejemplo "(R-12)". No se inventan reglas: si falta algo, se marca **[CONFIRMAR]** y se lleva a `docs/decisiones.md` como pendiente del mantenedor.
2. **Sin duplicados.** Cada contenido vive en un solo archivo y los demás remiten a él. La verificación por tipo y el resumen de auditoría son de `skills/gauntlet/`; las plantillas y la tabla de enrutamiento, de `references/`.
3. **Prefijo siempre.** Ninguna skill ni agente nombra a un agente ni a la skill gauntlet sin el prefijo `pit-lane:`. Excepciones: el campo `name` del frontmatter, las rutas de archivo y el contenido original de `skills/gauntlet/`.
4. **`skills/gauntlet/` no se reescribe.** Es la skill del mantenedor con los ajustes registrados en `docs/decisiones.md` (paso 2, paso 10, V2.1 y las revisiones de noviembre de 2026). Cualquier otro cambio necesita su aprobación. Es la única fuente de gauntlet: la copia de la cuenta de claude.ai se exporta desde aquí.
5. **Límites de tamaño.** `skills/pit-lane/SKILL.md`, menos de 250 líneas; este archivo, menos de 100.
6. **Idioma.** Español latinoamericano, con los términos técnicos en inglés. `LICENSE`, `NOTICE`, las claves de JSON y frontmatter, los nombres de archivo y el código quedan fuera de esta regla.
7. **Texto propio y autosuficiente.** Todo se escribe de cero y sin citar otras metodologías ni depender de plugins externos. Si hace falta una práctica que el repo no tiene, se integra con texto propio.

### Cómo se hace un cambio

1. Lee la sección del diseño que aplica y los archivos que vas a tocar, completos.
2. Declara tu superficie de escritura y no salgas de ella. Si el encargo dice "no modifiques X", X no se toca aunque tenga un error: se reporta.
3. Si encuentras una contradicción entre el diseño y el repo, repórtala y detente.
4. Cada decisión que tomes y que no estaba escrita va a `docs/decisiones.md`: una línea con fecha AAAA-MM-DD.
5. Comprueba lo que escribiste sobre el archivo real: IDs de regla presentes, nombres con prefijo, límites de líneas.

### Git

- Un commit local por paso, con el mensaje del plan (por ejemplo, "paso 6: skill"), que incluya **solo** los archivos de ese paso. Varios pasos pueden compartir el índice: agrega los archivos por nombre, nunca con `git add -A`.
- Si git informa de un bloqueo del índice (`index.lock`), espera unos segundos y reintenta. No borres el lock a mano.
- **Nunca hagas push** sin la aprobación explícita del mantenedor.

### Plan de construcción

La v1 se construyó en los pasos 0 a 10 (resumen en la sección 19 del diseño), cada uno en un chat nuevo y, con el plan Pro, de uno en uno. Desde entonces, cada cambio lo aprueba el mantenedor y queda en `docs/decisiones.md` (por ejemplo, el paso 11: gauntlet V2.1). Si el cambio altera una regla, se actualiza también el diseño, porque el diseño es la fuente de verdad.

### Comprobar que el plugin carga

```bash
claude plugin validate .
```

En una sesión nueva de la app de escritorio deben aparecer `/pit-lane:pit-lane` y los 7 agentes con prefijo. Si no cargan, la alternativa es declarar la carpeta en `CLAUDE_CODE_PLUGIN_DIRS`, solo con la aprobación del mantenedor (hipótesis H9).

### Hipótesis abiertas

Las hipótesis H1 a H12 están en la sección 20 del diseño, con su resultado. H3 falló (el freno usa `get_usage`), H9 se cumple en el equipo del mantenedor y H10 se resolvió haciendo que en modo A el Jefe de pits lance los árbitros, y H11 se cumplió en una prueba (falta un encargo real); H12 (Codex y Antigravity respetan la bahía del modo E) y las demás siguen abiertas. Cualquier ajuste nuevo se aplica solo si el mantenedor lo aprueba.
