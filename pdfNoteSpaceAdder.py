import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import PageObject
import re
import sys

SCALE_FACTOR = 0.50
ROTATION_DEGREES = -90

def crear_pagina_notas(pdf, pagina, orientacion):
    pagina_notas = PageObject.createBlankPage(pdf)
    tx = pagina_notas.mediaBox.upperLeft[0]  # traslacion en x
    ty = float(pagina_notas.mediaBox.upperLeft[1])  # traslacion en y
    if orientacion == "v":
        ty = ty - (ty * SCALE_FACTOR)
        pagina_notas.mergeScaledTranslatedPage(pagina, SCALE_FACTOR, tx, ty)
    else:
        pagina_notas.mergeRotatedScaledTranslatedPage(pagina, ROTATION_DEGREES, SCALE_FACTOR, tx, ty)
    return pagina_notas


# Argumentos
parser = argparse.ArgumentParser(description="Script para agregar espacio de notas en los PDF")
parser.add_argument("inputPDF", type=str, help="PDF que se quiere modificar")
parser.add_argument("-o", type=str,
                    help="Orientacion en la que está el pdf original [v = vertical, h = horizontal]", default="h")
args = parser.parse_args()

# Comprobar argumentos
if args.o != "v" and args.o != "h":
    parse_range("ERROR: la orientación debe ser [v = vertical, h = horizontal]")
    sys.exit()

# Abrir PDF's
with open(args.inputPDF, "rb") as (inputPDF), \
        open(args.inputPDF.replace(".pdf", "") + "_notes.pdf", "wb") as outputPDF:
    pdf = PdfFileReader(inputPDF)
    newPfd = PdfFileWriter()

    if r:
        for i in range(pdf.getNumPages()):
            pagina = pdf.getPage(i)
            if i in r:
                newPfd.addPage(crear_pagina_notas(pdf, pagina, args.o))
            else:
                newPfd.addPage(pagina)
    else:
        for i in range(pdf.getNumPages()):
            pagina = pdf.getPage(i)
            newPfd.addPage(crear_pagina_notas(pdf, pagina, args.o))
    newPfd.write(outputPDF)
