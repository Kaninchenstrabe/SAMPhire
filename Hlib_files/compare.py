from PyQt5.QtWidgets import *
class Settings_popup(QWidget):
    def __init__(self):
        QWidget.__init__(self)

class Hcomp:
    def comp_set(self):
        self.SetPop=Settings_popup()
        self.SetPop.setGeometry(100, 100, 400, 200)
        #self.setPop
        print("Settings")
    def comp_show(self):
        print("Show")
    def comp_explain(self):
        print("Explain")
