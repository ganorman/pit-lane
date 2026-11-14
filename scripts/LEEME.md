# Freno de gasto de Pit Lane

`uso-statusline.ps1` es un script de status line. Claude Code le pasa por la entrada estándar el JSON de la sesión; el script guarda el porcentaje de uso de las ventanas de 5 horas y 7 días en `~/.claude/pit-lane-uso.json` e imprime una línea corta (`5h: 42% | 7d: 7%`). El Jefe de pits lee ese archivo para aplicar el freno de gasto: al 80 % de la ventana de 5 horas no se despacha nada nuevo (R-30).

Si faltan los campos `rate_limits` (por ejemplo, antes de la primera respuesta de la API), el script imprime guiones y no escribe el archivo. Si el JSON es inválido, tampoco falla.

## Archivo que escribe

```json
{
  "five_hour_used_percentage": 42.3,
  "seven_day_used_percentage": 7,
  "actualizado": "2026-11-13T18:41:48-04:00"
}
```

## Cómo activarlo

Añade esto a `~/.claude/settings.json`, con la ruta absoluta y barras normales:

```json
"statusLine": {
  "type": "command",
  "command": "powershell -NoProfile -File C:/Users/<tu usuario>/.claude/skills/pit-lane/scripts/uso-statusline.ps1"
}
```

Luego abre una sesión nueva y comprueba que existe `~/.claude/pit-lane-uso.json` y que se actualiza.

## En la app de escritorio

El script funciona (probado a mano el 2026-11-14), pero en el piloto la status line configurada no escribió el archivo en la app de escritorio: la hipótesis H3 falló. Por eso el freno lee el uso en este orden (R-30):

1. La herramienta `get_usage` de la app, que devuelve el porcentaje de la ventana de 5 horas.
2. `~/.claude/pit-lane-uso.json`, que este script mantiene cuando Claude Code corre en la terminal.
3. Si ninguno responde, o el archivo no se actualiza, el freno queda manual: Gerardo escribe la palabra "freno" y no se despacha nada nuevo.

## Probarlo sin tocar la configuración

```bash
echo '{"rate_limits":{"five_hour":{"used_percentage":42.3},"seven_day":{"used_percentage":7}}}' | powershell -NoProfile -File scripts/uso-statusline.ps1 -Ruta "$TEMP/prueba.json"
```

El parámetro opcional `-Ruta` cambia dónde se escribe el archivo.
