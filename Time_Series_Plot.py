import datetime
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# example usage
# df['date'] = df.apply(lambda x: pd.Timestamp(x['d']), axis=1)
# df['error_low'] = df.apply(lambda x: get_beta_confidence_interval(x['total_queries_clicked'],x['total_queries'])[0],axis=1)
# df['error_high'] = df.apply(lambda x: get_beta_confidence_interval(x['total_queries_clicked'],x['total_queries'])[1],axis=1)
# ts = Time_Series_Plot(df, 'date', ['result_ctr'], conditions='cohort', error_col = ['error_low','error_high'])
# ts.error_band_plot()

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
        self.df = df_in.copy().reset_index()
        self.time_col = time_col
        self.value_cols = value_cols
        self.date_format=date_format
        self.__set_conditions(conditions)
        self.__set_errors(error_col)

        self.fig, self.ax = plt.subplots(len(value_cols), sharex=True)
        if len(value_cols)==1:
            self.ax = [self.ax]
        self.format_plot()
    
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
            self.conditions = [pd.Series([True]*len(self.df))]
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
        self.marker_size = marker_size
        for axis in self.ax:
            axis.grid(alpha=0.5)
            axis.patch.set_alpha(alpha)
            axis.set_axis_bgcolor(bgcolor)
            for tick in axis.xaxis.get_major_ticks():
                tick.label.set_fontsize(12)
            for tick in axis.yaxis.get_major_ticks():
                tick.label.set_fontsize(12)
    
    def set_plot_labels(self, n=0, title='', xaxis='', yaxis=''):
        self.ax[n].set_xlabel(xaxis, fontsize=14)
        self.ax[n].set_ylabel(yaxis, fontsize=14)
        self.ax[n].set_title(title, fontsize=14)
    
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
                plotx = self.ax[i].plot(self.df[cond][self.time_col].values,
                                self.df[cond][val],
                                '-o',
                                color=self.COLORS[(i*len(self.value_cols)+j)%len(self.COLORS)],
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
                plotx = self.ax[i].errorbar(self.df[cond][self.time_col].values,
                                self.df[cond][val],
                                yerr=[self.df[cond][self.error_low_col],self.df[cond][self.error_high_col]],
                                fmt='-o',
                                color=self.COLORS[(i*len(self.value_cols)+j)%len(self.COLORS)],
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
                self.ax[i].fill_between(self.df[cond][self.time_col].values, 
                                self.df[cond][val] - self.df[cond][self.error_low_col],
                                self.df[cond][val] + self.df[cond][self.error_high_col],
                                color=self.COLORS[(i*len(self.value_cols)+j)%len(self.COLORS)],
                                alpha=0.1)