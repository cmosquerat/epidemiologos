from django.http import request
from django.shortcuts import redirect, render
from django.views import View   
from django.contrib.auth.mixins import LoginRequiredMixin
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
import sqlite3
from django.conf import settings
import plotly.express as px
import plotly.figure_factory as ff
from dython import nominal
from sklearn.svm import SVR
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from django.urls import reverse
import logging
from django.http import HttpResponseRedirect
from django.contrib import messages
from sklearn.preprocessing import StandardScaler
from django.urls import reverse
import logging
from django.http import HttpResponseRedirect
from django.contrib import messages
import pickle
import catboost as cb
from sklearn.preprocessing import StandardScaler
import category_encoders as ce
import catboost as cb
from nazox.pdf import *
import io
from django.http import FileResponse

# Epilepsia
class EpilepsiaView(LoginRequiredMixin,View):
    def get(self, request):

        print(request.session)
        
        con = sqlite3.connect(settings.DATABASES['default']['NAME'])

        df = pd.read_sql_query("SELECT * from epilepsia", con,index_col="INDEX")
        
        observaciones = len(df.index) 

        data = df.groupby("SEXO")["SEXO"].count()
        labels = data.keys()
        graphs =  px.pie(data, values="SEXO",names=labels)
        graphs.update_traces( marker=dict( line=dict(color='#000000', width=3)))
        graphs.update_layout(  font=dict(
                size=18,
                
            ))

       

        # Setting layout of the figure.
        layout = {
            'title': 'Sexo de pacientes',
            'xaxis_title': 'Sexo',
            'yaxis_title': 'Cantidad',
        }


        
       


        # Getting HTML needed to render the plot.
        plot_div = plot({'data': graphs, 'layout': layout}, 
                        output_type='div')
        greeting = {}
        greeting['title'] = "Epilepsia"
        greeting['pageview'] = "Dashboard"
        greeting["plot_div"] = plot_div
        greeting["observaciones"] = str(observaciones)
        greeting["trastorno_c"] = len(df[df["TRASTORNO_DEL_APRENDIZAJE_(VV-NN-EE)"]=="SI"].index)
        greeting["rr"] = len(df[df["ALTERACIÓN_RR"]=="SI"].index)
        greeting["vv"] = len(df[df["ALTERACIÓN_VV"]=="SI"].index)
        greeting["nn"] = len(df[df["ALTERACIÓN_NN"]=="SI"].index)
        greeting["ee"] = len(df[df["ALTERACION_EE"]=="SI"].index)
        greeting["edad"] = epi_edad(df)
        greeting["cor"] = get_epicorr(df)
        greeting["trastorno"] = epi_trastorno(df)
        greeting["clinica_raz"] = get_clinicaraz(df)
        greeting["clinica_tras"] = epi_clinicatras(df)
        greeting["alteracionee"] = get_alteracion(df,"ALTERACION_EE")
        greeting["alteracionnn"] = get_alteracion(df,"ALTERACIÓN_NN")
        greeting["alteracionvv"] = get_alteracion(df,"ALTERACIÓN_VV")
        greeting["tipoall"] = get_tipoall(df)
        greeting["reg"] = epi_regression(df)
        replace = '<table border="1" class="dataframe">'
        greeting["tabla"] =  df.round(decimals=2).to_html(classes=None, border=None, justify=None,index=False).replace(replace,"").replace("</table>","")
        
        return render(request, 'menu/index_epilepsia.html',context=greeting)







def epi_edad(df):
    data = df.groupby("EDAD")["EDAD"].count()
    labels = data.keys()
    graphs = px.pie(data, values="EDAD",names=labels)
    graphs.update_traces( marker=dict( line=dict(color='#000000', width=3)))
    graphs.update_layout(  font=dict(
                size=18,
                
            ))
    layout = {
            'title': 'Edad de pacientes',
            'xaxis_title': 'Edad',
            'yaxis_title': 'Cantidad',
        }
    return plot({'data': graphs, 'layout': layout}, 
                        output_type='div')

