# modul zajišťující testování posloupnosti - všechny funkce testující jednotlivé možnosti rozvoje posloupnosti
# z modulu operator importuji funkce pro sčítání, odečítání, násobení a dělení - vysvětleno dále
from operator import add, mul, sub, truediv 

# funkce dostává list jako parametr a zjištuje, zda mezi prvky listu je stejný rozdíl, případně jsou vzájemně ve stejném poměru
# v případě poměru, který zjišťuji pomocí dělení po sobě jdoucích prvků, pracuji s číselným typem float
# funkce vrací hodnoty True/False podle toho, jestli se jeden z popsaných jevů objevil
def pridavaniStejnehoCisla(array, operator):
    if operator == truediv:
        rozdil = float(operator(array[1],array[0]))
    else:
        rozdil = operator(array[1], array[0])
    for i in range(1,len(array) - 1):
        if operator(array[i+1], array[i]) != rozdil:
            return False
    return True

# funkce vytváří list vyjadřující rozdíly, respektive poměry mezi jednotlivými prvky testované řady
# funkci volám 2x s operátory sub, add a truediv a mul
def pridaniPosloupnosti(array,operator1, operator2):
    # testuji, zda řada obsahuje nulu, pokud ano, nemá smysl testovat poměry (nedávalo by smysl)
    if operator1 == truediv:
        for i in array:
            if i == 0:
                return False,None
    pricitanaPosloupnost = []
    # vytvářím řadu, která vyjadřauje koeficienty rozdílu, případně poměru
    for i in range(len(array) - 1):
        pricitanaPosloupnost.append(operator1(array[i + 1],array[i]))
    # využívám přechozí funkce ke zjištění, zda prvky v listu spolu nějak souvisí
    if pridavaniStejnehoCisla(pricitanaPosloupnost,sub):
        # pokud podmínka projde, vytvořím si z prvních dvou prvků listu konstantu, která vyjadřuje o kolik, případně kolikrát se koeficienty zvětšují
        konstanta = pricitanaPosloupnost[1] - pricitanaPosloupnost[0]
        for i in range(5):
            # vyjadřuji koeficient posledních dvou prvků, přičítám k němu konstantu a přidávám nový prvek do původní řady - celkem 5x
            # v případě odečítání pracuji s INT, jinak FLOAT
            rozdil2 = operator1(array[-1], array[-2]) 
            if operator1 == sub:
                array.append(int(operator2(array[-1], konstanta + rozdil2)))
            else: 
                array.append(float(operator2(array[-1], konstanta + rozdil2)))
        # jedná se o funkci, která není pomocná jako přechozí, tuto funkci volám při testování posloupnosti v poslední funkci zkomtroluj
        # všechny tyto funkce vrací minimálně 2 hodnoty - první hodnota vyjadřuje, zda podmínka prošla -tzn. byla objevena souvislost mezi čísly, druhá hodnota vrací doplněnou řadu o nová čísla
        # toto schéma dodržuji striktně u všech funkcí, které na konci volám ve zkontroluj
        return True,array 
    return False,None

# funkce dostane 2 parametry - řadu a int n a zjišťuje, zda se v řadě vyskytují periodicky se opakující čísla s peridou n
def periodickeOpakovani(array, n):
    # v prvé řadě funkce zjišťuje, zda je řada dostatečně dlouhá, aby se v ní daná perioda mohla vyskytovat
    if int(n + n/2) < len(array):
        for i in range(len(array) - n):
            if array[i] != array[i+n]:
            # stačí, aby podmínka jednou neprošla a vracíme False
                return False,None,None
        # zjišťujeme, kde perioda skončila, abychom ji mohli doplnit
        rozdil = len(array) % n
        for i in range(n-rozdil):
            array.append(array[rozdil + i])
        # periodu ještě jednou celou doplním  
        for i in range(n):
            array.append(array[i])
        # vracím bool, jestli podmínka prošla, doplněnou řadu a periodu, kterou využívám později v jiné funkci
        return True,array,n
    return False,None,None

# ve funkci nicméně volám až tuto funkci perioda, využívám předchozí funkce, kam do parametru n postupně přidávám čísla od 1 do délky řady
# jakmile je perioda detekována, funkce vrací True, doplněnou řadu, n a končí
def perioda(array):
    for i in range(1,len(array)):
        var = periodickeOpakovani(array,i)
        if var[0]:
            return True,var[1], var[2]
    return False,i

