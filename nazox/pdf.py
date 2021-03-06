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

map_elementos = {
    'ph': "pH",
    'n': "N",
    'mo': "MO",
    'k': "K",
    'ca': "Ca",
    'mg': "Mg",
    'na': "Na",
    'al': "Al",
    'cic': "CIC",
    'p': "P",
    'fe': "Fe",
    'mn': "Mn",
    'zn': "Zn",
    'cu': "CU",
    's': "S",
    'b': "B",
    'ar': "Ar",
    'l': "L",
    'a': "A"
}

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

rangos_elementos_cafe = {
    'ph': [4.6, 5, 5.4, 5.8],
    'n': [0.2, 0.3, 0.4, 0.5],
    'mo': [4, 7, 10, 13],
    'k': [0.12, 0.24, 0.36, 0.48],
    'ca': [1, 3, 5, 9],
    'mg': [0.3, 0.8, 1.3, 2.3],
    'na': [0.02, 0.04, 0.06, 0.08],
    'al': [0.4, 0.8, 1.2, 2],
    'cic': [15, 19, 23, 27],
    'p': [3, 6, 12, 24],
    'fe': [150, 200, 250, 300],
    'mn': [12, 24, 36, 60],
    'zn': [1.8, 3.6, 5.4, 7.2],
    'cu': [1.8, 3.6, 5.4, 7.2],
    's': [4, 8, 12, 20],
    'b': [0.15, 0.3, 0.45, 0.6],
    'ar': [20, 26, 32, 38],
    'l': [21, 25, 29, 33],
    'a': [35, 42, 49, 56]
}

rangos_elementos_citricos = {
    'ph': [4.6, 5, 5.4, 5.8],
    'n': [0.2, 0.25, 0.3, 0.35],
    'mo': [4, 5, 6, 8],
    'k': [0.2, 0.4, 0.6, 0.8],
    'ca': [3, 4.5, 6, 7.5],
    'mg': [0.8, 1.6, 2.4, 4],
    'na': [0.02, 0.04, 0.06, 0.1],
    'al': [0.2, 0.5, 0.8, 1.4],
    'cic': [15, 18, 21, 24],
    'p': [5, 10, 20, 40],
    'fe': [200, 250, 300, 400],
    'mn': [30, 45, 60, 90],
    'zn': [4, 6, 8, 10],
    'cu': [4, 6, 8, 10],
    's': [5, 10, 20, 40],
    'b': [0.3, 0.4, 0.5, 0.7],
    'ar': [22, 28, 34, 40],
    'l': [22, 25, 28, 31],
    'a': [38, 43, 48, 53]
}

rangos_elementos_aguacate = {
    'ph': [5, 5.2, 5.4, 5.6],
    'n': [0.2, 0.3, 0.4, 0.5],
    'mo': [6, 8, 10, 14],
    'k': [0.15, 0.25, 0.35, 0.45],
    'ca': [1, 2, 3, 5],
    'mg': [0.3, 0.6, 0.9, 1.5],
    'na': [0.02, 0.03, 0.04, 0.6],
    'al': [0.25, 0.5, 0.75, 1],
    'cic': [18, 22, 26, 30],
    'p': [2, 6, 10, 18],
    'fe': [140, 180, 220, 300],
    'mn': [10, 20, 30, 50],
    'zn': [3, 5, 7, 9],
    'cu': [2, 4, 6, 8],
    's': [4, 8, 12, 20],
    'b': [0.15, 0.3, 0.45, 0.6],
    'ar': [16, 21, 26, 31],
    'l': [24, 27, 30, 33],
    'a': [43, 48, 53, 58]
}

