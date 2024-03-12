import os

def processFolder():
  for folder in os.listdir('prepro'):

    os.makedirs(f'postpro/{folder}', exist_ok=True)
    print("I'm working on " + folder)

    for file in os.listdir(f'prepro/{folder}'):

      if(file.endswith(".txt")):

        with open("./prepro/" + folder + "/" + file, "r") as pk1, \
          open("./postpro/" + folder + "/" + file, "w") as pk2:

            pk2.write("Rank,Pokemon,Usage,Raw,Percent,Real,RealPercent\n")

            start = False

            for line in pk1:

              final = ""

              if "| 1" in line:
                start = True

              if start is True:

                pieces = line.split("|")

                pieces = [p for p in pieces if p.strip()]

                count = 0

                for piece in pieces:
                  
                  piece = piece.strip().strip('%')

                  if piece.strip().strip('%') == pieces[-1].strip().strip('%') and count == len(pieces) - 1:
                      final += piece
                  else:
                      final += piece + ','

                  count += 1

                if '---' not in final:
                  pk2.write(final + '\n')


    for file in os.listdir(f'prepro/{folder}/leads/'):

      os.makedirs(f'postpro/{folder}/leads/', exist_ok=True)

      with open("./prepro/" + folder + "/leads/" + file, "r") as pk1, \
        open("./postpro/" + folder + "/leads/" + file, "w") as pk2:

          pk2.write("Rank,Pokemon,Usage,Raw,Percent\n")

          start = False

          for line in pk1:

            final = ""

            if "| 1" in line:
              start = True

            if start is True:

              pieces = line.split("|")

              pieces = [p for p in pieces if p.strip()]

              for piece in pieces:

                piece = piece.strip().strip('%')

                if piece.strip().strip('%') == pieces[-1].strip().strip('%'):
                    final += piece
                else:
                    final += piece + ','

              if '---' not in final:
                pk2.write(final + '\n')

    for file in os.listdir(f'prepro/{folder}/metagame/'):

      os.makedirs(f'postpro/{folder}/metagame/', exist_ok=True)

      with open("./prepro/" + folder + "/metagame/" + file, "r") as pk1, \
        open("./postpro/" + folder + "/metagame/" + file, "w") as pk2:

          pk2.write("Meta,Percent,Stall\n")

          final = ""

          stall = 0.00

          for line in pk1:
            if "Stalliness (mean:" in line:
              cut = line.split(" ")
              stall = cut[-1].strip().strip(')')

          pk1.seek(0)

          for line in pk1:
            pieces = line.split("..")
            
            if line.strip() == "":
              break

            if pieces[-1][0] == '.':
              percent = pieces[-1][1:]
            else:
              percent = pieces[-1]

            final = pieces[0].strip().strip('%') + ',' + percent.strip().strip('%') + ',' + str(stall)

            pk2.write(final + "\n")

    for file in os.listdir(f'prepro/{folder}/moveset/'):

      os.makedirs(f'postpro/{folder}/moveset/', exist_ok=True)

      with open("./prepro/" + folder + "/moveset/" + file, "r") as pk1, \
        open("./postpro/" + folder + "/moveset/" + file, "w") as pk2:

          pk2.write("Pokemon,Raw,Abilities,Items,Spreads,Moves,Teammates\n")

          megaString = ""

          for line in pk1:

            megaString += line.strip().strip('\n')

          megaSplit = megaString.split('-+')

          if(len(megaSplit) <= 1):
            print("bad file")
          else:

            indexPointer = 1

            while indexPointer + 8 < len(megaSplit):
            
              name = megaSplit[indexPointer]
              raw = megaSplit[indexPointer + 1]
              abilities = megaSplit[indexPointer + 2]
              items = megaSplit[indexPointer + 3]
              spreads = megaSplit[indexPointer+ 4]
              moves = megaSplit[indexPointer+ 5]
              teammates = megaSplit[indexPointer+ 6]

              # #name
              nameFinal = name.strip('|').strip()
              nameFinal = nameFinal.split("|")[0].strip()
              # print(nameFinal)

              #name
              rawFinal = raw.strip('|').strip()
              rawFinal = rawFinal.split("|")[0].strip()
              rawFinal = rawFinal.split(" ")[-1].strip()
              # print(rawFinal)

              #abilities
              abilitiesFinal = ""
              abilitiesPieces = abilities.split('||')
              for index in range(1,len(abilitiesPieces)):
                abilitiesFinal += abilitiesPieces[index].split("|")[0].strip().strip("%") + ';'
              abilitiesFinal = abilitiesFinal.strip(';')
              # print(abilitiesFinal)

              #items
              itemsFinal = ""
              itemsPieces = items.split('||')
              for index in range(1,len(itemsPieces)):
                itemsFinal += itemsPieces[index].split("|")[0].strip().strip("%") + ';'
              itemsFinal = itemsFinal.strip(';')
              # print(itemsFinal)

              #spreads
              spreadsFinal = ""
              spreadsPieces = spreads.split('||')
              for index in range(1,len(spreadsPieces)):
                spreadsFinal += spreadsPieces[index].split("|")[0].strip().strip("%") + ';'
              spreadsFinal = spreadsFinal.strip(';')
              # print(spreadsFinal)

              #moves
              movesFinal = ""
              movesPieces = moves.split('||')
              for index in range(1,len(movesPieces)):
                movesFinal += movesPieces[index].split("|")[0].strip().strip("%") + ';'
              movesFinal = movesFinal.strip(';')
              # print(movesFinal)

              #teammates
              teammatesFinal = ""
              teammatesPieces = teammates.split('||')
              for index in range(1,len(teammatesPieces)):
                teammatesFinal += teammatesPieces[index].split("|")[0].strip().strip("%") + ';'
              teammatesFinal = teammatesFinal.strip(';')
              # print(teammatesFinal)

              final = nameFinal + ',' + rawFinal + ',' + abilitiesFinal + ',' + itemsFinal + ',' + spreadsFinal + ',' + movesFinal + ',' + teammatesFinal

              # print(final + '\n')

              pk2.write(final + '\n')
              
              indexPointer = indexPointer + 9
            
            
          # for part in megaSplit:

          #   if ''
        

        

          

        


                

        