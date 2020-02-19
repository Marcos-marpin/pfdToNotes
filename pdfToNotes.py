import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import PageObject
import re
import sys

SCALE_FACTOR = 0.50


def crear_pagina_notas(pdf, pagina):
    width = pagina.mediaBox.upperRight[0]
    height = pagina.mediaBox.upperRight[1]
    pagina_notas = PageObject.createBlankPage(pdf, width, height)
    ty = float(height) - float(height) * SCALE_FACTOR  # traslacion en y
    pagina_notas.mergeScaledTranslatedPage(pagina, SCALE_FACTOR, 0, ty)
    return pagina_notas


# Argumentos
parser = argparse.ArgumentParser(description="Script para agregar espacio de notas en los PDF")
parser.add_argument("inputPDF", type=str, help="PDF que se quiere modificar")
args = parser.parse_args()

# Abrir PDF's
with open(args.inputPDF, "rb") as (inputPDF), \
        open(args.inputPDF.replace(".pdf", "") + "_notes.pdf", "wb") as outputPDF:
    pdf = PdfFileReader(inputPDF)
    newPfd = PdfFileWriter()
    for i in range(pdf.getNumPages()):
        pagina = pdf.getPage(i)
        newPfd.addPage(crear_pagina_notas(pdf, pagina))
    newPfd.write(outputPDF)