def epi_trastorno(df):
    data = df.groupby("TRASTORNO_DEL_APRENDIZAJE_(VV-NN-EE)")["TRASTORNO_DEL_APRENDIZAJE_(VV-NN-EE)"].count()
    labels = data.keys()
    graphs = px.pie(data, values="TRASTORNO_DEL_APRENDIZAJE_(VV-NN-EE)",names=labels)
    graphs.update_traces( marker=dict( line=dict(color='#000000', width=3)))
    graphs.update_layout(  font=dict(
                size=18,
                
            ))
    layout = {
            'title': 'Trastorno del aprendizaje',
            'xaxis_title': 'Trastorno',
            'yaxis_title': 'Cantidad',
        }
    return plot({'data': graphs, 'layout': layout}, 
                        output_type='div')

def get_epicorr(df):
    
    cor = nominal.compute_associations(df)

    graphs = px.imshow(cor,x=cor.columns,
    y=cor.columns, color_continuous_scale=px.colors.sequential.Inferno,height=1000)
    
    
    

    # Setting layout of the figure.
    layout = {
        'title': 'Correlacion de variables',
    
        
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': graphs, 'layout': layout}, 
                    output_type='div'))



def epi_clinicatras(df):
    fig = px.histogram(df, x="CLINICA", color="TRASTORNO_DEL_APRENDIZAJE_(VV-NN-EE)")
    fig.update_traces( marker=dict( line=dict(color='#000000', width=3)))
    fig.update_layout(  font=dict(
            size=18,
            
        ))
    
    
    

    # Setting layout of the figure.
    layout = {
        'title': 'Correlacion de variables',
    
        
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': fig, 'layout': layout}, 
                    output_type='div'))


def get_clinicaraz(df):
    
    fig = px.histogram(df, x="CLINICA", color="RAZONAMIENTO_LÓGICO_RR.1")
    fig.update_traces( marker=dict( line=dict(color='#000000', width=3)))
    fig.update_layout(  font=dict(
            size=18,
            
        ))
    
    
    

    # Setting layout of the figure.
    layout = {
        'title': 'Correlacion de variables',
    
        
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': fig, 'layout': layout}, 
                    output_type='div'))


def get_tipoall(df):
    
    fig = px.histogram(df, x="TIPO", color="TRASTORNO_DEL_APRENDIZAJE_(VV-NN-EE)",orientation="v")
    fig.update_traces( marker=dict( line=dict(color='#000000', width=3)))
    fig.update_layout(  font=dict(
            size=18,
            
        ))

    # Setting layout of the figure.
    layout = {
        'title': 'TIPO caracterizado por TRASTORNO_DEL_APRENDIZAJE_(VV-NN-EE) ',
    
        
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': fig, 'layout': layout}, 
                    output_type='div'))


def get_alteracion(df,alteracion):
    
    fig = px.histogram(df, x="TIPO", color=f"{alteracion}",orientation="v")
    fig.update_traces( marker=dict( line=dict(color='#000000', width=3)))
    fig.update_layout(  font=dict(
            size=18,
            
        ))

    # Setting layout of the figure.
    layout = {
        'title': f'TIPO caracterizado por {alteracion}',
    
        
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': fig, 'layout': layout}, 
                    output_type='div'))



def epi_regression(df):
    

    # Generate the plot
    fig = px.scatter_3d(df, x='FACTOR_VERBAL__VV', y='FACTOR_NUMÉRICO_NN', z='FACTOR_VISOESPACIAL_EE',height=1000)
    fig.update_traces(marker=dict(size=5))
    
    layout = {
        'title': 'Diagrama 3D de pruebas',
    
        
    }
    # Getting HTML needed to render the plot.
    return( plot({'data': fig, 'layout': layout}, 
                    output_type='div'))


