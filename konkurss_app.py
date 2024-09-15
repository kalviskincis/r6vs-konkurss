import sys
import zurija

def izveidot_db():
    pass

def pieslegsanas():
    vards = input("Ievadi lietotājvārdu: ")
    parole = input("Ievadi paroli: ")
    rezultats = zurija.pieslegties(vards, parole)
    return rezultats

def vertet(zurija):
    pass
    # pieslēgties pie personu DB un atlasīt dalībniekus
    # pieslēgties pie konkursa db
    # izveidot vārdnīcas struktūru
    # nodrošināt vārdnīcas ievadi

def rezultati():
    pass
    # pieslēgties pie konkursa
    # aprēķināt un savilkt rezultātus vārdnīcā
    # "smuki" parādīt


def main():
    zurija = pieslegsanas()
    if not zurija:
        print("Pieslēgšanās dati nepareizi.")
    else:
        vertet(zurija)

if __name__ == '__main__':
    main()