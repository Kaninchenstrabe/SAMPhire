
def Hase_sort(n, tab=[]):
    i=0
    j=0
    k=0
    l=0

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





    # for s in range(len(h)):
    #     for i in range(len(tab) // h[s]):
    #         ins = tab[i * h[s]]
    #         j = (i - 1) * h[s]
    #         while j > -1 and tab[j] > ins:
    #             tab[j + h[s]] = tab[j]
    #             j -= h[s]
    #         tab[j + h[s]] = ins

    # for i in range(len(tab)):
    #         ins = tab[i]
    #         j=i-1
    #         while j>-1 and tab[j]>ins:
    #                     tab[j+1]=tab[j]
    #                     j-=1
    #         tab[j+1] = ins

