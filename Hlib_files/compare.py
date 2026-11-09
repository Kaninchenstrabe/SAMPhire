from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *
from pathlib import Path
from Hlib_files.sort import Hsort
import numpy

class IntValidationDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.positive_validator = QIntValidator(1, 2147483647, self)
        self.any_integer_validator = QIntValidator(-2147483648, 2147483647, self)

    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        col = index.column()

        if col in (0, 1):
            editor.setValidator(self.positive_validator)
        elif col in (2, 3):
            editor.setValidator(self.any_integer_validator)

        return editor

class Hcomp:
    def __init__(self):
        super().__init__()
        self.Main = QWidget()
        self.Main.setGeometry(1000, 100, 852, 450)
        self.Layouts={"Main": QGridLayout(), "Checkbox":QVBoxLayout()}
        self.CheckBoxes={"Layout":QVBoxLayout(), "Widgets":[], "Data":[], "Algos":[]}
        self.Algorithms=[]
        self.parameters={"Rounds":[], "Length":[], "Min":[], "Max":[]}
        self.algo_runtimes={}
        for file in sorted((Path(__file__).resolve().parent / "Algorithms").glob("*.py")):
            filename = list(file.name[:-3])
            for i in range(len(filename)):
                if filename[i] == '_' and 0 < i < len(filename) - 1:
                    filename.pop(i)
                    filename.insert(i, " ")
            filename = ''.join(filename)
            self.CheckBoxes["Widgets"].append(QCheckBox(text=filename))
            self.CheckBoxes["Data"].append(False)
            self.CheckBoxes["Algos"].append(file.name[:-3])
        for i in range(len(self.CheckBoxes["Widgets"])):
            self.CheckBoxes["Widgets"][i].stateChanged.connect(self.check_change)
        self.label=QLabel("\nWybierz algorytmy, które wezmą udział w badaniu")
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.CheckBoxes["Layout"].addWidget(self.label)
        for checkbox in self.CheckBoxes["Widgets"]:
            self.CheckBoxes["Layout"].addWidget(checkbox)
        self.CheckBoxes["Layout"].addStretch(1)
        self.Layouts["Main"].addLayout(self.CheckBoxes["Layout"], 0, 0)
        self.Go = QPushButton("Rozpocznij badanie")
        self.Go.clicked.connect(self.comp_run)
        self.Go.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.Layouts["Main"].addWidget(self.Go, 1, 0)
        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        delegate = IntValidationDelegate(self.table)
        self.table.setItemDelegate(delegate)
        self.table.cellChanged.connect(self.validate_dependent_columns)
        self.table.setRowCount(10)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Rundy", "Długość \ndanych", "Min", "Max"])
        #self.table.horizontalHeader().setStretchLastSection(True)
        #self.table.setItem(0, 0, QTableWidgetItem("Ile podejść?"))
        #self.table.setItem(0, 1, QTableWidgetItem("Ile elementów?"))
        self.Layouts["Main"].addWidget(self.table, 0, 1, 0, 2)
        self.Main.setLayout(self.Layouts["Main"])

    def validate_dependent_columns(self, row, column):
        if column in (2, 3):
            item3 = self.table.item(row, 2)
            item4 = self.table.item(row, 3)

            if item3 and item3.text() and item4 and item4.text():
                try:
                    val3 = int(item3.text())
                    val4 = int(item4.text())

                    if val4 <= val3:
                        self.blockSignals(True)
                        corrected_val = val3 + 1
                        self.table.setItem(
                            row, 3, QTableWidgetItem(str(corrected_val))
                        )

                        self.blockSignals(False)

                        QMessageBox.warning(
                            self,
                            "Błąd",
                            f"Rząd {row + 1}: Kolumna 'Max' musi mieć wiekszą wartość niż kolumna 'Min'.\n"
                            f"Automatycznie poprawiam wartość kolumny 'Max' do {corrected_val}.",
                        )
                except ValueError:
                    pass
    def check_change(self):
        sender = self.sender()
        i=self.CheckBoxes["Widgets"].index(sender)
        self.CheckBoxes["Data"][i]= not(self.CheckBoxes["Data"][i])
        print(self.CheckBoxes["Data"])
    def table_read(self):
        self.value=0
        for i in range(4):
            for j in range(10):
                item = self.table.item(j,i)
                if item is not None:
                    try:
                        self.value = int(item.text())
                    except ValueError:
                        QMessageBox.warning(self, "Błąd", "Nieprawidłowe dane")
                if item is None:
                    self.value=None
                match i:
                    case 0:
                        self.parameters["Rounds"].append(self.value)
                    case 1:
                        self.parameters["Length"].append(self.value)
                    case 2:
                        self.parameters["Min"].append(self.value)
                    case 3:
                        self.parameters["Max"].append(self.value)
    def comp_run(self):
        if sum(self.CheckBoxes["Data"]) == 0:
            QMessageBox.warning(self, "Błąd", "Nie wybrano żadnego algorytmu do zbadania")
        else:
            print("Ok badam")
            self.table_read()
            #print(self.parameters)
            for i in range(min(len(self.parameters["Rounds"]), len(self.parameters["Length"]))):
                if self.parameters["Rounds"][i] != (0 or None) or self.parameters["Length"][i] != (0 or None):
                    print(
                        f"Wygeneruj {self.parameters["Rounds"][i]} losowych danych o długości {self.parameters["Length"][i]} od {self.parameters["Min"][i]} do {self.parameters["Max"][i]}")

                    random = numpy.random.randint(self.parameters["Min"][i], self.parameters["Max"][i],size=self.parameters["Length"][i], dtype=int)
                    for n in range(len(self.CheckBoxes["Data"])):
                        if self.CheckBoxes["Data"][n]:
                            temp = Hsort(self.CheckBoxes["Algos"][n])
                            self.Algorithms.append(temp)
                            self.Algorithms[-1].load_algorithms()
                            self.Algorithms[-1].load_data(random)

                            print(self.Algorithms[-1])
                            time=self.Algorithms[-1].sort()
                            self.algo_runtimes.update({self.CheckBoxes["Algos"][n], time})

                    print(self.algo_runtimes)
                    print(f"Posortuj te dane algorytmem {self.CheckBoxes["Data"]}")
                    for algo in self.CheckBoxes["Widgets"].text():
                        algo_r=Hsort(algo)
                        print(algo_r)
            print(f"Policz średnią, pokaż wykres")
    def comp_set(self):
        self.Main.show()
        print("Settings")

    def comp_show(self):
        print("Show")

    def comp_explain(self):
        print("Explain")
