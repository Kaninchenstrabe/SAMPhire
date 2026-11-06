### Moja Implementacja sortowania przez wybieranie
def main(tab=[]):
    i=0
    j=0
    k=0
    l=0
    n = len(tab)
    for i in range((n//2)):
        k=i
        l=i
        for j in range(i,n-i):
            if(tab[j]<tab[k]):
                k=j
            if(tab[j]>tab[l]):
                l=j
        tab[k],tab[i]=tab[i],tab[k]
        if l==i:
            l=k
        tab[l],tab[n-i-1]=tab[n-i-1],tab[l]