rangos_elementos_pasto = {
    'ph': [5.3, 5.5, 5.7, 5.9],
    'n': [0.2, 0.3, 0.4, 0.5],
    'mo': [5, 7, 9, 13],
    'k': [0.2, 0.3, 0.4, 0.6],
    'ca': [2, 4, 6, 8],
    'mg': [0.7, 1.3, 1.9, 3.1],
    'na': [0.04, 0.06, 0.08, 0.12],
    'al': [0.25, 0.5, 0.75, 1],
    'cic': [18, 22, 26, 30],
    'p': [2, 6, 10, 18],
    'fe': [140, 180, 220, 300],
    'mn': [10, 20, 30, 50],
    'zn': [3, 5, 7, 9],
    'cu': [2, 4, 6, 8],
    's': [4, 8, 12, 20],
    'b': [0.15, 0.3, 0.45, 0.6],
    'ar': [16, 21, 26, 31],
    'l': [24, 27, 30, 33],
    'a': [43, 48, 53, 58]
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


def get_database(orden):

    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    a??os = [year]
    #a??os = [2021]
    mydb = connection.connect(host="190.147.28.95",
                              database='multilab',
                              user="root",
                              passwd="d3f4g5h6")
    for a??o in a??os:
        query = f"Select * from muestra_{a??o} WHERE orden={orden};"
        print("Obteniendo muestras")
        muestras = pd.read_sql(query, mydb)
        query = f"Select * from orden_{a??o};"
        print("Obteniendo ??rdenes")
        ordenes = pd.read_sql(query, mydb)
        query = f"Select * from finca;"
        print("Obteniendo Fincas")
        finca = pd.read_sql(query, mydb)
        query = f"Select * from cliente;"
        print("Obteniendo Clientes")
        cliente = pd.read_sql(query, mydb)
        query = f"Select * from municipios;"
        print("Obteniendo Municipios")
        municipios = pd.read_sql(query, mydb)
        query = f"Select * from tipo_analisis;"
        print("Obteniendo Analisis")
        tipo_analisis = pd.read_sql(query, mydb)

    mydb.close()  #close the connection
    return muestras, ordenes, cliente, municipios, finca, tipo_analisis


def is_between_min(a, x, b):
    return min(a, b) < x <= max(a, b)

def is_between_max(a,x,b):
    return min(a, b) <= x < max(a, b)



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
                             .values[0]]["descripcion"].values[0]
    municipio = municipios[municipios["codigo_municipio"] ==
                           codigo_municipio]["nombre"].values[0]
    diccionario1 = {
        "Solicitante:": solicitante,
        "Propietario:": propietario,
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
    muestras = muestras[muestras["codigo"] == c_lab]
    blue = (0.27, 0.27, 0.52, 1)
    for key, value in rangos_elementos.items():
        valor = muestras[key].values[0]
        if valor != None:
            valor = float(valor.replace(",", "."))
            text = map_elementos[key] + " : " + str(valor)
            for i in range(0, 5, 1):
                if i == 0:
                    if is_between_max(0, valor, value[i]):
                        rangos.append([text, 1, 1])
                if i == 4:

                    if is_between_min(value[-1], valor, np.inf):
                        rangos.append([text, 5, 5])
                else:
                    if is_between_max(value[i - 1], valor, value[i]):
                        rangos.append([
                            text,
                            remap(valor, value[0], value[-1], 0, 5), i + 1
                        ])
    print(rangos)

    df = pd.DataFrame(rangos, columns=['Elemento', 'Rango', "Puesto"])
    print(df)
    PAGE_WIDTH = defaultPageSize[0]
    PAGE_HEIGHT = defaultPageSize[1]

    ############# Calculo relaciones #############

    rangos = []

    relaciones = dict()
    relaciones["Ca/Mg"] = float(muestras["ca"].values[0].replace(
        ",", ".")) / float(muestras["mg"].values[0].replace(",", "."))
    relaciones["Ca/K"] = float(muestras["ca"].values[0].replace(
        ",", ".")) / float(muestras["k"].values[0].replace(",", "."))
    relaciones["Mg/K"] = float(muestras["mg"].values[0].replace(
        ",", ".")) / float(muestras["k"].values[0].replace(",", "."))
    relaciones["Ca + Mg/K"] = (float(muestras["ca"].values[0].replace(
        ",", ".")) + float(muestras["mg"].values[0].replace(
            ",", "."))) / float(muestras["k"].values[0].replace(",", "."))

    for key, value in rangos_relaciones.items():
        valor = round(relaciones[key], 2)
        if valor != None:
            valor = float(valor)
            text = key + " : " + str(valor)
            for i in range(0, 5, 1):
                if i == 0:
                    if is_between_max(0, valor, value[i]):
                        rangos.append([text, 1, 1])
                if i == 4:

                    if is_between_min(value[-1], valor, np.inf):
                        print("?")
                        rangos.append([text, 5, 5])
                else:
                    if is_between_max(value[i - 1], valor, value[i]):
                        rangos.append([
                            text,
                            remap(valor, value[0], value[-1], 0, 5), i + 1
                        ])

    relaciones_df = pd.DataFrame(rangos,
                                 columns=['Elemento', 'Rango', "Puesto"])

    ############ C??lculo saturaciones ##############
    rangos = []

    saturaciones = dict()
    llaves = ["al", "k", "ca", "mg"]
    for key in llaves:
        temp_list = a = [x for x in llaves if x != key]
        sum = 0
        for value in temp_list:
            sum += float(muestras[value].values[0].replace(",", "."))
        saturaciones[key] = round(
            float(muestras[key].values[0].replace(",", ".")) / sum, 2)

    for key, value in rangos_saturaciones.items():
        valor = round(saturaciones[key], 2)
        if valor != None:
            valor = float(valor)
            text = map_elementos[key] + " : " + str(valor)
            for i in range(0, 5, 1):
                if i == 0:
                    if is_between_max(0, valor, value[i]):
                        rangos.append([text, 1, 1])
                if i == 4:

                    if is_between_min(value[-1], valor, np.inf):
                        print("?")
                        rangos.append([text, 5, 5])
                else:
                    if is_between_max(value[i - 1], valor, value[i]):
                        rangos.append([
                            text,
                            remap(valor, value[0], value[-1], 0, 5), i + 1
                        ])

    saturaciones_df = pd.DataFrame(rangos,
                                   columns=['Elemento', 'Rango', "Puesto"])

    cim = plt.imread("degradado.png")
    cim = cim[cim.shape[0] // 2, 8:740, :]
    sns.set(font_scale=2)
    cmap = colors.ListedColormap(cim)
    with plt.rc_context({
            'axes.edgecolor': blue,
            'xtick.color': blue,
            'ytick.color': blue
    }):
        ############## Imagen 1 ############
        plt.figure(figsize=(12, 12))
        plt.title("INTERPRETACI??N", weight='bold', color=(0.27, 0.27, 0.52, 1))
        gradient = np.linspace(0, 1, 100).reshape(1, -1)
        plt.imshow(gradient,
                   extent=[0.5, 5.5, -1, len(set(df.Elemento))],
                   aspect='auto',
                   cmap=cmap,
                   alpha=0.9)

        plot = sns.scatterplot(data=df,
                               y="Elemento",
                               x="Rango",
                               s=300,
                               color="black")
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
                   alpha=0.9)
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
                   alpha=0.9)
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
    text = f"Reporte {analisis}"
    text_width = stringWidth(text, "Titulo", 14)
    can.drawString(22, 695, text)
    #### Informaci??n
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
    diccionario2["Referencia"] = muestras["referencia"].values[0]
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
        c_orden)
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
