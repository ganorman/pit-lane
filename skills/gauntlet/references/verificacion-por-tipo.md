# Verificación por tipo de entregable

Principio: **verificar, no suponer.** La evidencia es lo que sale del archivo real, no lo que alguien dice que hizo. Este documento da el método mínimo por tipo; el contrato puede exigir más.

Script de apoyo: `scripts/verificar_office.py ARCHIVO [--render DIR] [--texto]`. Reporta metadatos (y alerta si el año de creación no es el actual), idiomas declarados (alerta si no son es-DO), apariciones de "PVDC", años mencionados en el texto, estructura (párrafos, tablas, diapositivas, notas, hojas, fórmulas, errores) y, con `--render`, el PDF y un PNG por página.

## Contenido

| Tipo | Ir a |
|---|---|
| DOCX | §1 |
| PPTX | §2 |
| XLSX | §3 |
| PDF | §4 |
| Código y scripts | §5 |
| Web / HTML / artifact | §6 |
| Datos y cifras | §7 |
| Citas bíblicas | §8 |
| Imágenes, diagramas, renders | §9 |
| Texto en el chat (sin archivo) | §10 |
| Material de entrenamiento o procedimiento técnico (SOP, OJT, examen) | §11 |

---

## 1. DOCX

1. `verificar_office.py archivo.docx --render render/ --texto`
2. **Idioma (B1):** la sección de idiomas solo debe mostrar es-DO. Cualquier en-US es NO PASA.
3. **Fecha (B2):** el año de creación en metadatos y los años del texto deben ser los reales. Una fecha de plantilla es NO PASA.
4. **Contenido:** usa `--texto` para contar secciones, preguntas o ítems contra el listón. Cuenta; no estimes.
5. **Visual:** abre cada PNG del render (con la herramienta de leer imágenes). Busca texto cortado, tablas desbordadas, páginas en blanco, encabezados y pies faltantes y logos mal puestos. Una inspección visual sin abrir las imágenes no cuenta.
6. **Doble cara / impresión:** si el listón lo pide, revisa en el PDF el número de páginas (par o impar) y los saltos de sección.

Dónde atacar: ¿responde lo que pidió la TAREA o se desvió hacia algo más fácil? · secciones del ENTREGABLE que faltan (compara lista contra lista) · cifras, nombres o fechas que cambian entre secciones · términos técnicos usados de forma inconsistente · títulos huérfanos, tablas partidas, numeración rota.

## 2. PPTX

1. `verificar_office.py archivo.pptx --render render/ --texto`
2. **Idioma:** igual que DOCX (atributos `lang` y `altLang`).
3. **Conteo:** número de diapositivas y diapositivas con notas del orador contra el listón.
4. **Visual:** abre cada PNG. Revisa texto fuera de los cuadros, superposiciones, contraste, tamaño mínimo de fuente y que las imágenes carguen.
5. **Notas del orador:** si el listón las exige, comprueba que cada diapositiva tenga notas con contenido real, no un relleno.

Dónde atacar: diapositivas con más texto del que se puede proyectar (más de unas 6 líneas de cuerpo) · saltos en el orden lógico · mezcla de marcas (GAN con Barrick) · imágenes pixeladas o deformadas.

## 3. XLSX

1. **Recalcula primero, sobre una copia.** Corre `scripts/recalc.py copia.xlsx` de la skill xlsx: fuerza `calculateAll()` en LibreOffice. Abrir y guardar con LibreOffice **no** basta, porque solo llena las fórmulas sin valor y deja intactos los valores guardados falsos. Si no tienes `recalc.py` ni otra forma de forzar el recálculo completo, los criterios sobre valores de celdas son NO VERIFICABLE, salvo que los cotejes con el cálculo independiente del paso 4. Sin recalcular, los valores cacheados pueden mentir. Hazlo sobre una copia porque LibreOffice reescribe el idioma del libro (puede dejarlo en en-US): el idioma (B1) se audita en el original, y los valores en la copia.
2. `verificar_office.py copia.xlsx`: debe dar `celdas_con_error: 0` y `formulas_sin_valor_cacheado: 0`.
3. **Fórmulas, no valores fijos:** en las celdas que el listón dice que se calculan, comprueba con openpyxl (`data_only=False`) que contienen una fórmula que empieza con `=`.
4. **Cuadre:** recalcula de forma independiente en Python 2 o 3 resultados clave (totales, cuotas, promedios) y compáralos con la celda. Reporta los dos valores.
5. **Casos límite:** si el listón lo pide, cambia una entrada en una copia (cero, negativo, vacío), recalcula y mira si algo se rompe.

Dónde atacar: rangos de fórmula que no cubren todas las filas (una SUMA que se quedó corta) · errores en celdas ocultas · unidades y formatos (moneda, %, fechas, redondeo) · entradas mezcladas con cálculos sin etiquetar.

