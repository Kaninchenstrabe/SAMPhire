### Dependecies
#import GUI
import sys
from PyQt5.QtWidgets import *
import json
from Hlib import *

class App(Hsort, Hfiles, Habout, Hgen, Hmeas, Hvis, Hcomp, QMainWindow,QWidget):
    def __init__(self):
        super().__init__()
        self.tab = []
    #Definiuje geometrię okna
        self.left = 100
        self.top = 100
        self.height = 500
        self.width = 600
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

        self.MainLayout = QVBoxLayout()
        #self.MainLayout.addWidget(Hvis().plot)


    #Wyświetlenie okna
        self.show()








app = QApplication(sys.argv)
ex = App()
app.exec_()