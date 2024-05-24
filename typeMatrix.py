#universe Matrix is a table containing all type relationships execluding immunities.
universeMatrix = [
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, -1, 0],        #NORMAL
  [0, -1, -1, 0, 1, 1, 0, 0, 0, 0, 0, 1, -1, 0, -1, 0, 1, 0],      #FIRE
  [0, 1, -1, 0, -1, 0, 0, 0, 1, 0, 0, 0, 1, 0, -1, 0, 0, 0],       #WATER
  [0, 0, 1, -1, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1, 0, 0, 0],       #ELECTRIC
  [0,-1, 1, 0, -1, 0, 0, -1, 1, -1, 0, -1, 1, 0, -1, 0, -1, 0],    #GRASS
  [0, -1, -1, 0, 1, -1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, -1, 0],      #ICE
  [1, 0, 0, 0, 0, 1, 0, -1, 0, -1, -1, -1, 1, 0, 0, 1, 1, -1],     #FIGHTING
  [0, 0, 0, 0, 1, 0, 0, -1, -1, 0, 0, 0, -1, -1, 0, 0, 0, 1],      #POISON
  [0, 1, 0, 1, -1, 0, 0, 1, 0, 0, 0, -1, 1, 0, 0, 0, 1, 0],        #GROUND
  [0, 0, 0, -1, 1, 0, 1, 0, 0, 0, 0, 1, -1, 0, 0, 0, -1, 0],       #FLYING
  [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, -1, 0, 0, 0, 0, 0, -1, 0],        #PSYCHIC
  [0, -1, 0, 0, 1, 0, -1, -1, 0, -1, 1, 0, 0, -1, 0, 1, -1, -1],   #BUG
  [0, 1, 0, 0, 0, 1, -1, 0, -1, 1, 0, 1, 0, 0, 0, 0, -1, 0],       #ROCK
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, -1, 0, 0],         #GHOST
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, -1, 0],         #DRAGON
  [0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 1, 0, 0, 1, 0, -1, 0, -1],       #DARK
  [0, -1, -1, -1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, -1, 1],      #STEEL
  [0, -1, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 1, 1, -1, 0]        #FAIRY
]       

#immunity Matrix is a table containing all type immnunities.
immunityMatrix = [
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],           #NORMAL
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],           #FIRE
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],           #WATER
  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],           #ELECTRIC
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],           #GRASS
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],           #ICE
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],           #FIGHTING
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],           #POISON
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],           #GROUND
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],           #FLYING
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],           #PSYCHIC
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],           #BUG
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],           #ROCK
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],           #GHOST
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],           #DRAGON
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],           #DARK
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],           #STEEL
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]            #FAIRY
]           

#a list of all types in pokemon
types = ["Normal", "Fire", "Water", "Electric", "Grass", 
         "Ice", "Fighting", "Poison", "Ground", "Flying", 
         "Psychic", "Bug", "Rock", "Ghost", "Dragon", 
         "Dark", "Steel", "Fairy"]

#a list of all base stats
stats = ["HP", "ATK", "DEF", "SPATK", "SPDEF", "SPD"]

#a list of all Natures along with the stats they increase and decrease
natures = [
    ["Adamant", "ATK", "SPATK"],
    ["Bashful", "SPATK", "SPATK"],
    ["Bold", "DEF", "ATK"],
    ["Brave", "ATK", "SPD"],
    ["Calm", "SPDEF", "ATK"],
    ["Careful", "SPDEF", "SPATK"],
    ["Docile", "DEF", "DEF"],
    ["Gentle", "SPDEF", "DEF"],
    ["Hardy", "ATK", "ATK"],
    ["Hasty", "SPD", "DEF"],
    ["Impish", "DEF", "SPATK"],
    ["Jolly", "SPD", "SPATK"],
    ["Lax", "DEF", "SPDEF"],
    ["Lonely", "ATK", "DEF"],
    ["Mild", "SPATK", "DEF"],
    ["Modest", "SPATK", "ATK"],
    ["Naive", "SPD", "SPDEF"],
    ["Naughty", "ATK", "SPDEF"],
    ["Quiet", "SPATK", "SPD"],
    ["Quirky", "SPDEF", "SPDEF"],
    ["Rash", "SPATK", "SPDEF"],
    ["Relaxed", "DEF", "SPD"],
    ["Sassy", "SPDEF", "SPD"],
    ["Serious", "SPD", "SPD"],
    ["Timid", "SPD", "ATK"]
]