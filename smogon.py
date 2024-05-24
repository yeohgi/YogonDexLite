#smogon.py is a library that retrieves and serves information related to smogon including data about formats, elo, and sprites.
#although not explicitly mentioned smogon.py requires the installation of php to be able to generate important temporary files.
import subprocess
import shlex
import time
import os

import processAll
import createSmogon
import createPokemon

from fuzzywuzzy import fuzz

specialFolders = ["leads","metagame","moveset"]

# grabOneFormat(format) is used to grab information about a format.
# Args: format refers to the format which data must be retrived for.
# Returns: does not return anything, files retrived if any are simply stored in /prepro.
def grabOneFormat(format):

    #get the latest folder/date by using a php script to get the html contents of https://www.smogon.com/stats/
    subprocess.Popen("php grabDate.php", shell = True, stdout = subprocess.PIPE)

    time.sleep(0.3)

    #get the last line of the html saved
    if os.path.exists('temp0.txt'):
        with open("temp0.txt", "r") as pk1:
            for line in pk1:
                if '"' in line:
                    lastLine = line
    else:
        print("Date could not be accessed")
        return

    formatDate = lastLine.split('"')[1].strip('/')

    #got the date
    #clean up
    subprocess.run(["rm", 'temp0.txt'])

    #get all format names & codes by checking inside the most recent folder we just got the name/date of
    subprocess.Popen(f"php grabFormatCodes.php {formatDate}", shell = True, stdout = subprocess.PIPE)

    time.sleep(0.5)

    #if the format provided as a parameter for this function appears in any line save that format to be retrived later
    if os.path.exists('temp1.txt'):
        formats = []
        with open("temp1.txt", "r") as pk1:
            for line in pk1:
                if format.lower() in line.lower():
                    formats.append(line.split('"')[1])
    else:
        print("Folder could not be accessed")
        return
    
    #got the format names
    #clean up
    subprocess.run(["rm", 'temp1.txt'])

    #make sure /prepro and all of its subfolders exist
    if not os.path.exists('prepro/'):
        subprocess.run(["mkdir", 'prepro'])

    if not os.path.exists(f'prepro/{formatDate}'):
        subprocess.run(["mkdir", f'prepro/{formatDate}'])
        
    if not os.path.exists(f'prepro/{formatDate}/leads/'):
        subprocess.run(["mkdir", f'prepro/{formatDate}/leads/'])

    if not os.path.exists(f'prepro/{formatDate}/metagame/'):
        subprocess.run(["mkdir", f'prepro/{formatDate}/metagame/'])

    if not os.path.exists(f'prepro/{formatDate}/moveset/'):
        subprocess.run(["mkdir", f'prepro/{formatDate}/moveset/'])

    #for each of the formats saved to be retrived, retrive their basic .txt files and special .txt files including info on leads, metagame, and moveset using grabBasic.php and grabSpecial.php
    for format in formats:

        subprocess.Popen(f"php grabBasic.php {formatDate} {format}", shell = True, stdout = subprocess.PIPE)

        time.sleep(0.3)

        for specialFolder in specialFolders:

            subprocess.Popen(f"php grabSpecial.php {formatDate} {specialFolder} {format}", shell = True, stdout = subprocess.PIPE)

            time.sleep(0.3)

