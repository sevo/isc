from numpy.random import normal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
import pylab

class Dendrogram:
    def __char_range(self, c, size):
        """Generates the characters from `c1` to `c2`, inclusive."""
        return [chr(ord(c)+index) for index in range(0, size)]

    def random_data(self, l=100, k=6):
        """" l = length of the time series, k = number of samples"""
        labels = self.__char_range('A', k)
        index = range(0,l)
        frame = pd.DataFrame(index=index, columns=labels)
        for label in labels:
            frame[label] = np.cumsum(normal(size=l))
        return frame

    def augmented_dendrogram(self, *args, **kwargs):
        orientation = kwargs.get('orientation')
        ddata = sch.dendrogram(*args, **kwargs)

        rotation = 'vertical' if(orientation in ['left', 'right']) else 'horizontal'
        va = 'center' if(orientation in ['left', 'right']) else 'top'
        if orientation == 'bottom':
            va = 'bottom'

        xytext = np.array([15, 0]) if(orientation in ['left', 'right']) else np.array([0, 8])
        if(orientation in ['top', 'left']):
            xytext = xytext * -1

        if not kwargs.get('no_plot', False):
            for i, d in zip(ddata['icoord'], ddata['dcoord']):
                x = 0.5 * sum(i[1:3])
                value = y = d[1]
                if(orientation in ['left', 'right']):
                    x, y = y, x
                plt.plot(x, y, 'ro')
                plt.annotate("%.3g" % value, (x, y), xytext=xytext,
                             textcoords='offset points',
                             va=va, ha='center', rotation=rotation)

        return ddata

    def annotated_dendrogram(self, data, orientation='right'):
        """Plots dendrogram with time series used as labels. data is the DataFrame with sequence in every column and orentation indicates the side where the label will be displayed"""
        labels = data.columns
        fig = pylab.figure(figsize=(8,8))
        ax1 = fig.add_axes([0.09,0.1,0.2,0.6]) if orientation == 'right' else fig.add_axes([0.71,0.1,0.2,0.6])
        D = self.augmented_dendrogram(sch.linkage(data.T.values), orientation=orientation, labels=labels)
        plt.axis('off')
        ax1.set_xticks([])
        ax1.set_yticks([])

        indexes = D['leaves']

        series_plot_height = 0.6 / len(labels)
        for i in range(0, len(labels)):

            ax = fig.add_axes([0.33,0.1 + (i*series_plot_height),0.57,series_plot_height]) if orientation == 'right' else fig.add_axes([0.10,0.1 + (i*series_plot_height),0.57,series_plot_height])
            pylab.plot(data[labels[indexes[i]]])
            p = pylab.gca()
            p.axes.get_xaxis().set_ticks([])
            p.axes.get_yaxis().set_ticks([])
            ax1.set_xticks([])
            ax1.set_yticks([])

            p.set_ylabel(labels[indexes[i]])
            if orientation == 'left':
                p.yaxis.set_label_position("right")

        fig.show()

    def plot_example(self, orientation='right'):
        data = self.random_data(100, 6)
        self.annotated_dendrogram(data, orientation)