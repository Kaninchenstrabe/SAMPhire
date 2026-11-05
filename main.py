### Dependecies
#import GUI
import sys
from PyQt5.QtWidgets import *
import json
from Hlib import *
import pyqtgraph as pg

class App(Hsort, Hfiles, Habout, Hgen, Hmeas, Hvis, Hcomp, QMainWindow,QWidget):
    def __init__(self):
        super().__init__()
        self.tab = {"Unsorted":[],"Sorted":[]}
        self.results = {"Custom":[], "Predef":[]}
    #Definiuje geometrię okna
        self.left = 100
        self.top = 100
        self.height = 500
        self.width = 900
        self.setGeometry(self.left, self.top, self.width, self.height)
    #Definiuje tytuł okna
        self.title = 'Algorytmy'
        self.setWindowTitle(self.title)
    #Definiuje zakładki w oknie
        menus={}
        submenus={}
        with open('config.json') as file_json:
            self.Menu_data=json.load(file_json)

        menuBar=self.menuBar()
        for menu in self.Menu_data:
            if self.Menu_data[menu]:
                menus.update({menu: menuBar.addMenu(menu)})
                for submenu in self.Menu_data[menu]:
                    print(f" Teraz konfiguruje       {menu}_{submenu}")
                    old_sub=submenu
                    submenu=submenu.replace(" ","")
                    submenus.update({submenu: QAction(old_sub, self)})
                    callback = getattr(self, f"{submenu.lower()}_{menu.lower()}")
                    submenus[submenu].triggered.connect(callback)
                    menus[menu].addAction(submenus[submenu])
            elif not self.Menu_data[menu]:
                print(f" Teraz konfiguruje       {menu}")
                #menus.update({menu: menuBar.addMenu(menu)})
                menus.update({menu: QAction(menu, self)})
                menuBar.addAction(menus[menu])
                callback = getattr(self, f"{menu.lower()}_fun")
                menus[menu].triggered.connect(callback)
                #menus[menu].addAction(submenus[menu])
        central = QWidget()
        self.setCentralWidget(central)
        self.MainLayout = QGridLayout(central)

        self.plot = pg.PlotWidget()
        self.plot.setBackground(background='#ffffff')
        self.plot.setMouseEnabled(x=False, y=False)
        self.plot.setFixedSize(300,250)

        Label1=QLabel("Unsorted")
        Label2=QLabel("Sorted")
        B1=QPushButton("Test")
        self.MainLayout.addWidget(Label1, 0, 0)
        self.MainLayout.addWidget(Label2, 0, 2)
        self.MainLayout.addWidget(B1, 1, 1)
        self.MainLayout.addWidget(self.plot, 1, 0)

        self.setLayout(self.MainLayout)
    #Wyświetlenie okna
        self.show()

        i = 0
        while i < 10:
            self.generate_fun()
            self.custom_sort()
            self.sorted_sort()
            print("###")
            i += 1
        ac=sum(self.results["Custom"])/len(self.results["Custom"])
        ap=sum(self.results["Predef"]) / len(self.results["Predef"])
        print(ac)
        print(ap)
        print(ac/ap)






app = QApplication(sys.argv)
ex = App()
app.exec_()