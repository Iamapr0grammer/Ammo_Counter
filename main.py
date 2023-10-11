import re
import string
import random

dane1 = "Artur.txt"
dane2 = "Brugi.txt"
dane3 = "Lukasz.txt"
dane4 = "Maciek.txt"
dane5 = "Mateusz.txt"
dane6 = "Paulina.txt"



# deklaracja, co to pogrubienie tekstu
def print_bold(text):
    bold_text = f"\033[1m{text}\033[0m"
    print(bold_text)

def pobranie(gracz, informacja, dodatek):

    # dodatek: info, pojedynczy, seria, reload, add, remove

    # początkowe informacje mówiące to, jakiego gracza ekwipunek czytamy:
    print(" ")
    print(gracz)

    # Odczytywanie pliku i zapisywanie jako "zawartość"
    global nowa_zmienna
    with open(gracz, "r") as plik:
        zawartosc = plik.read()  # Odczytaj całą zawartość pliku
        plik.close()

    # Liczenie ile będzie zmiennych poprzez zliczanie znaków "|"
    rozdzielnik = "|"
    licznik_zmiennych = 1
    for i in zawartosc:
        if i == rozdzielnik:
            licznik_zmiennych += 1

    # Tworzenie pomocnyczych zmiennych
    licznik_przypisan = 0
    wszystkie = []
    while licznik_przypisan < licznik_zmiennych:

        # Tworzenie nowych zmiennych dla każdego przedmiotu
        nazwa_zmiennej = f"przedmiot_{licznik_przypisan}"

        do_zrobienia = zawartosc.split("|")

        globals()[nazwa_zmiennej] = do_zrobienia[0 + licznik_przypisan]
        wszystkie.append(globals()[nazwa_zmiennej])
        licznik_przypisan += 1

    # SEKCJA SPECYFICZNIE CO DO WYBORU UŻYTKOWNIKA PONIŻEJ

    # wyświetl wszystko (info) :
    if re.search("info", informacja):
        i = 0
        for x in wszystkie:
            if re.search("obecnie uzywany", wszystkie[0 + i]):
                print_bold(wszystkie[0 + i])
                i += 1
            else:
                print(wszystkie[0 + i])
                i += 1

    # seria:
    if re.search("seria", informacja):
        print("seria")
        i = 0

        # odnalezienie broni, obecnie uzywanej przez gracza
        for x in wszystkie:
            if re.search("obecnie uzywany", wszystkie[0 + i]):

                # wypisz broń, z której strzela gracz:
                print(wszystkie[0 + i])

                # przypisz wartość, ile amunicji posiada maksymalnie magazynek tej broni:
                match = re.search(r"/\s*(\d+)", wszystkie[0 + i])
                amunicja_w_pelnym_magazynku = int(match.group(1))

                # przypisz wartość, ile amunicji posiada obecnie gracz
                match = re.search(r"\s*(\d+)/", wszystkie[0 + i])
                amunicja_dostepna = int(match.group(1))

                # sprawdź, ile amunicji jest wystrzeliwywane w czasie jednej serii:
                match = re.search(r"\s*(\d+)seria", wszystkie[0 + i])
                seria_broni = int(match.group(1))

                if re.search("zaporowa", informacja):
                    seria_broni = seria_broni * 3
                    print("Seria Zaporowa! 3x więcej amunicji!")

                # oddawanie serii:
                if amunicja_dostepna == 0:
                    print("Broń tego gracza posiada 0 pocisków w magazyku, nic nie strzela!")

                if amunicja_dostepna == seria_broni:
                    print("wystrzelona seria, ale na końcu słychać koniec amunicji w magazynku")
                    pozostala_amunicja = amunicja_dostepna - seria_broni
                    with open(gracz, "r") as plik:
                        zmiana_zawartosci = plik.read()
                        plik.close()

                    liczenie = 0

                    # rozłożenie tego tekstu na części pierwsze
                    wszystkie = []
                    while liczenie < licznik_zmiennych:
                        # Tworzenie nowych zmiennych dla każdego przedmiotu
                        nazwa_zmiennej = f"przedmiot_{liczenie}"

                        do_zrobienia = zmiana_zawartosci.split("|")

                        globals()[nazwa_zmiennej] = do_zrobienia[0 + liczenie]
                        wszystkie.append(globals()[nazwa_zmiennej])
                        liczenie += 1

                    # rozbicie tego tekstu na slowa
                    moja_zmieniona = wszystkie[0 + i].split(" ")
                    b = 0
                    wszystkie_zmienione_zmienne = []
                    for liczenie in moja_zmieniona:
                        nowa_zmienna_zmieniona = f"przedmiot_{b}"
                        globals()[nowa_zmienna_zmieniona] = moja_zmieniona[0 + b]
                        wszystkie_zmienione_zmienne.append(globals()[nowa_zmienna_zmieniona])
                        b += 1

                    # znalezienie slowa zawierajacego amunicje i zmiany tego slowa na nowa ilosc amunicji
                    c = 0
                    ostatni_licznik = b * 2
                    for b in wszystkie_zmienione_zmienne:
                        if "/" in b:
                            new_ammo = str(pozostala_amunicja) + "/" + str(amunicja_w_pelnym_magazynku)
                            wszystkie_zmienione_zmienne[0 + c] = new_ammo
                        c += 1

                    # poskladanie w calosc sekcji amunicji
                    finalowa_wersja_amunicji = ""
                    c = 0
                    for ostatni_licznik in wszystkie_zmienione_zmienne:
                        finalowa_wersja_amunicji += wszystkie_zmienione_zmienne[0 + c] + " "
                        c += 1
                    # znajdz, którą część tekstu należy zastąpić
                    f = 0
                    for licznik_przypisan in wszystkie:
                        if re.search("obecnie uzywany", wszystkie[0 + f]):
                            pamietnik = f
                        f += 1

                    # poskladanie w calosc calosci pliku i podmiane czesci z amunicja
                    c = 0
                    calosc = []
                    ostatni = licznik_przypisan
                    for licznik_przypisan in wszystkie:
                        calosc.append(wszystkie[0 + c])
                        c += 1
                    calosc[pamietnik] = finalowa_wersja_amunicji

                    # dodanie rozdzielnikow "|" pomiedzy wyrazy, oraz zamieniemie listy na ciąg tekstu string
                    tekst = ""
                    v = 0
                    for licznik_przypisan in calosc:
                        if v > 0:
                            tekst += "|"
                        tekst += calosc[0 + v]
                        v += 1

                    with open(gracz, "w") as plik:
                        plik.write(tekst)
                        plik.close()

                    # Odczytywanie pliku i zapisywanie jako "zawartość"
                    global nowa_zmienna
                    with open(gracz, "r") as plik:
                        zawartosc = plik.read()  # Odczytaj całą zawartość pliku
                        plik.close()

                if amunicja_dostepna > 0 and amunicja_dostepna < seria_broni:
                    pozostala_amunicja = 0
                    print("Wystrzeliwywujesz tylko ", amunicja_dostepna, " pocisków, zanim skończy Ci się amunicja")
                    with open(gracz, "r") as plik:
                        zmiana_zawartosci = plik.read()
                        plik.close()

                    liczenie = 0

                    # rozłożenie tego tekstu na części pierwsze
                    wszystkie = []
                    while liczenie < licznik_zmiennych:
                        # Tworzenie nowych zmiennych dla każdego przedmiotu
                        nazwa_zmiennej = f"przedmiot_{liczenie}"

                        do_zrobienia = zmiana_zawartosci.split("|")

                        globals()[nazwa_zmiennej] = do_zrobienia[0 + liczenie]
                        wszystkie.append(globals()[nazwa_zmiennej])
                        liczenie += 1

                    # rozbicie tego tekstu na slowa
                    moja_zmieniona = wszystkie[0 + i].split(" ")
                    b = 0
                    wszystkie_zmienione_zmienne = []
                    for liczenie in moja_zmieniona:
                        nowa_zmienna_zmieniona = f"przedmiot_{b}"
                        globals()[nowa_zmienna_zmieniona] = moja_zmieniona[0 + b]
                        wszystkie_zmienione_zmienne.append(globals()[nowa_zmienna_zmieniona])
                        b += 1

                    # znalezienie slowa zawierajacego amunicje i zmiany tego slowa na nowa ilosc amunicji
                    c = 0
                    ostatni_licznik = b * 2
                    for b in wszystkie_zmienione_zmienne:
                        if "/" in b:
                            new_ammo = str(pozostala_amunicja) + "/" + str(amunicja_w_pelnym_magazynku)
                            wszystkie_zmienione_zmienne[0 + c] = new_ammo
                        c += 1

                    # poskladanie w calosc sekcji amunicji
                    finalowa_wersja_amunicji = ""
                    c = 0
                    for ostatni_licznik in wszystkie_zmienione_zmienne:
                        finalowa_wersja_amunicji += wszystkie_zmienione_zmienne[0 + c] + " "
                        c += 1
                    # znajdz, którą część tekstu należy zastąpić
                    f = 0
                    for licznik_przypisan in wszystkie:
                        if re.search("obecnie uzywany", wszystkie[0 + f]):
                            pamietnik = f
                        f += 1

                    # poskladanie w calosc calosci pliku i podmiane czesci z amunicja
                    c = 0
                    calosc = []
                    ostatni = licznik_przypisan
                    for licznik_przypisan in wszystkie:
                        calosc.append(wszystkie[0 + c])
                        c += 1
                    calosc[pamietnik] = finalowa_wersja_amunicji

                    # dodanie rozdzielnikow "|" pomiedzy wyrazy, oraz zamieniemie listy na ciąg tekstu string
                    tekst = ""
                    v = 0
                    for licznik_przypisan in calosc:
                        if v > 0:
                            tekst += "|"
                        tekst += calosc[0 + v]
                        v += 1

                    with open(gracz, "w") as plik:
                        plik.write(tekst)
                        plik.close()

                    # Odczytywanie pliku i zapisywanie jako "zawartość"
                    global nowa_zmienna
                    with open(gracz, "r") as plik:
                        zawartosc = plik.read()  # Odczytaj całą zawartość pliku
                        plik.close()

                if amunicja_dostepna > seria_broni:
                    print("normalna seria, broń ma jeszcze amunicję")
                    pozostala_amunicja = amunicja_dostepna - seria_broni
                    with open(gracz, "r") as plik:
                        zmiana_zawartosci = plik.read()
                        plik.close()

                    liczenie = 0

                    # rozłożenie tego tekstu na części pierwsze
                    wszystkie = []
                    while liczenie < licznik_zmiennych:
                        # Tworzenie nowych zmiennych dla każdego przedmiotu
                        nazwa_zmiennej = f"przedmiot_{liczenie}"

                        do_zrobienia = zmiana_zawartosci.split("|")

                        globals()[nazwa_zmiennej] = do_zrobienia[0 + liczenie]
                        wszystkie.append(globals()[nazwa_zmiennej])
                        liczenie += 1

                    # rozbicie tego tekstu na slowa
                    moja_zmieniona = wszystkie[0 + i].split(" ")
                    b = 0
                    wszystkie_zmienione_zmienne = []
                    for liczenie in moja_zmieniona:
                        nowa_zmienna_zmieniona = f"przedmiot_{b}"
                        globals()[nowa_zmienna_zmieniona] = moja_zmieniona[0 + b]
                        wszystkie_zmienione_zmienne.append(globals()[nowa_zmienna_zmieniona])
                        b += 1

                    # znalezienie slowa zawierajacego amunicje i zmiany tego slowa na nowa ilosc amunicji
                    c = 0
                    ostatni_licznik = b * 2
                    for b in wszystkie_zmienione_zmienne:
                        if "/" in b:
                            new_ammo = str(pozostala_amunicja) + "/" + str(amunicja_w_pelnym_magazynku)
                            wszystkie_zmienione_zmienne[0 + c] = new_ammo
                        c += 1

                    # poskladanie w calosc sekcji amunicji
                    finalowa_wersja_amunicji = ""
                    c = 0
                    for ostatni_licznik in wszystkie_zmienione_zmienne:
                        finalowa_wersja_amunicji += wszystkie_zmienione_zmienne[0 + c] + " "
                        c += 1
                    # znajdz, którą część tekstu należy zastąpić
                    f = 0
                    for licznik_przypisan in wszystkie:
                        if re.search("obecnie uzywany", wszystkie[0 + f]):
                            pamietnik = f
                        f += 1

                    # poskladanie w calosc calosci pliku i podmiane czesci z amunicja
                    c = 0
                    calosc = []
                    ostatni = licznik_przypisan
                    for licznik_przypisan in wszystkie:
                        calosc.append(wszystkie[0 + c])
                        c += 1
                    calosc[pamietnik] = finalowa_wersja_amunicji

                    # dodanie rozdzielnikow "|" pomiedzy wyrazy, oraz zamieniemie listy na ciąg tekstu string
                    tekst = ""
                    v = 0
                    for licznik_przypisan in calosc:
                        if v > 0:
                            tekst += "|"
                        tekst += calosc[0 + v]
                        v += 1

                    with open(gracz, "w") as plik:
                        plik.write(tekst)
                        plik.close()

                    # Odczytywanie pliku i zapisywanie jako "zawartość"
                    global nowa_zmienna
                    with open(gracz, "r") as plik:
                        zawartosc = plik.read()  # Odczytaj całą zawartość pliku
                        plik.close()


            i += 1

    # pojedynczy:
    if re.search("pojedynczy", informacja):
        print("pojedynczy")
        i = 0

        # odnalezienie broni, obecnie uzywanej przez gracza
        for x in wszystkie:
            if re.search("obecnie uzywany", wszystkie[0 + i]):

                # wypisz broń, z której strzela gracz:
                print(wszystkie[0 + i])

                # przypisz wartość, ile amunicji posiada maksymalnie magazynek tej broni:
                match = re.search(r"/\s*(\d+)", wszystkie[0 + i])
                amunicja_w_pelnym_magazynku = int(match.group(1))

                # przypisz wartość, ile amunicji posiada obecnie gracz
                match = re.search(r"\s*(\d+)/", wszystkie[0 + i])
                amunicja_dostepna = int(match.group(1))

                # sprawdź, ile amunicji moze ta bron wystrzelic maksymalnie w trybie pojedynczym:
                match = re.search(r"\s*(\d+)pojedynczy", wszystkie[0 + i])
                pojedynczy_broni = int(match.group(1))

                # sprawdzenie, czy gracz chce wystrzelic mniej pociskow niz okreslony jest pojedynczy:
                if isinstance(dodatek, int):
                    if int(dodatek) < pojedynczy_broni:
                        pojedynczy_broni = dodatek

                # oddawanie serii:
                if amunicja_dostepna == 0:
                    print("Broń tego gracza posiada 0 pocisków w magazyku, nic nie strzela!")

                if amunicja_dostepna == pojedynczy_broni:
                    print("wystrzelone pociski pojedyncze, ale na końcu słychać koniec amunicji w magazynku")
                    pozostala_amunicja = amunicja_dostepna - pojedynczy_broni
                    with open(gracz, "r") as plik:
                        zmiana_zawartosci = plik.read()
                        plik.close()

                    liczenie = 0

                    # rozłożenie tego tekstu na części pierwsze
                    wszystkie = []
                    while liczenie < licznik_zmiennych:
                        # Tworzenie nowych zmiennych dla każdego przedmiotu
                        nazwa_zmiennej = f"przedmiot_{liczenie}"

                        do_zrobienia = zmiana_zawartosci.split("|")

                        globals()[nazwa_zmiennej] = do_zrobienia[0 + liczenie]
                        wszystkie.append(globals()[nazwa_zmiennej])
                        liczenie += 1

                    # rozbicie tego tekstu na slowa
                    moja_zmieniona = wszystkie[0 + i].split(" ")
                    b = 0
                    wszystkie_zmienione_zmienne = []
                    for liczenie in moja_zmieniona:
                        nowa_zmienna_zmieniona = f"przedmiot_{b}"
                        globals()[nowa_zmienna_zmieniona] = moja_zmieniona[0 + b]
                        wszystkie_zmienione_zmienne.append(globals()[nowa_zmienna_zmieniona])
                        b += 1

                    # znalezienie slowa zawierajacego amunicje i zmiany tego slowa na nowa ilosc amunicji
                    c = 0
                    ostatni_licznik = b * 2
                    for b in wszystkie_zmienione_zmienne:
                        if "/" in b:
                            new_ammo = str(pozostala_amunicja) + "/" + str(amunicja_w_pelnym_magazynku)
                            wszystkie_zmienione_zmienne[0 + c] = new_ammo
                        c += 1

                    # poskladanie w calosc sekcji amunicji
                    finalowa_wersja_amunicji = ""
                    c = 0
                    for ostatni_licznik in wszystkie_zmienione_zmienne:
                        finalowa_wersja_amunicji += wszystkie_zmienione_zmienne[0 + c] + " "
                        c += 1
                    # znajdz, którą część tekstu należy zastąpić
                    f = 0
                    for licznik_przypisan in wszystkie:
                        if re.search("obecnie uzywany", wszystkie[0 + f]):
                            pamietnik = f
                        f += 1

                    # poskladanie w calosc calosci pliku i podmiane czesci z amunicja
                    c = 0
                    calosc = []
                    ostatni = licznik_przypisan
                    for licznik_przypisan in wszystkie:
                        calosc.append(wszystkie[0 + c])
                        c += 1
                    calosc[pamietnik] = finalowa_wersja_amunicji

                    # dodanie rozdzielnikow "|" pomiedzy wyrazy, oraz zamieniemie listy na ciąg tekstu string
                    tekst = ""
                    v = 0
                    for licznik_przypisan in calosc:
                        if v > 0:
                            tekst += "|"
                        tekst += calosc[0 + v]
                        v += 1

                    with open(gracz, "w") as plik:
                        plik.write(tekst)
                        plik.close()

                    # Odczytywanie pliku i zapisywanie jako "zawartość"
                    global nowa_zmienna
                    with open(gracz, "r") as plik:
                        zawartosc = plik.read()  # Odczytaj całą zawartość pliku
                        plik.close()

                if amunicja_dostepna > 0 and amunicja_dostepna < pojedynczy_broni:
                    pozostala_amunicja = 0
                    print("Wystrzeliwywujesz tylko ", amunicja_dostepna, " pocisków, zanim skończy Ci się amunicja")
                    with open(gracz, "r") as plik:
                        zmiana_zawartosci = plik.read()
                        plik.close()

                    liczenie = 0

                    # rozłożenie tego tekstu na części pierwsze
                    wszystkie = []
                    while liczenie < licznik_zmiennych:
                        # Tworzenie nowych zmiennych dla każdego przedmiotu
                        nazwa_zmiennej = f"przedmiot_{liczenie}"

                        do_zrobienia = zmiana_zawartosci.split("|")

                        globals()[nazwa_zmiennej] = do_zrobienia[0 + liczenie]
                        wszystkie.append(globals()[nazwa_zmiennej])
                        liczenie += 1

                    # rozbicie tego tekstu na slowa
                    moja_zmieniona = wszystkie[0 + i].split(" ")
                    b = 0
                    wszystkie_zmienione_zmienne = []
                    for liczenie in moja_zmieniona:
                        nowa_zmienna_zmieniona = f"przedmiot_{b}"
                        globals()[nowa_zmienna_zmieniona] = moja_zmieniona[0 + b]
                        wszystkie_zmienione_zmienne.append(globals()[nowa_zmienna_zmieniona])
                        b += 1

                    # znalezienie slowa zawierajacego amunicje i zmiany tego slowa na nowa ilosc amunicji
                    c = 0
                    ostatni_licznik = b * 2
                    for b in wszystkie_zmienione_zmienne:
                        if "/" in b:
                            new_ammo = str(pozostala_amunicja) + "/" + str(amunicja_w_pelnym_magazynku)
                            wszystkie_zmienione_zmienne[0 + c] = new_ammo
                        c += 1

                    # poskladanie w calosc sekcji amunicji
                    finalowa_wersja_amunicji = ""
                    c = 0
                    for ostatni_licznik in wszystkie_zmienione_zmienne:
                        finalowa_wersja_amunicji += wszystkie_zmienione_zmienne[0 + c] + " "
                        c += 1
                    # znajdz, którą część tekstu należy zastąpić
                    f = 0
                    for licznik_przypisan in wszystkie:
                        if re.search("obecnie uzywany", wszystkie[0 + f]):
                            pamietnik = f
                        f += 1

                    # poskladanie w calosc calosci pliku i podmiane czesci z amunicja
                    c = 0
                    calosc = []
                    ostatni = licznik_przypisan
                    for licznik_przypisan in wszystkie:
                        calosc.append(wszystkie[0 + c])
                        c += 1
                    calosc[pamietnik] = finalowa_wersja_amunicji

                    # dodanie rozdzielnikow "|" pomiedzy wyrazy, oraz zamieniemie listy na ciąg tekstu string
                    tekst = ""
                    v = 0
                    for licznik_przypisan in calosc:
                        if v > 0:
                            tekst += "|"
                        tekst += calosc[0 + v]
                        v += 1

                    with open(gracz, "w") as plik:
                        plik.write(tekst)
                        plik.close()

                    # Odczytywanie pliku i zapisywanie jako "zawartość"
                    global nowa_zmienna
                    with open(gracz, "r") as plik:
                        zawartosc = plik.read()  # Odczytaj całą zawartość pliku
                        plik.close()

                if amunicja_dostepna > pojedynczy_broni:
                    print("kilka pojedynczych strzelow, bron ma jeszcze amunicje w magazynku")
                    pozostala_amunicja = amunicja_dostepna - pojedynczy_broni
                    with open(gracz, "r") as plik:
                        zmiana_zawartosci = plik.read()
                        plik.close()

                    liczenie = 0

                    # rozłożenie tego tekstu na części pierwsze
                    wszystkie = []
                    while liczenie < licznik_zmiennych:
                        # Tworzenie nowych zmiennych dla każdego przedmiotu
                        nazwa_zmiennej = f"przedmiot_{liczenie}"

                        do_zrobienia = zmiana_zawartosci.split("|")

                        globals()[nazwa_zmiennej] = do_zrobienia[0 + liczenie]
                        wszystkie.append(globals()[nazwa_zmiennej])
                        liczenie += 1

                    # rozbicie tego tekstu na slowa
                    moja_zmieniona = wszystkie[0 + i].split(" ")
                    b = 0
                    wszystkie_zmienione_zmienne = []
                    for liczenie in moja_zmieniona:
                        nowa_zmienna_zmieniona = f"przedmiot_{b}"
                        globals()[nowa_zmienna_zmieniona] = moja_zmieniona[0 + b]
                        wszystkie_zmienione_zmienne.append(globals()[nowa_zmienna_zmieniona])
                        b += 1

                    # znalezienie slowa zawierajacego amunicje i zmiany tego slowa na nowa ilosc amunicji
                    c = 0
                    ostatni_licznik = b * 2
                    for b in wszystkie_zmienione_zmienne:
                        if "/" in b:
                            new_ammo = str(pozostala_amunicja) + "/" + str(amunicja_w_pelnym_magazynku)
                            wszystkie_zmienione_zmienne[0 + c] = new_ammo
                        c += 1

                    # poskladanie w calosc sekcji amunicji
                    finalowa_wersja_amunicji = ""
                    c = 0
                    for ostatni_licznik in wszystkie_zmienione_zmienne:
                        finalowa_wersja_amunicji += wszystkie_zmienione_zmienne[0 + c] + " "
                        c += 1
                    # znajdz, którą część tekstu należy zastąpić
                    f = 0
                    for licznik_przypisan in wszystkie:
                        if re.search("obecnie uzywany", wszystkie[0 + f]):
                            pamietnik = f
                        f += 1

                    # poskladanie w calosc calosci pliku i podmiane czesci z amunicja
                    c = 0
                    calosc = []
                    ostatni = licznik_przypisan
                    for licznik_przypisan in wszystkie:
                        calosc.append(wszystkie[0 + c])
                        c += 1
                    calosc[pamietnik] = finalowa_wersja_amunicji

                    # dodanie rozdzielnikow "|" pomiedzy wyrazy, oraz zamieniemie listy na ciąg tekstu string
                    tekst = ""
                    v = 0
                    for licznik_przypisan in calosc:
                        if v > 0:
                            tekst += "|"
                        tekst += calosc[0 + v]
                        v += 1

                    with open(gracz, "w") as plik:
                        plik.write(tekst)
                        plik.close()

                    # Odczytywanie pliku i zapisywanie jako "zawartość"
                    global nowa_zmienna
                    with open(gracz, "r") as plik:
                        zawartosc = plik.read()  # Odczytaj całą zawartość pliku
                        plik.close()

            i += 1

    # reload:
    if re.search("reload", informacja):
        print("reload")
        i = 0

        # odnalezienie broni, obecnie uzywanej przez gracza
        for x in wszystkie:
            if re.search("obecnie uzywany", wszystkie[0 + i]):

                # wypisz broń, którą przeładowuje gracz
                print(wszystkie[0 + i])

                # przypisz wartość, jakiego rodzaju amunicji uzywa ta bron
                match = re.search(r"\((.*?)\)amunicja", wszystkie[0 + i])
                uzywana_amunicja = match.group(1)
                print(uzywana_amunicja, " uzywana amunicja")

                # sprawdzenie, ile gracz posiada amunicji w pelnym magaynku
                match = re.search(r"/\s*(\d+)", wszystkie[0 + i])
                amunicja_w_pelnym_magazynku = int(match.group(1))

                # sprawdzenie, ile amunicji posiada obecnie gracz
                match = re.search(r"\s*(\d+)/", wszystkie[0 + i])
                amunicja_dostepna = int(match.group(1))

                # obliczenie różnicy
                brakujaca_amunicja = amunicja_w_pelnym_magazynku - amunicja_dostepna

                # print("brakująca amunicja: ", brakujaca_amunicja)

                pamietnik = i

                # sprawdzenie, czy gracz posiada taka amunicje w ekwipunku
                liczenie = 0
                for x in wszystkie:
                    if re.search(re.escape(uzywana_amunicja), wszystkie[0 + liczenie]):
                            if liczenie != pamietnik:
                                # print("znaleniono amunicje!")
                                # print(uzywana_amunicja)
                                # print(wszystkie[0 + liczenie])

                                # sprawdzenie, czy posiada w ekwipunku amunicje do tego typu broni
                                if re.search(r"(\d+)x", wszystkie[0 + liczenie]) \
                                        and re.search(r"ammo", wszystkie[0 + liczenie]) \
                                        and re.search(re.escape(uzywana_amunicja), wszystkie[0 + liczenie]):

                                    match = re.search(r"(\d+)", wszystkie[0 + liczenie])
                                    ilosc_amunicji = int(match.group(1))
                                    # print(ilosc_amunicji)

                                    pozostala_luzna_amunicja = ilosc_amunicji - amunicja_w_pelnym_magazynku + amunicja_dostepna
                                    # print(ilosc_amunicji)
                                    # print("MOJA AMUNICJA:", wszystkie[0 + liczenie])

                                    ladownik = 0

                                    if pozostala_luzna_amunicja > 0:
                                        print("Wystarczajaca ilosc amunicji na pelne zaladowanie!")
                                        # print(pozostala_luzna_amunicja)
                                        ladownik = 1

                                    if pozostala_luzna_amunicja == 0:
                                        print("Wystarczajaca ilosc amunicji na dokladnie jedno pelne zaladowanie")
                                        # print(pozostala_luzna_amunicja)
                                        ladownik = 2

                                    if ilosc_amunicji > 0 and \
                                            (ilosc_amunicji + amunicja_dostepna) < amunicja_w_pelnym_magazynku:
                                        print("Nie ma wystarczajacej ilosci amunicji na pelne zaladowanie!")
                                        # print(pozostala_luzna_amunicja)
                                        ladownik = 3

                                    if ilosc_amunicji == 0:
                                        print("Nie ma wcale amunicji, żadna kula nie była załadowana")

                                    # print("pozostala amunicja: ", pozostala_luzna_amunicja)
                                    # print("pozostala amunicja: ", ilosc_amunicji + amunicja_dostepna - amunicja_w_pelnym_magazynku)

                                    if ladownik != 0:

                                        # stworzenie pliku, ktory podmieni plik txt, nowy, poprawiony
                                        # print(wszystkie)
                                        # print(licznik_przypisan)
                                        id_amunicji = None
                                        index_amunicji = None
                                        # print("START")
                                        for id_amunicji, item in enumerate(wszystkie):
                                            if uzywana_amunicja in item and "ammo" in item \
                                                    and "obecnie uzywany" not in item:
                                                # print("znaleziono amunicje!", item)
                                                index_amunicji = id_amunicji
                                        # print(index_amunicji, "ID amunicji")
                                        # print(uzywana_amunicja)

                                        id_magazynka = None
                                        index_magazynka = None
                                        for id_amunicji, item in enumerate(wszystkie):
                                            if uzywana_amunicja in item and "obecnie uzywany" in item:
                                                # print("znaleziono amunicje!", item)
                                                index_magazynka = id_amunicji
                                        # print(index_magazynka, "ID amunicji")

                                        # print(index_amunicji, index_magazynka)

                                        tekst_1 = wszystkie[index_amunicji]
                                        tekst_2 = wszystkie[index_magazynka]
                                        # print("TEST: ", tekst_1, tekst_2)

                                        if ladownik == 1 or ladownik == 2:
                                            tekst_1_changed = tekst_1.replace(str(ilosc_amunicji),str(pozostala_luzna_amunicja))
                                            # print(tekst_1_changed, "Po zamianie")

                                        if ladownik == 1 or ladownik == 2:
                                            nowa_amunicja = ""
                                            nowa_amunicja += str(amunicja_w_pelnym_magazynku) + "/" + str(amunicja_w_pelnym_magazynku)
                                            # print(nowa_amunicja)
                                            stara_amunicja = ""
                                            stara_amunicja += str(amunicja_dostepna) + "/" + str(amunicja_w_pelnym_magazynku)
                                            tekst_2_changed = tekst_2.replace(str(stara_amunicja),str(nowa_amunicja))

                                        # print(tekst_1_changed, tekst_2_changed)

                                        # tekst_1_changed = amunicja luźna | tekst_2_changed = amunicja w magazynku

                                        # print(wszystkie)

                                        nowy_wpis = ""
                                        licznik = 0
                                        for x in wszystkie:
                                            if licznik > 0:
                                                nowy_wpis += "|"
                                            if licznik != index_magazynka and licznik != index_amunicji:
                                                nowy_wpis += str(wszystkie[0 + licznik])
                                            if licznik == index_amunicji:
                                                nowy_wpis += str(tekst_1_changed)
                                            if licznik == index_magazynka:
                                                nowy_wpis += str(tekst_2_changed)

                                            licznik += 1

                                        # print(nowy_wpis)

                                        with open(gracz, "w") as plik:
                                            plik.write(nowy_wpis)
                                            plik.close()



                    liczenie += 1
            i += 1

    # zmiana:
    if re.search("zmiana", informacja):
        licznik = 0
        pamietnik_1 = 0
        pamietnik_2 = 0
        nowa_bron = ""

        print("Zmiana broni!")

        for x in wszystkie:
            if re.search(" obecnie uzywany", wszystkie[0 + licznik]):
                stara_bron = re.sub(r" obecnie uzywany", "", wszystkie[0 + licznik])
                print("Poprzedniu używana broń: ", stara_bron)
                pamietnik_1 = licznik
            licznik += 1

        licznik = 0
        for x in wszystkie:
            if re.search(re.escape(dodatek), wszystkie[0 + licznik]):
                nowa_bron = str(wszystkie[0 + licznik]) + " obecnie uzywany"
                pamietnik_2 = licznik
                print("Teraz używana broń: ", nowa_bron)
            licznik += 1

        nowa_zmienna = ""
        licznik = 0
        for x in wszystkie:
            if licznik > 0:
                nowa_zmienna += "|"
            if licznik == pamietnik_1:
                nowa_zmienna += str(stara_bron)
            if licznik == pamietnik_2:
                nowa_zmienna += str(nowa_bron)
            if licznik != pamietnik_1 and licznik != pamietnik_2:
                nowa_zmienna += wszystkie[0 + licznik]
            licznik += 1

        with open(gracz, "w") as plik:
            plik.write(nowa_zmienna)
            plik.close()

    # add:
    if re.search(r"add", informacja):

        nowe = ""
        znaleziono = False

        # sprawdź, czy gracz wpisał x, i jeśli nie wpisał, to samodzielnie dodaj x

        match_without_x = re.search(r"(\d+)", dodatek)
        if not re.search(r"(\d+)x", dodatek):
            bez_zmiany = int(match_without_x.group(1))
            zmiana = str(bez_zmiany) + "x"
            nowe = re.sub(str(bez_zmiany), str(zmiana), dodatek)
            dodatek = nowe


        match = re.search(r"(\d+)x", dodatek)

        ilosc = match.group(1)
        przedmiot = re.sub(r"\d+x ", "", dodatek).strip()
        przedmiot_z_escaped = re.escape(przedmiot)

        print("przedmiot:", przedmiot)
        print("ilosc:", ilosc)
        pamietnik = 0

        # znajdz poszukiwany przedmiot:
        licznik = 0
        for x in wszystkie:
            nowa_zmienna = ""
            pamietnik = ""
            nowa_liczba = ""

            if re.search(przedmiot_z_escaped, wszystkie[0 + licznik]):
                pamietnik = licznik
                znaleziono = True

                match = re.search(r"(\d+)x", wszystkie[0 + licznik])
                match_without_x = re.search(r"(\d+)", wszystkie[0 + licznik])

                if match:
                    extracted_number = int(match.group(1))
                    changed_number = int(extracted_number) + int(ilosc)
                    nowa_liczba = re.sub(str(extracted_number), str(changed_number), wszystkie[0 + licznik])


                liczenie = 0
                for x in wszystkie:
                    if liczenie > 0:
                        nowa_zmienna += "|"
                    if liczenie == pamietnik:
                        nowa_zmienna += str(nowa_liczba)
                    if liczenie != pamietnik:
                        nowa_zmienna += wszystkie[0 + liczenie]
                    liczenie += 1


                with open(gracz, "w") as plik:
                    plik.write(nowa_zmienna)
                    plik.close()

            licznik += 1

        # jeśli nie znajdziesz tego przedmiotu, to go stwórz:
        if not re.search(przedmiot_z_escaped, wszystkie[-1 + licznik]) and licznik == licznik_przypisan \
                and znaleziono == False:
            print("nie znaleziono przedmiotu! zostanie utworzony nowy!")
            nowy_przedmiot = str(ilosc) + "x " + str(przedmiot)
            wszystkie.append(nowy_przedmiot)
            zmiennik = 0

            for x in wszystkie:
                if zmiennik > 0:
                    nowa_zmienna += "|"
                nowa_zmienna += str(wszystkie[0 + zmiennik])
                zmiennik += 1

            with open(gracz, "w") as plik:
                plik.write(nowa_zmienna)
                plik.close()

    # remove:
    if re.search(r"remove", informacja):

        nowe = ""
        znaleziono = False

        # sprawdź, czy gracz wpisał x, i jeśli nie wpisał, to samodzielnie dodaj x

        match_without_x = re.search(r"(\d+)", dodatek)
        if not re.search(r"(\d+)x", dodatek):
            bez_zmiany = int(match_without_x.group(1))
            zmiana = str(bez_zmiany) + "x"
            nowe = re.sub(str(bez_zmiany), str(zmiana), dodatek)
            dodatek = nowe

        match = re.search(r"(\d+)x", dodatek)

        ilosc = match.group(1)
        przedmiot = re.sub(r"\d+x ", "", dodatek).strip()
        przedmiot_z_escaped = re.escape(przedmiot)

        print("przedmiot:", przedmiot)
        print("ilosc:", ilosc)
        pamietnik = 0

        # znajdz poszukiwany przedmiot:
        licznik = 0
        for x in wszystkie:
            nowa_zmienna = ""
            pamietnik = ""
            nowa_liczba = ""

            if re.search(przedmiot_z_escaped, wszystkie[0 + licznik]):
                pamietnik = licznik
                znaleziono = True

                match = re.search(r"(\d+)x", wszystkie[0 + licznik])
                match_without_x = re.search(r"(\d+)", wszystkie[0 + licznik])

                if match:
                    extracted_number = int(match.group(1))
                    changed_number = int(extracted_number) - int(ilosc)
                    nowa_liczba = re.sub(str(extracted_number), str(changed_number), wszystkie[0 + licznik])
                    print(nowa_liczba)


                liczenie = 0
                for x in wszystkie:
                    if liczenie > 0:
                        nowa_zmienna += "|"
                    if liczenie == pamietnik:
                        nowa_zmienna += str(nowa_liczba)
                    if liczenie != pamietnik:
                        nowa_zmienna += wszystkie[0 + liczenie]
                    liczenie += 1

                print(nowa_zmienna)

                with open(gracz, "w") as plik:
                    plik.write(nowa_zmienna)
                    plik.close()

            licznik += 1

        # jeśli nie znajdziesz tego przedmiotu, to poiformuj o tym użytkownika:
        if not re.search(przedmiot_z_escaped, wszystkie[-1 + licznik]) and licznik == licznik_przypisan and \
                znaleziono == False:
            print("nie znaleziono Przedmiotu!")

    #time:
    if re.search(r"time", informacja):

        licznik = 0
        czas_koncowy = 0
        biological_time = None
        biological_time_index = None
        game_time = None
        game_time_index = None
        planetary_time = None
        planetary_time_index = None
        generator_power = None
        generator_index = None
        nowe_glod = None
        blokada_czasu = 0
        blokada_zywienia = 0

        for x in wszystkie:

            # ogólny, czas gry
            if re.search(r"game time", wszystkie[0 + licznik]):



                # rozbij na liczby pierwsze czas podyktowany przez gracza

                sekundy_game_time = 0
                dodawane_sekundy = 0

                # znajdź lata
                if re.search(r"(\d+)\s?lat", informacja):
                    match = re.search(r"(\d+)\s?lat", informacja)
                    extracted_years = int(match.group(1))
                    dodawane_sekundy += extracted_years * 31104000

                # znajdź miesiace
                if re.search(r"(\d+)\s?miesi", informacja):  # miesiące dodwane
                    match = re.search(r"(\d+)\s?miesi", informacja)
                    extracted_months = int(match.group(1))
                    dodawane_sekundy += extracted_months * 2592000

                # znajdź dni
                if re.search(r"(\d+)\s?dni", informacja):  # dni dodawane
                    match = re.search(r"(\d+)\s?dni", informacja)
                    extracted_days = int(match.group(1))
                    dodawane_sekundy += extracted_days * 86400

                # znajdź godziny
                if re.search(r"(\d+)\s?godzin", informacja):  # godziny dodawane
                    match = re.search(r"(\d+)\s?godzin", informacja)
                    extracted_hours = int(match.group(1))
                    dodawane_sekundy += extracted_hours * 3600

                # znajdź minuty
                if re.search(r"(\d+)\s?minut", informacja):  # minuty dodwane
                    match = re.search(r"(\d+)\s?minut", informacja)
                    extracted_minutes = int(match.group(1))
                    dodawane_sekundy += extracted_minutes * 60

                # znajdź sekundy
                if re.search(r"(\d+)\s?sekund", informacja):  # sekundy dodwane
                    match = re.search(r"(\d+)\s?sekund", informacja)
                    extracted_seconds = int(match.group(1))
                    dodawane_sekundy += extracted_seconds




                # następnie rozbij na części pierwsze czas, który już jest zapisany w pliku txt

                # znajdź lata
                if re.search(r"(\d+)\s?lat", wszystkie[0 + licznik]):
                    match = re.search(r"(\d+)\s?lat", wszystkie[0 + licznik])
                    extracted_years = int(match.group(1))
                    sekundy_game_time += extracted_years * 31104000

                # znajdź miesiace
                if re.search(r"(\d+)\s?miesiecy", wszystkie[0 + licznik]):  # miesiące dodwane
                    match = re.search(r"(\d+)\s?miesiecy", wszystkie[0 + licznik])
                    extracted_months = int(match.group(1))
                    sekundy_game_time += extracted_months * 2592000

                # znajdź dni
                if re.search(r"(\d+)\s?dni", wszystkie[0 + licznik]):  # dni dodawane
                    match = re.search(r"(\d+)\s?dni", wszystkie[0 + licznik])
                    extracted_days = int(match.group(1))
                    sekundy_game_time += extracted_days * 86400

                # znajdź godziny
                if re.search(r"(\d+)\s?godzin", wszystkie[0 + licznik]):  # godziny dodawane
                    match = re.search(r"(\d+)\s?godzin", wszystkie[0 + licznik])
                    extracted_hours = int(match.group(1))
                    sekundy_game_time += extracted_hours * 3600

                # znajdź minuty
                if re.search(r"(\d+)\s?minut", wszystkie[0 + licznik]):  # minuty dodwane
                    match = re.search(r"(\d+)\s?minut", wszystkie[0 + licznik])
                    extracted_minutes = int(match.group(1))
                    sekundy_game_time += extracted_minutes * 60

                # znajdź sekundy
                if re.search(r"(\d+)\s?sekund", wszystkie[0 + licznik]):  # sekundy dodwane
                    match = re.search(r"(\d+)\s?sekund", wszystkie[0 + licznik])
                    extracted_seconds = int(match.group(1))
                    sekundy_game_time += extracted_seconds

                # print(sekundy_game_time, "game time")
                # print(dodawane_sekundy, "dodawane sekundy")

                czas_koncowy = 0

                # wykonaj działania matematyczne
                if re.search(r"\+", informacja):
                    # print("chcesz bym dodał time")
                    czas_koncowy = sekundy_game_time + dodawane_sekundy

                if re.search(r"-", informacja):
                    # print("chcesz bym odjął time")
                    czas_koncowy = sekundy_game_time - dodawane_sekundy

                # print(czas_koncowy)

                # poskładaj te sekundy w godziny, dni, miesiące a może nawet lata
                lata_w_sekundach = 31536000
                miesiace_w_sekundach = 2592000
                dni_w_sekundach = 86400
                godziny_w_sekundach = 3600
                minuty_w_sekundach = 60

                lata = czas_koncowy // lata_w_sekundach
                czas_koncowy %= lata_w_sekundach

                miesiace = czas_koncowy // miesiace_w_sekundach
                czas_koncowy %= miesiace_w_sekundach

                dni = czas_koncowy // dni_w_sekundach
                czas_koncowy %= dni_w_sekundach

                godziny = czas_koncowy // godziny_w_sekundach
                czas_koncowy %= godziny_w_sekundach

                minuty = czas_koncowy // minuty_w_sekundach
                czas_koncowy %= minuty_w_sekundach

                # print(lata,miesiace,dni,godziny,minuty,czas_koncowy)

                nowy_game_time = str(lata) + "Lat " + str(miesiace) + "miesiecy " + str(dni) + "dni "
                nowy_game_time += str(godziny) + "godzin " + str(minuty) + "minut " + str(czas_koncowy)
                nowy_game_time +=  "sekund " + " game time"
                # print(nowy_game_time)
                game_time = nowy_game_time
                game_time_index = licznik


                # popraw czas planetarny!
                licznik_czasu_planetarnego = 0
                for x in wszystkie:
                    if re.search(r"planetary time", wszystkie[0 + licznik_czasu_planetarnego]):

                        cykl_godzinowy = None
                        licznik_cyklu = 0
                        planetary_time_index = licznik_czasu_planetarnego

                        for x in wszystkie:
                            if re.search(r"planetary cycle", wszystkie[0 + licznik_cyklu]):
                                match = re.search("(\d+)h", wszystkie[0 + licznik_cyklu])
                                cykl_godzinowy = int(match.group(1))

                            licznik_cyklu += 1

                        match = re.search(r"(\d+)h", wszystkie[0 + licznik_czasu_planetarnego])
                        obecne_godziny = int(match.group(1))

                        match = re.search(r"(\d+)min", wszystkie[0 + licznik_czasu_planetarnego])
                        obecne_minuty = int(match.group(1))

                        godziny_w_sekundach = 3600
                        minuty_w_sekundach = 60

                        sekundy_czasowe = dodawane_sekundy

                        godziny_czasowe = dodawane_sekundy // godziny_w_sekundach
                        sekundy_czasowe %= godziny_w_sekundach

                        minuty_czasowe = dodawane_sekundy // minuty_w_sekundach
                        sekundy_czasowe %= minuty_w_sekundach

                        czas_godziny = obecne_godziny + godziny_czasowe
                        czas_minuty = minuty_czasowe + obecne_minuty

                        if czas_minuty >= 60:
                            reszta_czas_godziny = czas_minuty // minuty_w_sekundach
                            czas_minuty %= minuty_w_sekundach
                            czas_godziny += reszta_czas_godziny

                        if czas_godziny >= cykl_godzinowy:
                            czas_godziny %= cykl_godzinowy

                        dopiska = None

                        if czas_godziny > 15 and czas_godziny < 41:
                            dopiska = " Dzień"
                        else:
                            dopiska = " Noc"

                        time = None

                        if czas_minuty >= 10:
                            time = str(czas_godziny) + ":" + str(czas_minuty) + dopiska

                        if czas_minuty < 10:
                            time = str(czas_godziny) + ":0" + str(czas_minuty) + dopiska

                        planetary_time = str(czas_godziny) + "h " + str(czas_minuty) + "min planetary time"
                        if blokada_czasu == 0:
                            print(time)
                            blokada_czasu = 1

                    licznik_czasu_planetarnego += 1

                # popraw generator graczy!
                generator_licznik = 0
                for x in wszystkie:
                    if re.search("generator", wszystkie[generator_licznik]):
                        if re.search("aktywny", wszystkie[generator_licznik]):

                            # print(wszystkie[0 + generator_licznik])
                            generator_index = generator_licznik
                            # print(dodawane_sekundy)

                            pattern = r'\((\d+)\)pozostalo'
                            match = re.search(pattern, wszystkie[generator_licznik])
                            liczba_pozostale = 0
                            if match:
                                liczba_pozostale = int(match.group(1))
                                # print("Wyciągnięta liczba:", liczba_pozostale)

                            pattern = r'\((\d+)\)pelny'
                            match = re.search(pattern, wszystkie[generator_licznik])
                            liczba_max = 0
                            if match:
                                liczba_max = int(match.group(1))
                                # print("Wyciągnięta liczba:", liczba_max)

                            pattern = r'\((\d+)\)%'
                            match = re.search(pattern, wszystkie[generator_licznik])
                            liczba_procent = 0
                            if match:
                                liczba_procent = int(match.group(1))
                                # print("Wyciągnięta liczba:", liczba_procent)

                            if liczba_pozostale > 0:
                                nowa_liczba_generatora = ((liczba_pozostale * 60) - dodawane_sekundy) // 60
                                procent_pozostale = (nowa_liczba_generatora / liczba_max) * 100
                                # print("Pozostało:", procent_pozostale, "%")
                                # print(nowa_liczba_generatora)
                                liczba_procent_zaokraglona = round(procent_pozostale)
                                nowa_liczba_generatora_zaokraglona = round(nowa_liczba_generatora)

                                generator_power_0 = re.sub(str(liczba_procent), str(liczba_procent_zaokraglona),
                                                           wszystkie[0 + generator_licznik])
                                generator_power = re.sub(str(liczba_pozostale), str(nowa_liczba_generatora_zaokraglona),
                                                         generator_power_0)
                                # print(generator_power)
                            else:
                                generator_power = re.sub("aktywny", "dezaktywowany",
                                                           wszystkie[0 + generator_licznik])



                    generator_licznik += 1








                # popraw czas w zegarku biologicznym
                biological = 0
                for x in wszystkie:
                    if re.search("biological", wszystkie[0 + biological]):
                        # print("biologial time!!!!!!!!!!!!!!!")
                        # print(wszystkie[0 + biological])

                        # Szukamy ilości godzin i minut w tekście za pomocą wyrażeń regularnych

                        # poskładaj te sekundy w liczby, przynajmniej na ten czas
                        lata_w_sekundach = 31536000
                        miesiace_w_sekundach = 2592000
                        dni_w_sekundach = 86400
                        godziny_w_sekundach = 3600
                        minuty_w_sekundach = 60

                        lata = dodawane_sekundy // lata_w_sekundach
                        dodawane_sekundy %= lata_w_sekundach

                        miesiace = dodawane_sekundy // miesiace_w_sekundach
                        dodawane_sekundy %= miesiace_w_sekundach

                        dni = dodawane_sekundy // dni_w_sekundach
                        dodawane_sekundy %= dni_w_sekundach

                        godziny = dodawane_sekundy // godziny_w_sekundach
                        dodawane_sekundy %= godziny_w_sekundach

                        minuty = dodawane_sekundy // minuty_w_sekundach
                        dodawane_sekundy %= minuty_w_sekundach


                        ilosc_godzin = 0
                        ilosc_minut = 0

                        if re.search(r"(\d+)godziny", wszystkie[0 + biological]):
                            match = re.search(r"(\d+)godziny", wszystkie[0 + biological])
                            ilosc_godzin = int(match.group(1))

                        if re.search(r"(\d+)minuty", wszystkie[0 + biological]):
                            match = re.search(r"(\d+)minuty", wszystkie[0 + biological])
                            ilosc_minut = int(match.group(1))

                        # print(ilosc_godzin)
                        # print(ilosc_minut)
                        # print(lata, miesiace, dni, godziny, ilosc_godzin, ilosc_minut)

                        zmienna_minut_biologicznych = minuty + ilosc_minut
                        godziny_do_dodania = zmienna_minut_biologicznych // 60
                        reszta_minut = zmienna_minut_biologicznych % 60

                        zmienna_godzin_biologicznych = (lata * 8760) + (miesiace * 720) + (dni * 24) + (godziny) + ilosc_godzin + godziny_do_dodania
                        Liczba_minionych_dob_ziemskich = zmienna_godzin_biologicznych // 24
                        reszta = zmienna_godzin_biologicznych % 24
                        # print(zmienna_godzin_biologicznych)

                        # jeśli minął przynajmniej jeden cykl doby ziemskiej, to wyświetl tą wiadomość
                        if Liczba_minionych_dob_ziemskich > 0 and blokada_zywienia == 0:
                            print("Totalna liczba cyklów żywieniowych: ", Liczba_minionych_dob_ziemskich)

                        # print("Pozostałe godziny: ", reszta, "h", "pozostałe minuty: ", reszta_minut)

                        nowa_biologiczna = str(reszta) + "godziny " + str(reszta_minut) + "minuty biological time"
                        # print(nowa_biologiczna)
                        biological_time = nowa_biologiczna
                        biological_time_index = biological

                        # zmiana danych biologicznych u gracza:
                        index = 0
                        nowa_zmienna_biologiczna = ""
                        for x in wszystkie:
                            if index > 0:
                                nowa_zmienna_biologiczna += "|"
                            if index != biological:
                                nowa_zmienna_biologiczna += str(wszystkie[0 + index])
                            if index == biological:
                                nowa_zmienna_biologiczna += str(nowa_biologiczna)
                            index += 1

                        #zmiana wody u gracza:
                        index = 0
                        pragnienie = Liczba_minionych_dob_ziemskich
                        licznik_pragnienia = 0
                        nowa_zmienna_pragnienia = None
                        index_wody = None
                        index_pragnienia = None
                        nowa_woda = None
                        nowe_pragnienie = None
                        for x in wszystkie:
                            if re.search(r"(\.*?)woda", wszystkie[0 + index]):
                                # print(wszystkie[0 + index])
                                re.search(r"(\d+)x", wszystkie[0 + index])
                                match = re.search(r"(\d+)x", wszystkie[0 + index])
                                ilosc_wody = int(match.group(1))
                                index_wody = index


                                # gracz nie posiada wystarczającej wody:
                                if Liczba_minionych_dob_ziemskich > ilosc_wody and blokada_zywienia == 0:
                                    print("Dla gracza",gracz ," brakuje tyle wody: ", Liczba_minionych_dob_ziemskich - ilosc_wody)

                                    # dodaj graczowi pragnienie
                                    pragnienie = Liczba_minionych_dob_ziemskich - ilosc_wody
                                    wczesniejsze_pragnienie = None
                                    licznik_pragnienia = 0
                                    pamietnik = None
                                    for x in wszystkie:
                                        if re.search("pragnienie", wszystkie[0 + licznik_pragnienia]):
                                            match = re.search(r"(\d+)x", wszystkie[0 + licznik_pragnienia])
                                            wczesniejsze_pragnienie = int(match.group(1))
                                            wartosc = int(pragnienie) + int(wczesniejsze_pragnienie)
                                            # print("Pragnienie: ", pragnienie, wczesniejsze_pragnienie)
                                            nowe_pragnienie = re.sub(r'(\d+)', str(wartosc), wszystkie[0 + licznik_pragnienia])
                                            index_pragnienia = licznik_pragnienia
                                        licznik_pragnienia += 1


                                # gracz posiada wystarczającą wodę
                                if Liczba_minionych_dob_ziemskich <= ilosc_wody and Liczba_minionych_dob_ziemskich > 0 and blokada_zywienia == 0:
                                    print("Gracz", gracz, "wypił ", Liczba_minionych_dob_ziemskich, " sztuk", wszystkie[0 + index])



                                # odejmij graczowi wode
                                pozostala_woda = ilosc_wody - Liczba_minionych_dob_ziemskich
                                if pozostala_woda < 0:
                                    pozostala_woda = 0
                                nowa_woda = re.sub(r'(\d+)', str(pozostala_woda), wszystkie[0 + index])
                                # print(nowa_woda, "zmieniona wartość!")
                                if pragnienie >= 1 and pozostala_woda > 0:
                                    pozostala_woda -= 1
                                    pragnienie = int(pragnienie) - 1
                                    nowe_pragnienie = re.sub(r'(\d+)', str(pragnienie), str(nowe_pragnienie))
                                    # print(nowe_pragnienie, "nowe pragnienie?")

                            index += 1




                        #zmiana jedzenia u gracza:
                        index = 0
                        glod = Liczba_minionych_dob_ziemskich
                        licznik_glodu = 0

                        for x in wszystkie:
                            if re.search(r"(\.*?)jedzenie", wszystkie[0 + index]):
                                # print(wszystkie[0 + index])
                                re.search(r"(\d+)x", wszystkie[0 + index])
                                match = re.search(r"(\d+)x", wszystkie[0 + index])
                                ilosc_jedzenia = int(match.group(1))
                                nowe_jedzenie = None
                                pamietnik = None


                                # gracz nie posiada wystarczającej wody:
                                if Liczba_minionych_dob_ziemskich > ilosc_jedzenia and blokada_zywienia == 0:
                                    print("Dla gracza",gracz," brakuje tyle jedzenia: ", Liczba_minionych_dob_ziemskich - ilosc_jedzenia)

                                    # dodaj graczowi glod
                                    glod = Liczba_minionych_dob_ziemskich - ilosc_jedzenia
                                    wczesniejszy_glod = None
                                    licznik_glodu = 0
                                    for x in wszystkie:
                                        if re.search("glod", wszystkie[0 + licznik_glodu]):
                                            match = re.search(r"(\d+)x", wszystkie[0 + licznik_glodu])
                                            wczesniejszy_glod = int(match.group(1))
                                            wartosc = int(glod) + int(wczesniejszy_glod)
                                            nowe_glod = re.sub(r'(\d+)', str(wartosc), wszystkie[0 + licznik_glodu])
                                            pamietnik = licznik_glodu
                                            print(nowe_glod)
                                        licznik_glodu += 1


                                # gracz posiada wystarczającą ilosc jedzenia
                                if Liczba_minionych_dob_ziemskich <= ilosc_jedzenia and Liczba_minionych_dob_ziemskich > 0 and blokada_zywienia == 0:
                                    print("Gracz", gracz, "zjadł ", Liczba_minionych_dob_ziemskich, " sztuk", wszystkie[0 + index])

                                blokada_zywienia = 1

                                # odejmij graczowi jedzenie
                                pozostale_jedzenie = ilosc_jedzenia - Liczba_minionych_dob_ziemskich
                                if pozostale_jedzenie < 0:
                                    pozostale_jedzenie = 0
                                nowe_jedzenie = re.sub(r'(\d+)', str(pozostale_jedzenie), wszystkie[0 + index])
                                # print(nowe_jedzenie, "zmieniona wartość!")
                                if glod >= 1 and pozostale_jedzenie > 0:
                                    pozostale_jedzenie -= 1
                                    nowe_glod = re.sub(r'(\d+)', str(glod - 1), str(nowe_jedzenie))
                                    # print(nowe_jedzenie, "nowe jedzenie?")

                                liczenie_jedzenia = 0
                                nowa_zmienna_jedzenia = ""
                                # print(licznik_glodu)
                                # print(glod)

                                for x in wszystkie:
                                    if liczenie_jedzenia > 0:
                                        nowa_zmienna_jedzenia += "|"
                                    if liczenie_jedzenia != index and liczenie_jedzenia != pamietnik \
                                            and liczenie_jedzenia != index_wody and liczenie_jedzenia \
                                            != biological_time_index and liczenie_jedzenia != game_time_index \
                                            and liczenie_jedzenia != index_pragnienia \
                                            and liczenie_jedzenia != planetary_time_index \
                                            and liczenie_jedzenia != generator_index:
                                        nowa_zmienna_jedzenia += str(wszystkie[0 + liczenie_jedzenia])
                                    if liczenie_jedzenia == index:
                                        nowa_zmienna_jedzenia += str(nowe_jedzenie)
                                    if liczenie_jedzenia == pamietnik:
                                        nowa_zmienna_jedzenia += str(nowe_glod)
                                    if liczenie_jedzenia == index_pragnienia:
                                        nowa_zmienna_jedzenia += str(nowe_pragnienie)
                                    if liczenie_jedzenia == index_wody:
                                        nowa_zmienna_jedzenia += str(nowa_woda)
                                    if liczenie_jedzenia == biological_time_index:
                                        nowa_zmienna_jedzenia += str(biological_time)
                                    if liczenie_jedzenia == game_time_index:
                                        nowa_zmienna_jedzenia += str(game_time)
                                    if liczenie_jedzenia == planetary_time_index:
                                        nowa_zmienna_jedzenia += str(planetary_time)
                                    if liczenie_jedzenia == generator_index:
                                        nowa_zmienna_jedzenia += str(generator_power)
                                    liczenie_jedzenia += 1

                                with open(gracz, "w") as plik:
                                    plik.write(nowa_zmienna_jedzenia)
                                    plik.close()


                            index += 1

                    biological += 1


            licznik += 1

    #drive:
    if re.search(r"drive", informacja):
        licznik_pojazdu = 0
        obecne_paliwo = None
        index_paliwa = None
        maksymalne_paliwo = None
        zuzycie_paliwa = None
        predkosc_maksymalna = None
        metrowy_dystans = None

        # pobierz dane pojazdu
        for x in wszystkie:

            if re.search(r"obecnie paliwa w litrach", wszystkie[0 + licznik_pojazdu]):
                if re.search(r"(\d+\.\d+)x", wszystkie[licznik_pojazdu]):
                    match = re.search(r"(\d+\.\d+)x", wszystkie[licznik_pojazdu])
                else:
                    match = re.search(r"(\d+)x", wszystkie[0 + licznik_pojazdu])
                obecne_paliwo = float(match.group(1))
                index_paliwa = licznik_pojazdu

            if re.search(r"litrow maksymalnie", wszystkie[0 + licznik_pojazdu]):
                match = re.search(r"(\d+)", wszystkie[0 + licznik_pojazdu])
                maksymalne_paliwo = int(match.group(1))

            if re.search(r"zuzycie ml paliwa", wszystkie[0 + licznik_pojazdu]):
                match = re.search(r"(\d+\.\d+)", wszystkie[0 + licznik_pojazdu])
                zuzycie_paliwa = float(match.group(1))

            if re.search(r"predkosc", wszystkie[0 + licznik_pojazdu]):
                match = re.search(r"(\d+)km", wszystkie[0 + licznik_pojazdu])
                predkosc_maksymalna = int(match.group(1))

            licznik_pojazdu += 1

        # oblicz i podaj czas podróży w przypadku kilometrów drogi
        if re.search("(\d+)km",informacja):
            match = re.search(r"(\d+)", informacja)
            dystans = int(match.group(1))
            metrowy_dystans = dystans * 1000
            czas = dystans / predkosc_maksymalna
            if czas > 0 and czas < 1:
                odpowiedz = czas * 60
                print(gracz," dojedze tam za: ", int(odpowiedz), " minut przy maksymalnej prędkości")

                czasownik = czas * 2
                odpowiedz = czasownik * 60
                print(gracz," dojedze tam za: ", int(odpowiedz), " minut przy komfortowej prędkości")


            if czas > 1:
                godziny_odpowiedz = czas // 1
                czas %= 1
                odpowiedz_minute = czas * 100
                print(gracz," dojedze tam za: ",int(godziny_odpowiedz)," godzin oraz ", int(odpowiedz_minute),
                      " minut przy maksymalnej prędkości")

                czasownik = czas * 2
                godziny_odpowiedz = czasownik // 1
                czasownik %= 1
                odpowiedz_minute = czasownik * 100
                print(gracz, " dojedze tam za: ", int(godziny_odpowiedz * 2), " godzin oraz ", int(odpowiedz_minute * 2)
                      ," minut przy komfortowej prędkości")

        # oblicz i podaj czas podróży w przypadku metrów drogi
        if re.search("(\d+)m",informacja):
            match = re.search(r"(\d+)", informacja)
            dystans = int(match.group(1))
            metrowy_dystans = dystans
            czas = (dystans / 1000) / predkosc_maksymalna
            if czas > 0 and czas < 1:
                odpowiedz = czas * 60
                print(gracz," dojedze tam za: ", int(odpowiedz), " minut przy maksymalnej prędkości")

                czasownik = czas * 2
                odpowiedz = czasownik * 60
                print(gracz, " dojedze tam za: ", int(odpowiedz), " minut przy komfortowej prędkości")


            if czas > 1:
                godziny_odpowiedz = czas // 1
                czas %= 1
                odpowiedz_minute = czas * 100
                print(gracz," dojedze tam za: ",int(godziny_odpowiedz)," godzin oraz ", int(odpowiedz_minute),
                      " minut przy maksymalnej prędkości")

                godziny_odpowiedz = czas // 1
                czasownik = czas * 2
                czasownik %= 1
                odpowiedz_minute = czasownik * 100
                print(gracz, " dojedze tam za: ", int(godziny_odpowiedz), " godzin oraz ", int(odpowiedz_minute)
                      , " minut przy komfortowej prędkości")


        # oblicz zużyte paliwo
        print(float(metrowy_dystans))
        print((float(zuzycie_paliwa)))
        if zuzycie_paliwa >= 1:
            zuzyte_paliwo = (float(metrowy_dystans) / 1000) / float(zuzycie_paliwa)
        if zuzycie_paliwa < 1:
            zuzyte_paliwo = (float(metrowy_dystans) / 1000) * float(zuzycie_paliwa)

        print("Metrowy dystans:", metrowy_dystans)

        # jeśli gracz nie ma wystarczającej ilości paliwa, to powiedz Mu to:
        print(obecne_paliwo)
        print(zuzyte_paliwo)
        if float(zuzyte_paliwo) > float(obecne_paliwo):
            if zuzycie_paliwa >= 1:
                pozostale = obecne_paliwo * zuzycie_paliwa
            if zuzycie_paliwa < 1:
                pozostale = obecne_paliwo / zuzycie_paliwa
            odpowiedz_paliwa = round(pozostale, 3)
            print("NIE MA PALIWA! Starczy tylko, by przejechać: ",float(odpowiedz_paliwa)," kilometrów")

        else:

            paliwo_po_odjeciu = float(obecne_paliwo) - float(zuzyte_paliwo)
            # print(paliwo_po_odjeciu, "paliwo po odjeciu")
            zaokraglone_paliwo_po_odjeciu = round(paliwo_po_odjeciu, 2)
            nowe_paliwo = str(zaokraglone_paliwo_po_odjeciu) + "x" + " obecnie paliwa w litrach" \
                          + " (" + str(maksymalne_paliwo) + ")maksymalnie"
            # print(nowe_paliwo)

            licznik_przypisan_paliwa = 0
            nowy_wpis_paliwa = ""
            for x in wszystkie:
                if licznik_przypisan_paliwa > 0:
                    nowy_wpis_paliwa += "|"
                if licznik_przypisan_paliwa == index_paliwa:
                    nowy_wpis_paliwa += str(nowe_paliwo)
                if licznik_przypisan_paliwa != index_paliwa:
                    nowy_wpis_paliwa += str(wszystkie[0 + licznik_przypisan_paliwa])
                licznik_przypisan_paliwa += 1

            print(nowy_wpis_paliwa)

            with open(gracz, "w") as plik:
                plik.write(nowy_wpis_paliwa)
                plik.close()



    # końcowe oddzielenie informacji od innego gracza
    print(" ")
    print("--------------------------------------------------------------------------------------------------------")



