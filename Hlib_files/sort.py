from Hlib_files.Algorithms.custom import Hase_sort
import time
class Hsort:
    def insertion_sort(self, a):
        for i in range(1, len(a)):
            x = a[i]
            j = i - 1
            while j >= 0 and a[j] > x:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = x
        return a
    def f_merge(self, a, b):
        wynik = []
        i = j = 0
        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                wynik.append(a[i])
                i += 1
            else:
                wynik.append(b[j])
                j += 1
        wynik.extend(a[i:])
        wynik.extend(b[j:])
        return wynik

    def sort_div(self,tab=[]):
        n = len(tab)
        div=4
        q = n // div
        czesci = []
        czesci = [tab[i*q:(i+1)*q] for i in range(div)]
        #czesci = [tab[:q], tab[q:2 * q], tab[2 * q:3 * q], tab[3 * q:]]
        for c in czesci:
            self.insertion_sort(c)
        tab = self.f_merge(self.f_merge(czesci[0], czesci[1]), self.f_merge(czesci[2], czesci[3]))
        return tab

    def custom_sort(self):
        #print("Custom")
        data = self.tab["Unsorted"]
        #Sortowanie shella
        n=len(data)
        start = time.perf_counter()
        #Hase_sort(n,data)
        self.tab["Unsorted"]=self.sort_div(data)
        koniec = time.perf_counter()
        t=(koniec-start)*10**6
        print(f"Czas sortowania insertion: {(t)} mikrosekund")
        self.results["Custom"].append(t)
        return t

    def sorted_sort(self):
        data=self.tab["Unsorted"]
        start = time.perf_counter()
        sorted(data)
        koniec = time.perf_counter()
        t = (koniec - start)*10**6
        print(f"Czas sortowania sorted: {(t)} mikrosekund")
        self.results["Predef"].append(t)
        return t
    def sortingtechniques_sort(self):
        print("Techniques")