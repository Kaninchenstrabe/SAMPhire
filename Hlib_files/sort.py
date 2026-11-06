import time
from Hlib_files import visualize
from Hlib_files.Algorithms.Custom import main as custom
from Hlib_files.Algorithms.Selection import main as selection
from Hlib_files.Algorithms.Techniques import main as techniques
from Hlib_files.Algorithms.Built_in import main as built_in
from PyQt5.QtWidgets import *
from Hlib_files.visualize import Hvis
import importlib.util
from pathlib import Path
class Hsort:
    #algos = ["Selection", "Built in", "Techniques", "Custom"]
    def __init__(self, type):
        self.data={"Unsorted":[], "Sorted":[], "Time":[]}
        self.type=type
        self.algorithms={}
        self.faults=[]
    def load_data(self, data):
        self.data["Unsorted"]=data
        self.data["Sorted"]=data
    def load_algorithms(self):
        self.dir = Path(__file__).parent
        for file in sorted((self.dir / "Algorithms").glob("*.py")):
            spec = importlib.util.spec_from_file_location(file.stem, file)
            module=importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.algorithms.update({module.__name__:module})
    def sort(self):
        start = time.perf_counter()
        self.algorithms[self.type].main(self.data["Sorted"])
        koniec = time.perf_counter()
        t = (koniec - start)*10**6
        self.data["Time"].append(t)
        return t
    def check_sort(self):
        for i in range(1,len(self.data["Sorted"])):
            if self.data["Sorted"][i-1]>self.data["Sorted"][i]:
                self.faults.append(i)
        return self.faults
    # def selection_sort(self):
    #     start = time.perf_counter()
    #     selection(self.tab["Sorted"])
    #     koniec = time.perf_counter()
    #     t = (koniec - start)*10**6
    #     self.data["Time"].append(t)
    #     return t
    #
    # def custom_sort(self):
    #     start = time.perf_counter()
    #     custom(self.data["Sorted"])
    #     koniec = time.perf_counter()
    #     t=(koniec-start)*10**6
    #     self.data["Time"].append(t)
    #     return t
    #
    # def built_in_sort(self):
    #     start = time.perf_counter()
    #     built_in(self.data["Sorted"])
    #     koniec = time.perf_counter()
    #     t = (koniec - start)*10**6
    #     self.data["Time"].append(t)
    #     return t
    #
    # def techniques_sort(self):
    #     print("techniques")
    #     start = time.perf_counter()
    #     techniques(self.data["Sorted"])
    #     koniec = time.perf_counter()
    #     t = (koniec - start) * 10 ** 6
    #     return t
    #     self.data["Time"].append(t)
