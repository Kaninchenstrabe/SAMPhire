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
from pathlib import Path

class App(Hfiles, Habout, Hgen, Hvis, Hcomp, QMainWindow,QWidget):
    def __init__(self):
        super().__init__()
    # DEFINICJA ZMIENNYCH
        self.tab = {"Unsorted":[],"Sorted":[]}
        self.algos=[]
        self.objalgo={}
    # KONFIGURACJA OKNA
        self.left = 100
        self.top = 100
        self.height = 100
        self.width = 100
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setWindowTitle('Algorytmy sortujące')
    # KONFIGURACJA ZAKŁADEK W TOOLBARZE
        menus={}
        submenus={}
        with open('config.json') as file_json:
            self.Menu_data=json.load(file_json)

        menu_bar=self.menuBar()
        for menu in self.Menu_data:
            if self.Menu_data[menu]:
                menus.update({menu: menu_bar.addMenu(menu)})
                for submenu in self.Menu_data[menu]:
                    #print(f" Teraz konfiguruje       {menu}_{submenu}")
                    old_sub=submenu
                    submenu=submenu.replace(" ","")
                    submenus.update({submenu: QAction(old_sub, self)})
                    callback = getattr(self, f"{self.Menu_data[menu][submenu]}")
                    submenus[submenu].triggered.connect(callback)
                    menus[menu].addAction(submenus[submenu])
            elif not self.Menu_data[menu]:
                #print(f" Teraz konfiguruje       {menu}")
                #menus.update({menu: menuBar.addMenu(menu)})
                menus.update({menu: QAction(menu, self)})
                menu_bar.addAction(menus[menu])
                callback = getattr(self, f"{menu.lower()}")
                menus[menu].triggered.connect(callback)

    # KONFIGURACJA GŁÓWNEGO EKRANU I WIDGETÓW
        central = QWidget()
        self.setCentralWidget(central)
        self.MainLayout = QGridLayout(central)

        self.graphs = {"Plot": {}, "Label":{}}
        for name in "Unsorted", "Sorted":
            #self.graphs.update({"Plot": {}})
            self.graphs["Plot"][name]=pg.PlotWidget(title=name)
            self.graphs["Plot"][name].setBackground(background='#ffffff')
            self.graphs["Plot"][name].setMouseEnabled(x=False, y=False)
            self.graphs["Plot"][name].setFixedSize(300,250)
            self.graphs["Plot"][name].setStyleSheet("border: 1px solid black")

        self.sort_layout=QVBoxLayout()
        self.pick_algo = QComboBox()
        #self.pick_algo.setPlaceholderText("Wybierz algorytm")

        dir = sorted((Path(__file__).resolve().parent / "Hlib_files" / "Algorithms").glob("*.py"))
        for file in dir:
            filename = list(file.name[:-3])
            for i in range(len(filename)):
                if filename[i]=='_' and 0<i<len(filename)-1:
                    filename.pop(i)
                    filename.insert(i," ")
            filename = ''.join(filename)
            self.algos.append({filename:file.name[:-3]})
            self.pick_algo.addItem(filename)
            self.objalgo.update({filename:None})
        # self.pick_algo.addItems(self.algos.keys())
        self.pick_algo.setCurrentIndex(-1)
        self.pick_algo.setItemText(-1, "+Wybierz algorytm+")
        self.pick_algo.setFixedHeight(50)
        self.sort_layout.addWidget(self.pick_algo)
        self.Sort_Button=QPushButton("S   O   R   T")
        self.Sort_Button.setFixedHeight(100)
        self.Sort_Button.clicked.connect(self.run_sort)
        self.sort_layout.addWidget(self.Sort_Button)
        self.MainLayout.addLayout(self.sort_layout, 1, 1)
        self.MainLayout.addWidget(self.graphs["Plot"]["Unsorted"], 1, 0)
        self.MainLayout.addWidget(self.graphs["Plot"]["Sorted"], 1, 2)
        self.MainLayout.setRowMinimumHeight(0,1)
        self.MainLayout.setColumnMinimumWidth(1,250)
        self.setLayout(self.MainLayout)
    #Wyświetlenie okna
        self.show()
    # Funkcja pośrednicząca w uruchamianiu sortowań
    def run_sort(self):
        i =self.pick_algo.currentIndex()
        if i <0:
            QMessageBox.warning(self, "Błąd", "Wybierz algorytm")
        else:
            type = next(iter((self.algos[i].values())))
            if self.objalgo[type]==None:
                self.objalgo[type] = Hsort(type)
                self.objalgo[type].load_algorithms()
            self.objalgo[type].load_data(self.tab["Unsorted"])
            print(self.objalgo[type].sort())
            print(self.objalgo[type].check_sort())
            self.tab["Sorted"]=self.objalgo[type].data["Sorted"]
            Hvis.visualize_fun(self,"Sorted")

app = QApplication(sys.argv)
ex = App()
app.exec_()