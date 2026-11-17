# Enrutamiento de modelo y esfuerzo

Qué modelo y qué esfuerzo corre cada rol. Origen: sección 7 del diseño (`docs/diseno.md`). Los nombres de agente llevan siempre el prefijo del plugin.

## Tabla

| Trabajo | Modelo | Esfuerzo | Por qué |
|---|---|---|---|
| Jefe de pits: triage, contrato, plan, enrutamiento, resolver conflictos | Opus 5.5 | alto | Es trabajo de arquitectura: un error aquí se multiplica en cada encargo |
| Jefe de pits: coordinar (estado, propagar cambios, despachar oleadas) | la misma sesión | medio | Seguir el estado no exige el razonamiento del plan |
| Lector del plan (`pit-lane:lector-ingenuo`, `pit-lane:lector-critico`, `pit-lane:lector-ejecucion`) | Sonnet 5.5 (crítico en XL: Opus 5.5) | medio (alto en XL) | La revisión se escala al riesgo del plan |
| Mecánico (`pit-lane:mecanico`): redactar con criterio, analizar, integrar varias fuentes | Sonnet 5.5 | medio | Integrar y juzgar pide un modelo estándar, no el más caro |
| Mecánico experto (`pit-lane:mecanico-experto`): diseño difícil, decisiones con muchas dependencias | Opus 5.5 | alto | Es arquitectura, como el plan |
| Mecánico auxiliar (`pit-lane:mecanico-auxiliar`): transcribir, convertir, formatear, inventariar, con todo especificado | Haiku 5.5 | bajo | Rutina con especificación completa: no hay nada que interpretar |
| Subagente de búsqueda o lectura | Haiku 5.5 | bajo | Explorar y leer es barato y paralelo |
| Árbitro (`pit-lane:arbitro`), error costoso | Opus 5.5 | alto | La última revisión antes de que algo salga va al más capaz |
| Árbitro (`pit-lane:arbitro`), rutina | Sonnet 5.5 | medio | La revisión se escala al riesgo del entregable |

## Reglas

1. **El modelo y el esfuerzo se escriben siempre** en el encargo y en el despacho (R-12). Omitirlos hace que el mecánico herede los del Jefe de pits, que son los más caros.
2. **Antes del primer despacho** se comprueba que ninguna variable de entorno anule el enrutamiento (R-38). Ver la advertencia al final de este archivo.
3. **Haiku solo cuando el encargo lo trae todo** (R-13). Si el mecánico tiene que interpretar, el modelo barato toma dos o tres veces más turnos y termina costando más: pesa más el número de turnos que el precio por token. En la duda, Sonnet.
4. **Escalada** (R-27): un criterio que falla dos rondas seguidas pasa a un modelo un nivel superior, con enfoque distinto.
   - En el modo A, el Jefe de pits relanza el encargo con el nuevo modelo.
   - En el modo B, el Jefe de pits le indica al usuario el modelo que debe poner en el selector de esa sesión.
5. **Árbitro en modelo distinto del constructor** cuando el error es costoso y el constructor no es Opus (R-36). Si el constructor es Opus, el árbitro también lo es: la independencia la da el contexto limpio, no el modelo.
6. **La columna de esfuerzo es hipótesis.** Parte de una regla general: esfuerzo medio por defecto y alto para razonamiento profundo. El desglose por rol es propio y se calibra en el piloto midiendo rondas de auditoría por nivel.
   Sin ID en la sección 15 del diseño: es una nota de calibración, no una regla de comportamiento (decisión 2026-11-14).
7. **Plan Pro.** Según el artículo de soporte de Anthropic sobre los modelos Fable, en el plan Pro esos modelos no entran en los límites del plan: corren con créditos de uso, que se pagan aparte. Por eso el modelo más capaz de esta tabla es Opus 5.5 y Fable queda fuera del enrutamiento. Opus es el que más rápido gasta el límite de 5 horas, así que se reserva para el Jefe de pits, el mecánico experto y el árbitro de error costoso.
   Sin ID en la sección 15 del diseño; es una regla de enrutamiento (decisión 2026-11-14): Fable va fuera.

## Dónde se fija el modelo y el esfuerzo

- Un subagente acepta `model` (`sonnet`, `opus`, `haiku`, `fable`) y `effort` (`low` a `max`) en su definición y en cada invocación. **La invocación gana a la definición.** El parámetro de esfuerzo por invocación requiere Claude Code v2.1.292 o posterior.
- En la app de escritorio, cada sesión tiene su selector de modelo y de esfuerzo.
- En Projects hay ajustes separados de modelo y esfuerzo para el coordinador y para los hilos.

## Advertencia: variables de entorno que anulan el enrutamiento

El enrutamiento puede ignorarse sin aviso (R-38):

- **`CLAUDE_CODE_EFFORT_LEVEL`** tiene prioridad sobre el esfuerzo de la invocación y sobre el de la definición del agente. Si está fijada en `settings.json` (algunas guías de ahorro de tokens recomiendan fijarla), **toda la columna de esfuerzo se ignora**.
- **`CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`**, sola o junto con `CLAUDE_CODE_SUBAGENT_MODEL`, hace lo mismo con el modelo.

Antes del primer despacho, el Jefe de pits comprueba que no estén fijadas. Si lo están, no las cambia por su cuenta: se lo dice al usuario (hipótesis H8: quitarlas con su aprobación, o aceptar que el enrutamiento por agente no aplica).
