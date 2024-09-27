from pickle import FALSE

from zurija import parbaudit, iegut_id, pieslegties


def test_parbaudit():
    assert parbaudit("lietotaji", "lietotajvards", "kalvis") == False
    assert parbaudit("lietotaji", "lietotajvards", "ojars") == True
    assert parbaudit("foo", "bar", "johnsmith") == True
    assert parbaudit("iestades", "nosaukums", "Rīgas 6. vidusskola") == False
    assert parbaudit("iestades", "nosaukums", "Rīgas Biznesa skola") == True
    assert parbaudit("iestades", "fasades_krasa", "dzeltena") == True

def test_iegut_id():
    assert iegut_id("iestades", "nosaukums", "Rīgas 6. vidusskola") == 3
    assert iegut_id("iestades", "nosaukums", "Rīgas Biznesa skola") == -1
    assert iegut_id("iestades", "full_name", "Rīgas Biznesa skola") == -1

def test_pieslegties():
    assert pieslegties("hakeris", "00000000") == False

test_parbaudit()
test_iegut_id()
test_pieslegties()