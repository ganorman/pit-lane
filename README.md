# Pit Lane

Metodología de trabajo con Claude: un Jefe de pits que planifica y enruta, mecánicos que ejecutan en paralelo y un árbitro independiente que audita.

Es un plugin de Claude Code con 2 skills y 7 agentes. Estado: v1 construida y probada en un piloto real (noviembre de 2026).

## Instalación

Clona el repo en tu carpeta personal de skills. Como trae `.claude-plugin/plugin.json`, Claude Code lo carga solo en cada sesión:

```bash
git clone https://github.com/ganorman/pit-lane.git ~/.claude/skills/pit-lane
claude plugin validate ~/.claude/skills/pit-lane
```

En una sesión nueva deben aparecer `/pit-lane:pit-lane`, `/pit-lane:gauntlet` y los agentes `pit-lane:…`.

## Uso

| Tamaño | Cuándo | Qué corre |
|---|---|---|
| S | Tarea chica y reversible | Se hace directo, sin contrato |
| M | Un entregable que debe salir bien | `/pit-lane:gauntlet`: contrato, construir y auditar |
| L y XL | Varios entregables, fuentes o datos compartidos | `/pit-lane:pit-lane`: contrato, plan, mecánicos en paralelo y auditoría |

Ejemplo: *"/pit-lane:pit-lane — 3 informes DOCX con la producción de las fuentes A y B; cifras en `datos.xlsx`."* El Jefe de pits responde con el tamaño, el contrato y el plan, y no construye nada hasta que los apruebes.

## Más información

- Guía de uso: `docs/manual-de-uso.md`
- Qué es y por qué: `docs/analisis-y-diseno.md` (fuente de verdad)
- Cómo se trabaja en este repo: `AGENTS.md`
- Decisiones registradas: `docs/decisiones.md`
- Skills: `skills/pit-lane` (flujo completo) y `skills/gauntlet` (auditoría)
- Créditos: `NOTICE`
