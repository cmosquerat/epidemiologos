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





# Epilepsia
class EpilepsiaView(LoginRequiredMixin,View):
    def get(self, request):

        print(request.session)
        
        con = sqlite3.connect(settings.DATABASES['default']['NAME'])

        df = pd.read_sql_query("SELECT * from epilepsia", con)

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


        orden = ['CLINICA', 'EDAD', 'SEXO', 'TIPO_DE_EPILEPSIA', 'TIPO',
       'FARMACOS__1', 'FARMACO_2', 'RAZONAMIENTO_LÓGICO_RR',
       'RAZONAMIENTO_LÓGICO_RR.1', 'ALTERACIÓN_RR', 'FACTOR_VERBAL__VV',
       'FACTOR_VERBAL__VV.1', 'ALTERACIÓN_VV', 'FACTOR_NUMÉRICO_NN',
       'FACTOR_NUMÉRICO_NN.1', 'ALTERACIÓN_NN', 'FACTOR_VISOESPACIAL_EE',
       'FACTOR_VISOESPACIAL_EE.1', 'ALTERACION_EE',
       'TRASTORNO_DEL_APRENDIZAJE_(VV-NN-EE)']
        df = df[orden]

       


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
        replace = '<table border="1" class="dataframe">'
        greeting["tabla"] =  df.to_html(classes=None, border=None, justify=None).replace(replace,"").replace("</table>","")
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
    y=cor.columns, color_continuous_scale=px.colors.sequential.Inferno)
    
    
    

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




# Trasplante renal
class TrasplanteView(LoginRequiredMixin,View):
    def get(self, request):

        print(request.session)
        
        con = sqlite3.connect(settings.DATABASES['default']['NAME'])

        df = pd.read_sql_query("SELECT * from renal", con)

        observaciones = len(df.index) 

        # List of graph objects for figure.
        # Each object will contain on series of data.
        graphs = []

        # Adding bar plot of y3 vs x.
        graphs.append(
              go.Bar(
            x=["Hombres","Mujeres"],
        y=df['SEXO'].value_counts(),
            text=[1,2],
            textposition='auto',
        )
            
        )

        # Setting layout of the figure.
        layout = {
            'title': 'Sexo de pacientes',
            'xaxis_title': 'Sexo',
            'yaxis_title': 'Cantidad',
        }

        inputs = df.reset_index().iloc[: , 2:14].drop("AÑO_",axis=1)
        outputs = df.reset_index().iloc[: , 14:]


        # Getting HTML needed to render the plot.
        plot_div = plot({'data': graphs, 'layout': layout}, 
                        output_type='div')
        greeting = {}
        greeting['title'] = "Trasplante renal"
        greeting['pageview'] = "Dashboard"
        greeting["plot_div"] = plot_div
        greeting["observaciones"] = str(observaciones)
        greeting["funcion"] = len(df[df["FUNCIÓN_RENAL_ALTERADA_A_5_AÑOS_"]==2].index)
        greeting["fallecidos"] = len(df[df["SUPERVIVENCIA_DE_PACIEE_A_5_AÑOS"]==2].index)
        greeting["no_fallecidos"] = len(df[df["SUPERVIVENCIA_DE_PACIEE_A_5_AÑOS"]==1].index)
        greeting["Cakut"] = len(df[df["ETIOLOGÍA"]==1].index)
        greeting["No_Cakut"] = len(df[df["ETIOLOGÍA"]==2].index)
        greeting["plot_etiologia"] = get_etiologia(df)
        greeting["plot_edad"] = get_edad(df)
        greeting["plot_funcion"] = get_funcion(df)
        greeting["plot_cakut"] = get_cakut(df)
        greeting["plot_nocakut"] = get_nocakut(df)
        greeting["dialisis"] = get_dialisis(df)
        greeting["linear"] = get_linear(df)
        greeting["muerte"] = get_muerte_sexo(df)
        greeting["corr1"] = get_corr(inputs)
        greeting["corr2"] = get_corr(outputs)
        greeting["etiologia_funcion"] = get_etilogia_funcion(df)
        greeting["io"] = get_iocorr(df,inputs,outputs)
        replace = '<table border="1" class="dataframe">'
        greeting["tabla"] =  df.to_html(classes=None, border=None, justify=None).replace(replace,"").replace("</table>","")
        print(observaciones)
        return render(request, 'menu/index_renal.html',context=greeting)





def get_edad(df):
    graphs = []

    # Adding bar plot of y3 vs x.
    
    graph = ff.create_distplot([df["EDAD"].values], ["EDAD DE PACIENTES EN MESES"],  show_rug=False)
    

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
    y=df['ETIOLOGÍA'].value_counts(),
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
     


    graph=px.bar(df, x=["No Alterada","Alterada"], y=df["FUNCIÓN_RENAL_ALTERADA_A_5_AÑOS_"].value_counts(), title="Función renal alterada a 5 años")


       

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

    graphs = go.Heatmap(
    z=corr,
    x=corr.columns,
    y=corr.columns,
    colorscale=px.colors.diverging.RdBu,
    zmin=-1,
    zmax=1
)


    

    # Setting layout of the figure.
    layout = {
        'title': 'Relación etiología y función renal alterada a 5 años',
        'xaxis_title': 'Etiología',
        'yaxis_title': 'Conteo',
        
        
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': graphs, 'layout': layout}, 
                    output_type='div'))



def get_iocorr(df,input,output):
    
    corr = nominal.compute_associations(df,num_num_assoc="spearman")

    graphs = go.Heatmap(
    z=corr,
    x=input.columns,
    y=output.columns,
    colorscale=px.colors.diverging.RdBu,

)


    

    # Setting layout of the figure.
    layout = {
        'title': 'Relación etiología y función renal alterada a 5 años',
        'xaxis_title': 'Etiología',
        'yaxis_title': 'Conteo',
        
        
    }

    # Getting HTML needed to render the plot.
    return( plot({'data': graphs, 'layout': layout}, 
                    output_type='div'))




# Dashboard
class DashboardView(LoginRequiredMixin,View):
    def get(self, request):
        print(request.session)
        greeting = {}
        greeting['title'] = "Dashboard"
        greeting['pageview'] = "Nazox"        
        return render(request, 'menu/index.html',greeting)



class UploadView(LoginRequiredMixin,View):
    def get(self, request):
        print(request.session)
        greeting = {}
        greeting['title'] = "Actualizar"
        greeting['pageview'] = "Transplante Renal"        
        return render(request, 'menu/upload.html',greeting)


# Calender
class EdaView(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['title'] = "Análisis Exploratiorio"
        greeting['pageview'] = "Transplante Renal"        
        return render(request, 'menu/eda.html',greeting)


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