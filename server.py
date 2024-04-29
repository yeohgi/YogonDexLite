import sys
import cgi
import os
import json

import smogon
import dex

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

            content = smogon.validFormat(format)
            content = str(content)

            print(content, format)

            self.send_response( 200 )
            self.send_header( "Content-type", "text/plain" )
            self.send_header( "Content-length", len( content ) )
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
                inFormat = pkdex.pokemonInFormat(pokemon)
                if inFormat:
                    returnStatus = 0

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
                    content.append("N/A")

                #4 - pokemon usage
                if returnStatus == 0:
                    content.append(pkdex.dexFetch('basic', pokemon, 'Usage'))
                else:
                    content.append("N/A")

                #5 - pokemon types
                types = []
                types.append(pkdex.dexFetch('pokemon', pokemon, 'Type1').upper())
                types.append(pkdex.dexFetch('pokemon', pokemon, 'Type2').upper())
                content.append(types)

                #6 - def matchups
                matchups = pkdex.slashWeak(types[0], types[1])
                content.append(matchups)

                #7 - abilities
                ablContent = []
                abilities = pkdex.dexFetch('moveset', pokemon, 'Abilities').split(';') #NO RETURN STATUS CHECK COME BACK LATER
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

                    for i, abl in enumerate(ablContent):
                        if '"' in abl:
                            ablContent[i] = ablContent[i].strip('"')

                    # print(abilityName, desc, ablContent, ablContent[0])

                    for i, abl in enumerate(ablContent):
                        if abl in [ability[-1], abilityName, desc]:
                            ablContent[i] = [ability[-1], abilityName, desc]
                        elif len(abl) < 3:
                            ablContent[i] = ['','','']
                        

                
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
                    content.append(spreads)
                else:
                    content.append("N/A")

                #10 - moves
                movesContent = []
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
                        movesContent.append([move[-1], moveName, desc[1], desc[2], desc[3], desc[0]])

                content.append(movesContent)

                #11 - items
                itemContent = []
                items = pkdex.dexFetch('moveset', pokemon, 'Items').split(';')
                itemsAndUsages = [item.split(' ') for item in items]

                for item in itemsAndUsages:

                    itemName = ''

                    for part in item[:-1]:
                        itemName += ' ' + part
                    itemName = itemName.strip(' ').strip('"')

                    desc = pkdex.itemFetch(itemName)

                    item[-1] = item[-1].strip('"')

                    if itemName != 'Other':
                        itemContent.append([item[-1], itemName, desc])

                content.append(itemContent)

                #12 - teammates
                teammatesContent = []
                teammates = pkdex.dexFetch('moveset', pokemon, 'Teammates').split(';')
                teammatesAndUsages = [teammate.split(' ') for teammate in teammates]

                for teammate in teammatesAndUsages:

                    teammateName = ''

                    for part in teammate[:-1]:
                        teammateName += ' ' + part
                    teammateName = teammateName.strip(' ').strip('"')

                    teammatesContent.append([teammate[-1], teammateName])

                content.append(teammatesContent)

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

        #return a background if need be
        elif parsed.path in [ '/background.png' ]:

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