# checkForLatest(format) is a huge list of checks that can confirm if we have all the information we need about a format, useful so that the application does not have to fetch info if it already has it.
# Args: format refers to the format we would like to check if we already have up to date information for.
# Returns: True if nothing need to be retrived and no files are missing, False if anything at all is missing regarding the format and any smogon related database.
def checkForLatest(format):

    #get the latest folder/date by using a php script to get the html contents of https://www.smogon.com/stats/
    subprocess.Popen("php grabDate.php", shell = True, stdout = subprocess.PIPE)

    time.sleep(0.5)

    if os.path.exists('temp0.txt'):
        with open("temp0.txt", "r") as pk1:
            for line in pk1:
                if '"' in line:
                    lastLine = line
    else:
        print("Date could not be accessed")
        return

    formatDate = lastLine.split('"')[1].strip('/')

    #clean up
    subprocess.run(["rm", 'temp0.txt'])

    #check for data folder
    if not os.path.exists(f'prepro/{formatDate}'):
        return False
    
    #check basic
    check = 0
    for file in os.listdir(f'prepro/{formatDate}'):
        if format.lower() in file:
            check += 1
    if check < 4:
        return False
    
    #check leads
    if not os.path.exists(f'prepro/{formatDate}/leads'):
        return False
    
    check = 0
    for file in os.listdir(f'prepro/{formatDate}/leads'):
        if format.lower() in file:
            check += 1
    if check < 4:
        return False
    
    #check metagame
    if not os.path.exists(f'prepro/{formatDate}/metagame'):
        return False
    
    check = 0
    for file in os.listdir(f'prepro/{formatDate}/metagame'):
        if format.lower() in file:
            check += 1
    if check < 4:
        return False
    
    #check moveset
    if not os.path.exists(f'prepro/{formatDate}/moveset'):
        return False
    
    check = 0
    for file in os.listdir(f'prepro/{formatDate}/moveset'):
        if format.lower() in file:
            check += 1
    if check < 4:
        return False
    
    #check for data folder
    if not os.path.exists(f'postpro/{formatDate}'):
        return False
    
    #check basic
    check = 0
    for file in os.listdir(f'postpro/{formatDate}'):
        if format.lower() in file:
            check += 1
    if check < 4:
        return False
    
    #check leads
    if not os.path.exists(f'postpro/{formatDate}/leads'):
        return False
    
    check = 0
    for file in os.listdir(f'postpro/{formatDate}/leads'):
        if format.lower() in file:
            check += 1
    if check < 4:
        return False
    
    #check metagame
    if not os.path.exists(f'postpro/{formatDate}/metagame'):
        return False
    
    check = 0
    for file in os.listdir(f'postpro/{formatDate}/metagame'):
        if format.lower() in file:
            check += 1
    if check < 4:
        return False
    
    #check moveset
    if not os.path.exists(f'postpro/{formatDate}/moveset'):
        return False
    
    check = 0
    for file in os.listdir(f'postpro/{formatDate}/moveset'):
        if format.lower() in file:
            check += 1
    if check < 4:
        return False
    
    cwd = os.getcwd()
    if 'basic.db' not in os.listdir(cwd) or 'leads.db' not in os.listdir(cwd) or 'metagame.db' not in os.listdir(cwd) or 'moveset.db' not in os.listdir(cwd):
        return False

    #end of the gauntlet
    return True

#processPrepro() simply calls processFolder() from processAll.py
#processAll.py is used to process the prepro(preprocessed) folder of .txt files containing plain usage data to create the postpro(postprocessed) folder of .txt files in a .csv format
#processFolder() processes the prepro folder and creates the postpro folder
def processPrepro():

    processAll.processFolder()

#createSmogonDB() simply calls createDB() from createSmogon.py
#createSmogon.py is used to create pokemon related databases from .csv files generated from data obtained using php from https://www.smogon.com/stats/
def createSmogonDB():

    createSmogon.createDB()

#createPokemonDB() simply calls createDB() from createPokemon.py
#createPokemon.py is used to create pokemon related databases from static .csv files
def createPokemonDB():

    createPokemon.createDB()

#checkPokemon() checks if the current work directory has at least 8 data bases. This function could be improved later.
def checkPokemon():

    cwd = os.getcwd()
    
    check = 0
    for file in os.listdir(cwd):
        if file.endswith('.db'):
            check += 1
    if check < 8:
        return False
    
    return True

