# Pit Lane

Metodología de trabajo con Claude: un Jefe de pits que planifica y enruta, mecánicos que ejecutan en paralelo y un árbitro independiente que audita.

Es un plugin de Claude Code con 2 skills y 7 agentes, escrito en español. Versión 1.3, probada en un piloto real (noviembre de 2026). Licencia MIT.

## Requisitos

- **Claude Code**, en la terminal o en la app de escritorio. Los subagentes, el enrutamiento de modelo y esfuerzo y la lectura del uso con `get_usage` solo existen ahí. Para fijar el esfuerzo en cada invocación hace falta la v2.1.292 o posterior. En otra IA solo se traslada el método (ver la sección 5 del manual).
- **Plan:** pensado para Pro, con dos topes: como máximo 2 mecánicos Claude a la vez (más hasta 2 de otros proveedores en el modo E), y Opus 5.5 como el modelo más capaz (Fable queda fuera porque en Pro corre con créditos aparte). Con un plan mayor puedes subir a 3 mecánicos y sumar Fable: cambia R-14 en `skills/pit-lane/SKILL.md` y la tabla de `references/enrutamiento.md`.
- **Freno de gasto:** en la app de escritorio lee el uso solo. En la terminal usa `scripts/uso-statusline.ps1`, que necesita PowerShell (en macOS o Linux, `pwsh`); sin él, el freno es manual: escribe "freno".
- **Nada más para el flujo.** No necesita otros plugins: para código y especificaciones de software trae su propio proceso (`references/software.md`).
- **Para la verificación de Office** (`skills/gauntlet/scripts/verificar_office.py`): Python 3. Para ver cómo se ve un documento (`--render`) y recalcular un Excel (`--recalcular`), Microsoft Office en Windows (si no hay Office, el render intenta con LibreOffice). Sin ninguno de los dos, el árbitro marca esos criterios como NO VERIFICABLE en vez de aprobarlos.

## Instalación

Elige una de las dos vías.

**Desde el marketplace** (se actualiza con `claude plugin update`):

```bash
claude plugin marketplace add ganorman/pit-lane
claude plugin install pit-lane@pit-lane
```

**Clonando el repo** en tu carpeta personal de skills. Como trae `.claude-plugin/plugin.json`, Claude Code lo carga solo en cada sesión:

```bash
git clone https://github.com/ganorman/pit-lane.git ~/.claude/skills/pit-lane
claude plugin validate ~/.claude/skills/pit-lane
```

En una sesión nueva deben aparecer `/pit-lane:pit-lane`, `/pit-lane:gauntlet` y los agentes `pit-lane:…`.

## Tus reglas permanentes

El listón base que audita el árbitro (idioma del archivo, fechas reales, nombres y marcas, datos con fuente) es genérico. Para fijar tus valores, por ejemplo tu variante de español o cómo se escribe el nombre de tu empresa, copia `skills/gauntlet/references/liston-base-ejemplo.md` a `~/.claude/pit-lane-liston-base.md` y edítalo. Ese archivo es tuyo y no forma parte del plugin. Sin él, el idioma es el de tu pedido y no se exige ningún nombre ni marca.

## Uso

| Tamaño | Cuándo | Qué corre |
|---|---|---|
| S | Tarea chica y reversible | Se hace directo, sin contrato |
| M | Un entregable que debe salir bien | `/pit-lane:gauntlet`: contrato, construir y auditar |
| L y XL | Varios entregables, fuentes o datos compartidos | `/pit-lane:pit-lane`: contrato, plan, mecánicos en paralelo y auditoría |

Ejemplo: *"/pit-lane:pit-lane — 3 informes DOCX con la producción de las fuentes A y B; cifras en `datos.xlsx`."* El Jefe de pits responde con el tamaño, el contrato y el plan, y no construye nada hasta que los apruebes.

## Más información

- Guía de uso: `docs/manual-de-uso.md`
- Qué es y por qué: `docs/diseno.md` (fuente de verdad)
- Cómo se trabaja en este repo: `AGENTS.md`
- Decisiones registradas: `docs/decisiones.md`
- Skills: `skills/pit-lane` (flujo completo) y `skills/gauntlet` (auditoría)
- Créditos: `NOTICE` · Licencia: `LICENSE` (MIT)
- Errores y propuestas: [issues del repo](https://github.com/ganorman/pit-lane/issues)
