import os
from PyQt5.QtWidgets import QFileDialog
class Hfiles:

    def file_save(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getOpenFileName()","", "JSON (*.json)", options=options)
        file = open(filename, 'w')
        text = "Zawartość pliku"
        file.write(text)
        file.close()


    def file_open(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "JSON (*.json)", options=options)
        file = open(filename, 'r')
        text = file.read()
        print(text)
        file.close()


    def file_exit(self):
        os._exit(0)

class Habout:
    def about(self):
        print("About")