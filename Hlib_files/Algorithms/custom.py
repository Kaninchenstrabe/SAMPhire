def insertion_sort( a):
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x
    return a


def merge(a, b):
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


def sort_div(tab):
    n = len(tab)
    if n < 2:
        return tab
    div = max(1, n.bit_length() - 1)
    q = n // div
    czesci = []
    czesci = [tab[i * q:(i + 1) * q] for i in range(div - 1)]
    czesci.append(tab[(div - 1) * q:])
    for c in czesci:
        insertion_sort(c)
    while len(czesci) > 1:
        nowe = []
        for i in range(0, len(czesci) - 1, 2):
            nowe.append(merge(czesci[i], czesci[i + 1]))
        if len(czesci) % 2 == 1:
            nowe.append(czesci[-1])
        czesci = nowe
    tab = czesci[0]
    return tab
