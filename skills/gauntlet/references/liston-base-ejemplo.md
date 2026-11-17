# Listón base personal: ejemplo

El listón base de `SKILL.md` es genérico. Los valores propios de cada usuario viven fuera del plugin, en `~/.claude/pit-lane-liston-base.md` (en Windows, `C:\Users\<tu usuario>\.claude\pit-lane-liston-base.md`). El archivo es opcional: sin él, B1 y B6 usan el idioma del pedido, y B3 y B4 no aplican.

Copia este ejemplo a esa ruta y cambia los valores. Los nombres son inventados.

```markdown
# Mi listón base

| ID | Mi valor |
|---|---|
| B1 | es-MX |
| B3 | La empresa se escribe "Acme Minera"; prohibidas las formas "ACME S.A." y "Acme Mining" |
| B4 | No mezclar mi marca personal con la marca de Acme Minera en un mismo documento |
| B6 | Español latinoamericano; términos técnicos en inglés (SOP, KPI, PLC…) |
| B7 | Las citas de normas usan la edición vigente; se indica el año de la edición |

Para `verificar_office.py`: `--idioma es-MX --prohibido "ACME S.A." --prohibido "Acme Mining"`
```

Cómo se usa: al redactar un contrato, la sesión lee el archivo y escribe en el LISTÓN el valor concreto de cada criterio base que aplique. El árbitro no lee este archivo: audita lo que dice el contrato.
