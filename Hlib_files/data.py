from PyQt5.QtWidgets import QDialog, QFormLayout, QSpinBox, QDialogButtonBox, QFileDialog
import numpy
from Hlib_files.visualize import Hvis
class Hgen:

    def __init__(self):
        super().__init__()
        self.low = None
        self.high = None
        self.amount = None
        self.imported = []
    def data_generate(self):
        #print("Generate")
        dialog = RangeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.low, self.high, self.amount = dialog.values()
            #print(f"Generate from {self.low} to {self.high}")
        self.tab["Unsorted"] = numpy.random.randint(self.low, self.high, size=self.amount, dtype=int)
        Hvis.visualize_fun(self, "Unsorted")
        return self.tab["Unsorted"]

    def data_import(self):
        options = QFileDialog.Options()
        filename, filetype = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Text files (*.txt);;CSV files (*.csv)", options=options)

        file = open(filename, 'r')
        text = file.read()
        num=[]
        match filetype:
            case "Text files (*.txt)":
                self.delimiter='\n'
            case "CSV files (*.csv)":
                self.delimiter=','
        for char in text:
            match char:
                case '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9':
                        num.append(char)
                case self.delimiter:
                    if len(num)!=0:
                        print(num)
                        self.tab["Unsorted"].append(int(''.join(num)))
                        num=[]
                case _ :
                    print("Nie zawracaj mi dupy, wróć z poprawnym plikiem")

        #self.tab["Unsorted"] = self.imported
        #print(self.tab["Unsorted"])
        Hvis.visualize_fun(self, "Unsorted")
        file.close()


    def data_export(self):
        options = QFileDialog.Options()
        filename, filetype = QFileDialog.getSaveFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Text files (*.txt);;CSV files (*.csv)", options=options)

        match filetype:
            case "Text files (*.txt)":
                delimiter = '\n'
            case "CSV files (*.csv)":
                delimiter = ','
        file = open(filename, 'w')
        text=[]
        for i in range(len(self.tab["Unsorted"])):
            text.append(str(self.tab["Unsorted"][i])+delimiter)
        file.write(''.join(text))
        file.close()

class RangeDialog(QDialog):
    MIN, MAX = 0, 10**6

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Zakres")

        self.low = QSpinBox()
        self.high = QSpinBox()
        self.amount = QSpinBox()
        self.low.setRange(self.MIN, self.MAX - 1)
        self.high.setRange(self.MIN + 1, self.MAX)
        self.amount.setRange(0, 10**6)
        self.low.setValue(0)
        self.high.setValue(100)
        self.amount.setValue(10)
        self.low.valueChanged.connect(self.update_limits)
        self.high.valueChanged.connect(self.update_limits)
        self.update_limits()

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QFormLayout(self)
        layout.addRow("Minimum:", self.low)
        layout.addRow("Maksimum:", self.high)
        layout.addRow("Ilość", self.amount)
        layout.addWidget(buttons)

    def update_limits(self):
        # high must stay above low, low must stay below high
        self.high.setMinimum(self.low.value() + 1)
        self.low.setMaximum(self.high.value() - 1)

    def values(self):
        return self.low.value(), self.high.value(), self.amount.value()


