# Manual de uso de Pit Lane

Guía corta para instalar Pit Lane en Claude Code, usarlo en un proyecto y adaptarlo a otra IA.

## 1. Qué es

Pit Lane organiza el trabajo en tres roles:

- **Jefe de pits:** clasifica la tarea, redacta el contrato y el plan.
- **Mecánicos:** ejecutan los encargos, en paralelo y por oleadas de hasta 2.
- **Árbitro:** audita cada entregable con contexto limpio, contra el listón aprobado.

## 2. Instalación (Claude Code)

Desde el marketplace (se actualiza con `claude plugin update`):

```bash
claude plugin marketplace add ganorman/pit-lane
claude plugin install pit-lane@pit-lane
```

O clona el repo en tu carpeta personal de skills (en Windows, `C:\Users\<tu usuario>\.claude\skills\pit-lane`). Como trae `.claude-plugin/plugin.json`, se carga solo en cada sesión, sin instalarlo. Usa una sola de las dos vías: con las dos, tendrías el plugin cargado dos veces.

```bash
git clone https://github.com/ganorman/pit-lane.git ~/.claude/skills/pit-lane
claude plugin validate ~/.claude/skills/pit-lane
```

Abre una sesión nueva y comprueba que existen `/pit-lane:pit-lane`, `/pit-lane:gauntlet` y los 7 agentes con prefijo `pit-lane:`. Si en otro equipo no carga, declara la carpeta en la variable `CLAUDE_CODE_PLUGIN_DIRS` de tu configuración de usuario (hipótesis H9).

## 3. Elegir el tamaño

| Tamaño | Cuándo | Qué usar |
|---|---|---|
| S | Tarea chica, sin riesgo | Pídelo directo, sin contrato |
| M | Un entregable con revisión | `/pit-lane:gauntlet` |
| L / XL | Varios entregables o fuentes | `/pit-lane:pit-lane` |

## 4. Flujo paso a paso

1. **Pide la tarea completa.** Incluye fuentes, formato y destinatario. Ejemplo: *"Con Pit Lane: 3 DOCX con producción de las fuentes A y B. Español, cifras en `datos.xlsx`."*
2. **Triage.** El Jefe de pits responde con el tamaño y el motivo. Puedes vetarlo.
3. **Contrato.** Lee INSTRUCCIONES ORIGINALES y el LISTÓN. Es tu único veto. Responde las preguntas críticas (máximo 4).
4. **Plan** (L y XL). Revisa los encargos, modelos y esfuerzos.
5. **Aprobación.** Aprueba contrato y plan en un bloque. En XL son dos aprobaciones. Queda `Aprobado: AAAA-MM-DD` y el listón se congela.
6. **Ejecución.** Los mecánicos construyen y prueban. Devuelven un informe de 15 líneas.
7. **Auditoría.** Un árbitro nuevo revisa cada encargo, con un máximo de 3 rondas. En L y XL hay además una auditoría de coherencia entre los entregables.
8. **Cierre.** Recibes las rutas de los entregables, el resumen de auditoría y la lista "revisa tú".
9. **Retomar tras un corte.** Pide: *"Lee `pit-lane/estado.md` y reanuda."*

**Freno de gasto:** al 80 % de la ventana de 5 horas, o si dices "freno", no se despacha nada nuevo.

## 5. Usarlo en otro proyecto

**Con Claude Code**
1. Instala el plugin (sección 2). No hace falta copiar archivos al proyecto.
2. La primera vez, el Jefe de pits crea `pit-lane/` dentro del proyecto.
3. Fija tus valores del listón base (idioma, nombres, marcas) en `~/.claude/pit-lane-liston-base.md`; el formato está en `skills/gauntlet/references/liston-base-ejemplo.md`.
4. Si un entregable es código o una especificación de software, el Jefe de pits aplica el proceso de `references/software.md`: no hace falta instalar nada más.

**Con otra IA (ChatGPT, Gemini, etc.)**
No tiene subagentes ni enrutamiento de modelos. Solo se traslada el método:
1. Copia la plantilla de contrato de `references/plantillas.md`.
2. Pide el contrato en el chat y espera tu aprobación.
3. Construye en una conversación.
4. Audita en **otra conversación nueva**, con un prompt que solo contenga el contrato y los archivos. El resumen debe decir **AUDITORÍA NO INDEPENDIENTE**.

## 6. Qué es tuyo y qué es del plugin

El repo es público. Las reglas no nombran a ninguna persona y el listón base B1 a B6 es genérico. Lo tuyo vive fuera del plugin y no se sube a ningún lado:

- `~/.claude/pit-lane-liston-base.md`: tus valores del listón base.
- `~/.claude/pit-lane-uso.json`: el uso de tu plan, si activas el script del freno.
- La carpeta `pit-lane/` de cada trabajo, dentro de tu proyecto.

`agents/arbitro.md` no es una copia: es un envoltorio que remite al método de `skills/gauntlet/agents/arbitro.md`, que es la única fuente.
