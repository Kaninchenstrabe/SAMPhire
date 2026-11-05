from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries
import pyqtgraph as pg
class Hvis:
    def visualize_fun(self):
        #print("vis")
        #print(self.tab)
        #print(len(self.tab))
        #print(len(list(set(self.tab))))
        x=[]
        x.append([i for i in range(len(self.tab["Unsorted"]))])
        self.plot.clear()
        self.plot.addItem(pg.BarGraphItem(x = x, height=self.tab["Unsorted"], width=1, brush='#000000'))