class Reportes(LoginRequiredMixin,View):
    def get(self,request):
        data = {}
        data["title"] = "Predicción"
        data["pageview"] = "Aluminio"

        data["result"] = None

        if "GET" == request.method:
            return render(request, "menu/reportes.html", data)
    
    def post(self,request):
        c_orden = request.POST.get('reportes')
        data = {}
        data["title"] = "Reportes"
        data["pageview"] = "Interpretación"
        c_orden = int(c_orden)
        if not isinstance(c_orden, int):
            messages.error(
                        request,
                        "Ingrese un número válido de orden",
                    )
            return HttpResponseRedirect(reverse("reportes"))
        else:
            output,finca = get_muestras(c_orden)
            str_corden = str(c_orden)
            return FileResponse(output, as_attachment=True, filename=f'{finca}_{str_corden}.pdf')



# Trasplante renal
class TrasplanteView(LoginRequiredMixin,View):
    def get(self,request):
        data = {}
        data["title"] = "Predicción"
        data["pageview"] = "Aluminio"

        data["result"] = None

        if "GET" == request.method:
            return render(request, "menu/index_renal.html", data)

        # if not GET, then proceed
    def post(self,request):
            model = pickle.load(open("./static/predict/model_al.pkl", "rb"))
            sc = pickle.load(open("./static/predict/sc_al.pkl", "rb"))
            
            data = {}
            data["title"] = "Predicción"
            data["pageview"] = "Aluminio"
           
            try:
                xlsx_file = request.FILES["xlsx_file"]
                if not xlsx_file.name.endswith(".xlsx"):
                    messages.error(request, "El archivo seleccionado no es de tipo xlsx.")
                    return HttpResponseRedirect(reverse("trasplante"))
                # if file is too large, return
                if xlsx_file.multiple_chunks():
                    messages.error(
                        request,
                        "El archivo es muy grande(%.2f MB)." % (xlsx_file.size / (1000 * 1000),),
                    )
                    return HttpResponseRedirect(reverse("trasplante"))

                db = pd.read_excel(xlsx_file,sheet_name="Al")  
                test_df = db[['pH', 'M.O.', 'Al', 'K', 'Ca', 'Mg']]
                x = test_df[['pH', 'M.O.',  'K', 'Ca', 'Mg']]

                x = sc.transform(x)
                pred = model.predict(x)
                db["Aluminio Predicho"] = pred
                replace = '<table border="1" class="dataframe">'
                data["result"] = db.reset_index(drop=True).round(decimals=2).to_html(classes=None, border=None, justify=None).replace(replace,"").replace("</table>","")
                """ 
                data["error_media"] = error_media(db) """
                return render(request, "menu/index_renal.html", data)

            except Exception as e:
                logging.getLogger("error_logger").error(
                    "No se pudo abrir el archivo: " + repr(e)
                )
                messages.error(request, "No se pudo abrir el archivo: " + repr(e))

            return HttpResponseRedirect(reverse("trasplante"))





def get_edad(df):
    graphs = []

    # Adding bar plot of y3 vs x.
    
    graph = px.box(df, y="EDAD", points="all")
    graph.update

    # Setting layout of the figure.
    layout = {
        'title': 'Edad de pacientes en meses',
        'xaxis_title': 'Edad',
        'yaxis_title': 'Cantidad',
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': graph, 'layout': layout}, 
                    output_type='div'))
    

def get_etiologia(df):
    graphs = []

    # Adding bar plot of y3 vs x.
    
    graphs.append(
            go.Bar(
        x=["CAKUT","NO CAKUT"],
    y=df['ETIOLOGÍA'].value_counts(sort=False),
        text=["CAKUT","NO CAKUT"],
        textposition='auto',
    )
        
        )

       

    # Setting layout of the figure.
    layout = {
        'title': 'Distribución de Etiología',
        'xaxis_title': 'Etiología',
        'yaxis_title': 'Cantidad',
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': graphs, 'layout': layout}, 
                    output_type='div'))




