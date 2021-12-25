from core1 import zkontroluj
from operator import add, mul

# funkce se spustí pouze na začátku, stručně popisuje program
def starter():
    print("Zdravím, uživateli! Tento program by ti měl pomoci při řešení jednoduchých matematických úloh, které se často objevují v IQ testech. Tvým úkolem je doplnit číselnou posloupnost tak, aby následující čísla dávala smysl. Tento program ti může značně pomoci. Zadej mu 4 nebo více čísel a posloupnost ti automaticky doplní. Hodně štěstí!")
starter()

# načtení vstupu od uživatele
# v případě, že uživatel chce uložit posloupnost, tak k proměnné vypsat přidáváme již zadanou posloupnost, kterou vypisujeme
# toto zařizuje parametr boolean
def vstup(boolean = False,array = []):
    vypsat = "Zadej posloupnost:" + "\n"
    if boolean:
        for i in array:
            vypsat = vypsat + str(i) + " "
    vstup = input(vypsat)
    string = ""
    posloupnost = []
    # podle mezer rozdělujeme jednotlivá čísla do posloupnosti, pokud se konverze nepodaří, tzn. uživatel zadal špatné číslo, vypíše se špatný vstup
    try: 
        for i in vstup:
            if i == " ":
                posloupnost.append(int(string))
                string = ""
            else:
                string = string + i
        posloupnost.append(int(string))
    except ValueError:
        print("Špatný vstup!")
        return False,[]
    # kontrolujeme, zda uživatel zadal alespoň 4 čísla
    if len(posloupnost) > 3:
        return True,posloupnost
    else:
        print("Špatný vstup!")
        return False,[]

# nekonečným cyklem načítám vstup, který vyhodnocuji funkcí z core1
while True:
    vstupniarray = vstup()
    if vstupniarray[0]:
    # kontroluji, zda byla objevena posloupnost
        pokracovani = zkontroluj(vstupniarray[1])
        if pokracovani[0]:
        # pokud nebyla objevena a uživatel zadal ANO
            pridavanaPosl = vstup(boolean =True, array = vstupniarray[1])
            if pridavanaPosl[0]:
            # kontroluje, zda doplněná posloupnost je ve správném formátu, k první části přidáváme zbytek
                vysl = vstupniarray[1] + pridavanaPosl[1]
                # do souboru zapisujeme na nový řádek novou posloupnost
                f= open("seznamPosloupnosti.txt","a+")
                for i in vysl:
                    f.write(str(i) + " ")
                f.write("\n")
                f.close()
                print("Posloupnost zaznamenána!")


