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

    #gets something that exists
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

        # check for valid format
        elif parsed.path.endswith(".format"):

            format = parsed.path[:-7].strip('/')

            validFormatReturn = smogon.validFormat(format)

            content = validFormatReturn[0]

            if(validFormatReturn[1] is not None):
                format = validFormatReturn[1][0].split('-')[0]
                print(format, "THIS IS THE FORMAT WE WILL USE", validFormatReturn[1])

            if(content):
                if not smogon.checkForLatest(format):
                    smogon.grabOneFormat(format)
                    time.sleep(0.3)
                    smogon.processPrepro()
                    smogon.createSmogonDB()

                if not smogon.checkPokemon():
                    smogon.createPokemonDB()

                content = [str(content), format]
            else:
                formats = smogon.similarFormatTo(format)
                content = [str(content), formats]
                print(content)
    
            content = json.dumps(content)

            self.send_response( 200 )
            self.send_header( "Content-type", "application/json" )
            self.send_header( "Content-length", len(content.encode('utf-8')) )
            self.end_headers()

            self.wfile.write( bytes(content, "utf-8") )

        # return information about a pokemon
        elif parsed.path.endswith(".pokemon"):

            pokemon = parsed.path[:-8].strip('/')

            pokemon = unquote(pokemon)

            params = parse_qs(parsed.query)
    
            # Get the 'format' param
            format = params.get('format', [''])[0]
            elo = params.get('elo', [''])[0]

            # THE CONTENT (MUSIC)
            content = []

            format += str('-') + str(smogon.assignElo(format, elo))
            pkdex = dex.dex(format)

            print(format, elo, pokemon)

            #0 - return status | 0 = exists & in format, 1 = exists & not in format, -1 = wtf is a skrunkly?

            returnStatus = -1

            validPokemon = pkdex.pokemonExist(pokemon)
            
            if validPokemon:
                returnStatus = 1
                inFormat = pkdex.pokemonInFormat(pokemon, format)
                if inFormat:
                    returnStatus = 0

            print(returnStatus, 9000)

            if returnStatus > -1:

                content.append(returnStatus)

                #1 - pokemon name

                content.append(pokemon.title())

                #2 - pokemon number

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

                if returnStatus == 0:
                    abilities = pkdex.dexFetch('moveset', pokemon, 'Abilities').split(';')
                    abilitiesAndUsages = [ability.split(' ') for ability in abilities]

                    ablContent.append(pkdex.dexFetch('pokemon', pokemon, 'Ability1'))
                    ablContent.append(pkdex.dexFetch('pokemon', pokemon, 'Ability2'))
                    ablContent.append(pkdex.dexFetch('pokemon', pokemon, 'Hidden'))

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
                elif returnStatus == 1:

                    ablContent.append(pkdex.dexFetch('pokemon', pokemon, 'Ability1'))
                    ablContent.append(pkdex.dexFetch('pokemon', pokemon, 'Ability2'))
                    ablContent.append(pkdex.dexFetch('pokemon', pokemon, 'Hidden'))

                    for i, abl in enumerate(ablContent):
                        desc = pkdex.ablFetch(abl)

                        if desc is None:
                            desc = ''

                        ablContent[i] = [ablContent[i], desc]

                    print(ablContent)


                
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
                if returnStatus == 0:
                    spreads = pkdex.dexFetch('moveset', pokemon, 'Spreads').upper().split(';')
                    for i, spread in enumerate(spreads):
                        spreads[i] = spreads[i].replace(":", " ")
                        spreads[i] = spreads[i].split(" ")
                        spreads[i] = list(filter(None, spreads[i]))
                        spreads[i][0] = [spreads[i][0], pkdex.getNaturePlusMinus(spreads[i][0])]
                    content.append(spreads)
                else:
                    content.append([])

                #10 - moves
                movesContent = []
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
                            #usage, name, type, power, cat, desc
                            if(desc[2] == ''):
                                desc[2] = "—"
                            print([desc[0]], [''])
                            if(desc[0] == ''):
                                desc[0] = "No Effect"
                            movesContent.append([move[-1], moveName, desc[1].capitalize(), desc[2], desc[3].capitalize(), desc[0]])

                content.append(movesContent)

                #11 - items
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

                savedAs = smogon.grabImage(pokemon.lower())
                content.append([savedAs])

                # #14 - tera type defensively
                teraContent = []
                teraContent.append(pkdex.teraGuess(content[5][0], content[5][1]))
                content.append(teraContent)

                # #14 - type defensively
                # typesDefContent = []
                # for type in typeMatrix.types:
                #     typesDefContent.append([type, pkdex.slashWeak(type, 'None')])
                # content.append(typesDefContent)

                # #15 - type offensively
                # typesStrongContent = []
                # for type in typeMatrix.types:
                #     typesStrongContent.append([type, pkdex.slashStrong(type, 'None')])
                # content.append(typesStrongContent)
            
            else:

                content.append(returnStatus)

                content.append(pkdex.similarNameTo(pokemon))

            print("CONTENT INFO BELOW", format)

            for i, item in enumerate(content):
                print("")
                print(i, item)

            content = json.dumps(content)

            self.send_response( 200 )
            self.send_header( "Content-type", "application/json" )
            self.send_header( "Content-length", len(content.encode('utf-8')) )
            self.end_headers()

            self.wfile.write( bytes(content, "utf-8") )

        #get a pokemon img name
        elif parsed.path.endswith(".pkimg"):

            pokemon = parsed.path[:-6].strip('/')

            pokemon = pokemon.lower()

            pokemon = unquote(pokemon)

            print(pokemon, 8000)

            content = smogon.grabImage(pokemon)

            content = json.dumps(content)

            self.send_response( 200 )
            self.send_header( "Content-type", "application/json" )
            self.send_header( "Content-length", len(content.encode('utf-8')) )
            self.end_headers()

            self.wfile.write( bytes(content, "utf-8") )

        #return a background if need be
        elif parsed.path in [ '/pkbg.png' ]:

            fp = open('.' + self.path, 'rb')
            content = fp.read()

            self.send_response( 200 )
            self.send_header( "Content-type", "image/png" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            self.wfile.write( bytes(content) )
            fp.close()

        #otherwise 404
        else:
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )

    #makes something that doesnt exist
    def do_POST(self):

        parsed = urlparse( self.path )

        #if display then we want to build html
        if parsed.path in [ '/display.html' ]:
            pass
        #otherwise 404
        else:
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )

#main
if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )
    print( "Server listing in port:  ", int(sys.argv[1]) )
    httpd.serve_forever()