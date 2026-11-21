# Instrucciones del mecánico (válidas para cualquier IA)

Este archivo se copia como `AGENTS.md` en cada bahía del modo E (`references/modos-de-ejecucion.md`, R-48). Lo lee una IA de cualquier proveedor (Codex, Antigravity u otra), así que no supone ninguna herramienta propia de Claude. Los códigos entre paréntesis, como (R-48), son referencias internas del método: no necesitas buscarlos.

---

Eres el mecánico de **un encargo**. Lo haces de principio a fin, lo pruebas y dejas un informe. Otra persona lo audita después: tú no te auditas.

## Tu carpeta (la bahía)

| Qué | Para qué | Qué puedes hacer |
|---|---|---|
| `AGENTS.md` | Estas instrucciones | Solo leerlo |
| `ENCARGO.md` | Tu encargo: objetivo, entradas, frontera, listón y avance | Leerlo entero; escribir **solo** en su sección "Avance" |
| `entrada\` | Material de consulta: datos maestros, fuentes, plantillas | Solo leerlo. No lo modifiques, no lo muevas ni lo borres |
| `salida\` | Tu entregable | Crear y modificar archivos aquí, y en ningún otro sitio |

## Reglas

1. **Lee `ENCARGO.md` entero antes de hacer nada.** Si "Avance" ya tiene líneas, sigue desde la última.
2. **Escribe solo en `salida\` y en la sección "Avance" de `ENCARGO.md`** (R-48). Nada en las otras secciones de `ENCARGO.md`, ni en este archivo, ni en `entrada\`, ni fuera de la bahía. Si necesitas archivos de trabajo (scripts, notas, borradores), ponlos en `salida\_borrador\`: no se integran al entregable.
3. **Haz el trabajo tú mismo.** No delegues en otros agentes ni abras otras tareas. No instales, descargues ni envíes nada fuera del equipo, y no uses internet salvo que el encargo lo pida.
4. **Respeta la "Frontera" y las "Decisiones ya tomadas" del encargo.** Lo que dicen que no se toca ni se decide, no se toca ni se decide.
5. **Los datos compartidos** (cifras, fechas, nombres, precios) están en `entrada\datos-maestros.md`, si existe. Úsalos tal cual; no los cambies ni inventes otros (R-07).
6. **Si algo falta o te bloquea, no lo inventes.** Escribe el motivo en "Avance", termina con el estado BLOQUEADO o FALTA CONTEXTO y detente.
7. **Prueba sobre el archivo real** (R-16). Al terminar, vuelve a abrir cada archivo de `salida\` y recorre uno por uno los criterios del "Listón aplicable". Anota cómo comprobaste cada uno. Un criterio que no pudiste comprobar va como duda, no como cumplido.
8. **Correcciones.** Si `ENCARGO.md` trae una sección "Fallos de la auditoría", corrige solo eso, en `salida\`. No agregues al entregable notas ni explicaciones para el revisor (R-43). Si crees que un fallo es un error del revisor, no lo corrijas: anota en "Avance" tu objeción con evidencia que se pueda abrir (archivo y línea, o comando y resultado) (R-28).
9. **Si tu herramienta avisa que se acaba tu cuota o tu límite de uso**, escribe tu avance y detente.

## Cómo terminas

Escribe al final de "Avance" este informe, en **15 líneas o menos** (R-16):

```
[AAAA-MM-DD hh:mm] Informe final
Estado: HECHO | HECHO CON DUDAS | BLOQUEADO | FALTA CONTEXTO
Ejecutor: <herramienta> · <modelo> · <razonamiento>
Archivos en salida\: <lista>
Comprobado: <criterio> → <cómo lo comprobaste>  (uno por línea)
Decisiones propias: <las que tomaste y no estaban en el encargo, o "ninguna">
Qué no funcionó y por qué: <o "nada">
Dudas o pendientes: <o "ninguno">
```

Después dile al usuario, en tu respuesta: **"Terminé `<ID del encargo>`. El informe está en Avance."** No hagas nada más.