# funkce dostává řadu, číslo n a operátor(testuji pro sčítání a odčítání) a zjišťuje, zda součet/součin (n-1) čísel se rovná n-tému číslu
def pridavaniPredchozichCisel(array, n,operator):
    # opět, pokud řada obsahuje nulu, součin netestujeme
    if operator == mul:
        for i in array:
            if i == 0:
                return False,None
    zacatek = -n
    # testování probíhá tolikrát, kolikrát se tam celý součet/součin mohl objevit
    for i in range(int(len(array)/n)):
        # postupně si vytváříme mezivýsledek z n-1 čísel a kontrolujeme, zda se rovná n-tému číslu
        # pomocí proměnné zacatek si vždy vyjadřuji začátek dané "periody"
        if operator == mul:
            mezivysledek = 1
        else:
            mezivysledek = 0
        zacatek += n
        for s in range(n - 1):
            mezivysledek = operator(mezivysledek, array[zacatek + s])
        if mezivysledek != array[zacatek + n- 1]:
            return False,None
    # tuto řadu jsme schopni doplnit pouze o 1 číslo pouze v případě, že chybí chybí právě n-té číslo v dané periodě
    # to získáme tak, že do rozdil si uložíme délku řady mod n, pokud se to rovná n-1, můžeme číslo doplnit
    rozdil = len(array) % n
    if rozdil == n-1:
        if operator == mul:
            zacatek = 1
        else:
            zacatek = 0
        for i in range(1,n):
            if operator == mul:
                zacatek *= array[-i]
            else:
                zacatek += array[-i]
        array.append(zacatek)
    # v opačném případě pouze slovně vypisujeme, jakou souvislot jsme našli
    else:
        if operator == add:
            print("Součet " + str(n-1) + " čísel rovná se " + str(n) + ". číslu.")
        else:
            print("Součin " + str(n-1) + " čísel rovná se " + str(n) + ". číslu.")
    return True,array

# ve zkontroluj voláme až tuto funkci, kde do parametru n předchozí funkce postupně přidáváme čísla v omezeném intervalu v závislosti na délce řady
def pridani(array,operator):
    for i in range(3,int(len(array)/2) + 1):
        var = pridavaniPredchozichCisel(array,i,operator)
        if var[0]:
            return True, var[1]
    return False,None

moznostiStridani = []

# následující funkce zjišťuje, zda se k posloupnmosti periodciky přičítají čísla nebo se násobí nějakými čísly (kombinuje sčítání a násobení)
# zjišťuje to pro periodu délky n, rekurzivně generuje všechny možnosti sčítání a násobení
# výsledek přidává do proměné moznostiStridani, která reprezentuje seznam seznamů funkcí
def generujMoznosti(n, vysledek = []):
    if n == 0:
        global moznostiStridani
        moznostiStridani.append(vysledek)
    else:
        generujMoznosti(n-1, vysledek = vysledek + [sub])
        generujMoznosti(n-1, vysledek = vysledek + [truediv])

# tato funkce dostane parametr parametry řadu a číslo n vyjadřující periodu sčítání a násobení
# pomocí předchozí funkce zjišťuje, zda se daný jev v listu objevuje
def stridaniOperatoru(array,n):
    # list musí být dlouhý alespoň 2n - perioda se musí alespoň 2x opakovat
    if int(2*n) <= len(array):
        generujMoznosti(n)
        global moznostiStridani
        moznostiStridani1 = True
        # postupně procházíme seznamy funkcí uložené v proměnné i
        for i in moznostiStridani:
            # pomocí operátorů uložených v seznamu i vytváříme nový seznam pomocnaRada
            # výjimky používáme z toho důvodu, kdyby se v posloupnosti objevila nula na nevhodném místě
            # jiné možné řešení by bylo "ořezat" rekurzi, takto je to ale jasnější a přehlednější
            pomocnaRada = []
            try:
                for s in range(len(array)-1):
                    pomocnaRada.append(float((i[s%n](array[s+1], array[s]))))
            except ZeroDivisionError:
                moznostiStridani1 = False
            if moznostiStridani1:
                # ověříme, zda vytvořený seznam odpovídá periodicky se opakující posloupnosti
                var = perioda(pomocnaRada)
                if var[0]:
                    # pokud podmínka projde, ořízneme původní posloupnost tak, aby se v ní neobjevovala nedokončená perioda
                    array = array[:(len(array)-((len(array)-1)%var[2]))]
                    # doplníme 2 další periody
                    for e in range(2*n):
                        if i[e%n] == sub:
                            array.append(int(array[len(array)-1] + pomocnaRada[e]))
                        elif i[e%n] == truediv:
                            array.append(int(array[len(array)-1] * pomocnaRada[e]))
                    moznostiStridani = []
                    return True,array
    moznostiStridani = []
    return False,None

