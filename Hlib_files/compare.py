from PyQt5.QtWidgets import *
from pathlib import Path

class Hcomp:
    def __init__(self):
        super().__init__()
        self.Main = QWidget()
        self.Main.setGeometry(1000, 100, 600, 600)
        self.popupsiatka = QGridLayout()
        self.CBWidget = QVBoxLayout()
        self.lens = QVBoxLayout()
        self.CheckBoxes=[]
        self.SpinBoxes=[]
        for file in sorted((Path(__file__).resolve().parent / "Algorithms").glob("*.py")):
            filename = list(file.name[:-3])
            for i in range(len(filename)):
                if filename[i] == '_' and 0 < i < len(filename) - 1:
                    filename.pop(i)
                    filename.insert(i, " ")
            filename = ''.join(filename)
            self.CheckBoxes.append(QCheckBox(text=filename))

        self.CBWidget.addWidget(QLabel("Wybierz algorytmy, które wezmą udział w badaniu"))
        for i in range(len(self.CheckBoxes)):
            self.CBWidget.addWidget(self.CheckBoxes[i])
        self.popupsiatka.addLayout(self.CBWidget, 0, 0)
        self.proby=QSpinBox()
        self.proby.valueChanged.connect(self.comp_dlrprob)
        self.popupsiatka.addWidget(self.proby,1,0)


        self.Main.setLayout(self.popupsiatka)
        self.dlugosciprob = QVBoxLayout()
    def comp_dlrprob(self, count):

        while len(self.SpinBoxes) < count:
            self.SpinBoxes.append(QSpinBox())
            self.dlugosciprob.insertWidget(self.dlugosciprob.count()-1,self.SpinBoxes[-1])

        while len(self.SpinBoxes) > count:
            spin = self.SpinBoxes.pop()
            self.dlugosciprob.removeWidget(spin)
            spin.deleteLater()

        self.popupsiatka.addLayout(self.dlugosciprob, 1, 1)

    def comp_set(self):


        self.Main.show()
        print("Settings")

    def comp_show(self):
        print("Show")

    def comp_explain(self):
        print("Explain")