def get_funcion(df):
    

    # Adding bar plot of y3 vs x.
     


    graph=px.bar(df, x=["No Alterada","Alterada"], y=df["FUNCIÓN_RENAL_ALTERADA_A_5_AÑOS_"].value_counts(sort=False), title="Función renal alterada a 5 años")


       

    # Setting layout of the figure.
    layout = {
        'title': 'Distribución de Función renal a 5 años',
        'xaxis_title': 'Función renal alterada',
        'yaxis_title': 'Cantidad',
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': graph, 'layout': layout}, 
                    output_type='div'))


def get_cakut(df):
    

    graphs = px.histogram(df, x='CLASIFICACIÓN_DE_CAKUT', color="SEXO", barmode='group')
    graphs.update_traces( marker=dict( line=dict(color='#000000', width=3)))
    graphs.update_layout(  font=dict(
                size=18,
                
            ))

    # Setting layout of the figure.
    layout = {
        'title': 'Distribución de clasificación CAKUT',
        'xaxis_title': 'Clasificación',
        'yaxis_title': 'Cantidad',
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': graphs, 'layout': layout}, 
                    output_type='div'))



def get_nocakut(df):
    

    graphs = px.histogram(df, x='CLASIFICACIÓN_NO_CAKUT', color="SEXO", barmode='group')
    graphs.update_traces( marker=dict( line=dict(color='#000000', width=3)))
    graphs.update_layout(  font=dict(
                size=18,
                
            ))

    # Setting layout of the figure.
    layout = {
        'title': 'Distribución de clasificación no CAKUT',
        'xaxis_title': 'Clasificación',
        'yaxis_title': 'Cantidad',
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': graphs, 'layout': layout}, 
                    output_type='div'))


def get_linear(df):
    

    graphs =  px.scatter(df, x="EDAD", y="CREATININA_SÉRICA_AL_1ER__AÑO", trendline="ols",)
    graphs.update_traces( marker=dict( line=dict(color='#000000', width=3)))
    graphs.update_layout(  font=dict(
                size=18,
                
            ))

    # Setting layout of the figure.
    layout = {
        'title': 'Distribución de clasificación no CAKUT',
        'xaxis_title': 'EDAD',
        'yaxis_title': 'Creatinina Sérica al primer año',
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': graphs, 'layout': layout}, 
                    output_type='div'))



def get_dialisis(df):
    

    graphs = px.histogram(df, x='TIPO_DE_DIALISIS',y="TIEMPO_DE_DIÁLISIS", color="SUPERVIVENCIA_DE_PACIEE_A_5_AÑOS", barmode='group')
    graphs.update_traces( marker=dict( line=dict(color='#000000', width=3)))
    graphs.update_layout(  font=dict(
                size=18,
                
            ))

    # Setting layout of the figure.
    layout = {
        'title': 'Relación entre tipo de diálisis, tiempo de diálisis y supervivencia del paciente',
        'xaxis_title': 'Tipo de diális',
        'yaxis_title': 'Tiempo de diálisis',
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': graphs, 'layout': layout}, 
                    output_type='div'))



def get_muerte_sexo(df):
    

    graphs = px.histogram(df, x='SUPERVIVENCIA_DE_PACIEE_A_5_AÑOS', color="SEXO", barmode='group')
    graphs.update_traces( marker=dict( line=dict(color='#000000', width=3)))
    graphs.update_layout(  font=dict(
                size=18,
                
            ))

    # Setting layout of the figure.
    layout = {
        'title': 'Relación supervivencia del paciente y sexo',
        'xaxis_title': 'Sexo',
        'yaxis_title': 'Supervivencia',
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': graphs, 'layout': layout}, 
                    output_type='div'))


def get_etilogia_funcion(df):
    

    graphs = px.histogram(df, x='ETIOLOGÍA', color="FUNCIÓN_RENAL_ALTERADA_A_5_AÑOS_", barmode='group')
    graphs.update_traces( marker=dict( line=dict(color='#000000', width=3)))
    graphs.update_layout(  font=dict(
                size=18,
                
            ))

    # Setting layout of the figure.
    layout = {
        'title': 'Relación etiología y función renal alterada a 5 años',
        'xaxis_title': 'Etiología',
        'yaxis_title': 'Conteo',
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': graphs, 'layout': layout}, 
                    output_type='div'))


