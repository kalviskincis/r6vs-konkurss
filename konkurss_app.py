import csv
import zurija
import db_savienotajs as db

def izveidot_db():
    pass

def pieslegsanas():
    vards = input("Ievadi lietotājvārdu: ")
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
    # print(dalibnieki)


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
            punkti[kriterijs] = int(input(f"Ievadi punktus par {kriterijs}"))


        vertejums = {}
        vertejums["zurijas_parstavis"] = zurija["id"]
        vertejums["dalibnieks"] = katrs["id"]
        vertejums["prieksnesums"] = katrs["prieksnesums"]
        for kriterijs in punkti:
            vertejums[kriterijs] = punkti[kriterijs]

        conn.execute("INSERT INTO konkurss (zurijas_parstavis, dalibnieks, prieksnesums, punkti1, punkti2, punkti3, punkti4, punkti5) VALUES (:zurijas_parstavis, :dalibnieks, :prieksnesums, :punkti1, :punkti2, :punkti3, :punkti4, :punkti5)", vertejums)
        conn.commit()

        # print(vertejums)
    db.slegt_savienojumu(conn)


def rezultati():
    conn = db.izveidot_savienojumu()
    vaicajums = """
    SELECT vards, uzvards, nosaukums, konkurss.prieksnesums, SUM(punkti1+punkti2+punkti3+punkti4+punkti5) / CAST(COUNT(zurijas_parstavis) as float) as punkti
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
    print(rezultati)
    virsraksti = rezultati[0].keys()
    print(virsraksti)

    with open('rezultati.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = virsraksti
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(rezultati)

# automatizēt pakāpju piešķiršanu, bet tā vispār labi.


def main():
    zurija = pieslegsanas()
    if not zurija:
        print("Pieslēgšanās dati nepareizi.")
    else:
        #vertet(zurija)
        rezultati()

if __name__ == '__main__':
    main()