# ve zkontroluj voláme až tuto funkci, kde do parametru n předchozí funkce postupně přidáváme čísla v omezeném intervalu v závislosti na délce řady
def stridacko(array):
    for i in range(2,int(len(array)/2 + 1)):
        var = stridaniOperatoru(array,i)
        if var[0]:
            return var
    return False,None

# funkce dostane číslo n a zjišťuje, zda je prvočíslo, vrací Bool
def prvocislo(s): 
    if s % 2 == 0: 
        return s == 2
    else: 
        d=3
        while d * d <= s: 
            if s % d == 0:
                return False 
            else:
                d += 2
        return True

# funkce kontrolující, zda seznam je tvořen po sobě jdoucími prvočísly
def prvocisla(array):
    # kontroluje, zda první a poslední číslo v seznamu jsou prvočísla a zda je poslední větší než první
    if prvocislo(array[0]) and prvocislo(array[len(array) - 1]) and ((array[len(array) - 1]) > (array[0])):
        index = 1
        # procházíme všechna čísla od prvního prvočísla +1 až do posledního prvočísla
        # kontrolujeme, zda čísla mezi nimi jsou prvočísla a pokud ano, tak zda jsou obsaženy v seznamu
        for i in range(array[0] + 1, (array[len(array) -1] + 1)):
            if prvocislo(i):
                if array[index] != i:
                    return False, []
                else:
                    index += 1 
        pridavat = (array[len(array) -1]) + 1
        dokonceno = False
        index = 0
        # zde již víme, že seznam obsahuje po sobě jdoucí prvočísla
        # následující while cyklus přidá do posloupnosti 3 následující prvočísla
        while not dokonceno:
            if prvocislo(pridavat):
                array.append(pridavat)
                index += 1
            if index == 3:
                dokonceno = True
            pridavat += 1
        return True,array
    return False,[]

# funkce dostává string, hledá mezery a jednotlivá "slova" přidává do řady, kterou vrací
# využíváme ji v následující funkci, kde čteme jednotlivé řádky souboru s posloupnostmi a zpětně z nich vytváříme seznam
def vstup(string):
    rada = []
    temp = ""
    for i in string:
        if i == " ":
            rada.append(int(temp))
            temp = ""
        else:
            temp = temp + i
    return rada

# funkce načítá soubor s posloupnostmi a hledá, zda uživatelem zadaná posloupnost odpovídá začátku některé ze zaznamenaných posloupností
def seznamPosloupnosti(array):
    f = open("seznamPosloupnosti.txt", "r")
    x = ""
    for i in f:
        if i != "\n":
            x = x + i
    f.close()
    temp = ""
    for i in x:
        if i != "\n":
            temp = temp + i
        else:
            rada = vstup(temp)
            skore = 0
            if len(rada) > len(array):
                for i in range(len(array)):
                    if array[i] == rada[i]:
                        skore += 1
                    if skore == len(array):
                        return True,rada
                temp = ""
                skore = 0
    return False,[]

# funkce zkontroluj for-cyklem prochází přes jednotlivé popsané funkce, do parametru jim dává posloupnost uživatele a čeká, až některé vratí True
# v proměnné i pak máme uložené doplněné posloupnosti, které vypisujeme        
def zkontroluj(array):
    ind = 0
    for i in [
            pridaniPosloupnosti(array, sub, add),
            pridaniPosloupnosti(array, truediv, mul), 
            perioda(array), 
            pridani(array,add), 
            pridani(array,mul),
            stridacko(array),
            prvocisla(array),
            seznamPosloupnosti(array)]:
        ind += 1
        if i[0]:
            # výpis posloupnosti
            for r in i[1]:
                print(r, end = " ")
            print()
            return False,[]
    # pokud posloupnost nerozezná, program propadne sem, kde načítá vstup od uživatele
    print("Omlouvám se, tuto posloupnost nejsem schopen rozeznat. Můžeš mi zadat výsledek, příště ji budu znát! Napiš ANO!")
    
    # v závislosti na odpovědi uživatele vrací Bool, toho pak využívá modul run
    UserAnswer = input()
    if UserAnswer == "ANO":
        return True,array
    return False,[]