#assignElo(format, elo) takes in a format and a users elo and returns the elo tier closest to them. This function is important to provide accurate insights based on a players skill level as in different levels of play different pokemon and strategies are used more or less frequently.
# Args: format refers to the format to retrive elo tiers for.
#     : elo refers to the users elo rating.
# Returns: An integer elo tier closest to the users elo.
def assignElo(format, elo):

    elo = int(elo)

    #get the latest folder/date by using a php script to get the html contents of https://www.smogon.com/stats/
    subprocess.Popen("php grabDate.php", shell = True, stdout = subprocess.PIPE)

    time.sleep(0.5)

    if os.path.exists('temp0.txt'):
        with open("temp0.txt", "r") as pk1:
            for line in pk1:
                if '"' in line:
                    lastLine = line
    else:
        print("Date could not be accessed")
        return

    formatDate = lastLine.split('"')[1].strip('/')

    #clean up
    subprocess.run(["rm", 'temp0.txt'])

    #get format names/codes
    subprocess.Popen(f"php grabFormatCodes.php {formatDate}", shell = True, stdout = subprocess.PIPE)

    time.sleep(1)

    if os.path.exists('temp1.txt'):
        formats = []
        with open("temp1.txt", "r") as pk1:
            for line in pk1:
                if format.lower() in line.lower():
                    formats.append(line.split('"')[1])
    else:
        print("Folder could not be accessed")
        return

    #format names/codes contain their elo tier, in the form format-elo.txt, so we may split to get all the formats elo tiers
    eloBounds = []

    for format in formats:
        eloBounds.append(int(format.split('-')[1].split('.')[0]))

    eloBoundsNoZero = []

    #there is a weird quirk in smogons naming scheme where the first file starts at elo tier 0, even though the lowest elo possible is 1000. to make assigning elo more accurate i make a duplicate elo tier list with 0 as 1000 for calculations
    for anElo in eloBounds:
        if anElo == 0:
            eloBoundsNoZero.append(1000)
        else:
            eloBoundsNoZero.append(anElo)

    #determine closest elo tier
    for i, eloBound in enumerate(eloBoundsNoZero):
        if i == 0:
            useIndex = i
            difference = abs(elo - eloBound)
        else:
            if abs(elo - eloBound) < difference:
                useIndex = i
                difference = abs(elo - eloBound)

    #cleanup
    subprocess.run(["rm", 'temp1.txt'])

    #return closest elo tier
    return eloBounds[useIndex]

#validFormat(format) determines whether a format is valid, a valid format is a format that exists in the most recent folder on https://www.smogon.com/stats/.
# Args: format refers to the format to confirm the validity of.
# Returns: A list containing the validity of the format, and a list of format codes. Validity is True if format is valid, False if the format is deemed not valid.
def validFormat(format):
    
    #get the latest folder/date by using a php script to get the html contents of https://www.smogon.com/stats/
    subprocess.Popen("php grabDate.php", shell = True, stdout = subprocess.PIPE)

    time.sleep(0.3)

    if os.path.exists('temp0.txt'):
        with open("temp0.txt", "r") as pk1:
            for line in pk1:
                if '"' in line:
                    lastLine = line
    else:
        print("Date could not be accessed")
        return

    formatDate = lastLine.split('"')[1].strip('/')

    #clean up
    subprocess.run(["rm", 'temp0.txt'])

    #get format names/codes
    subprocess.Popen(f"php grabFormatCodes.php {formatDate}", shell = True, stdout = subprocess.PIPE)

    time.sleep(0.3)

    if os.path.exists('temp1.txt'):
        formats = []
        with open("temp1.txt", "r") as pk1:
            for line in pk1:
                if format.lower() in line.lower():
                    formats.append(line.split('"')[1])
    else:
        print("Folder could not be accessed")
        return
    
    #if the format we searched yields a list of formats greater than zero it must be valid
    if len(formats) == 0:
        return [False, None]
    
    #return valid, and a list of the format codes associated with its validity
    return [True, formats]

