# server.py
import sys
import cgi
import os
import json

import smogon
import dex
import time
import typeMatrix

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qs, parse_qsl, unquote

# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):

    #service get requests
    def do_GET(self):

        parsed  = urlparse( self.path )

        # give main
        if parsed.path in [ '/main.html' ]:

            fp = open( '.'+self.path )
            content = fp.read()

            self.send_response( 200 )
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            self.wfile.write( bytes( content, "utf-8" ) )
            fp.close()

        # return whether a format is valid or not when a user is trying to change their selected format
        elif parsed.path.endswith(".format"):

            print("Servicing format request: ", parsed.path)

            #extract format
            format = parsed.path[:-7].strip('/')

            #confirm validity
            validFormatReturn = smogon.validFormat(format)

            #set content to the formats validity
            content = validFormatReturn[0]

            #this line is kinda confusing but im actually setting the format provided to a real existing format here, since the name do not have to be an exact match for me to deem a user given format as valid
            if(validFormatReturn[1] is not None):
                format = validFormatReturn[1][0].split('-')[0]
                print("Going to use: ", format ,validFormatReturn[1])

            #if the format is real we should update our databases with the latest information related to this format
            if(content):

                #its possible we already have it
                if not smogon.checkForLatest(format):
                    smogon.grabOneFormat(format)
                    time.sleep(0.3)
                    smogon.processPrepro()
                    smogon.createSmogonDB()

                #make sure we also have our static databases
                if not smogon.checkPokemon():
                    smogon.createPokemonDB()

                content = [str(content), format]

            #if the format does not exist we send back similarly spelt formats
            else:
                print("Invalid format: ", parsed.path)
                print("Will send similar formats back: ", parsed.path)
                formats = smogon.similarFormatTo(format)
                content = [str(content), formats]
    
            content = json.dumps(content)

            self.send_response( 200 )
            self.send_header( "Content-type", "application/json" )
            self.send_header( "Content-length", len(content.encode('utf-8')) )
            self.end_headers()

            self.wfile.write( bytes(content, "utf-8") )

        # return information about a pokemon
        elif parsed.path.endswith(".pokemon"):

            print("Servicing pokemon request: ", parsed.path)

            pokemon = parsed.path[:-8].strip('/')

            pokemon = unquote(pokemon)

            #we need to know the users selected format and elo which are sent as parameters
            params = parse_qs(parsed.query)
            format = params.get('format', [''])[0]
            elo = params.get('elo', [''])[0]

            #this content will grow alot
            content = []

            #smogon provides statistics for 4 different levels of elo, we assign the elo rating we want to search from as the closest to the users elo
            format += str('-') + str(smogon.assignElo(format, elo))

            #make a dex
            pkdex = dex.dex(format)

            print("Deciphered Pokemon, Format, Elo: ", pokemon, format, elo)

            #explanations for return status from dex.pokemonExist(pokemon)
            #0 - return status | 0 = exists & in format, 1 = exists & not in format, -1 = wtf is a skrunkly? (invalid pokemon)

            returnStatus = -1

            validPokemon = pkdex.pokemonExist(pokemon)
            
            #if pokemon exists
            if validPokemon:
                print("Pokemon:", pokemon, "exists, return set to: 1")
                returnStatus = 1
                inFormat = pkdex.pokemonInFormat(pokemon, format)
                #if its in the format sent as a parameter with the pokemon
                if inFormat:
                    print("Pokemon:", pokemon, "exists in format, return set to: 0")
                    returnStatus = 0

            print("Final Return Status:", returnStatus)

            #if the returnStatus is greater than -1 it must be exist so we can send back some info about the pokemon
            if returnStatus > -1:

                #the below are numbered by their indexes in content = [] which is sent back to the web application

                #0 - return status
                content.append(returnStatus)

                #1 - pokemon name
                content.append(pokemon.title())

                #2 - pokemon number (not used in final implementation but its so small i dont need to disable it)
                content.append(pkdex.dexFetch('pokemon', pokemon, 'Number'))

                #3 - pokemon rank
                if returnStatus == 0:
                    content.append(pkdex.dexFetch('basic', pokemon, 'Rank'))
                else:
                    content.append([])

                #4 - pokemon usage
                if returnStatus == 0:
                    content.append(pkdex.dexFetch('basic', pokemon, 'Usage'))
                else:
                    content.append([])

                #5 - pokemon types
                types = []
                types.append(pkdex.dexFetch('pokemon', pokemon, 'Type1').title())
                types.append(pkdex.dexFetch('pokemon', pokemon, 'Type2').title())
                content.append(types)

                #6 - def matchups
                matchups = pkdex.slashWeak(types[0], types[1])
                content.append(matchups)

                #7 - abilities
                ablContent = []

                #if the pokemon exists in the format we can get ability info with usages.
                if returnStatus == 0:
                    abilities = pkdex.dexFetch('moveset', pokemon, 'Abilities').split(';')
                    abilitiesAndUsages = [ability.split(' ') for ability in abilities]

                    ablContent.append(pkdex.dexFetch('pokemon', pokemon, 'Ability1'))
                    ablContent.append(pkdex.dexFetch('pokemon', pokemon, 'Ability2'))
                    ablContent.append(pkdex.dexFetch('pokemon', pokemon, 'Hidden'))

                    for i, abl in enumerate(ablContent):
                        if abl is not None:
                            ablContent[i] = ablContent[i].strip(' ')

                    for ability in abilitiesAndUsages:

                        abilityName = ''

                        for part in ability[:-1]:
                            abilityName += ' ' + part
                        abilityName = abilityName.strip(' ').strip('"')

                        desc = pkdex.ablFetch(abilityName)

                        if(desc is not None):
                            desc = desc.strip('"')

                        for i, abl in enumerate(ablContent):
                            if '"' in abl:
                                ablContent[i] = ablContent[i].strip('"')

                        for i, abl in enumerate(ablContent):

                            if abl in [ability[-1], abilityName, desc]:
                                ablContent[i] = [ability[-1], abilityName, desc]
                            elif len(abl) < 3:
                                ablContent[i] = ['','','']

                #otherwise if the pokemon only exists and does not exist in the format than we can still provide information without usages.
                elif returnStatus == 1:

                    ablContent.append(pkdex.dexFetch('pokemon', pokemon, 'Ability1'))
                    ablContent.append(pkdex.dexFetch('pokemon', pokemon, 'Ability2'))
                    ablContent.append(pkdex.dexFetch('pokemon', pokemon, 'Hidden'))

                    for i, abl in enumerate(ablContent):
                        desc = pkdex.ablFetch(abl)

                        if(desc is not None):
                            desc = desc.strip('"')

                        if desc is None:
                            desc = ''

                        ablContent[i] = [ablContent[i], desc]
                
                content.append(ablContent)

                #8 - stats
                stats = []
                stats.append(pkdex.dexFetch('pokemon', pokemon, 'HP').upper())
                stats.append(pkdex.dexFetch('pokemon', pokemon, 'ATK').upper())
                stats.append(pkdex.dexFetch('pokemon', pokemon, 'DEF').upper())
                stats.append(pkdex.dexFetch('pokemon', pokemon, 'SPATK').upper())
                stats.append(pkdex.dexFetch('pokemon', pokemon, 'SPDEF').upper())
                stats.append(pkdex.dexFetch('pokemon', pokemon, 'SPD').upper())
                content.append(stats)

                #9 - spreads
                #can only be provided if a pokemon exists in a format as they are entirely dictated by real players.
                if returnStatus == 0:
                    spreads = pkdex.dexFetch('moveset', pokemon, 'Spreads').upper().split(';')
                    for i, spread in enumerate(spreads):
                        spreads[i] = spreads[i].replace(":", " ")
                        spreads[i] = spreads[i].split(" ")
                        spreads[i] = list(filter(None, spreads[i]))
                        spreads[i][0] = [spreads[i][0].title(), pkdex.getNaturePlusMinus(spreads[i][0])]
                    content.append(spreads)
                else:
                    content.append([])

                #10 - moves
                movesContent = []
                #though it is possible to make it so that I could provide the user with all the moves a pokemon can learn it would be very painful and i dont wanna do that.
                #therefore info related to moves can only be returned if a pokemon is in a format through move usage.
                if returnStatus == 0:
                    moves = pkdex.dexFetch('moveset', pokemon, 'Moves').split(';')
                    movesAndUsages = [move.split(' ') for move in moves]

                    for move in movesAndUsages:

                        moveName = ''

                        for part in move[:-1]:
                            moveName += ' ' + part
                        moveName = moveName.strip(' ')

                        desc = pkdex.moveFetch(moveName)

                        if str(desc[0]) != 'Other':

                            #indexes order: usage, name, type, power, cat, desc, acc
                            if(desc[2] == ''):
                                desc[2] = "—"

                            if(desc[0] == ''):
                                desc[0] = "No Effect"

                            if(desc[4] is None or desc[4] == ''):
                                desc[4] = "—"

                            movesContent.append([move[-1], moveName, desc[1].capitalize(), desc[2], desc[3].capitalize(), desc[0], desc[4]])

                content.append(movesContent)

                #11 - items
                #can only be provided if a pokemon exists in a format as they are entirely dictated by real players.
                itemContent = []
                if returnStatus == 0:
                    items = pkdex.dexFetch('moveset', pokemon, 'Items').split(';')
                    itemsAndUsages = [item.split(' ') for item in items]

                    for item in itemsAndUsages:

                        itemName = ''

                        for part in item[:-1]:
                            itemName += ' ' + part
                        itemName = itemName.strip(' ').strip('"')

                        desc = pkdex.itemFetch(itemName)

                        if desc is not None:
                            desc = desc.strip('"')

                        item[-1] = item[-1].strip('"')

                        if itemName != 'Other':
                            itemContent.append([item[-1], itemName, desc])

                content.append(itemContent)

                #12 - teammates
                #can only be provided if a pokemon exists in a format as they are entirely dictated by real players.
                teammatesContent = []
                if returnStatus == 0:
                    teammates = pkdex.dexFetch('moveset', pokemon, 'Teammates').split(';')
                    teammatesAndUsages = [teammate.split(' ') for teammate in teammates]

                    for teammate in teammatesAndUsages:

                        teammateName = ''

                        for part in teammate[:-1]:
                            teammateName += ' ' + part
                        teammateName = teammateName.strip(' ').strip('"')

                        teammatesContent.append([teammate[-1], teammateName, smogon.grabImage(teammateName.lower())])

                content.append(teammatesContent)

                #13 - image name
                #return the image name of the pokemon so we can display it using smogons sprites database.
                savedAs = smogon.grabImage(pokemon.lower())
                content.append([savedAs])
            
            #if the pokemon does not exist at all we instead can send back some pokemon with similar names so the user can select from those.
            else:

                content.append(returnStatus)
                content.append(pkdex.similarNameTo(pokemon))

            print("Sending content for", pokemon, elo, format)

            #uncomment to see the content list being sent back
            # for i, item in enumerate(content):
            #     print("")
            #     print(i, item)

            content = json.dumps(content)

            self.send_response( 200 )
            self.send_header( "Content-type", "application/json" )
            self.send_header( "Content-length", len(content.encode('utf-8')) )
            self.end_headers()

            self.wfile.write( bytes(content, "utf-8") )

        #get a pokemon img name, sometimes we dont want to get all the information about a pokemon and would only like to display its existance
        elif parsed.path.endswith(".pkimg"):

            pokemon = parsed.path[:-6].strip('/')

            pokemon = pokemon.lower()

            pokemon = unquote(pokemon)

            content = smogon.grabImage(pokemon)

            content = json.dumps(content)

            self.send_response( 200 )
            self.send_header( "Content-type", "application/json" )
            self.send_header( "Content-length", len(content.encode('utf-8')) )
            self.end_headers()

            self.wfile.write( bytes(content, "utf-8") )

        #return a background for displayed pokemon
        elif parsed.path in [ '/pkbg.png' ]:

            fp = open('.' + self.path, 'rb')
            content = fp.read()

            self.send_response( 200 )
            self.send_header( "Content-type", "image/png" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            self.wfile.write( bytes(content) )
            fp.close()

        #return a typechart
        elif parsed.path in [ '/tctable.png' ]:

            fp = open('.' + self.path, 'rb')
            content = fp.read()

            self.send_response( 200 )
            self.send_header( "Content-type", "image/png" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            self.wfile.write( bytes(content) )
            fp.close()

        #return a custom made exclamation point (i did a great job w it)
        elif parsed.path in [ '/esprite.png' ]:

            fp = open('.' + self.path, 'rb')
            content = fp.read()

            self.send_response( 200 )
            self.send_header( "Content-type", "image/png" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            self.wfile.write( bytes(content) )
            fp.close()

        #return a star to symbolize shinyness (not used rn)
        elif parsed.path in [ '/star.png' ]:

            fp = open('.' + self.path, 'rb')
            content = fp.read()

            self.send_response( 200 )
            self.send_header( "Content-type", "image/png" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            self.wfile.write( bytes(content) )
            fp.close()

        #return a loading gif, loaded early
        elif parsed.path in [ '/loading.gif' ]:

            fp = open('.' + self.path, 'rb')
            content = fp.read()

            self.send_response( 200 )
            self.send_header( "Content-type", "image/gif" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            self.wfile.write( bytes(content) )
            fp.close()

        #otherwise 404
        else:
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )

    #I never need to use post so i dont, keeping it simple
    def do_POST(self):

        parsed = urlparse( self.path )

        self.send_response( 404 )
        self.end_headers()
        self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )

#main
if __name__ == "__main__":

    # check if we have the format that is set for the user by default, if we dont have it we need to get it
    print("Checking for default format gen9doublesou: ")
    if not smogon.checkForLatest("gen9doublesou"):
        print("-Not found, grabbing gen9doublesou: ")
        smogon.grabOneFormat("gen9doublesou")
        time.sleep(0.3)
        smogon.processPrepro()
        smogon.createSmogonDB()
    else:
        print("-Found")

    # check we have static pokemon related databases
    print("Checking for Pokemon databases: ")
    if not smogon.checkPokemon():
        print("-Not found, creating Pokemon databases: ")
        smogon.createPokemonDB()
    else:
        print("-Found")

    #start server
    httpd = HTTPServer( ( '0.0.0.0', int(sys.argv[1]) ), MyHandler )
    print( "Server listing in port:  ", int(sys.argv[1]) )
    httpd.serve_forever()