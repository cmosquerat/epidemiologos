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

# Trasplante renal
class TrasplanteView(LoginRequiredMixin,View):
    def get(self, request):

        print(request.session)
        
        con = sqlite3.connect(settings.DATABASES['default']['NAME'])

        df = pd.read_sql_query("SELECT * from renal", con)

        observaciones = len(df.index) + 1


        x = [i for i in range(-10, 11)]
        y1 = [3*i for i in x]
        y2 = [i**2 for i in x]
        y3 = [10*abs(i) for i in x]

        # List of graph objects for figure.
        # Each object will contain on series of data.
        graphs = []

        # Adding bar plot of y3 vs x.
        graphs.append(
            go.Bar(
            x=df['Sexo'].value_counts().keys().values,
        y=df['Sexo'].value_counts(),
            text=[1,2],
            textposition='auto',
        )
        )

        # Setting layout of the figure.
        layout = {
            'title': 'Sexo de pacientes',
            'xaxis_title': 'X',
            'yaxis_title': 'Y',
            'height': 420,
            'width': 560,
        }

        # Getting HTML needed to render the plot.
        plot_div = plot({'data': graphs, 'layout': layout}, 
                        output_type='div')
        greeting = {}
        greeting['title'] = "Trasplante renal"
        greeting['pageview'] = "Nazox"
        greeting["plot_div"] = plot_div
        greeting["observaciones"] = str(observaciones)
        print(observaciones)
        return render(request, 'menu/index_renal.html',context=greeting)




# Dashboard
class DashboardView(LoginRequiredMixin,View):
    def get(self, request):
        print(request.session)
        greeting = {}
        greeting['title'] = "Dashboard"
        greeting['pageview'] = "Nazox"        
        return render(request, 'menu/index.html',greeting)

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