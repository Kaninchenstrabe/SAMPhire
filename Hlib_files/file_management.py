import os
from PyQt5.QtWidgets import QFileDialog
class Hfiles:
    def import_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", options=options)
        file = open(fileName, 'r')
        self.tab["Unsorted"]=file.read()
        print(self.tab["Unsorted"])
        file.close()
        print("Import")


    def export_file(self):
        Dialog = QFileDialog()
        Dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        fileName, _ = QFileDialog.getSaveFileName(self, "Export", "", options=Dialog.Options())
        file = open(f"{fileName}.txt", 'w')
        file.write(str(self.tab["Unsorted"]))
        file.close()
        print("Export")



    def save_file(self):

        print("Save")

    def saveas_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getOpenFileName()", "", options=options)
        file = open(fileName, 'w')
        text = "Zawartość pliku"
        file.write(text)
        file.close()



    def open_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", options=options)
        file = open(fileName, 'r')
        text = file.read()
        print(text)
        file.close()


    def exit_file(self):
        os._exit(0)

class Habout:
    def about_fun(self):
        print("About")