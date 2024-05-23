#NOT NEEDED ANYMORE WE ARE NOT LONGER STUCK TO THE TERMINAL :D
#run.py will not work anymore and was used as a prototype bound to a terminal, it was used for user testing with friends, and to confirm correct information when i was working on all the behind the scenes stuff.
import smogon
import dex
import time

print("Welcome to Yogon Dex Lite")
format = input("Please enter the format you will be playing (For example: gen9doublesou): ")

while not smogon.validFormat(format):
    format = input("No no no, that format might not exist anymore (For example: gen9doublesou): ")

if not smogon.checkForLatest(format):
    smogon.grabOneFormat(format)
    time.sleep(0.3)
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
print("To see information about your opponents Pokemon, type 'pokemons name'")
print("To see information about your own Pokemon, type 'my pokemons name'")
dex = dex.dex(format)

pokemon = input("Who's that Pokemon? ")
while pokemon != 'exit' and pokemon != 'quit':

    if pokemon.startswith('my '):
        mypokemon = pokemon[3:]
        dex.my_pokemon(mypokemon)
    elif pokemon.startswith('!'):
        if pokemon == '!EV':
            dex.explainSpreads()
        if pokemon == '!TC':
            dex.printTypeChart()
    elif(dex.pokemonExist(pokemon)):
        if(dex.pokemonInFormat(pokemon)):
            dex.query_pokemon(pokemon)
        else:
            print("There is no information about this Pokemon in the format you are playing, either it's super niche or banned")
            print("Here is some basic information about the Pokemon")
            dex.printPokemon(pokemon)
        
    elif(pokemon != 'exit' and pokemon != 'quit'):
        print("Invalid Pokemon, check your spelling? (Alola, Hisui, Therian)")
    pokemon = input("Who's that Pokemon? ")
