import datetime
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Time_Series_Plot:
    
    COLORS = ['red','blue','green','pink','cyan','black','yellow']
    
    def __init__(self,
                df_in,
                time_col,
                value_cols,
                conditions = None,
                error_col = None,
                date_format="%Y-%m-%d"):
        """
        df_in: a Pandas dataframe object
        time_col: the column of datetime information
        value_cols: array of value columns for the y-axis
        conditions: rows to generate additional slice by
        error_col: error columns in the form of [errorlow, errorhigh]
        date_formatter: how to format the datetime column
        """
        self.df = df_in.copy()
        self.time_col = time_col
        self.value_cols = value_cols
        self.date_format=date_format
        self.__set_conditions(conditions)
        self.__set_errors(error_col)
        self.__set_datetime()

        self.fig, self.ax = plt.subplots(len(value_cols), sharex=True)
        if len(value_cols)==1:
            self.ax = [self.ax]
        self.format_plot()
    
    def __set_datetime(self):
        self.df['datetime'] = self.df.apply(
            lambda x: datetime.datetime.strptime(x[self.time_col], self.date_format), axis=1)
        
    def __set_errors(self, error_col):
        if not error_col:
        # dummy error calc
            self.error_low_col = 'error_low'
            self.error_high_col = 'error_high'
            self.df[self.error_low_col] = self.df.apply(lambda x: 0, axis=1)
            self.df[self.error_high_col] = self.df.apply(lambda x: 0, axis=1)
        else:
            self.error_low_col = error_col[0]
            self.error_high_col = error_col[1]

    def __set_conditions(self, conditions):
        if conditions is None:
            self.conditions = [pd.Series([True]*len(df1))]
            self.all_cond_labels = None
        else:
            self.all_cond_labels = [x for x in self.df.groupby(conditions).all().index]
            self.conditions = [self.df[conditions]==cond for cond in self.all_cond_labels]
            
    def format_plot(self, 
                    height=6, 
                    width=14, 
                    alpha=0.1, 
                    bgcolor=[0.0,0.2,0.5], 
                    marker_size=10):
        self.fig.set_figheight(height)
        self.fig.set_figwidth(width)
        self.fig.set_dpi(60)
        self.fig.set_facecolor('w')
        self.fig.set_edgecolor('k')
        self.marker_size = 10
        for axis in self.ax:
            axis.grid(alpha=0.5)
            axis.patch.set_alpha(alpha)
            axis.set_axis_bgcolor(bgcolor)
            for tick in axis.xaxis.get_major_ticks():
                tick.label.set_fontsize(10)
            for tick in axis.yaxis.get_major_ticks():
                tick.label.set_fontsize(12) 

    
    def simple_plot(self):
        """
        Simple plot. No error bars
        """
        for i, val in enumerate(self.value_cols):
            for j, cond in enumerate(self.conditions):
                if not self.all_cond_labels:
                    label=str(val)
                else:
                    label=str(val) + " - " + self.all_cond_labels[j]
                plotx = self.ax[i].plot(self.df[cond]['datetime'].values,
                                self.df[cond][val],
                                '-o',
                                color=time_series_plot.COLORS[(i*len(self.value_cols)+j)%len(time_series_plot.COLORS)],
                                label=label,
                                markersize = self.marker_size)
                self.ax[i].legend(prop={'size':14}, fancybox=True, framealpha=0.7)
        
    def errorbar_plot(self):
        """
        Error bar plot.
        """
        for i, val in enumerate(self.value_cols):
            for j, cond in enumerate(self.conditions):
                if not self.all_cond_labels:
                    label=str(val)
                else:
                    label=str(val) + " - " + self.all_cond_labels[j]
                plotx = self.ax[i].errorbar(self.df[cond]['datetime'].values,
                                self.df[cond][val],
                                yerr=[self.df[cond][self.error_low_col],self.df[cond][self.error_high_col]],
                                fmt='-o',
                                color=time_series_plot.COLORS[(i*len(self.value_cols)+j)%len(time_series_plot.COLORS)],
                                label=label,
                                markersize = self.marker_size)
                self.ax[i].legend(prop={'size':14}, fancybox=True, framealpha=0.7)      
    
    def error_band_plot(self):
        """
        Simple plot with error bands.
        """
        self.simple_plot()
        for i, val in enumerate(self.value_cols):
            for j, cond in enumerate(self.conditions):
                self.ax[i].fill_between(self.df[cond]['datetime'].values, 
                                self.df[cond][val] - self.df[cond][self.error_low_col],
                                self.df[cond][val] + self.df[cond][self.error_high_col],
                                color=time_series_plot.COLORS[(i*len(self.value_cols)+j)%len(time_series_plot.COLORS)],
                                alpha=0.1)