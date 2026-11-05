### Dependecies
import sys
from PyQt5.QtWidgets import *
import json
import pyqtgraph as pg
from Hlib_files.sort import Hsort
from Hlib_files.file_management import Hfiles, Habout
from Hlib_files.data import Hgen
from Hlib_files.visualize import Hvis
from Hlib_files.compare import Hcomp
from PyQt5 import QtCore

class App(Hsort, Hfiles, Habout, Hgen, Hvis, Hcomp, QMainWindow,QWidget):
    def __init__(self):
        super().__init__()
        self.tab = {"Unsorted":[],"Sorted":[]}
        self.results = {"Custom":[], "Predef":[]}
    #Definiuje geometrię okna
        self.left = 100
        self.top = 100
        self.height = 100
        self.width = 100
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        #self.setFixedSize(self.width,self.height)
    #Definiuje tytuł okna
        self.title = 'Algorytmy'
        self.setWindowTitle(self.title)
    #Definiuje zakładki w oknie
        menus={}
        submenus={}
        with open('config.json') as file_json:
            self.Menu_data=json.load(file_json)

        menu_bar=self.menuBar()
        for menu in self.Menu_data:
            if self.Menu_data[menu]:
                menus.update({menu: menu_bar.addMenu(menu)})
                for submenu in self.Menu_data[menu]:
                    print(f" Teraz konfiguruje       {menu}_{submenu}")
                    old_sub=submenu
                    submenu=submenu.replace(" ","")
                    submenus.update({submenu: QAction(old_sub, self)})
                    callback = getattr(self, f"{self.Menu_data[menu][submenu]}")
                    submenus[submenu].triggered.connect(callback)
                    menus[menu].addAction(submenus[submenu])
            elif not self.Menu_data[menu]:
                print(f" Teraz konfiguruje       {menu}")
                #menus.update({menu: menuBar.addMenu(menu)})
                menus.update({menu: QAction(menu, self)})
                menu_bar.addAction(menus[menu])
                callback = getattr(self, f"{menu.lower()}")
                menus[menu].triggered.connect(callback)
        central = QWidget()
        self.setCentralWidget(central)
        self.MainLayout = QGridLayout(central)

        self.graphs = {"Plot": {}, "Label":{}}
        for name in "Unsorted", "Sorted":
            #self.graphs.update({"Plot": {}})
            self.graphs["Plot"][name]=pg.PlotWidget()
            self.graphs["Plot"][name].setBackground(background='#ffffff')
            self.graphs["Plot"][name].setMouseEnabled(x=False, y=False)
            self.graphs["Plot"][name].setFixedSize(300,250)
            #self.graphs.update({"Label": {}})
            self.graphs["Label"][name]=QLabel()
            self.graphs["Label"][name].setText(name)
            self.graphs["Label"][name].setAlignment(QtCore.Qt.AlignCenter)
            self.graphs["Label"][name].setStyleSheet("font-size: 15px, bold")

        self.sort_layout=QVBoxLayout()
        self.pick_algo = QComboBox()
        #self.pick_algo.setPlaceholderText("Wybierz algorytm")
        self.pick_algo.addItems(Hsort.algos)
        self.pick_algo.currentTextChanged.connect(self.updateAlgo)
        self.pick_algo.setFixedHeight(50)
        self.graphs["Label"][name].setStyleSheet("font-size: 15px, bold")
        self.sort_layout.addWidget(self.pick_algo)
        self.B1=QPushButton("S   O   R   T")
        self.B1.setFixedHeight(100)
        self.B1.clicked.connect(self.run_sort)
        self.sort_layout.addWidget(self.B1)
        self.MainLayout.addLayout(self.sort_layout, 1, 1)
        self.MainLayout.addWidget(self.graphs["Label"]["Unsorted"], 0, 0)
        self.MainLayout.addWidget(self.graphs["Label"]["Sorted"], 0, 2)
        self.MainLayout.addWidget(self.graphs["Plot"]["Unsorted"], 1, 0)
        self.MainLayout.addWidget(self.graphs["Plot"]["Sorted"], 1, 2)
        self.MainLayout.setRowMinimumHeight(0,1)
        self.MainLayout.setColumnMinimumWidth(1,250)
        self.setLayout(self.MainLayout)
    #Wyświetlenie okna
        self.show()
    def updateAlgo(self, s):
        Hsort.algo=s

    def run_sort(self):
        if Hsort.algo =="": #or "Wybierz algorytm":
            QMessageBox.warning(self, "Błąd", "Wybierz algorytm")
        else:
            print(f"running {Hsort.algo}")
            exec(f"self.{Hsort.algo.lower()}_sort()")








app = QApplication(sys.argv)
ex = App()
app.exec_()