## 4. PDF

1. `pdftotext -layout archivo.pdf -` para el texto; `pdftoppm -png -r 60` para las páginas.
2. Número de páginas: `pdfinfo`.
3. Abre las imágenes para lo visual. Coteja el texto extraído contra las fuentes según §7 y §8.

## 5. Código y scripts

1. **Ejecútalo.** Con las entradas del caso real y con al menos un caso límite (vacío, valor extremo, archivo inexistente).
2. Si hay tests, córrelos y cita la salida. Si no los hay y el listón exige que funcione, escribe un test mínimo de comprobación (en un directorio aparte, no dentro del entregable salvo que se pida).
3. Lee los errores y avisos de la salida; un "funcionó" sin salida no es evidencia.
4. Para macros, VBA o automatizaciones que no se pueden ejecutar aquí, el criterio es NO VERIFICABLE, salvo que el contrato lo marque como "revisión humana".

Dónde atacar: fallos silenciosos (atrapa el error y sigue) · secretos o credenciales en el código · efectos irreversibles (borrar, enviar, sobrescribir) sin confirmación ni modo de prueba · acentos y caracteres especiales · funciones que nadie pidió.

## 6. Web / HTML / artifact

1. Ábrela en un navegador headless (Playwright con Chromium) y toma una captura de pantalla de escritorio y otra a 375 px de ancho.
2. Revisa la consola: cero errores de JavaScript.
3. Prueba cada interacción que exige el listón (botones, formularios, filtros) y cita el resultado observado.

## 7. Datos y cifras

1. Haz una tabla: dato del entregable → ubicación en la fuente → valor en la fuente → coincide sí/no.
2. Todo dato sin fuente es NO PASA por B5, salvo que esté marcado como "pendiente de confirmar" en el entregable.
3. Recalcula los derivados (porcentajes, sumas, conversiones) en Python; no los verifiques de cabeza.
4. Si el dato depende del estado actual del mundo (precios, tarifas, normativas, cargos), comprueba con búsqueda web y cita la fuente y la fecha.
5. **Conteos:** si el entregable dice "10 puntos", cuéntalos.

Dónde atacar: lo que suena bien pero no aparece en ninguna fuente (márcalo como inventado) · fuentes que discrepan entre sí: ¿se usó la fuente base de forma consistente? · citas atribuidas a quien no las dijo.

## 8. Citas bíblicas

1. Versión por defecto: RV1960, salvo que el contrato diga otra.
2. Tabla: referencia → texto del entregable → texto de la versión → coincide sí/no.
3. Revisa que la referencia (libro, capítulo, versículo) corresponda al contenido citado: es el error más común. Por ejemplo, poner Job 34:5 donde va Job 3:3.
4. Si no tienes acceso a la versión para cotejar (ni archivo ni web), el criterio es NO VERIFICABLE, no PASA.

## 9. Imágenes, diagramas, renders

1. Abre la imagen con la herramienta de lectura de imágenes. Describe lo que ves contra cada criterio.
2. Revisa el texto dentro de la imagen letra por letra: ortografía, cifras, nombres.
3. En diagramas, comprueba que cada nodo y cada conexión del listón existan y apunten en la dirección correcta.

## 10. Texto en el chat (sin archivo)

Guarda el texto en un archivo `.md` en el directorio de trabajo para que el árbitro lo audite desde el disco, con los mismos criterios de §7 y §8.

## 11. Material de entrenamiento o procedimiento técnico (SOP, OJT, examen)

Recórrelo como un aprendiz que no sabe nada, paso por paso.

1. **Objetivos:** cada uno es observable y medible (verbo de acción, condición, criterio).
2. **Pasos:** cada paso dice quién lo hace, qué hace, con qué herramienta y cómo sabe que terminó.
3. **Seguridad:** cada paso con energía peligrosa tiene su control (LOTO, verificación de energía cero o try-out, EPP), y el orden de los pasos es seguro. Las advertencias van **antes** del paso peligroso, no después.
4. **Terminología:** coincide con la del sitio, los equipos reales y las normas citadas.
5. **Evaluación:** cada objetivo tiene al menos una pregunta o actividad que lo mide. En exámenes de selección múltiple: número exacto de preguntas, una sola respuesta correcta por pregunta, clave cotejada pregunta por pregunta, distractores plausibles y sin pistas gramaticales.
6. **Nivel:** adecuado al público declarado (por ejemplo, aprendiz del Sistema Dual frente a técnico con experiencia).

Lo técnico de seguridad que no se pueda cotejar con un procedimiento del sitio o una norma disponible es NO VERIFICABLE y va a "Revisa tú": un SOP de LOTO nunca se aprueba solo por el árbitro.
