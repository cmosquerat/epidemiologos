import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mysql.connector as connection
import seaborn as sns
import datetime

from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch, cm

from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch, cm
from io import StringIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfbase import pdfmetrics
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
import matplotlib.colors as colors
from reportlab.lib.colors import HexColor

rangos_elementos = {
    'ph': [4.5, 5, 5.5, 6],
    'n': [0.2, 0.3, 0.4, 0.5],
    'mo': [5, 10, 15, 20],
    'k': [0.2, 0.4, 0.6, 0.8],
    'ca': [1.5, 3, 5, 6],
    'mg': [0.6, 1.2, 1.8, 2.4],
    'na': [0.02, 0.04, 0.06, 0.08],
    'al': [0.4, 0.8, 1.2, 1.6],
    'cic': [10, 15, 20, 25],
    'p': [7, 14, 21, 28],
    'fe': [70, 140, 210, 280],
    'mn': [20, 40, 60, 80],
    'zn': [3, 6, 9, 12],
    'cu': [3, 6, 9, 12],
    's': [5, 10, 15, 20],
    'b': [0.15, 0.3, 0.45, 0.6],
    'ar': [7, 14, 21, 28],
    'l': [20, 25, 30, 35],
    'a': [30, 40, 50, 60]
}

rangos_relaciones = {
    "Ca/Mg": [2, 3, 4, 5],
    "Ca/K": [4, 8, 16, 32],
    "Mg/K": [1.25, 2.5, 5, 10],
    "Ca + Mg/K": [5, 10, 20, 40],
}

rangos_saturaciones = {
    "al": [0.05, 0.15, 0.29, 0.49],
    "k": [0.028, 0.046, 0.066, 0.095],
    "ca": [0.31, 0.46, 0.58, 0.68],
    "mg": [0.09, 0.13, 0.17, 0.23]
}


def remap(x, oMin, oMax, nMin, nMax):

    #range check
    if oMin == oMax:
        print("Warning: Zero input range")
        return None

    if nMin == nMax:
        print("Warning: Zero output range")
        return None

    #check reversed input range
    reverseInput = False
    oldMin = min(oMin, oMax)
    oldMax = max(oMin, oMax)
    if not oldMin == oMin:
        reverseInput = True

    #check reversed output range
    reverseOutput = False
    newMin = min(nMin, nMax)
    newMax = max(nMin, nMax)
    if not newMin == nMin:
        reverseOutput = True

    portion = (x - oldMin) * (newMax - newMin) / (oldMax - oldMin)
    if reverseInput:
        portion = (oldMax - x) * (newMax - newMin) / (oldMax - oldMin)

    result = portion + newMin
    if reverseOutput:
        result = newMax - portion

    return result


def get_database():

    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    años = [year]
    años = [2021]
    mydb = connection.connect(host="localhost",
                              database='multilab',
                              user="root",
                              passwd="admin")
    for año in años:
        query = f"Select * from muestra_{año};"
        muestras = pd.read_sql(query, mydb)
        query = f"Select * from orden_{año};"
        ordenes = pd.read_sql(query, mydb)
        query = f"Select * from solicitudes_{año};"
        solicitudes = pd.read_sql(query, mydb)
        query = f"Select * from finca;"
        finca = pd.read_sql(query, mydb)
        query = f"Select * from cliente;"
        cliente = pd.read_sql(query, mydb)
        query = f"Select * from municipios;"
        municipios = pd.read_sql(query, mydb)
        query = f"Select * from departamentos;"
        departamentos = pd.read_sql(query, mydb)
        query = f"Select * from tipo_analisis;"
        tipo_analisis = pd.read_sql(query, mydb)

    mydb.close()  #close the connection
    return muestras, ordenes, cliente, municipios, finca, tipo_analisis


def is_between(a, x, b):
    return min(a, b) < x < max(a, b)


