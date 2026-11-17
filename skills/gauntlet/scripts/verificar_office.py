#!/usr/bin/env python3
"""
verificar_office.py — Evidencia objetiva sobre un archivo DOCX, PPTX o XLSX para auditorías GAUNTLET.

Qué reporta:
  - Metadatos (docProps/core.xml): título, autor, fechas de creación/modificación, idioma;
    alerta si el año de creación no es el actual.
  - Idiomas declarados en el contenido (w:lang en DOCX, lang/altLang en PPTX) con su conteo;
    con --idioma, alerta de los que no coinciden con el idioma del contrato (B1).
  - Con --prohibido, apariciones de cada texto prohibido (B3); y años mencionados en el texto,
    para revisar fechas.
  - Conteos de estructura: párrafos y tablas (DOCX), diapositivas y notas (PPTX),
    hojas, fórmulas y celdas con error en valores cacheados (XLSX).
  - Opcional --render DIR: exporta a PDF con Microsoft Office (office.ps1, en Windows) para
    la inspección visual; el PDF se abre con la herramienta de lectura, página por página.
    Si no hay Office, intenta con LibreOffice (soffice) si está instalado.
  - Opcional --recalcular (XLSX): recalcula una copia temporal con Excel y reporta los valores
    recalculados; el original no se toca.
  - Opcional --texto: imprime el texto extraído (por diapositiva / párrafo / hoja).

Uso:
  python3 verificar_office.py ARCHIVO [--render DIR] [--recalcular] [--texto]
          [--idioma es-MX] [--prohibido TEXTO --prohibido OTRO]

--idioma y --prohibido no tienen valor por defecto: se pasan los que fija el contrato.
Sin --idioma, los idiomas se listan pero no se comparan; sin --prohibido, no se busca ningún texto.

Sale con código 0 siempre que pudo leer el archivo; las alertas van en la sección ALERTAS.
Sin --recalcular, un XLSX se audita con sus valores cacheados, que pueden estar desactualizados.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter
from xml.etree import ElementTree as ET

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
}
W = "{%s}" % NS["w"]
A = "{%s}" % NS["a"]
YEAR_RE = re.compile(r"\b(19[5-9]\d|20[0-4]\d)\b")
EXCEL_ERRORS = ("#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A", "#NUM!", "#NULL!")


def read_xml(z, name):
    try:
        return ET.fromstring(z.read(name))
    except KeyError:
        return None


def core_props(z):
    root = read_xml(z, "docProps/core.xml")
    out = {}
    if root is None:
        return out
    for tag, key in [("dc:title", "titulo"), ("dc:creator", "autor"),
                     ("dcterms:created", "creado"), ("dcterms:modified", "modificado"),
                     ("dc:language", "idioma"), ("cp:lastModifiedBy", "modificado_por")]:
        el = root.find(tag, NS)
        if el is not None and el.text:
            out[key] = el.text
    return out


def docx_info(z):
    langs = Counter()
    for name in z.namelist():
        if name.startswith("word/") and name.endswith(".xml"):
            root = read_xml(z, name)
            if root is None:
                continue
            for el in root.iter(W + "lang"):
                v = el.get(W + "val")
                if v:
                    langs[v] += 1
    doc = read_xml(z, "word/document.xml")
    paras, texts, tables = 0, [], 0
    if doc is not None:
        tables = len(list(doc.iter(W + "tbl")))
        for p in doc.iter(W + "p"):
            t = "".join(x.text or "" for x in p.iter(W + "t")).strip()
            if t:
                paras += 1
                texts.append(t)
    # encabezados/pies también cuentan para buscar texto
    extra = []
    for name in z.namelist():
        if re.match(r"word/(header|footer)\d*\.xml", name):
            root = read_xml(z, name)
            if root is not None:
                extra.append(" ".join(x.text or "" for x in root.iter(W + "t")))
    struct = {"parrafos_con_texto": paras, "tablas": tables}
    return langs, struct, texts, extra


def pptx_info(z):
    langs = Counter()
    slides = sorted([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)],
                    key=lambda s: int(re.findall(r"\d+", s)[-1]))
    notes = [n for n in z.namelist() if re.match(r"ppt/notesSlides/notesSlide\d+\.xml$", n)]
    texts = []
    for name in z.namelist():
        if name.startswith("ppt/") and name.endswith(".xml"):
            root = read_xml(z, name)
            if root is None:
                continue
            for tag in ("rPr", "defRPr", "endParaRPr"):
                for el in root.iter(A + tag):
                    for attr in ("lang", "altLang"):
                        v = el.get(attr)
                        if v:
                            langs[v] += 1
    ilegibles = []
    for i, s in enumerate(slides, 1):
        root = read_xml(z, s)
        if root is None:
            ilegibles.append(s)
            continue
        t = " | ".join((x.text or "").strip() for x in root.iter(A + "t") if (x.text or "").strip())
        texts.append(f"[Diapositiva {i}] {t}")
    extra = []
    for n in notes:
        root = read_xml(z, n)
        if root is None:
            ilegibles.append(n)
            continue
        extra.append(" ".join(x.text or "" for x in root.iter(A + "t")))
    struct = {"diapositivas": len(slides), "diapositivas_con_notas": sum(1 for e in extra if e.strip())}
    if ilegibles:
        struct["partes_ilegibles"] = ilegibles
    return langs, struct, texts, extra


def xlsx_info(path):
    """Lee el XML de cada hoja: una celda con <f> y sin <v> no tiene valor calculado;
    t="e" o un valor de error es un error. Una fórmula que devuelve texto vacío ("")
    sí tiene <v> y no se cuenta como sin valor (openpyxl no distingue esos casos)."""
    import posixpath
    S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
    formulas, sin_valor, errores, texts, nombres = 0, [], [], [], []
    with zipfile.ZipFile(path) as z:
        wb = read_xml(z, "xl/workbook.xml")
        hojas = wb.find(S + "sheets") if wb is not None else None
        rels = read_xml(z, "xl/_rels/workbook.xml.rels")
        relmap = {r.get("Id"): r.get("Target") for r in rels} if rels is not None else {}
        shared = []
        sst = read_xml(z, "xl/sharedStrings.xml")
        if sst is not None:
            for si in sst.findall(S + "si"):
                shared.append("".join(t.text or "" for t in si.iter(S + "t")))
        for sh in (hojas if hojas is not None else []):
            nombre = sh.get("name")
            nombres.append(nombre)
            target = relmap.get(sh.get(R + "id"), "")
            target = target.lstrip("/") if target.startswith("/") else posixpath.join("xl", target)
            root = read_xml(z, target)
            if root is None:
                continue
            for c in root.iter(S + "c"):
                ref, t = c.get("r"), c.get("t")
                f, v = c.find(S + "f"), c.find(S + "v")
                val = v.text if v is not None else None
                if f is not None:
                    formulas += 1
                    if (v is None or v.text is None) and t != "str":
                        sin_valor.append(f"{nombre}!{ref}")
                if t == "e" or (val in EXCEL_ERRORS):
                    errores.append(f"{nombre}!{ref}={val}")
                if f is None and t == "s" and val is not None:
                    try:
                        texts.append(f"[{nombre}!{ref}] {shared[int(val)]}")
                    except (ValueError, IndexError):
                        pass
                elif f is None and t == "inlineStr":
                    texts.append(f"[{nombre}!{ref}] " + "".join(x.text or "" for x in c.iter(S + "t")))
    struct = {"hojas": nombres, "formulas": formulas,
              "formulas_sin_valor_cacheado": len(sin_valor),
              "celdas_con_error": len(errores)}
    if sin_valor:
        struct["ejemplos_sin_valor"] = sin_valor[:15]
    if errores:
        struct["ejemplos_error"] = errores[:30]
    return Counter(), struct, texts, []


OFFICE_PS1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "office.ps1")


def office(accion, entrada, salida=None):
    """Corre office.ps1. Devuelve (ok, salida estándar o mensaje de error)."""
    powershell = shutil.which("powershell") or shutil.which("pwsh")
    if os.name != "nt" or not powershell or not os.path.exists(OFFICE_PS1):
        return False, "Microsoft Office no disponible (requiere Windows con Office)"
    cmd = [powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", OFFICE_PS1,
           "-Accion", accion, "-Entrada", os.path.abspath(entrada)]
    if salida:
        cmd += ["-Salida", os.path.abspath(salida)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return False, "Office no respondió en 5 minutos"
    if r.returncode != 0:
        return False, (r.stderr or r.stdout).strip()[:300] or f"office.ps1 salió con código {r.returncode}"
    return True, r.stdout.strip()


def render(path, outdir):
    """Exporta a PDF para la inspección visual. Devuelve (ok, mensaje)."""
    os.makedirs(outdir, exist_ok=True)
    if path.lower().endswith(".pdf"):
        return True, f"PDF: {path} · ábrelo con la herramienta de lectura, página por página"
    base = os.path.splitext(os.path.basename(path))[0]
    pdf = os.path.join(outdir, base + ".pdf")
    ok, msg = office("pdf", path, pdf)
    if ok and os.path.exists(pdf):
        m = re.search(r"PAGINAS=(\S+)", msg)
        paginas = m.group(1) if m and m.group(1) != "?" else "ver en el PDF"
        return True, f"PDF (Microsoft Office): {pdf} · páginas: {paginas} · ábrelo con la herramienta de lectura, página por página"
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice:
        r = subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", outdir, path],
                           capture_output=True, text=True, timeout=180)
        if os.path.exists(pdf):
            return True, f"PDF (LibreOffice): {pdf} · ábrelo con la herramienta de lectura, página por página"
        msg += f" · LibreOffice también falló: {r.stderr.strip()[:200]}"
    return False, f"No se pudo exportar a PDF: {msg}"


def recalcular(path):
    """Recalcula una copia temporal con Excel. Devuelve (ruta de la copia o None, mensaje).
    La copia va siempre a la misma carpeta (%TEMP%/verificar_office) y reemplaza la de la corrida
    anterior del mismo archivo, para que las copias no se acumulen."""
    tmp = os.path.join(tempfile.gettempdir(), "verificar_office")
    os.makedirs(tmp, exist_ok=True)
    copia = os.path.join(tmp, os.path.basename(path))
    shutil.copy2(path, copia)
    ok, msg = office("recalcular", copia)
    if ok:
        return copia, f"Valores recalculados con Excel sobre una copia ({copia}); el original no se tocó"
    return None, msg


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("archivo")
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--recalcular", action="store_true")
    ap.add_argument("--texto", action="store_true")
    ap.add_argument("--prohibido", action="append", default=None)
    ap.add_argument("--idioma", default=None)
    args = ap.parse_args()
    # En Windows la salida redirigida usa cp1252, que no tiene "⚠": sin esto el script se cae justo al imprimir las alertas.
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    prohibidos = args.prohibido or []
    path = args.archivo
    ext = os.path.splitext(path)[1].lower()
    alertas = []

    print(f"# Verificación: {path}")
    if not os.path.exists(path):
        print("ALERTA: el archivo no existe")
        sys.exit(1)

    if ext in (".docx", ".pptx", ".xlsx") and not zipfile.is_zipfile(path):
        print("\n## ALERTAS\n- ⚠ El archivo no es un paquete Office válido (no es ZIP): está corrupto o no es lo que dice su extensión")
        sys.exit(1)
    if ext in (".docx", ".pptx", ".xlsx"):
        with zipfile.ZipFile(path) as z:
            meta = core_props(z)
            if ext == ".docx":
                langs, struct, texts, extra = docx_info(z)
            elif ext == ".pptx":
                langs, struct, texts, extra = pptx_info(z)
        if ext == ".xlsx":
            origen_valores = path
            if args.recalcular:
                copia, msg = recalcular(path)
                print(f"\n## Recálculo\n- {msg}")
                if copia:
                    origen_valores = copia
                else:
                    alertas.append(f"No se pudo recalcular ({msg}): los criterios sobre valores de celdas "
                                   "son NO VERIFICABLE salvo cálculo independiente")
            langs, struct, texts, extra = xlsx_info(origen_valores)
        if args.recalcular and ext != ".xlsx":
            alertas.append("--recalcular solo aplica a XLSX; se ignoró")

        print("\n## Metadatos")
        for k, v in meta.items():
            print(f"- {k}: {v}")
        import datetime
        anio = str(datetime.date.today().year)
        if meta.get("creado") and not meta["creado"].startswith(anio):
            alertas.append(f"Fecha de creación en metadatos = {meta['creado'][:10]} (no es {anio}; ¿plantilla vieja?)")
        if not meta.get("idioma"):
            alertas.append("core.xml sin dc:language")
        elif args.idioma and meta.get("idioma") != args.idioma:
            alertas.append(f"core.xml dc:language = {meta['idioma']} (se esperaba {args.idioma})")

        print("\n## Idiomas declarados en el contenido")
        if langs:
            for k, v in langs.most_common():
                print(f"- {k}: {v}")
            if args.idioma:
                otros = {k: v for k, v in langs.items() if k != args.idioma}
                if otros:
                    alertas.append(f"Idiomas distintos de {args.idioma}: {otros}")
            else:
                alertas.append("No se pasó --idioma: los idiomas se listan pero no se compararon con el del contrato (B1)")
        else:
            print("- (ninguno declarado en el contenido)")
            if ext in (".docx", ".pptx"):
                alertas.append(f"El contenido no declara idioma; el editor puede asumir inglés")

        print("\n## Estructura")
        for k, v in struct.items():
            print(f"- {k}: {v}")
        if struct.get("partes_ilegibles"):
            alertas.append(f"{len(struct['partes_ilegibles'])} parte(s) del paquete no se pudieron leer y no se revisaron")
        if ext == ".xlsx":
            if not struct.get("hojas"):
                alertas.append("El libro no tiene xl/workbook.xml legible o no declara hojas: no se revisó ninguna celda")
            if struct.get("celdas_con_error"):
                alertas.append(f"{struct['celdas_con_error']} celda(s) con error de Excel")
            if struct.get("formulas_sin_valor_cacheado"):
                alertas.append(f"{struct['formulas_sin_valor_cacheado']} fórmula(s) sin valor calculado: "
                               "corre de nuevo con --recalcular antes de auditar valores")

        todo = "\n".join(texts + extra)
        print("\n## Texto")
        if not prohibidos:
            print("- Texto prohibido: no se buscó ninguno (no se pasó --prohibido)")
        for p in prohibidos:
            n = len(re.findall(re.escape(p), todo, re.IGNORECASE))
            print(f"- '{p}' (sin distinguir mayúsculas): {n} aparición(es)")
            if n:
                alertas.append(f"Texto prohibido '{p}' aparece {n} vez/veces")
        years = Counter(YEAR_RE.findall(todo))
        print(f"- Años mencionados: {dict(years) if years else 'ninguno'}")
        if args.texto:
            print("\n## Texto extraído")
            for t in texts:
                print(t)
            for e in extra:
                if e.strip():
                    print(f"[Notas/encabezados] {e.strip()}")
    elif ext != ".pdf":
        print(f"Tipo {ext} no soportado por este script; usa el método de references/verificacion-por-tipo.md")
        alertas.append(f"Tipo {ext} no soportado: este script no revisó nada del contenido")
    elif not args.render:
        alertas.append("PDF: este script no revisa su contenido; ábrelo con la herramienta de lectura (verificacion-por-tipo.md §4)")

    if args.render:
        print("\n## Render")
        ok, msg = render(path, args.render)
        print("- " + msg)
        if not ok:
            alertas.append("Sin render: los criterios visuales son NO VERIFICABLE salvo revisión humana")

    print("\n## ALERTAS")
    if alertas:
        for a in alertas:
            print(f"- ⚠ {a}")
    else:
        print("- ninguna")


if __name__ == "__main__":
    main()
