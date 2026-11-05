import pyqtgraph as pg
class Hvis:
    def visualize_fun(self, prompt):
        #print("vis")
        #print(self.tab)
        #print(len(self.tab))
        #print(len(list(set(self.tab))))
        x=[]
        x.append([i for i in range(len(self.tab[prompt]))])
        self.graphs["Plot"][prompt].clear()
        self.graphs["Plot"][prompt].addItem(pg.BarGraphItem(x = x, height=self.tab[prompt], width=1, brush='#000000'))

