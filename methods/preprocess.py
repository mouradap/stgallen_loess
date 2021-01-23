import numpy as np
import pandas as pd
from skmisc.loess import loess
import warnings

warnings.filterwarnings('ignore')


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

    def __calc_foph(self, row):
        if row.fever == 1 or row.cough == 1 or row.shortness_breath == 1 or row.sore_throat == 1 or row.loss_of_taste_smell == 1:
            foph = 1
        else:
            foph = 0
        
        return foph

    def __get_pos_ratio(self, symp):
        ratio_series = []
        for date in self.grouped_df['date'].unique():
            date_df = self.grouped_df[self.grouped_df['date'] == date]
            try:
                negatives, positives  = date_df[symp].value_counts()
                ratio = positives / (positives + negatives)
            except ValueError:
                ratio = 1.0
                
            ratio_series.append(ratio)
        return ratio_series


    def process_data(self, data_file, **dates):
        self.df = pd.read_csv(data_file, sep = ';')
        self.df['date'] = pd.to_datetime(self.df['date'])
        if 'start_date' in dates:
            self.df = self.df[self.df['date'] >= dates['start_date']]
        if 'end_date' in dates:
            self.df = self.df[self.df['date'] <= dates['end_date']]
        self.df.fillna(0, inplace=True)
        symp_idx = ['2', '3', '4', '12', '14', '15']

        for symp in symp_idx:
            self.df[symp] = self.df[symp].astype(int)

        self.grouped_df = self.df.groupby(['userId', pd.Grouper(key='date', freq='W-MON')])[symp_idx].first().reset_index().sort_values('date')

        cols = self.grouped_df.columns.to_list()
        cols = self.__replace_symptom(cols)
        
        self.grouped_df.columns = cols

        self.grouped_df['foph'] = self.grouped_df.apply(self.__calc_foph, axis = 1)
        
        self.ratio_df = pd.DataFrame()
        self.ratio_df['date'] = self.grouped_df['date'].unique()
        for symp in self.symptom_list:
            self.ratio_df[symp] = self.__get_pos_ratio(symp)

        return self.ratio_df