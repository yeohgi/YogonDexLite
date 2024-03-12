import smogon
import dex

print("Welcome to Yogon Dex Lite")
format = input("Please enter the format you will be playing (Gen#Format) (For example: gen9doublesou): ")

while not smogon.validFormat(format):
    format = input("No no no, look at the style guide -> (Gen#Format) (For example: gen9doublesou): ")

if not smogon.checkForLatest(format):
    smogon.grabOneFormat(format)
    smogon.processPrepro()
    smogon.createSmogonDB()

if not smogon.checkPokemon():
    smogon.createPokemonDB()

print("Great! The formats most recent data has been imported!")

elo = input("Next how shit are you? What's your elo rating? ")

while not elo.isdigit():
    elo = input("Oops you must have typed incorrectly, what's your elo?")

format += str('-') + str(smogon.assignElo(format, elo))

print("Your set up! Time to kick some ass!")
dex = dex.dex(format)

pokemon = input("Who's that Pokemon? ")
while pokemon != 'exit':
    if(dex.pokemonExist(pokemon)):
        dex.query_pokemon(pokemon)
    else:
        print("Invalid Pokemon, check your spelling? (Alola, Hisui, Therian)")
    pokemon = input("Who's that Pokemon? ")