#grabImage(pokemon) is used to find pokemon image names on smogon sprites https://play.pokemonshowdown.com/sprites/.
# Args: pokemon refers to the pokemon which we are trying to find the image for.
# Returns: A pokemon image name to be used in a url if the pokemon name is found, if it is not found an empty string is returned.
def grabImage(pokemon):

    #could improve later
    #note: just improved it a little more, should be alot faster

    #naming conventions for ' pokemon like farfetch'd
    if "'" in pokemon:
        pokemon = pokemon.replace("'", "")

    #naming conventions for . pokemon like mr. mime
    if '.' in pokemon:
        pokemon = pokemon.replace('. ', '')
        pokemon = pokemon.replace('.', '')

    #we dont use spaces in image names
    pokemon = pokemon.replace(' ', '-')

    #if multiple dashes in a pokemon name keep only the first
    if len(pokemon.split('-')) > 1:
        parts = pokemon.split('-', 1)
        if len(parts) > 1:
            pokemon = parts[0] + '-' + parts[1].replace('-', '')

    #build try pokemon
    tryPokemon = []
    #this line im a little confused about looking back at it, i could probably remove it but i dont wanna check it rn
    if ' ' not in pokemon:
        tryPokemon.append(pokemon)
    tryPokemon.append(pokemon.replace('-', ''))

    #savedAs will refer to the image name associated with the pokemon
    savedAs = ''

    #try all names and if one is successful stop the searching and return it
    for tryName in tryPokemon:

        #using a php script named grabImage.php we decode a return value based on if the image name we tried was successful
        process = subprocess.Popen(f"php grabImage.php {tryName}", shell = True, stdout = subprocess.PIPE)

        process.wait()

        output = process.stdout.read().strip().decode("utf-8")

        returnValue = int(output)

        # print(tryName, returnValue)

        #if the return value was 0 it was successful and can move forward using this image name
        if returnValue == 0:
            savedAs = tryName
            break

    #return image name
    return savedAs

#similarFormatTo(wrongFormat) is used when a format is deemed invalid and want to point the user to formats similar to what they searched using fuzzywuzzys WRatio.
# Args: wrongFormat refers to an invalid format that we want to find formats spelt similarily too.
# Returns: A list of formats deemed similar from most to least similar, if no formats are deemed similar to wrongFormat the list will be empty.
def similarFormatTo(wrongFormat):

    #get the latest folder/date
    subprocess.Popen("php grabDate.php", shell = True, stdout = subprocess.PIPE)

    time.sleep(0.3)

    if os.path.exists('temp0.txt'):
        with open("temp0.txt", "r") as pk1:
            for line in pk1:
                if '"' in line:
                    lastLine = line
    else:
        print("Date could not be accessed")
        return

    formatDate = lastLine.split('"')[1].strip('/')

    #clean up
    subprocess.run(["rm", 'temp0.txt'])
    
    #get format names/codes
    subprocess.Popen(f"php grabFormatCodes.php {formatDate}", shell = True, stdout = subprocess.PIPE)

    time.sleep(0.5)

    #create a list of all formats in the most recent folder
    if os.path.exists('temp1.txt'):
        formats = []
        with open("temp1.txt", "r") as pk1:
            for line in pk1:
                if '"' in line:
                    formats.append(line.split('"')[1].split("-")[0])
    else:
        print("Folder could not be accessed")
        return ["Folder could not be accessed"]
    
    #clean up
    subprocess.run(["rm", 'temp1.txt'])

    #go through all format codes and compare with wrongFormat, if a format is deemed similar it is appended to similarFormats along with its similarity score.
    similarFormats = []
    for format in formats:
        score = fuzz.WRatio(format, wrongFormat)
        if score > 60:
            if [format, score] not in similarFormats:
                similarFormats.append([format, score])

    #sort by similarity score from most to least similar before returning
    similarFormats = sorted(similarFormats, key=lambda x: x[-1], reverse=True)

    return similarFormats


