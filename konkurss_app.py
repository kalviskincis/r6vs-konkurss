import sys
import csv
import zurija
import db_savienotajs as db
from tabulate import tabulate

def izveidot_db():
    pass

def pieslegsanas():
    vards = input("Ievadi lietotājvārdu: ").strip().lower()
    parole = input("Ievadi paroli: ")
    rezultats = zurija.pieslegties(vards, parole)
    return rezultats


def vertet(zurija):
    conn = db.izveidot_savienojumu()
    dalibnieki_vaicajums = """
    SELECT personas.id, vards, uzvards, nosaukums, prieksnesums
    FROM personas 
    INNER JOIN iestades ON personas.iestade = iestades.id 
    INNER JOIN pieteikumi ON personas.id = pieteikumi.dalibnieks    
    WHERE personas.loma = 1;
    """

    dalibnieki_atbilde = conn.execute(dalibnieki_vaicajums)
    dalibnieki = []
    for katrs in dalibnieki_atbilde:
        dalibnieki.append(dict(katrs))

    print(f"Žūrijas pārstāvis: {zurija['vards']} {zurija['uzvards']}")
    for katrs in dalibnieki:
        print(f"Dalībnieks {katrs['vards']} {katrs['uzvards']}, priekšnesums {katrs['prieksnesums']}")
        
        punkti = {
            "punkti1": 0,
            "punkti2": 0,
            "punkti3": 0,
            "punkti4": 0,
            "punkti5": 0
        }

        for kriterijs in punkti:
            ievadits = False
            while not ievadits:
                try:
                    vertiba = int(input(f"Ievadi punktus (0 līdz 10) par {kriterijs}"))
                    if vertiba in range(0, 11):
                        punkti[kriterijs] = vertiba
                        ievadits = True
                    else:
                        print(f"Vērtējumam par {kriterijs} jābūt veselam skaitlim robežās starp 0 un 10.")
                except ValueError:
                    print(f"Vērtējumam par {kriterijs} jābūt veselam skaitlim robežās starp 0 un 10.")

        vertejums = {}
        vertejums["zurijas_parstavis"] = zurija["id"]
        vertejums["dalibnieks"] = katrs["id"]
        vertejums["prieksnesums"] = katrs["prieksnesums"]
        for kriterijs in punkti:
            vertejums[kriterijs] = punkti[kriterijs]

        conn.execute("INSERT INTO konkurss (zurijas_parstavis, dalibnieks, prieksnesums, punkti1, punkti2, punkti3, punkti4, punkti5) VALUES (:zurijas_parstavis, :dalibnieks, :prieksnesums, :punkti1, :punkti2, :punkti3, :punkti4, :punkti5)", vertejums)
        conn.commit()




def rezultati():
    conn = db.izveidot_savienojumu()
    vaicajums = """
    SELECT vards as Vārds, uzvards as Uzvārds, nosaukums as 'Izglītības iestāde', konkurss.prieksnesums as Priekšnesums, SUM(punkti1+punkti2+punkti3+punkti4+punkti5) / CAST(COUNT(zurijas_parstavis) as float) as Punkti
    FROM konkurss
    INNER JOIN personas ON konkurss.dalibnieks = personas.id
    INNER JOIN iestades ON personas.iestade = iestades.id
    INNER JOIN pieteikumi ON personas.id = pieteikumi.dalibnieks 
    GROUP BY uzvards, vards
    ORDER BY punkti DESC
    """
    atbilde = conn.execute(vaicajums).fetchall()
    rezultati = []
    for katrs in atbilde:
        rezultati.append(dict(katrs))
    virsraksti = rezultati[0].keys()

    print(tabulate(rezultati, headers = 'keys', tablefmt="simple"))
    print()

    with open('rezultati.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = virsraksti
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(rezultati)
        print("Rezultāti saglabāti CSV datnē")
        print()




def main():
    piesledzies = False
    drosiba = 0
    while not piesledzies and drosiba < 3:
        zurija = pieslegsanas()
        if not zurija:
            print("Pieslēgšanās dati nepareizi.")
            drosiba += 1
        else:
            piesledzies = True
            while piesledzies:
                print("Izvēlieties darbību:\n1. ievadīt vērtējumus\n2. apskatīt un saglabāt rezultātus\n3. beigt darbu")
                izvele = input("Jūsu izvēle: ").strip()
                print()
                if izvele == "1":
                    vertet(zurija)
                elif izvele == "2":
                    rezultati()
                elif izvele == "3":
                    piesledzies = False
                    sys.exit("Darbs pabeigts.")
                else:
                    print("Neatpazīta izvēle.")
    else:
        sys.exit("Pārsniegts atļauto pieslēgšanās mēģinājumu skaits. Mēģiniet vēlāk.")

if __name__ == '__main__':
    main()