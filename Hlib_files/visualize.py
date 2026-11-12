import pyqtgraph
class Hvis:
    def visualize_fun(self, prompt):
        x = []
        x.append([i for i in range(len(self.tab[prompt]))])
        self.graphs["Plot"][prompt].clear()
        self.graphs["Plot"][prompt].addItem(pyqtgraph.BarGraphItem(x=x, height=self.tab[prompt], width=1, brush='#000000'))