def get_corr(df):
    
    corr = df.corr()
    

    graphs = px.imshow(corr,x=df.columns,
    y=df.columns, color_continuous_scale=px.colors.sequential.Inferno,height=1000)
    


    

    # Setting layout of the figure.
    layout = {
        'title': 'Matriz de correlación',
        
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': graphs, 'layout': layout}, 
                    output_type='div'))



def get_iocorr(df,input,output):
    
    cor = nominal.compute_associations(df,num_num_assoc="spearman")
    
    graphs = px.imshow(cor,x=df.columns,y=df.columns, color_continuous_scale=px.colors.sequential.Inferno,height=1000)
    


    

    # Setting layout of the figure.
    layout = {
        'title': 'Correlaciones',
    
        
        
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': graphs, 'layout': layout}, 
                    output_type='div'))


def pca(input,output):
    sc=StandardScaler()
    pca = PCA(n_components=3)
    components = pca.fit_transform(sc.fit_transform(input))

    total_var = pca.explained_variance_ratio_.sum() * 100

    fig = px.scatter_3d(
        components, x=0, y=1, z=2, color=output,
        title=f'Varianza Total Explicada: {total_var:.2f}%',
        labels={'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'},
        height=1000
    )
    layout = {
        'title': 'Primeras 3 componentes y caracterización por Malfunción renal',
    
        
    }
    # Getting HTML needed to render the plot.
    return( plot({'data': fig, 'layout': layout}, 
                    output_type='div'))

# Dashboard
class DashboardView(LoginRequiredMixin,View):
    def get(self, request):
        print(request.session)
        greeting = {}
        greeting['title'] = "Dashboard"
        greeting['pageview'] = "Nazox"        
        return render(request, 'menu/index.html',greeting)


from django import forms
def UploadView(request):
        data = {}
        con = sqlite3.connect(settings.DATABASES['default']['NAME'])

        df = pd.read_sql_query("SELECT * from renal", con,index_col="INDEX")
        if "GET" == request.method:
            return render(request, "menu/upload.html", data)
        # if not GET, then proceed
        try:
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'El archivo seleccionado no es de tipo CSV')
                return HttpResponseRedirect(reverse("update"))
            #if file is too large, return
            if csv_file.multiple_chunks():
                messages.error(request,"El archivo es muy grande(%.2f MB)." % (csv_file.size/(1000*1000),))
                return HttpResponseRedirect(reverse("update"))

            db = pd.read_csv(csv_file,index_col="INDEX")
            if (db.columns.values != df.columns.values).all():
                logging.getLogger("error_logger").error(forms.errors.as_json())
                messages.error(request,'El archivo no tiene el formato correcto')
            else:
                db.dropna().to_sql('renal_input', con, if_exists ='replace')
                cur = con.cursor()
                cur.execute("INSERT or IGNORE INTO renal SELECT * FROM renal_input")
                con.commit()
                messages.info(request,'El archivo se ha subido correctamente')
                

            

        except Exception as e:
            logging.getLogger("error_logger").error("No se pudo abrir el archivo: "+repr(e))
            messages.error(request,"No se pudo abrir el archivo: "+repr(e))

        return HttpResponseRedirect(reverse("update"))



