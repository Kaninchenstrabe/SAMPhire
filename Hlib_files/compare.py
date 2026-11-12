from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *
from pathlib import Path
from Hlib_files.sort import Hsort
import numpy
import pandas as pd
import matplotlib.pyplot as plt

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
        self.algo_grades={}
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
        #self.value=0
        for i in range(4):
            for j in range(10):
                item = self.table.item(j,i)
                if item is not None:
                    try:
                        value = int(item.text())
                        match i:
                            case 0:
                                self.parameters["Rounds"].append(value)
                            case 1:
                                self.parameters["Length"].append(value)
                            case 2:
                                self.parameters["Min"].append(value)
                            case 3:
                                self.parameters["Max"].append(value)

                    except ValueError:
                        QMessageBox.warning(self, "Błąd", "Nieprawidłowe dane")

    def comp_run(self):
        self.Main.close()
        if sum(self.CheckBoxes["Data"]) == 0:
            QMessageBox.warning(self, "Błąd", "Nie wybrano żadnego algorytmu do zbadania")
        else:
            print("Ok badam")
            self.table_read()
            print(self.parameters)

            stages=len(self.parameters["Rounds"])
            for k in range(stages):#
                for i in range(self.parameters["Rounds"][k]):
                    if self.parameters["Rounds"][k] != (0 or None) or self.parameters["Length"][k] != (0 or None):
                        random = numpy.random.randint(self.parameters["Min"][k], self.parameters["Max"][k],size=self.parameters["Length"][k], dtype=int)
                        for n in range(len(self.CheckBoxes["Data"])):
                            if self.CheckBoxes["Data"][n]:
                                #print(f"Posortuj te dane algorytmem {self.CheckBoxes["Algos"][n]}")
                                temp = Hsort(self.CheckBoxes["Algos"][n])
                                self.Algorithms.append(temp)
                                self.Algorithms[-1].load_algorithms()
                                self.Algorithms[-1].load_data(random)
                                time=self.Algorithms[-1].sort()
                                grade = self.Algorithms[-1].check_sort()
                                if self.CheckBoxes["Algos"][n] not in self.algo_runtimes:
                                    self.algo_runtimes.update({self.CheckBoxes["Algos"][n]: [[] for _ in range(stages)]})
                                    self.algo_grades.update({self.CheckBoxes["Algos"][n]: [[] for _ in range(stages)]})
                                self.algo_runtimes[self.CheckBoxes["Algos"][n]][k].append(round(time,2))
                                self.algo_grades[self.CheckBoxes["Algos"][n]][k].append(grade)

                self.comp_analyze()
            print(f"Policz średnią, pokaż wykres")
            self.comp_show()
    def comp_analyze(self):
        self.avg={"Time":{}, "Grade":{}}
        for name, all_times in self.algo_runtimes.items():
            self.avg["Time"][name] = []
            for index, times in enumerate(all_times):
                print(f"{index}, {times}")
                self.avg["Time"][name].append(sum(times)/max(1,len(times)))
        for name, all_grades in self.algo_grades.items():
            self.avg["Grade"][name] = []
            for index, grades in enumerate(all_grades):
                print(f"{index}, {grades}")
                self.avg["Grade"][name].append(sum(grades)/max(1,len(grades)))
        print(self.avg)
    def comp_set(self):
        self.Main.show()
        print("Settings")
    def comp_show(self):
        df = pd.DataFrame(self.avg["Time"], index=self.parameters["Length"])
        df = df.sort_index()
        ax = df.plot(marker='o', title='Średni czas sortowania', logy=True, logx=True)
        ax.set_ylabel('Czas (skala logarytmiczna)')
        ax.set_xlabel('Długość zestawu danych (skala logarytmiczna')
        ax.legend(title='Algorytm')
        ax.grid(True, which='both', alpha=0.3)

        plt.show()
    def comp_explain(self):
        print("Explain")
