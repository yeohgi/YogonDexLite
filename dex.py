import sqlite3
import os
import csv
import re
import dask
dask.config.set({'dataframe.query-planning': True})
import dask.dataframe as dd
import typeMatrix as pk

class dex:
    
    format = ''

    # constructor
    def __init__(self, format):
        self.setFormat(format)

    def query_pokemon(self, pokemon):

        #pokemon number + rank in format + usage in current format
        number = self.dexFetch('pokemon', pokemon, 'Number')
        rank = self.dexFetch('basic', pokemon, 'Rank')
        usage = self.dexFetch('basic', pokemon, 'Usage')
        print(f"{pokemon.title()} | Number: {number} Rank: {rank} Usage %: {usage}")
       
        #pokemon type(s)
        type1 = self.dexFetch('pokemon', pokemon, 'Type1').upper()
        type2 = self.dexFetch('pokemon', pokemon, 'Type2').upper()
        print(f"Type: {type1} {type2}")

        #type matchup defensive
        
        #abilities + descs (ordered by usage)
        print('Abilities: ')

        abilities = self.dexFetch('moveset', pokemon, 'Abilities').split(';')
        abilitiesAndUsages = [ability.split(' ') for ability in abilities]

        for ability in abilitiesAndUsages:

            abilityName = ''

            for part in ability[:-1]:
                abilityName += ' ' + part
            abilityName = abilityName.strip(' ')

            desc = self.ablFetch(abilityName)

            print(f"    {ability[-1]} {abilityName} : {desc}")

        #base stats + common spreads
        print('Stats: ')

        stats = []
        stats.append(self.dexFetch('pokemon', pokemon, 'HP').upper())
        stats.append(self.dexFetch('pokemon', pokemon, 'ATK').upper())
        stats.append(self.dexFetch('pokemon', pokemon, 'DEF').upper())
        stats.append(self.dexFetch('pokemon', pokemon, 'SPATK').upper())
        stats.append(self.dexFetch('pokemon', pokemon, 'SPDEF').upper())
        stats.append(self.dexFetch('pokemon', pokemon, 'SPD').upper())

        spreads = self.dexFetch('moveset', pokemon, 'Spreads').upper().split(';')

        for index, stat in enumerate(stats):
            print('    ' + pk.stats[index] + ': ' + stat)

        print('Spreads: ')
        
        for spread in spreads:
            spreadSplit = spread.split(' ')
            if (float(spreadSplit[-1]) > 20.00):
                print('    ' + spreadSplit[-1] + ' ' + spreadSplit[0])

        #moves sorted by usage
        print('Moves: ')
        moves = self.dexFetch('moveset', pokemon, 'Moves').split(';')
        movesAndUsages = [move.split(' ') for move in moves]

        for move in movesAndUsages:

            moveName = ''

            for part in move[:-1]:
                moveName += ' ' + part
            moveName = moveName.strip(' ')

            desc = self.moveFetch(moveName)

            if (float(move[-1]) > 20.00):
                if(moveName == 'Other'):
                    print(f"    {move[-1]} {'Other'}")
                else:
                    if(desc is not None and len(desc) != 0):
                        desc = desc.strip('"')
                        print(f"    {move[-1]} {moveName} : {desc}")
                    else:
                        print(f"    {move[-1]} {moveName} : {'No Effect'}")
                
        #commonly held items + item desc
        print('Items: ')
        items = self.dexFetch('moveset', pokemon, 'Items').split(';')
        itemsAndUsages = [item.split(' ') for item in items]

        for item in itemsAndUsages:

            itemName = ''

            for part in item[:-1]:
                itemName += ' ' + part
            itemName = itemName.strip(' ').strip('"')

            desc = self.itemFetch(itemName)

            if (float(item[-1]) > 12.00):
                if(itemName == 'Other'):
                    print(f"    {item[-1]} {'Other'}")
                else:
                    if(desc is not None and len(desc) != 0):
                        desc = desc.strip('"')
                        print(f"    {item[-1]} {itemName} : {desc}")

        #common teammates + potenial synergys 
        print('Teammates: ')
        teammates = self.dexFetch('moveset', pokemon, 'Teammates').split(';')
        teammatesAndUsages = [teammate.split(' ') for teammate in teammates]

        for teammate in teammatesAndUsages:

            teammateName = ''

            for part in teammate[:-1]:
                teammateName += ' ' + part
            teammateName = teammateName.strip(' ').strip('"')

            desc = self.itemFetch(teammateName)

            if float(teammate[-1]) > 20:
                if(teammateName == 'Other'):
                    print(f"    {teammate[-1]} {'Other'}")
                else:
                    print(f"    {teammate[-1]} {teammateName}")
    
        #possible defensive tera types
    
    def dexFetch(self, table, pokemon, column):

        table = table.lower()

        pokemon = pokemon.title()

        column = column.capitalize()

        if os.path.exists(table + '.db'):

            conn = sqlite3.connect(table + '.db')
            cursor = conn.cursor()

            if ' ' in pokemon or '-' in pokemon:

                tryNames = []

                tryNames.append(pokemon.replace(' ','-'))
                tryNames.append(pokemon.replace('-',' '))

                for name in tryNames:
                    if(self.columnExists(table, "Year") and self.columnExists(table, "Month")):
                        sqlCommand = f"SELECT {column} FROM {table} WHERE Pokemon == '{name}' AND Format == '{self.format}' ORDER BY Year DESC, Month DESC LIMIT 1"
                    else:
                        sqlCommand = f"SELECT {column} FROM {table} WHERE Pokemon == '{name}'"
                    cursor.execute(sqlCommand)
                    rows = cursor.fetchall()
                    if(len(rows) != 0):
                        return str(rows[-1]).strip('(').strip(')').strip(',').strip("'")
                
                return None

            else:
                if(self.columnExists(table, "Year") and self.columnExists(table, "Month")):
                    sqlCommand = f"SELECT {column} FROM {table} WHERE Pokemon == '{pokemon}' AND Format == '{self.format}' ORDER BY Year DESC, Month DESC LIMIT 1"
                else:
                    sqlCommand = f"SELECT {column} FROM {table} WHERE Pokemon == '{pokemon}'"
                cursor.execute(sqlCommand)
                rows = cursor.fetchall()
                if(len(rows) != 0):
                    return str(rows[-1]).strip('(').strip(')').strip(',').strip("'")
                else:
                    return None
        
        else:
            print("TABLE DNE")
            return None
        
    def ablFetch(self, ability):

        db = 'abilities.db'

        if os.path.exists(db):

            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            sqlCommand = f"SELECT Desc FROM abilities WHERE Ability == '{ability}'"

            cursor.execute(sqlCommand)

            rows = cursor.fetchall()
            
            if(len(rows) != 0):
                return str(rows[-1]).strip('(').strip(')').strip(',').strip("'")
            else:
                return None
        
        else:
            print("TABLE DNE")
            return None
        
    def moveFetch(self, move):

        db = 'moves.db'

        if os.path.exists(db):

            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            sqlCommand = f"SELECT Effect FROM moves WHERE Move == '{move}'"

            cursor.execute(sqlCommand)

            rows = cursor.fetchall()
            
            if(len(rows) != 0):
                return str(rows[-1]).strip('(').strip(')').strip(',').strip("'")
            else:
                return None
        
        else:
            print("TABLE DNE")
            return None
        
    def itemFetch(self, item):

        db = 'items.db'

        if os.path.exists(db):

            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            sqlCommand = f'SELECT Desc FROM items WHERE Item == "{item}"'

            cursor.execute(sqlCommand)

            rows = cursor.fetchall()
            
            if(len(rows) != 0):
                return str(rows[-1]).strip('(').strip(')').strip(',').strip("'")
            else:
                return None
        
        else:
            print("TABLE DNE")
            return None
        
    def teraGuess(self, pokemon):
        
        db = 'pokemon.db'

        if os.path.exists(db):

            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            sqlCommand = f"SELECT Type1, Type2 FROM pokemon WHERE Pokemon == '{pokemon}'"

            cursor.execute(sqlCommand)

            rows = cursor.fetchall()

            for row in rows:
                print(row)

    def getFormat(self):
        return self.format
    
    def setFormat(self, format):
        self.format = format

    def columnExists(self, table, columnName):
        if os.path.exists(table + '.db'):
            conn = sqlite3.connect(table + '.db')
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info('{}')".format(table))
            columns = cursor.fetchall()
            conn.close()
            for column in columns:
                if column[1].lower() == columnName.lower():
                    return True
            return False

        else:
            return False
        
    def pokemonExist(self, pokemon):

        db = 'pokemon.db'

        pokemon = pokemon.title()

        tryNames = []           
        if '-' in pokemon or ' ' in pokemon:
            tryNames.append(pokemon.replace(' ','-'))
            tryNames.append(pokemon.replace('-',' '))
        else:
            tryNames.append(pokemon)

        if os.path.exists(db):

            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            for name in tryNames:
                sqlCommand = f"SELECT Pokemon FROM pokemon WHERE Pokemon == '{name}'"

                cursor.execute(sqlCommand)

                rows = cursor.fetchall()

                if len(rows) == 1:
                    return True
            
            return False

    # tostring
    def __repr__(self):
        return str(self.format)