def get_description(c_lab, muestras, ordenes, cliente, municipios, finca,
                    tipo_analisis):
    n_orden = muestras[muestras["codigo"] == c_lab]["orden"].values[0]
    orden = ordenes[ordenes["codigo"] == n_orden]
    c_muestras = orden["muestras"].values[0]
    fecha_solicitud = orden["fecha_solicitud"].values[0]
    fecha_solicitud = np.datetime_as_string(fecha_solicitud, unit='D')
    fecha_entrega = datetime.datetime.today().strftime('%Y-%m-%d')
    proyecto = orden["proyecto"].values[0]
    codigo_solicitante = orden["codigo_solicitante"].values[0]
    solicitante = cliente[cliente["codigo"] ==
                          codigo_solicitante]["nombre"].values[0]
    codigo_propietario = orden["codigo_propietario"].values[0]
    propietario = cliente[cliente["codigo"] ==
                          codigo_propietario]["nombre"].values[0]
    codigo_finca = orden["codigo_finca"].values[0]
    nombre_finca = finca[finca["codigo"] == codigo_finca]["nombre"].values[0]
    vereda = finca[finca["codigo"] == codigo_finca]["vereda"].values[0]
    codigo_municipio = finca[finca["codigo"] ==
                             codigo_finca]["municipio"].values[0]
    analisis = tipo_analisis[tipo_analisis["codigo"] == orden["clase_analisis"]
                             .values[0]]["nombre"].values[0]
    municipio = municipios[municipios["codigo_municipio"] ==
                           codigo_municipio]["nombre"].values[0]
    diccionario1 = {
        "Solicitante:": solicitante.encode('utf-8'),
        "Propietario:": propietario.encode('utf-8'),
        "Proyecto:": proyecto,
        "Finca:": nombre_finca,
        "Vereda:": vereda,
        "Municipio:": municipio
    }
    diccionario2 = {
        "N. Orden:": n_orden,
        "N. Muestras:": c_muestras,
        "N. lab:": c_lab,
        "Fecha Recibo: ": fecha_solicitud,
        "Fecha Entrega:": fecha_entrega
    }
    return diccionario1, diccionario2, analisis


