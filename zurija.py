import hashlib
import db_savienotajs as db

def parbaudit(tabula, lauks, vertiba):
    conn = db.izveidot_savienojumu()
    vaicajums = f"SELECT {lauks} FROM {tabula} WHERE {lauks}=\"{vertiba}\""
    atbilde = conn.execute(vaicajums).fetchone()
    try:
        nekas = len(atbilde[0])
        db.slegt_savienojumu(conn)
        return False

    except TypeError:
        db.slegt_savienojumu(conn)
        return True



def iegut_id(tabula):
    conn = db.izveidot_savienojumu()
    vaicajums = f"SELECT max(id) FROM {tabula}"
    atbilde = conn.execute(vaicajums).fetchone()
    if isinstance(atbilde[0], int):
        nr = atbilde[0] + 1
    else:
        nr = 1
    db.slegt_savienojumu(conn)
    return nr


def izveidot(vards, uzvards, lietotajvards, iestade, parole):
    conn = db.izveidot_savienojumu()

    nav_lietotajs = parbaudit("lietotaji", "lietotajvards", lietotajvards)
    nav_iestade = parbaudit("iestades", "nosaukums", iestade)
    id_iest = iegut_id("iestades")

    if nav_iestade:
        iestade = {"id": id_iest,
                   "nosaukums": iestade,
                   "pasvaldiba": ""}

        conn.execute("INSERT INTO iestades VALUES (:id, :nosaukums, :pasvaldiba)", iestade)
        print("Iestāde pievienota")
    else:
        print(f"Iestāde {iestade} jau ir datubāzē. Netiks pievienota.")

    if nav_lietotajs:
        id_pers = iegut_id("personas")
        id_liet = iegut_id("lietotaji")

        persona = {"id": id_pers,
                   "vards": vards,
                   "uzvards": uzvards,
                   "iestade": id_iest,
                   "loma": 3
                   }

        lietotajs = {
            "id": id_liet,
            "persona": id_pers,
            "lietotajvards": lietotajvards,
            "paroles_hash": parole
        }

        conn.execute("INSERT INTO personas VALUES (:id, :vards, :uzvards, :iestade, :loma)", persona)
        conn.execute("INSERT INTO lietotaji VALUES (:id, :persona, :lietotajvards, :paroles_hash)", lietotajs)

    else:
        print(f"Reģistrēts lietotājs {lietotajvards} jau ir datubāzē. Netiks pievienots.")

    db.slegt_savienojumu(conn)

def pieslegties(lietotajs, parole):
    conn = db.izveidot_savienojumu()
    vaicajums = f"""
    SELECT personas.id, persona, vards, uzvards, lietotajvards, paroles_hash 
    FROM lietotaji 
    INNER JOIN personas on lietotaji.persona = personas.id
    WHERE lietotajvards=\"{lietotajs}\""""

    atbilde = conn.execute(vaicajums).fetchone()
    db.slegt_savienojumu(conn)

    parole_bin = str.encode(parole)
    parole_hash = hashlib.md5(parole_bin)
    parole_md5 = parole_hash.hexdigest()
    if lietotajs == atbilde["lietotajvards"] and parole_md5 == atbilde["paroles_hash"]:
        return atbilde
    else:
        return False

def main():
    vards = input("Žūrijas locekļa vārds").strip().title()
    uzvards = input("Žūrijas locekļa uzvārds").strip().title()
    lietotajvards = input("Žūrijas locekļa lietotājvārds").strip().lower()
    iestade = input("Pārstāvētās iestādes nosaukums")
    parole_txt = input("Lietotāja parole")

    parole_bin = str.encode(parole_txt)
    parole_hash = hashlib.md5(parole_bin)
    parole = parole_hash.hexdigest()

    izveidot(vards, uzvards, lietotajvards, iestade, parole)

if __name__ == '__main__':
    main()