def UploadViewE(request):
        data = {}
        con = sqlite3.connect(settings.DATABASES['default']['NAME'])

        df = pd.read_sql_query("SELECT * from epilepsia", con,index_col="INDEX")
        if "GET" == request.method:
            return render(request, "menu/uploade.html", data)
        # if not GET, then proceed
        try:
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'El archivo seleccionado no es de tipo CSV')
                return HttpResponseRedirect(reverse("update"))
            #if file is too large, return
            if csv_file.multiple_chunks():
                messages.error(request,"El archivo es muy grande(%.2f MB)." % (csv_file.size/(1000*1000),))
                return HttpResponseRedirect(reverse("update"))

            db = pd.read_csv(csv_file,index_col="INDEX")
            if (db.columns.values != df.columns.values).all():
                logging.getLogger("error_logger").error(forms.errors.as_json())
                messages.error(request,'El archivo no tiene el formato correcto')
            else:
                db.dropna().to_sql('epilepsia_input', con, if_exists ='replace')
                cur = con.cursor()
                cur.execute("INSERT or IGNORE INTO epilepsia SELECT * FROM renal_input")
                con.commit()
                messages.info(request,'El archivo se ha subido correctamente')
                

            

        except Exception as e:
            logging.getLogger("error_logger").error("No se pudo abrir el archivo: "+repr(e))
            messages.error(request,"No se pudo abrir el archivo: "+repr(e))

        return HttpResponseRedirect(reverse("update"))




# Calender
class EdaView(LoginRequiredMixin,View):
     def get(self,request):
        data = {}
        data["title"] = "Predicción"
        data["pageview"] = "Aluminio"

        data["result"] = None

        if "GET" == request.method:
            return render(request, "menu/eda.html", data)
        # if not GET, then proceed
     def post(self,request):
            model = pickle.load(open("./static/predict/model_cic.pkl", "rb"))
            sc = pickle.load(open("./static/predict/sc_cic.pkl", "rb"))
            
            data = {}
            data["title"] = "Predicción"
            data["pageview"] = "CIC"
           
            try:
                xlsx_file = request.FILES["xlsx_file"]
                if not xlsx_file.name.endswith(".xlsx"):
                    messages.error(request, "El archivo seleccionado no es de tipo xlsx.")
                    return HttpResponseRedirect(reverse("eda"))
                # if file is too large, return
                if xlsx_file.multiple_chunks():
                    messages.error(
                        request,
                        "El archivo es muy grande(%.2f MB)." % (xlsx_file.size / (1000 * 1000),),
                    )
                    return HttpResponseRedirect(reverse("eda"))

                db = pd.read_excel(xlsx_file,sheet_name="CIC")  
                test_df = db[['pH', 'M.O.', 'CIC', 'K', 'Ca', 'Mg']]
                x = test_df[['pH', 'M.O.',  'K', 'Ca', 'Mg']]

                x = sc.transform(x)
                pred = model.predict(x)
                db["CIC Predicho"] = pred
                replace = '<table border="1" class="dataframe">'
                data["result"] = db.reset_index(drop=True).round(decimals=2).to_html(classes=None, border=None, justify=None).replace(replace,"").replace("</table>","")
                """ 
                data["error_media"] = error_media(db) """
                return render(request, "menu/eda.html", data)

            except Exception as e:
                logging.getLogger("error_logger").error(
                    "No se pudo abrir el archivo: " + repr(e)
                )
                messages.error(request, "No se pudo abrir el archivo: " + repr(e))

            return HttpResponseRedirect(reverse("eda"))


class Manual(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['title'] = "Manual de usuario"
        greeting['pageview'] = "Epidemiólogos"        
        return render(request, 'menu/pages-faqs.html',greeting)

class EdaViewEpi(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['title'] = "Análisis Exploratiorio"
        greeting['pageview'] = "Transplante Epilepsia"        
        return render(request, 'menu/eda_epi.html',greeting)


# Calender
class CalendarView(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['title'] = "Calendar"
        greeting['pageview'] = "Nazox"        
        return render(request, 'menu/calendar.html',greeting)

# Chat
class ChatView(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['title'] = "Chat"
        greeting['pageview'] = "Nazox"        
        return render(request, 'menu/apps-chat.html',greeting)

# Kanban Board
class KanbanBoardView(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['title'] = "Kanban Board"
        greeting['pageview'] = "Nazox"        
        return render(request, 'menu/apps-kanban-board.html',greeting)