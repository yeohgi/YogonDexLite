#dex.py is a class that serves information regarding specific pokemon and pokemon attributes.
#dex takes a format as a parameter to be constructed to simplify how often it would otherwise need to be passed as a parameter.

import sqlite3
import os
import csv
import re
import dask
dask.config.set({'dataframe.query-planning': True})
import dask.dataframe as dd
import typeMatrix as pk
from fuzzywuzzy import fuzz
import smogon

class dex:
    
    format = ''

    # __init__(self, format) initializes an instance of dex with the specified format.
    # Args: format refers to the competitive format/ruleset to retrive data from.
    def __init__(self, format):
        self.setFormat(format)
    
    # dexFetch() used to simlify queries regarding a Pokemon
    # Args: table refers to the table/db to be read from.
    #       pokemon refers to the pokemon to be queried.
    #       column refers to which attribute to return from the specified table.
    # Returns: Desired query as a string. Or None if N/A.
    def dexFetch(self, table, pokemon, column):

        table = table.lower()

        pokemon = pokemon.title()

        #Nessacary for searching pokemon with ' in their name like sirfetch'd and farfetch'd as title() no longer serves its intended function.
        #If a ' exists in the Pokemon name make adjacent letters to the right lowercase.
        if "'" in pokemon:
            newPokemon = ''
            skip = False
            for i, letter in enumerate(pokemon):
                if not skip:
                    if letter == "'" and i + 1 < len(pokemon):
                        newPokemon += letter + pokemon[i + 1].lower()
                        skip = True
                    else:
                        newPokemon += letter
                else:
                    skip = False

            pokemon = newPokemon

        column = column.capitalize()

        #check if db exists
        if os.path.exists(table + '.db'):

            conn = sqlite3.connect(table + '.db')
            cursor = conn.cursor()

            #if a space or - exists in the pokemon check multiple Pokemon names to forgive the user for providing an incorrect but almost correct Pokemon name.
            if ' ' in pokemon or '-' in pokemon:

                #add alternate spellings to tryNames
                tryNames = []
                tryNames.append(pokemon.replace(' ','-'))
                tryNames.append(pokemon.replace('-',' '))

                #Need to be forgiving if a user enters an inproper spelling for Pokemon names containing spaces and .'s. For example, Mr. Mime.
                if "." in pokemon:
                    for i, name in enumerate(tryNames):
                        tryNames[i] = tryNames[i].replace('.-', '. ')

                #Try each name and see which one works, take the most recent information that is most applicable to the current day user.
                for name in tryNames:
                    if(self.columnExists(table, "Year") and self.columnExists(table, "Month")):
                        sqlCommand = f'SELECT {column} FROM {table} WHERE Pokemon == "{name}" AND Format == "{self.format}" ORDER BY Year DESC, Month DESC LIMIT 1'
                    else:
                        sqlCommand = f'SELECT {column} FROM {table} WHERE Pokemon == "{name}"'
                    cursor.execute(sqlCommand)
                    rows = cursor.fetchall()
                    if(len(rows) != 0):
                        return str(rows[-1]).strip('(').strip(')').strip(',').strip("'")
                
                return None

            #if there is no space or - in the Pokemon name we can simply search it as it will be spelt correctly.
            else:
                if(self.columnExists(table, "Year") and self.columnExists(table, "Month")):
                    sqlCommand = f'SELECT {column} FROM {table} WHERE Pokemon == "{pokemon}" AND Format == "{self.format}" ORDER BY Year DESC, Month DESC LIMIT 1'
                else:
                    sqlCommand = f'SELECT {column} FROM {table} WHERE Pokemon == "{pokemon}"'
                cursor.execute(sqlCommand)
                rows = cursor.fetchall()
                if(len(rows) != 0):
                    return str(rows[-1]).strip('(').strip(')').strip(',').strip("'")
                else:
                    return None
        
        #if table does not exist.
        else:
            print("TABLE DNE")
            return None
    
    # ablFetch(self, ability) used to simlify queries regarding an ability, it only returns a description
    # Args: ability refers to the ability to return the description of.
    # Returns: An ability description, or None if N/A.
    def ablFetch(self, ability):

        db = 'abilities.db'

        if os.path.exists(db):

            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            if "'" in ability:
                ability = ability.replace("'",";")

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
    
    # moveFetch(self, move) used to simlify queries regarding a move.
    # Args: move refers to the move to return the effect/description, type, power, category, and accuracy of.
    # Returns: The effect/description, type, power, category, and accuracy of a move as a list, or None if N/A.
    def moveFetch(self, move):

        db = 'moves.db'

        if os.path.exists(db):

            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            sqlCommand = f"SELECT Effect, Type, Power, Category, Accuracy FROM moves WHERE Move == '{move}'"

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
    
    # itemFetch(self, item) used to simlify queries regarding a item.
    # Args: item refers to the item to return the description of.
    # Returns: An item description, or None if N/A.
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
    
    #teraGuess(self, type1, type2) is not used in current implementation of YogonDexLite
    #teraGuess(self, type1, type2) is used to guess the tera type of a Pokemon based on its typing. Uses a scoring system from -32 to 32 to determine what type provides the most net resistances to previously threating types.
    # Args: type1 refers to the primary type of a pokemon to guess the tera type for.
    #     : type2 refers to the secondary type of a pokemon to guess the tera type for.
    # Returns: A list of all types along with and sorted by their scores from most optimal to least optimal to terastalize into.

    def teraGuess(self, type1, type2):

        #all types have a corresponding type number on a "universeMatrix" from typeMatrix.py containing all type relationships.
        #set t1 and t2 to the sentinal value -1.
        t1 = -1
        t2 = -1

        #assign the correct type values to t1 and t2 based on strings type1 and type2
        for i, type in enumerate(pk.types):
            if type.lower() == type1.lower():
                t1 = i
            if type.lower() == type2.lower():
                t2 = i

        #it is possible for a pokemon to have 1-2 types. Handle the case where the pokemon only has one type.
        if t2 == -1:

            typeScore = []
            weaknesses = []

            #make a list of all threatening types (types that deal neutral damage or more to our pokemon type)
            for i, typei in enumerate(pk.universeMatrix):

                if pk.immunityMatrix[i][t1] == 1:
                    #do nothing we dont need to worry about an immunity
                    pass
                elif pk.universeMatrix[i][t1] == 1:
                    #if we are weak let us consider a defenseive tera
                    weaknesses.append(i)

            #provide each type with a score based on our weaknesses list containing types we want to matchup better aganist
            for i, typei in enumerate(pk.universeMatrix):
                typeScore.append(0) 
                for j in weaknesses:
                    if pk.immunityMatrix[j][i] == 1:
                        typeScore[i] = -16
                        break
                    else:
                        typeScore[i] += pk.universeMatrix[j][i]

            #this is a long and complicated function that isnt even being used rn im gonna stop commenting ill do it later :P
            #it needs to be edited a bit anyways
            for i, type in enumerate(typeScore):
                typeScore[i] = (typeScore[i], pk.types[i])

            typeScore = sorted(typeScore, key=lambda x: x[0], reverse=False)

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

            for i, type in enumerate(typeScore):
                typeScore[i] = (typeScore[i], pk.types[i])

            typeScore = sorted(typeScore, key=lambda x: x[0], reverse=False)

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

        return typeScore           

    #getter and setter for format
    def getFormat(self):
        return self.format
    def setFormat(self, format):
        self.format = format

    #columnExists(self, table, columnName) checks if a column exists in a table.
    # Args: table refers to the table to search column for.
    #     : columnName refers to which column to confirm the existance of.
    # Returns: True it exists, or False it does not.
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
    
    # pokemonExist(self, pokemon) is used to confirm whether a Pokemon exists at all. Useful to confirm so that user can view Pokemon illegal or never used in their selected format.
    # Args: pokemon refers to the pokemon to confirm the existance of.
    # Returns: True if the pokemon exists, False if it is mumbo jumbo garbage.
    def pokemonExist(self, pokemon):

        db = 'pokemon.db'

        pokemon = pokemon.title()

        tryNames = []  

        #naming shenanigans with farfetch'd and other similarly named pokemon
        if "'" in pokemon:
            newPokemon = ''
            skip = False
            for i, letter in enumerate(pokemon):
                if not skip:
                    if letter == "'" and i + 1 < len(pokemon):
                        newPokemon += letter + pokemon[i + 1].lower()
                        skip = True
                    else:
                        newPokemon += letter
                else:
                    skip = False

            pokemon = newPokemon

        #checking alternate spellings if the user inputs a pokemon with a space or -.
        if '-' in pokemon or ' ' in pokemon:

            tryNames.append(pokemon.replace(' ','-'))
            tryNames.append(pokemon.replace('-',' '))

            #mime and rime
            if "." in pokemon:
                for i, name in enumerate(tryNames):
                    tryNames[i] = tryNames[i].replace('.-', '. ')
        else:
            tryNames.append(pokemon)

        #try all names aganist pokemon.db. pokemon.db stores information on all pokemon as recent of 2024-05-22.
        if os.path.exists(db):

            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            for name in tryNames:

                sqlCommand = f'SELECT Pokemon FROM pokemon WHERE Pokemon == "{name}"'

                cursor.execute(sqlCommand)

                rows = cursor.fetchall()

                if len(rows) == 1:
                    return True
            
            return False
    
    #slashWeak(self, type1, type2) is used to determine the defensive matchups of a pokemons types. Uses typeMatrix.py for an immunityMatrix detailing immunity relationships between types and a universeMatrix detailing general relationships between types. Named based on the command /weak apokemon on Pokemon Showdown.
    # Args: type1 refers to the primary type of a pokemon to return the defensive matchups for.
    #     : type2 refers to the secondary type of a pokemon to guess the defensive matchups for.
    # Returns: The defensive matchups of the pokemon as a list in the following form [immunities, weaknessesx4, weaknesses, neutral, resistances, resistancesx4].
    def slashWeak(self, type1, type2):

        #all types have a corresponding type number on a "universeMatrix" from typeMatrix.py containing all type relationships.
        #set t1 and t2 to the sentinal value -1.
        t1 = -1
        t2 = -1

        #create empty lists for all possible type interactions even if pokemon only has one type.
        immunities = []
        weaknessesx4 = []
        weaknesses = []
        neutral = []
        resistances = []
        resistancesx4 = []

        #assign the correct type values to t1 and t2 based on strings type1 and type2
        for i, type in enumerate(pk.types):
            if type.lower() == type1.lower():
                t1 = i
            if type.lower() == type2.lower():
                t2 = i

        #if pokemon only has one type we can consider only immunities, weaknesses, neutral, and resistances
        if t2 == -1:

            #based on immunities and net effectiveness we can sort each type into the above categories
            for i, typei in enumerate(pk.universeMatrix):

                if pk.immunityMatrix[i][t1] == 1:
                    immunities.append(pk.types[i])
                elif pk.universeMatrix[i][t1] == 1:
                    weaknesses.append(pk.types[i])
                elif pk.universeMatrix[i][t1] == 0:
                    neutral.append(pk.types[i])
                elif pk.universeMatrix[i][t1] == -1:
                    resistances.append(pk.types[i])

        #if pokemon has more than one type we can consider more categories as we can now have 4x weaknesses and 4x resistances.
        else:

            #based on immunities and net effectiveness we can sort each type into the above categories
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

        #sort each of these
        immunities = sorted(immunities)
        weaknessesx4 = sorted(weaknessesx4)
        weaknesses = sorted(weaknesses)
        neutral = sorted(neutral)
        resistances = sorted(resistances)
        resistancesx4 = sorted(resistancesx4)

        #return the big list of everything!!!
        return [immunities, weaknessesx4, weaknesses, neutral, resistances, resistancesx4]

    #not in final implementation but keeping it around for later
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

        return [immunities, weaknesses, neutral, resistances]

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

    #pokemonInFormat(self, pokemon, format) checks whether a pokemon exists in a format. Called after a pokemon is confirmed to exist.
    # Args: pokemon refers to a pokemon confirmed to exist but we would like to check if it appears in smogons statistical data.
    #     : format refers to the format we are checking.
    # Returns: True if a pokemon exists in provided format, False if the pokemon does not exist in the provided format.
    def pokemonInFormat(self, pokemon, format):

        #always search in moveset.db as it contains information about pokemon configurations in different formats.
        db = 'moveset.db'

        pokemon = pokemon.title()

        #fault checking if name could be spelt incorrectly
        tryNames = []     
        if '-' in pokemon or ' ' in pokemon:
            tryNames.append(pokemon.replace(' ','-'))
            tryNames.append(pokemon.replace('-',' '))
        else:
            tryNames.append(pokemon)

        #if db exists
        if os.path.exists(db):

            conn = sqlite3.connect(db)
            cursor = conn.cursor()

            #try all names
            for name in tryNames:

                #farfetch'd
                if "'" in name:
                    name = name.capitalize()

                sqlCommand = f'SELECT Pokemon FROM moveset WHERE Pokemon == "{name}" AND Format LIKE "%{format}%"'

                cursor.execute(sqlCommand)

                rows = cursor.fetchall()

                if len(rows) >= 1:
                    return True
            
            return False

    #getNaturePlusMinus(self, aNature) takes a nature by name and returns what base stat it increases and decreases if any.
    # Args: aNature refers to a nature to get the boon and bane of.
    # Returns a list containing the increased and decreased stats. Or if the nature is gibberish and does not exist it returns an empty list.
    def getNaturePlusMinus(self, aNature):

        aNature = aNature.title()

        for i, nature in enumerate(pk.natures):
            if aNature == nature[0]:
                return [nature[1], nature[2]]

        return []
    
    #similarNameTo(self, wrongPokemon) is a function to provide spellchecking functionality using fuzzywuzzy's WRatio.
    # Args: wrongPokemon refers to a pokemon that is confirmed to not exist, or rather is most likely spelt incorrectly.
    # Returns: A list of all pokemon in pokemon.db with a WRatio rating above 70, sorted by most to least similar.
    def similarNameTo(self, wrongPokemon):

        similarPokemon = []

        #connect to pokemon.db
        if os.path.exists('pokemon.db'):

            conn = sqlite3.connect('pokemon.db')
            cursor = conn.cursor()
            command = f'SELECT pokemon FROM pokemon'
            cursor.execute(command)
            rows = cursor.fetchall()

            #for every pokemon take its WRatio and if its above 70 add it to similarPokemon in the form [pokemon, pokemon image name, score].
            for row in rows:
                pokemon = row[0]
                score = fuzz.WRatio(pokemon, wrongPokemon)
                if score > 70:
                    similarPokemon.append([pokemon, smogon.grabImage(pokemon.lower()), score])

        #sort to be most to least similar
        similarPokemon = sorted(similarPokemon, key=lambda x: x[-1], reverse=True)

        return similarPokemon

    # tostring, lol i never used this ever
    def __repr__(self):
        return str(self.format)