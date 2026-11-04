from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries
import pyqtgraph as pg
class Hvis:
    def visualize_fun(self):
        print("vis")
        print(self.tab)
        print(len(self.tab))
        print(len(list(set(self.tab))))
        x=[]
        x.append([i for i in range(len(self.tab))])
        self.plot = pg.plot()
        self.plot.addItem(pg.BarGraphItem(x = x, height=self.tab, width=1, brush='#000000'))
        self.plot.setBackground(background='#ffffff')
        self.MainLayout.addWidget(self.plot)