informacja = "nic"

while informacja != "exit":

    dane_gracza = "nic"
    dane = "nic"
    dodatek = "nic"
    blaze = "cc-4 blaze.txt"
    renegade = "cc-5 renegade.txt"

    informacja = input("Jakie polecenie?: ")

    # sprawdzanie, czy była wpisana nazwa, odwołująca się do konkretnego gracza
    if re.search("artur", informacja):
        dane_gracza = "artur"
        dane = dane1
    if re.search("brugi", informacja):
        dane_gracza = "brugi"
        dane = dane2
    if re.search("lukasz", informacja):
        dane_gracza = "lukasz"
        dane = dane3
    if re.search("maciek", informacja):
        dane_gracza = "maciek"
        dane = dane4
    if re.search("mateusz", informacja):
        dane_gracza = "mateusz"
        dane = dane5
    if re.search("paulina", informacja):
        dane_gracza = "paulina"
        dane = dane6
    if re.search("blaze", informacja):
        dane_gracza = "Blaze"
        dane = blaze
    if re.search("renegade", informacja) or re.search("basia", informacja):
        dane_gracza = "Renegade"
        dane = renegade

    # sprawdzenie, czy użytkownik wpisał określoną komendę
    if re.search("pojedynczy", informacja):
        if re.search("(\d+)", informacja):
            match = re.search(r"(\d+)", informacja)
            dodatek = int(match.group(1))
        pobranie(dane, informacja, dodatek)

    if re.search("seria", informacja):
        pobranie(dane, informacja, dodatek)

    if re.search("reload", informacja):
        pobranie(dane, informacja, dodatek)

    if re.search("zmiana", informacja):
        gun = re.sub(r"zmiana", "", informacja)
        gun = re.sub(re.escape(str(dane_gracza)), "", gun)
        dodatek = gun.strip()
        print(dodatek)
        pobranie(dane, informacja, dodatek)

    if re.search("add", informacja):
        item = re.sub(r"add", "", informacja)
        item = re.sub(re.escape(str(dane_gracza)), "", item)
        dodatek = item.strip()
        print(dodatek)
        pobranie(dane, informacja, dodatek)

    if re.search("remove", informacja):
        item = re.sub(r"remove", "", informacja)
        item = re.sub(re.escape(str(dane_gracza)), "", item)
        dodatek = item.strip()
        print(dodatek)
        pobranie(dane, informacja, dodatek)

    if re.search("info", informacja) and dane_gracza != "nic":
        pobranie(dane, informacja, dodatek)


    if re.search("info", informacja) and dane_gracza == "nic":
        pobranie(dane1, informacja, dodatek)
        pobranie(dane2, informacja, dodatek)
        pobranie(dane3, informacja, dodatek)
        pobranie(dane4, informacja, dodatek)
        pobranie(dane5, informacja, dodatek)
        pobranie(dane6, informacja, dodatek)

    if re.search("time", informacja):
        if dane == "nic":
            pobranie(dane1, informacja, dodatek)
            pobranie(dane2, informacja, dodatek)
            pobranie(dane3, informacja, dodatek)
            pobranie(dane4, informacja, dodatek)
            pobranie(dane5, informacja, dodatek)
            pobranie(dane6, informacja, dodatek)
        if dane != "nic":
            pobranie(dane, informacja, dodatek)

    if informacja == "move":
        print(" ")

    if re.search("drive", informacja):
        if re.search("all", informacja):
            pobranie(blaze, informacja, dodatek)
            pobranie(renegade, informacja, dodatek)
        if re.search("blaze", informacja):
            pobranie(blaze, informacja, dodatek)
        if re.search("renegade", informacja) or re.search("basia", informacja):
            pobranie(renegade, informacja, dodatek)

    if informacja == "rest":
        print(" ")




    if informacja == "help":
        print(" ")
        print("oto lista wszystko możliwych komend:")
        print("help - by wyświetlić listę wszystkich dostępnych komend")
        print("info - by wyświetlić ekwipunek wszystkich graczy i pojazdów")
        print("info (nazwa gracza) - by wyświetlić ekwipunek tylko tego gracza")
        print("exit - by wyjść z tego programu ")
        print("miesi dni godzin minut sekund")

