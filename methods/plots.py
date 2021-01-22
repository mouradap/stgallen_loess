import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime
import plotly.graph_objs as go
from skmisc.loess import loess
import plotly.express as px
from itertools import cycle


class Plots():
    def __init__(self, df):
        self.symp_dict = {
    '2': 'sore_throat',
    '3': 'cough',
    '4': 'shortness_breath',
    '12': 'fever',
    '14': 'limb_muscle_pain',
    '15': 'loss_of_taste_smell'
}
        self.symptom_list = [symp for symp in self.symp_dict.values()]
        self.symptom_list.append('foph')

        self.symptom_full_name = {'sore_throat': 'Sore Throat',
                                'cough': 'Cough',
                                'shortness_breath': 'Shortness of Breath',
                                'fever': 'Fever',
                                'limb_muscle_pain': 'Limb Muscle Pain',
                                'loss_of_taste_smell': 'Loss of Taste and Smell',
                                'foph': 'FOPH'}
        self.df = df

        self.palette = cycle(px.colors.qualitative.Plotly)
        self.palette = cycle(px.colors.sequential.haline)


    def __format_date(self, date):
        return date.strftime('%b %d %Y')

    # def __customLegend(self, fig, nameSwap):
    #     for i, dat in enumerate(fig.data):
    #         for elem in dat:
    #             if elem == 'name':
    #                 fig.data[i].name = nameSwap[fig.data[i].name]
    #     return(fig)

    def save_figure(self, output_path):
        self.fig.write_html(output_path)

    def plot_figure(self):
        self.fig.show()

    # def prepare_figure(self, df):
    #     fig = px.line(df, x = range(len(df['sore_throat'])),
    #           y=self.symptom_list,
    #           labels = { 'x': 'Week',
    #                     'value': '% symptoms',
    #                     'variable': ''
    #           },
    #           title = 'Time series of symptoms (percentage)')

    #     fig = self.__customLegend(fig=fig, nameSwap = self.symptom_full_name)

    #     x_axis_labels = df['date'].apply(self.__format_date)

    #     fig.update_layout(
    #         xaxis = dict(
    #             tickmode = 'array',
    #             tickvals = list(range(len(df['date']))),
    #             ticktext = x_axis_labels
    #         )
    #     )

    #     self.fig = fig

    def __get_lowess(self, symp):
        x = list(range(len(self.df['date'])))
        y = self.df[symp]
        l = loess(x, y)
        l.fit()
        pred = l.predict(x, stderror=True)
        conf = pred.confidence()

        lowess = pred.values
        ll = conf.lower
        ul = conf.upper
        return lowess, ll, ul

    def __prepare_objects(self, symp):
        obj_palette = next(self.palette)
        obj_rgba = 'rgba' + obj_palette[3:-1] + ',0.3)'
        symp_objs = [
            go.Scatter(
                name='{} Scatter'.format(self.symptom_full_name[symp]),
                x=self.x,
                y=self.df[symp],
                mode='markers',
                showlegend=False,
                line=dict(color=obj_palette),
            ),

            go.Scatter(
                name='{}'.format(self.symptom_full_name[symp]),
                x=self.x,
                y=self.__get_lowess(symp)[0],
                mode='lines',
                marker=dict(color=obj_palette),
                line=dict(width=2),
                showlegend=True
            ),

            go.Scatter(
                name='{} Upper Bound'.format(self.symptom_full_name[symp]),
                x=self.x,
                y=self.__get_lowess(symp)[2],
                mode='lines',
                marker=dict(color=obj_palette),
                line=dict(width=0),
                fillcolor=obj_rgba,
                showlegend=False
            ),

            go.Scatter(
                name='{} Lower Bound'.format(self.symptom_full_name[symp]),
                x=self.x,
                y=self.__get_lowess(symp)[1],
                marker=dict(color=obj_palette),
                line=dict(width=0),
                mode='lines',
                fillcolor=obj_rgba,
                fill='tonexty',
                showlegend=False
            )
        ]

        return symp_objs

    def prepare_figure(self):
        self.x = list(range(len(self.df['date'])))

        all_objects = []
        for symptom in self.symptom_list:
            all_objects.append(self.__prepare_objects(symptom))

        all_objects = sum(all_objects, [])

        self.fig = go.Figure(all_objects)

        # self.fig = self.__customLegend(fig=self.fig, nameSwap = self.symptom_full_name)

        x_axis_labels = self.df['date'].apply(self.__format_date)

        self.fig.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = list(range(len(self.df['date']))),
                ticktext = x_axis_labels
            ),
            yaxis_title = '% symptoms',
            title = 'Time series of symptoms (percentage)'            
        )