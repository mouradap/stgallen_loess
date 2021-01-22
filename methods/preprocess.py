import numpy as np
import pandas as pd
from skmisc.loess import loess


class DataProcessor():
    def __init__(self):
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

    def __replace_symptom(self, cols):
        for n, i in enumerate(cols):
            if i in self.symp_dict.keys():
                cols[n] = self.symp_dict[i]
        return cols

    def __replace_symptom(self, cols):
        for n, i in enumerate(cols):
            if i in self.symp_dict.keys():
                cols[n] = self.symp_dict[i]
        return cols

    def __calc_foph(self, row):
        if row.fever == 1 or row.cough == 1 or row.shortness_breath == 1 or row.sore_throat == 1 or row.loss_of_taste_smell == 1:
            foph = 1
        else:
            foph = 0
        
        return foph

    def __get_lowess(self, symp):
        x = list(range(len(self.ratio_df['sore_throat'])))
        y = self.ratio_df[symp]
        l = loess(x, y)
        l.fit()
        pred = l.predict(x, stderror=True)
        conf = pred.confidence()

        lowess = pred.values
        ll = conf.lower
        ul = conf.upper
        return lowess, ll, ul
        

    def __get_pos_ratio(self, symp):
        ratio_series = []
        for date in self.grouped_df['date'].unique():
            date_df = self.grouped_df[self.grouped_df['date'] == date]
            positives = len(date_df[self.grouped_df[symp] == 1])
            negatives = len(date_df[self.grouped_df[symp] == 0])
            
            if negatives == 0:
                ratio = 1.0
            else:
                ratio = positives / negatives
            
            ratio_series.append(ratio)
            

        return ratio_series

    def process_data(self, data_file):
        self.df = pd.read_csv(data_file, sep = ';')
        self.df['date'] = pd.to_datetime(self.df['date']) - pd.to_timedelta(7, unit = 'd')

        self.grouped_df = self.df.groupby(['userId', pd.Grouper(key='date', freq='W-MON')])['2', '3', '4', '12', '14', '15'].sum().reset_index().sort_values('date')

        cols = self.grouped_df.columns.to_list()
        cols = self.__replace_symptom(cols)
        
        self.grouped_df.columns = cols

        self.grouped_df['foph'] = self.grouped_df.apply(self.__calc_foph, axis = 1)

        self.ratio_df = pd.DataFrame()
        for symptom in self.symptom_list:
            self.ratio_df[symptom] = self.__get_pos_ratio(symptom)
        
        self.ratio_df['date'] = self.grouped_df['date']
        
        self.ratio_df.drop(0, axis = 0, inplace=True)

        # self.lowess_df = pd.DataFrame()
        # for symptom in self.symptom_list:
        #     _, lowess = self.__get_lowess(self.ratio_df, symptom)
        #     self.lowess_df[symptom] = lowess
        
        # self.lowess_df['date'] = self.grouped_df['date']

        return self.ratio_df