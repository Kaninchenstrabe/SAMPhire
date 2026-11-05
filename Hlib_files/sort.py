from Hlib_files.Algorithms.custom import Hase_sort
import time
class Hsort:

    def custom_sort(self):
        #print("Custom")
        data = self.tab["Unsorted"]
        #Sortowanie shella
        n=len(data)
        start = time.perf_counter()
        Hase_sort(n,data)
        koniec = time.perf_counter()
        t=(koniec-start)*10**5
        print(f"Czas sortowania insertion: {(t)}")
        self.results["Custom"].append(t)
        return t
    def sorted_sort(self):
        data=self.tab["Unsorted"]
        start = time.perf_counter()
        sorted(data)
        koniec = time.perf_counter()
        t = (koniec - start)*10**5
        print(f"Czas sortowania sorted: {(t)}")
        self.results["Predef"].append(t)
        return t
    def sortingtechniques_sort(self):
        print("Techniques")