import time
import sorting_techniques
from Hlib_files import visualize
from Hlib_files.Algorithms.custom import sort_div
from Hlib_files.Algorithms.Selection import Selection_sort
from PyQt5.QtWidgets import *
from Hlib_files.visualize import Hvis

class Hsort:
    algo = ""
    algos = ["Selection", "Sorted", "Techniques", "Custom"]

    def custom_sort(self):
        print("custom")
        data = self.tab["Unsorted"]
        n=len(data)
        start = time.perf_counter()
        data=sort_div(data)
        koniec = time.perf_counter()
        t=(koniec-start)*10**6
        print(f"Czas sortowania custom: {(t)} mikrosekund")
        self.results["Custom"].append(t)
        self.tab["Sorted"]=data
        Hvis.visualize_fun(self,"Sorted")
        return t

    def sorted_sort(self):
        print("sorted()")
        data=self.tab["Unsorted"]
        start = time.perf_counter()
        sorted(data)
        koniec = time.perf_counter()
        t = (koniec - start)*10**6
        print(f"Czas sortowania sorted(): {(t)} mikrosekund")
        self.results["Predef"].append(t)
        self.tab["Sorted"] = data
        Hvis.visualize_fun(self,"Sorted")
        return t
    def techniques_sort(self):
        print("techniques")
        data = self.tab["Unsorted"]
        start = time.perf_counter()
        sorting_techniques.selection_sort(data)
        koniec = time.perf_counter()
        t = (koniec - start) * 10 ** 6
        print(f"Czas sortowania techniques: {(t)} mikrosekund")
        self.results["Predef"].append(t)
        self.tab["Sorted"] = data
        Hvis.visualize_fun(self, "Sorted")
        return t
    def selection_sort(self):
        print("Selection")
        data = self.tab["Unsorted"]
        n=len(data)
        start = time.perf_counter()
        Selection_sort(n,data)
        koniec = time.perf_counter()
        t = (koniec - start)*10**6
        print(f"Czas sortowania Selection: {(t)} mikrosekund")
        self.results["Predef"].append(t)
        print("Techniques")
        self.tab["Sorted"] = data
        Hvis.visualize_fun(self,"Sorted")
        return t