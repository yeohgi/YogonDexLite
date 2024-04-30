import subprocess
import shlex
import time
import os

import processAll
import createSmogon
import createPokemon

specialFolders = ["leads","metagame","moveset"]

def grabOneFormat(format):

    #get the latest folder
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

    #got the date
    #clean up
    subprocess.run(["rm", 'temp0.txt'])

    #get format names
    subprocess.Popen(f"php grabFormatCodes.php {formatDate}", shell = True, stdout = subprocess.PIPE)

    time.sleep(0.5)

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

    #get all required .txts
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

    for format in formats:

        subprocess.Popen(f"php grabBasic.php {formatDate} {format}", shell = True, stdout = subprocess.PIPE)

        time.sleep(0.3)

        for specialFolder in specialFolders:

            subprocess.Popen(f"php grabSpecial.php {formatDate} {specialFolder} {format}", shell = True, stdout = subprocess.PIPE)

            time.sleep(0.3)

def checkForLatest(format):

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

def processPrepro():

    processAll.processFolder()

def createSmogonDB():

    createSmogon.createDB()

def createPokemonDB():

    createPokemon.createDB()

def checkPokemon():

    cwd = os.getcwd()
    
    check = 0
    for file in os.listdir(cwd):
        if file.endswith('.db'):
            check += 1
    if check < 8:
        return False
    
    return True

def assignElo(format, elo):

    elo = int(elo)

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

    #get format names
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

    eloBounds = []

    for format in formats:
        eloBounds.append(int(format.split('-')[1].split('.')[0]))

    for i, eloBound in enumerate(eloBounds):
        if i == 0:
            useIndex = i
            difference = abs(elo - eloBound)
        else:
            if abs(elo - eloBound) < difference:
                useIndex = i
                difference = abs(elo - eloBound)

    subprocess.run(["rm", 'temp1.txt'])

    return eloBounds[useIndex]

def validFormat(format):
    
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

    #get format names
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
    
    if len(formats) == 0:
        return False
    
    return True

def grabImage(pokemon):

    if "'" in pokemon:
        pokemon = pokemon.replace("'", "")

    if '.' in pokemon:
        pokemon = pokemon.replace('. ', '')
        pokemon = pokemon.replace('.', '')


    tryPokemon = []
    if ' ' not in pokemon:
        tryPokemon.append(pokemon)
    tryPokemon.append(pokemon.replace(' ', '-'))
    tryPokemon.append(pokemon.replace(' ', ''))
    tryPokemon.append(pokemon.replace('-', ' '))
    tryPokemon.append(pokemon.replace('-', ''))

    print(tryPokemon)

    savedAs = ''

    for tryName in tryPokemon:

        process = subprocess.Popen(f"php grabImage.php {tryName}", shell = True, stdout = subprocess.PIPE)

        process.wait()

        output = process.stdout.read().strip().decode("utf-8")

        returnValue = int(output)

        print(tryName, returnValue)

        if returnValue == 0:
            savedAs = tryName
            break

    return savedAs


