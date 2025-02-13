import sqlite3
conn = sqlite3.connect('mokykla.db')
c = conn.cursor()

c.execute(
    '''
    CREATE TABLE IF NOT EXISTS mokiniai (
                vardas TEXT,
                pavarde TEXT,
                idnumber INTEGER,
                klase TEXT,
                vidurkis INTEGER)
    '''
)
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS mokytojai (
                vardas TEXT,
                pavarde TEXT,
                idnumber INTEGER,
                dalykas TEXT)
    '''
)
conn.commit()
# 5
def registratorius(func):
    def apvalkalas(*args, **kwargs):
        try:
            print(f'Vykdoma operacija: {func.__name__}')
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            print(f'Klaida: {e}')
    return apvalkalas
# 2
class Asmuo:
    def __init__(self, vardas, pavarde, idnumber):
        self.vardas = vardas
        self.pavarde = pavarde
        self.idnumber = idnumber

class Mokinys(Asmuo):
    def __init__(self, vardas, pavarde, idnumber, klase, vidurkis):
        super().__init__(vardas, pavarde, idnumber)
        self.klase = klase
        self.vidurkis = vidurkis

class Mokytojas(Asmuo):
    def __init__(self, vardas, pavarde, idnumber, dalykas):
        super().__init__(vardas, pavarde, idnumber)
        self.dalykas = dalykas
# 3
@registratorius
def prideti_mokini(vardas, pavarde, idnumber, klase, vidurkis):
    try:
        if not isinstance(idnumber, int):
            print(f'Klaida: idnumber turi buti integer')
            return
        if 1<=vidurkis<=10:
            with sqlite3.connect('mokykla.db') as conn:
                c = conn.cursor()
                c.execute('INSERT INTO mokiniai (vardas, pavarde, idnumber, klase, vidurkis) VALUES (?,?,?,?,?)',(vardas, pavarde, idnumber, klase, vidurkis))
        else:
            print (f'Klaida pridedant{vardas, pavarde, idnumber}, Vidurkis yra tarp 1 ir 10')
    except Exception as e:
        print(f'Klaida: {e}')

@registratorius
def prideti_mokytoja(vardas, pavarde, idnumber, dalykas):
    try:
        if not isinstance(idnumber, int):
            print(f'Klaida: idnumber turi buti integer')
            return
        with sqlite3.connect('mokykla.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO mokytojai (vardas, pavarde, idnumber, dalykas) VALUES (?,?,?,?)',(vardas, pavarde, idnumber, dalykas))
    except Exception as e:
        print(f'Klaida: {e}')
@registratorius
def gauti_mokinius():
    try:
        with sqlite3.connect('mokykla.db') as conn:
            c = conn.cursor()
            for row in c.execute('SELECT * FROM mokiniai'):
                print(row)
    except Exception as e:
        print(f'Klaida: {e}')
@registratorius
def gauti_mokytojus():
    try:
        with sqlite3.connect('mokykla.db') as conn:
            c = conn.cursor()
            for row in c.execute('SELECT * FROM mokytojai'):
                print(row)
    except Exception as e:
        print(f'Klaida: {e}')
@registratorius
def gauti_mokiniu_vardus():
    try:
        with sqlite3.connect('mokykla.db') as conn:
            c = conn.cursor()
            for row in c.execute('SELECT vardas FROM mokiniai'):
                print(row)
    except Exception as e:
        print(f'Klaida: {e}')
@registratorius
def gauti_mokini_pagal_klase(klase):
    try:
        with sqlite3.connect('mokykla.db') as conn:
            c = conn.cursor()
            for row in c.execute('SELECT * FROM mokiniai WHERE klase = ?',(klase,)):
                print(row)
    except Exception as e:
        print(f'Klaida: {e}')
@registratorius
def keisti_klase (klase, idnumber):
    try:
        if not isinstance(idnumber, int):
            print(f'Klaida: idnumber turi buti integer')
            return
        with sqlite3.connect('mokykla.db') as coon:
            c = conn.cursor()
            c.execute('UPDATE mokiniai SET klase = ? WHERE idnumber = ?',(klase, idnumber,))
            conn.commit()
    except Exception as e:
        print(f'Klaida: {e}')
@registratorius
def salinti_mokini_pagal_id(idnumber):
    try:
        if not isinstance(idnumber, int):
            print(f'Klaida: idnumber turi buti integer')
            return
        with sqlite3.connect('mokykla.db') as conn:
            c = conn.cursor()
            c.execute('DELETE FROM mokiniai WHERE idnumber = ?', (idnumber,))
            conn.commit()
    except Exception as e:
        print(f'Klaida: {e}')
# 4
class MokiniaiIterator:
    def __init__(self):
        self.conn = sqlite3.connect('mokykla.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM mokiniai")
        self.mokiniai = self.cursor.fetchall()

    def __iter__(self):
        for mokinys_data in self.mokiniai:
            yield Mokinys(*mokinys_data)
        self.conn.close()

# prideti_mokini('Edgaras','L',124,'9B',10)
# prideti_mokytoja('Dariuš','D',777,'Python')
# gauti_mokiniu_vardus()
# gauti_mokinius()
# gauti_mokytojus()
# keisti_klase('5B', 123)
# salinti_mokini_pagal_id(123)
mokiniai_iter = MokiniaiIterator()
for savybe in mokiniai_iter:
    print(savybe.vardas, savybe.pavarde, savybe.idnumber, savybe.klase, savybe.vidurkis)
conn.close()
