import os
from db_savienotajs import izveidot_savienojumu

def test_izveidot_savienojumu():
    assert os.path.exists("konkurss.db") == True
    assert izveidot_savienojumu() == "Kļūda. Datubāze nav atrasta vai bojāta tās struktūra."

test_izveidot_savienojumu()