def generate_pdf(c_lab, muestras, ordenes, cliente, municipios, finca,
                 tipo_analisis, rangos_elementos, rangos_relaciones,
                 rangos_saturaciones, output):

    diccionario1, diccionario2, analisis = get_description(
        c_lab, muestras, ordenes, cliente, municipios, finca, tipo_analisis)
    rangos = []
    blue = (0.27, 0.27, 0.52, 1)
    for key, value in rangos_elementos.items():
        valor = muestras.iloc[c_lab][key]
        if valor != None:
            valor = float(valor.replace(",", "."))
            text = key.upper() + " : " + str(valor)
            for i in range(0, 5, 1):
                if i == 0:
                    if is_between(0, valor, value[i]):
                        rangos.append([text, 1, 1])
                if i == 4:

                    if is_between(value[-1], valor, np.inf):
                        rangos.append([text, 5, 5])
                else:
                    if is_between(value[i - 1], valor, value[i]):
                        rangos.append(
                            [text,
                             remap(valor, 0, value[-1], 0, 5), i + 1])

    df = pd.DataFrame(rangos, columns=['Elemento', 'Rango', "Puesto"])
    PAGE_WIDTH = defaultPageSize[0]
    PAGE_HEIGHT = defaultPageSize[1]

    ############# Calculo relaciones #############

    rangos = []

    relaciones = dict()
    relaciones["Ca/Mg"] = float(muestras.iloc[c_lab]["ca"].replace(
        ",", ".")) / float(muestras.iloc[c_lab]["mg"].replace(",", "."))
    relaciones["Ca/K"] = float(muestras.iloc[c_lab]["ca"].replace(
        ",", ".")) / float(muestras.iloc[c_lab]["k"].replace(",", "."))
    relaciones["Mg/K"] = float(muestras.iloc[c_lab]["mg"].replace(
        ",", ".")) / float(muestras.iloc[c_lab]["k"].replace(",", "."))
    relaciones["Ca + Mg/K"] = (float(muestras.iloc[c_lab]["ca"].replace(
        ",", ".")) + float(muestras.iloc[c_lab]["mg"].replace(
            ",", "."))) / float(muestras.iloc[c_lab]["k"].replace(",", "."))

    for key, value in rangos_relaciones.items():
        valor = round(relaciones[key], 2)
        if valor != None:
            valor = float(valor)
            text = key + " : " + str(valor)
            for i in range(0, 5, 1):
                if i == 0:
                    if is_between(0, valor, value[i]):
                        rangos.append([text, 1, 1])
                if i == 4:

                    if is_between(value[-1], valor, np.inf):
                        print("?")
                        rangos.append([text, 5, 5])
                else:
                    if is_between(value[i - 1], valor, value[i]):
                        rangos.append(
                            [text,
                             remap(valor, 0, value[-1], 0, 5), i + 1])

    relaciones_df = pd.DataFrame(rangos,
                                 columns=['Elemento', 'Rango', "Puesto"])

    ############ Cálculo saturaciones ##############
    rangos = []

    saturaciones = dict()
    llaves = ["al", "k", "ca", "mg"]
    for key in llaves:
        temp_list = a = [x for x in llaves if x != key]
        sum = 0
        for value in temp_list:
            sum += float(muestras.iloc[c_lab][value].replace(",", "."))
        saturaciones[key] = round(
            float(muestras.iloc[c_lab][key].replace(",", ".")) / sum, 2)

    for key, value in rangos_saturaciones.items():
        valor = round(saturaciones[key], 2)
        if valor != None:
            valor = float(valor)
            text = key.upper() + " : " + str(valor)
            for i in range(0, 5, 1):
                if i == 0:
                    if is_between(0, valor, value[i]):
                        rangos.append([text, 1, 1])
                if i == 4:

                    if is_between(value[-1], valor, np.inf):
                        print("?")
                        rangos.append([text, 5, 5])
                else:
                    if is_between(value[i - 1], valor, value[i]):
                        rangos.append(
                            [text,
                             remap(valor, 0, value[-1], 0, 5), i + 1])

    saturaciones_df = pd.DataFrame(rangos,
                                   columns=['Elemento', 'Rango', "Puesto"])

    cim = plt.imread("degradado.png")
    cim = cim[cim.shape[0] // 2, 8:740, :]

    cmap = colors.ListedColormap(cim)
    with plt.rc_context({
            'axes.edgecolor': blue,
            'xtick.color': blue,
            'ytick.color': blue
    }):
        ############## Imagen 1 #############
        plt.figure(figsize=(12, 12))
        plt.title("INTERPRETACIÓN", weight='bold', color=(0.27, 0.27, 0.52, 1))
        gradient = np.linspace(0, 1, 100).reshape(1, -1)
        plt.imshow(gradient,
                   extent=[0.5, 5.5, -1, len(set(df.Elemento))],
                   aspect='auto',
                   cmap=cmap,
                   alpha=0.7)
        plot = sns.scatterplot(data=df,
                               y="Elemento",
                               x="Rango",
                               s=300,
                               color="black")
        sns.set(font_scale=2)
        plot.set_xticks([1, 2, 3, 4, 5])
        plot.set_xticklabels(
            ["BAJO", "MOD. \n BAJO", "MEDIO", "MOD. \n ALTO", "ALTO"])
        plot.set_xlim([0.5, 5.5])
        plot.set(xlabel=None)
        plot.set(ylabel=None)
        imgdata = io.BytesIO()
        plot.get_figure().savefig(imgdata, format='png', bbox_inches='tight')
        imgdata.seek(0)  # rewind the data
        Image = ImageReader(imgdata)
        plt.close()

    with plt.rc_context({
            'axes.edgecolor': blue,
            'xtick.color': blue,
            'ytick.color': blue
    }):
        ############# Imagen 2 ##############

        plt.figure(figsize=(10, 5))
        plt.title("RELACIONES", weight='bold', color=(0.27, 0.27, 0.52, 1))
        gradient = np.linspace(0, 1, 100).reshape(1, -1)
        plt.imshow(gradient,
                   extent=[0.5, 5.5, -1,
                           len(set(relaciones_df.Elemento))],
                   aspect='auto',
                   cmap=cmap,
                   alpha=0.7)
        plot = sns.scatterplot(data=relaciones_df,
                               y="Elemento",
                               x="Rango",
                               s=300,
                               color="black")
        plot.set_xticks([1, 2, 3, 4, 5])
        plot.set_xticklabels(
            ["BAJO", "MOD. \n BAJO", "MEDIO", "MOD. \n ALTO", "ALTO"],
            color=(0.27, 0.27, 0.52, 1))
        plot.set_xlim([0.5, 5.5])
        plot.set(xlabel=None)
        plot.set(ylabel=None)
        imgdata = io.BytesIO()
        plot.get_figure().savefig(imgdata, format='jpg', bbox_inches='tight')
        imgdata.seek(0)  # rewind the data
        Image2 = ImageReader(imgdata)
        plt.close()

    with plt.rc_context({
            'axes.edgecolor': blue,
            'xtick.color': blue,
            'ytick.color': blue
    }):
        ########## Imagen 3 ##############
        plt.figure(figsize=(10, 5))
        plt.title("SATURACIONES", weight='bold', color=(0.27, 0.27, 0.52, 1))
        gradient = np.linspace(0, 1, 100).reshape(1, -1)
        plt.imshow(gradient,
                   extent=[0.5, 5.5, -1,
                           len(set(saturaciones_df.Elemento))],
                   aspect='auto',
                   cmap=cmap,
                   alpha=0.7)
        plot = sns.scatterplot(data=saturaciones_df,
                               y="Elemento",
                               x="Rango",
                               s=300,
                               color="black")
        plot.set_xticks([1, 2, 3, 4, 5])
        plot.set_xticklabels(
            ["BAJO", "MOD. \n BAJO", "MEDIO", "MOD. \n ALTO", "ALTO"],
            color=(0.27, 0.27, 0.52, 1))
        plot.set_xlim([0.5, 5.5])
        plot.set(xlabel=None)
        plot.set(ylabel=None)
        imgdata = io.BytesIO()
        plot.get_figure().savefig(imgdata, format='jpg', bbox_inches='tight')
        imgdata.seek(0)  # rewind the data
        Image3 = ImageReader(imgdata)
        plt.close()

    ######### PDF ################

    packet = io.BytesIO()
    pdfmetrics.registerFont(
        TTFont('Titulo', 'ProximaNova/Proxima Nova Cond Black It.ttf'))
    pdfmetrics.registerFont(
        TTFont('Header', 'ProximaNova/Proxima Nova Black.ttf'))
    pdfmetrics.registerFont(
        TTFont('Light', 'ProximaNova/Proxima Nova Light.ttf'))
    can = canvas.Canvas(packet)
    can.setFillColorRGB(0, 0, 0)
    #### Titulo
    can.setFont("Header", 20)
    can.setFillColor(HexColor(0x454785))
    text = f"Reportes Suelos {analisis}"
    text_width = stringWidth(text, "Titulo", 14)
    can.drawString(22, 695, text)
    #### Información
    con = 0
    for key, value in diccionario1.items():
        can.setFont("Header", 10)
        text = str(key)
        text_width = stringWidth(text, "Header", 10)
        can.drawString((PAGE_WIDTH) / 8 - 30, 643 - (con * 20), text)
        can.setFont("Light", 10)
        text = str(value)
        can.drawString((PAGE_WIDTH) / 8 - 30 + text_width + 10,
                       643 - (con * 20), text)
        con += 1
    con = 0
    for key, value in diccionario2.items():
        can.setFont("Header", 10)
        text = str(key)
        text_width = stringWidth(text, "Header", 10)
        can.drawString((PAGE_WIDTH) / 8 + (PAGE_WIDTH) / 2, 643 - (con * 20),
                       text)
        can.setFont("Light", 10)
        text = str(value)
        can.drawString(
            ((PAGE_WIDTH) / 8) + ((PAGE_WIDTH) / 2) + text_width + 10,
            643 - (con * 20), text)
        con += 1

    can.drawImage(Image, (PAGE_WIDTH) / 8 - 40, (PAGE_WIDTH) / 2 - 110, 300,
                  300)
    can.drawImage(Image2, (PAGE_WIDTH) / 2 + 50, (PAGE_WIDTH) - 230, 200, 100)
    can.drawImage(Image3, (PAGE_WIDTH) / 2 + 60, (PAGE_WIDTH) - 370, 200, 100)
    can.save()
    can.showPage()

    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    existing_pdf = PdfFileReader(open("template.pdf", "rb"))
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    return diccionario1["Finca:"]


def get_muestras(c_orden):
    muestras, ordenes, cliente, municipios, finca, tipo_analisis = get_database(
    )
    buffer = io.BytesIO()
    muestras_t = muestras[muestras["orden"] == c_orden]
    output = PdfFileWriter()

    for c_lab in muestras_t.codigo:
        print(c_lab)
        finca_o = generate_pdf(c_lab, muestras, ordenes, cliente, municipios,
                               finca, tipo_analisis, rangos_elementos,
                               rangos_relaciones, rangos_saturaciones, output)

    output.write(buffer)
    outputStream = open("destination.pdf", "wb")
    output.write(outputStream)
    buffer.seek(0)
    return buffer, finca_o
