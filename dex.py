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

    def printStatBar(self, stat):
        bar = ''
        for i in range(0,stat//5):
            bar += '|'
        return bar
    
    def explainSpreads(self):
        print("Effort Value Spreads AKA EV Spreads allow players to invest 508 EVs into any of a Pokemons stats with each stat allowing for a maximum of 252 EVs.")
        print("EVs make all the difference, Pokemon interactions can completely change based on what stats are invested into.")
        print("For example, Pokemon who are invested into offensively may be able to threaten OHKOs previously unattainable.")
        print("Or Pokemon who are invested into defensively may be able to just barely survive attacks that would previously knock them out, allowing for another turns worth of value.")

    def printTypeChart(self):

        print("                                                                                          Attacking ▼ Defending ►")

        print("          ", end='')
        for i, typei in enumerate(pk.types):
            print(f"{pk.types[i]:>10}", end='')
        print("")

        for i, typei in enumerate(pk.types):
            print("          ", end='')
            for j in range(0,len(pk.types) * 10 + 1):
                if j%10 == 0:
                    print(f"\033[1m|\033[0m", end='')
                else:
                    print(f"\033[1m-\033[0m", end='')
            print("")

            print(f"{pk.types[i]:>10}", end='')

            for j in range(0,len(pk.types) * 10 + 1):
                if j%10 == 0:
                    print(f"\033[1m|\033[0m", end='')
                elif j%10 - 5 == 0:

                    typej = j//10

                    if pk.immunityMatrix[i][typej] == 1:
                        print(f"\033[1m\033[35m0\033[0m", end='')
                        print(f"\033[37m", end='')
                    elif pk.universeMatrix[i][typej] == 1:
                        print(f"\033[1m\033[32m2\033[0m", end='')
                        print(f"\033[37m", end='')
                    elif pk.universeMatrix[i][typej] == 0:
                        print(f"1", end='')
                    else:
                        print(f"\033[1m\033[31m½\033[0m", end='')
                        print(f"\033[37m", end='')
                else:
                    print(f" ", end='')
            print("")
        
        print("          ", end='')
        for j in range(0,len(pk.types) * 10 + 1):
            if j%10 == 0:
                print(f"\033[1m|\033[0m", end='')
            else:
                print(f"\033[1m-\033[0m", end='')
        print("")
        
    def my_pokemon(self, pokemon):
        print(f"{pokemon.title()}")

        type1 = self.dexFetch('pokemon', pokemon, 'Type1').upper()
        type2 = self.dexFetch('pokemon', pokemon, 'Type2').upper()

        self.slashStrong(type1, type2)

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
        self.slashWeak(type1, type2)
        
        #abilities + descs (ordered by usage)
        print('Most Used Abilities: ')

        abilities = self.dexFetch('moveset', pokemon, 'Abilities').split(';')
        abilitiesAndUsages = [ability.split(' ') for ability in abilities]

        for ability in abilitiesAndUsages:

            abilityName = ''

            for part in ability[:-1]:
                abilityName += ' ' + part
            abilityName = abilityName.strip(' ')

            desc = self.ablFetch(abilityName)

            print(f"    {ability[-1]:>10}% {abilityName} : {desc}")

        #base stats + common spreads
        print('Pokemons Base Stats: ')

        stats = []
        stats.append(self.dexFetch('pokemon', pokemon, 'HP').upper())
        stats.append(self.dexFetch('pokemon', pokemon, 'ATK').upper())
        stats.append(self.dexFetch('pokemon', pokemon, 'DEF').upper())
        stats.append(self.dexFetch('pokemon', pokemon, 'SPATK').upper())
        stats.append(self.dexFetch('pokemon', pokemon, 'SPDEF').upper())
        stats.append(self.dexFetch('pokemon', pokemon, 'SPD').upper())

        spreads = self.dexFetch('moveset', pokemon, 'Spreads').upper().split(';')

        for index, stat in enumerate(stats):
            bar = self.printStatBar(int(stat))
            print(f"{pk.stats[index]:>10}: {stat:>5}", end=bar + '\n')

        print("Most Used Spreads(For more info on EV Spreads '!EV'): ")
        
        for spread in spreads:
            spreadSplit = spread.split(' ')
            if (float(spreadSplit[-1]) > 20.00):
                print(f"    {spreadSplit[-1]}%   {spreadSplit[0]}")

        #moves sorted by usage
        print('Most Used Moves: ')
        moves = self.dexFetch('moveset', pokemon, 'Moves').split(';')
        movesAndUsages = [move.split(' ') for move in moves]

        for move in movesAndUsages:

            moveName = ''

            for part in move[:-1]:
                moveName += ' ' + part
            moveName = moveName.strip(' ')

            desc = self.moveFetch(moveName)

            if str(desc[0]) != 'Other':
                # print(1,desc, len(desc)) #1,effect, 2,type, 3,power, 4,cat
                for i, row in enumerate(desc):
                    if row is None or len(str(row)) == 0:
                        desc[i] = '-'

            if (float(move[-1]) > 20.00):
                if(moveName == 'Other'):
                    print(f"    {move[-1]}% {'Other'}")
                else:
                    if(desc is not None and len(desc) != 0 and desc[0] != 'Other'):
                        print(f"    {move[-1]:>10}% {moveName:>20}      Type: {desc[1]:>10}     Power: {desc[2]:>5}        Category: {desc[3]:>10}     Description: {desc[0]}")
                    else:
                        print(f"    {move[-1]:>10}% Other")
                
        #commonly held items + item desc
        print('Most Used Items: ')
        items = self.dexFetch('moveset', pokemon, 'Items').split(';')
        itemsAndUsages = [item.split(' ') for item in items]

        for item in itemsAndUsages:

            itemName = ''

            for part in item[:-1]:
                itemName += ' ' + part
            itemName = itemName.strip(' ').strip('"')

            desc = self.itemFetch(itemName)

            item[-1] = item[-1].strip('"')

            if (float(item[-1]) > 12.00):
                if(itemName == 'Other'):
                    print(f"    {item[-1]}% {'Other'}")
                else:
                    if(desc is not None and len(desc) != 0):
                        desc = desc.strip('"')
                        print(f"    {item[-1]}% {itemName} : {desc}")

        #common teammates + potenial synergys 
        print('Most Common Teammates: ')
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
                    print(f"    {teammate[-1]}% {'Other'}")
                else:
                    print(f"    {teammate[-1]}% {teammateName}")
    
        #possible defensive tera types
        self.teraGuess(type1, type2)
    
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

            sqlCommand = f"SELECT Effect, Type, Power, Category FROM moves WHERE Move == '{move}'"

            cursor.execute(sqlCommand)

            rows = cursor.fetchall()

            final = []

            if rows is not None and len(rows) != 0:
                for row in rows[0]:
                    if rows is None:
                        final.append('-')
                    else:
                        final.append(row)
            
            if(len(final) != 0):
                return final
            else:
                return ['Other']
        
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
        
    def teraGuess(self, type1, type2):

        pass

        t1 = -1
        t2 = -1

        for i, type in enumerate(pk.types):
            if type.lower() == type1.lower():
                t1 = i
            if type.lower() == type2.lower():
                t2 = i

        if t2 == -1:

            typeScore = []
            weaknesses = []

            for i, typei in enumerate(pk.universeMatrix):

                if pk.immunityMatrix[i][t1] == 1:
                    #do nothing we dont need to worry about an immunity
                    pass
                elif pk.universeMatrix[i][t1] == 1:
                    #if we are weak let us consider a defenseive tera
                    weaknesses.append(i)

            # print(weaknesses)
            # for i in weaknesses:
            #     print(pk.types[i])

            for i, typei in enumerate(pk.universeMatrix):
                typeScore.append(0) 
                for j in weaknesses:
                    if pk.immunityMatrix[j][i] == 1:
                        typeScore[i] = -16
                        break
                    else:
                        typeScore[i] += pk.universeMatrix[j][i]

            # print(typeScore)
            for i, type in enumerate(typeScore):
                typeScore[i] = (typeScore[i], pk.types[i])

            typeScore = sorted(typeScore, key=lambda x: x[0], reverse=False)
            # print(typeScore)

            print("Guessed Defensive Tera Types: ")
            for type in typeScore:
                if type[0] >= 0:
                    break
                elif type[0] == -16:
                    print(f"    {type[1]:>10}:      Grants an immunity to a 2x super effective weakness")
                else:
                    print(f"    {type[1]:>10}:      Provides a net {abs(type[0])} resistances to previously threating types")
                        
        else:

            typeScore = []
            weaknesses = []

            for i, typei in enumerate(pk.universeMatrix):

                if pk.immunityMatrix[i][t1] == 1 or pk.immunityMatrix[i][t2] == 1:
                    pass
                elif pk.universeMatrix[i][t1] + pk.universeMatrix[i][t2] == 2:
                    weaknesses.append((i, 2))
                elif pk.universeMatrix[i][t1] + pk.universeMatrix[i][t2] == 1:
                    weaknesses.append((i, 1))

            # print(weaknesses)

            for i, typei in enumerate(pk.universeMatrix):
                typeScore.append(0) 
                for j in weaknesses:
                    if pk.immunityMatrix[j[0]][i] == 1 and j[1] == 2:
                        typeScore[i] = -32
                        break
                    elif pk.immunityMatrix[j[0]][i] == 1:   
                        typeScore[i] = -16
                        break
                    elif j[1] == 2:
                        typeScore[i] += 2 * pk.universeMatrix[j[0]][i]
                    else:
                        typeScore[i] += pk.universeMatrix[j[0]][i]

            # print(typeScore)

            for i, type in enumerate(typeScore):
                typeScore[i] = (typeScore[i], pk.types[i])

            typeScore = sorted(typeScore, key=lambda x: x[0], reverse=False)
            # print(typeScore)

            print("Guessed Defensive Tera Types: ")
            for type in typeScore:
                if type[0] >= 0:
                    break
                elif type[0] == -32:
                    print(f"    {type[1]:>10}:      Grants an immunity to a 4x super effective weakness")
                elif type[0] == -16:
                    print(f"    {type[1]:>10}:      Grants an immunity to a 2x super effective weakness")
                else:
                    print(f"    {type[1]:>10}:      Provides a net {abs(type[0])} resistances to previously threating types (Dual type calculations factor in 4x weaknesses)")

                

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
        
    def slashWeak(self, type1, type2):

        t1 = -1
        t2 = -1

        immunities = []
        weaknessesx4 = []
        weaknesses = []
        neutral = []
        resistances = []
        resistancesx4 = []

        for i, type in enumerate(pk.types):
            if type.lower() == type1.lower():
                t1 = i
            if type.lower() == type2.lower():
                t2 = i

        if t2 == -1:

            for i, typei in enumerate(pk.universeMatrix):

                if pk.immunityMatrix[i][t1] == 1:
                    immunities.append(pk.types[i])
                elif pk.universeMatrix[i][t1] == 1:
                    weaknesses.append(pk.types[i])
                elif pk.universeMatrix[i][t1] == 0:
                    neutral.append(pk.types[i])
                elif pk.universeMatrix[i][t1] == -1:
                    resistances.append(pk.types[i])

        else:

            for i, typei in enumerate(pk.universeMatrix):

                if pk.immunityMatrix[i][t1] == 1 or pk.immunityMatrix[i][t2] == 1:
                    immunities.append(pk.types[i])
                elif pk.universeMatrix[i][t1] + pk.universeMatrix[i][t2] == 2:
                    weaknessesx4.append(pk.types[i])
                elif pk.universeMatrix[i][t1] + pk.universeMatrix[i][t2] == 1:
                    weaknesses.append(pk.types[i])
                elif pk.universeMatrix[i][t1] + pk.universeMatrix[i][t2] == 0:
                    neutral.append(pk.types[i])
                elif pk.universeMatrix[i][t1] + pk.universeMatrix[i][t2] == -1:
                    resistances.append(pk.types[i])
                elif pk.universeMatrix[i][t1] + pk.universeMatrix[i][t2] == -2:
                    resistancesx4.append(pk.types[i])

        immunities = sorted(immunities)
        weaknessesx4 = sorted(weaknessesx4)
        weaknesses = sorted(weaknesses)
        neutral = sorted(neutral)
        resistances = sorted(resistances)
        resistancesx4 = sorted(resistancesx4)

        print("Defensive Matchups: ")
        # immunities = []
        if len(immunities) != 0:
            print("    0x Immunities :", end=' ')
            for type in immunities:
                print(type, end=' ')
            print("")
        # weaknessesx4 = []
        if len(weaknessesx4) != 0:
            print("    4x Weaknesses :", end=' ')
            for type in weaknessesx4:
                print(type, end=' ')
            print("")
        # weaknesses = []
        if len(weaknesses) != 0:
            print("    2x Weaknesses :", end=' ')
            for type in weaknesses:
                print(type, end=' ')
            print("")
        # neutral = []
        if len(neutral) != 0:
            print("    Neutral :", end=' ')
            for type in neutral:
                print(type, end=' ')
            print("")
        # resistances = []
        if len(resistances) != 0:
            print("    1/2 Resistances :", end=' ')
            for type in resistances:
                print(type, end=' ')
            print("")
        # resistancesx4 = []
        if len(resistancesx4) != 0:
            print("    1/4x Resistances :", end=' ')
            for type in resistancesx4:
                print(type, end=' ')
            print("")

    def slashStrong(self, type1, type2):

        t1 = -1
        t2 = -1

        dualtype = []

        immunities = []
        weaknesses = []
        neutral = []
        resistances = []

        for i, type in enumerate(pk.types):
            if type.lower() == type1.lower():
                t1 = i
            if type.lower() == type2.lower():
                t2 = i

        for i, typei in enumerate(pk.universeMatrix):

            if pk.immunityMatrix[t1][i] == 1:
                immunities.append(pk.types[i])
            elif pk.universeMatrix[t1][i] == 1:
                weaknesses.append(pk.types[i])
                dualtype.append(pk.types[i])
            elif pk.universeMatrix[t1][i] == 0:
                neutral.append(pk.types[i])
            elif pk.universeMatrix[t1][i] == -1:
                resistances.append(pk.types[i])

        immunities = sorted(immunities)
        weaknesses = sorted(weaknesses)
        neutral = sorted(neutral)
        resistances = sorted(resistances)

        print(f"Offensive Matchups For {type1.title()}: ")
        # immunities = []
        if len(immunities) != 0:
            print("    0x Cannot Hit:", end=' ')
            for type in immunities:
                print(type, end=' ')
            print("")
        # weaknesses = []
        if len(weaknesses) != 0:
            print("    2x Supereffective Aganist:", end=' ')
            for type in weaknesses:
                print(type, end=' ')
            print("")
        # neutral = []
        if len(neutral) != 0:
            print("    1x Neutral:", end=' ')
            for type in neutral:
                print(type, end=' ')
            print("")
        # resistances = []
        if len(resistances) != 0:
            print("    1/2x Not Very Effective Aganist:", end=' ')
            for type in resistances:
                print(type, end=' ')
            print("")

        immunities = []
        weaknesses = []
        neutral = []
        resistances = []

        if t2 != -1:

            for i, typei in enumerate(pk.universeMatrix):

                if pk.immunityMatrix[t2][i] == 1:
                    immunities.append(pk.types[i])
                elif pk.universeMatrix[t2][i] == 1:
                    weaknesses.append(pk.types[i])
                    dualtype.append(pk.types[i])
                elif pk.universeMatrix[t2][i] == 0:
                    neutral.append(pk.types[i])
                elif pk.universeMatrix[t2][i] == -1:
                    resistances.append(pk.types[i])

            immunities = sorted(immunities)
            weaknesses = sorted(weaknesses)
            neutral = sorted(neutral)
            resistances = sorted(resistances)

            print("")
            print(f"Offensive Matchups For {type2.title()}: ")
            # immunities = []
            if len(immunities) != 0:
                print("    0x Cannot Hit:", end=' ')
                for type in immunities:
                    print(type, end=' ')
                print("")
            # weaknesses = []
            if len(weaknesses) != 0:
                print("    2x Supereffective Aganist:", end=' ')
                for type in weaknesses:
                    print(type, end=' ')
                print("")
            # neutral = []
            if len(neutral) != 0:
                print("    1x Neutral:", end=' ')
                for type in neutral:
                    print(type, end=' ')
                print("")
            # resistances = []
            if len(resistances) != 0:
                print("    1/2x Not Very Effective Aganist:", end=' ')
                for type in resistances:
                    print(type, end=' ')
                print("")

            print("")
            dualtype = list(set(dualtype))
            if len(dualtype) != 0:
                    print("What Your Dual Type Pokemon Can Hit For Super Effective:", end=' ')
                    for type in dualtype:
                        print(type, end=' ')
                    print("")



    def pokemonInForamt(self, pokemon):

        db = 'moveset.db'

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
                sqlCommand = f"SELECT Pokemon FROM moveset WHERE Pokemon == '{name}'"

                cursor.execute(sqlCommand)

                rows = cursor.fetchall()

                if len(rows) >= 1:
                    return True
            
            return False
        
    def printPokemon(self, pokemon):

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
                sqlCommand = f"SELECT * FROM pokemon WHERE Pokemon == '{name}'"

                cursor.execute(sqlCommand)

                rows = cursor.fetchall()[0]

                if len(rows) > 12:

                    #header
                    print(f'{rows[1]} | Number: {rows[0]} Rank: N/A Usage: N/A')

                    type1 = 'None'
                    type2 = 'None'

                    #type + weak
                    print("Type: ", end='')
                    if(len(rows[2]) > 0):
                        print(rows[2].upper(), end='')
                        type1 = rows[2]
                    if(len(rows[3]) > 0):
                        print(" " + rows[3].upper(), end='')
                        type2 = rows[3]
                    print("")

                    self.slashWeak(type1, type2)

                    #abilities
                    print("Abilities: ")
                    for i in range(10,13):
                        if len(rows[i]) > 0:
                            desc = self.ablFetch(rows[i])
                            print(f"    {rows[i]} : {desc}")

                    print('Pokemons Base Stats: ')

                    stats = []
                    stats.append(self.dexFetch('pokemon', pokemon, 'HP').upper())
                    stats.append(self.dexFetch('pokemon', pokemon, 'ATK').upper())
                    stats.append(self.dexFetch('pokemon', pokemon, 'DEF').upper())
                    stats.append(self.dexFetch('pokemon', pokemon, 'SPATK').upper())
                    stats.append(self.dexFetch('pokemon', pokemon, 'SPDEF').upper())
                    stats.append(self.dexFetch('pokemon', pokemon, 'SPD').upper())

                    for index, stat in enumerate(stats):
                        bar = self.printStatBar(int(stat))
                        print(f"{pk.stats[index]:>10}: {stat:>5}", end=bar + '\n')
            

    # tostring
    def __repr__(self):
        return str(self.format)