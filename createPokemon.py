import sqlite3
import os
import csv
import dask
dask.config.set({'dataframe.query-planning': True})
import dask.dataframe as dd

def createDB():
  if os.path.exists('pokemon.db'):
    os.remove('pokemon.db')
    print("pokemon.db deleted successfully")
  else:
    print("pokemon.db does not exist")

  if os.path.exists('abilities.db'):
    os.remove('abilities.db')
    print("abilities.db deleted successfully")
  else:
    print("abilities.db does not exist")

  if os.path.exists('moves.db'):
    os.remove('moves.db')
    print("moves.db deleted successfully")
  else:
    print("moves.db does not exist")

  if os.path.exists('items.db'):
    os.remove('items.db')
    print("items.db deleted successfully")
  else:
    print("items.db does not exist")

  sql_create_pokemon_table = """ CREATE TABLE IF NOT EXISTS pokemon (
      Number INT,
      Pokemon TEXT,
      Type1 TEXT,
      Type2 TEXT,
      HP INT,
      ATK INT,
      DEF INT,
      SPATK INT,
      SPDEF INT,
      SPD INT,
      Ability1 TEXT,
      Ability2 TEXT,
      Hidden TEXT
  ); """

  sql_create_abilities_table = """ CREATE TABLE IF NOT EXISTS abilities (
      Ability TEXT,
      Desc TEXT
  ); """

  sql_create_moves_table = """ CREATE TABLE IF NOT EXISTS moves (
      Move TEXT,
      Type TEXT,
      Category TEXT,
      Power INT,
      Accuracy FLOAT,
      PP INT,
      Effect TEXT,
      Probability FLOAT
  ); """

  sql_create_items_table = """ CREATE TABLE IF NOT EXISTS items (
      Item TEXT,
      Desc TEXT
  ); """

  sql_insert_pokemon_row = """
    INSERT INTO pokemon (Number, Pokemon, Type1, Type2, HP, ATK, DEF, SPATK, SPDEF, SPD, Ability1, Ability2, Hidden)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  """

  sql_insert_abilities_row = """
      INSERT INTO abilities (Ability, Desc)
        VALUES (?, ?)
  """

  sql_insert_moves_row = """
      INSERT INTO moves (Move, Type, Category, Power, Accuracy, PP, Effect, Probability)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  """

  sql_insert_items_row = """
      INSERT INTO items (Item, Desc)
        VALUES (?, ?)
  """

  pokemonConn = sqlite3.connect('pokemon.db')
  abilitiesConn = sqlite3.connect('abilities.db')
  movesConn = sqlite3.connect('moves.db')
  itemsConn = sqlite3.connect('items.db')

  pokemonCursor = pokemonConn.cursor()
  abilitiesCursor = abilitiesConn.cursor()
  movesCursor = movesConn.cursor()
  itemsCursor = itemsConn.cursor()

  pokemonCursor.execute(sql_create_pokemon_table)
  abilitiesCursor.execute(sql_create_abilities_table)
  movesCursor.execute(sql_create_moves_table)
  itemsCursor.execute(sql_create_items_table)

  #pokemon.db
  print("Creating pokemon.db")
  with open("pokemon.csv", "r") as pk1:

    csvReader = csv.reader(pk1)
    next(csvReader)

    for row in csvReader:
      Number, Pokemon, Type1, Type2, HP, ATK, DEF, SPATK, SPDEF, SPD, Ability1, Ability2, Hidden = row
      pokemonCursor.execute(sql_insert_pokemon_row, (Number, Pokemon, Type1, Type2, HP, ATK, DEF, SPATK, SPDEF, SPD, Ability1, Ability2, Hidden))

  pokemonConn.commit()
  pokemonConn.close()

  #abilities.db
  print("Creating abilities.db")
  with open("abilities.csv", "r") as pk1:

    csvReader = csv.reader(pk1)
    next(csvReader)

    for row in csvReader:
      Ability, Desc = row
      abilitiesCursor.execute(sql_insert_abilities_row, (Ability, Desc))

  abilitiesConn.commit()
  abilitiesConn.close()

  #moves.db
  print("Creating moves.db")
  with open("moves.csv", "r") as pk1:

    csvReader = csv.reader(pk1)
    next(csvReader)

    for row in csvReader:
      Move, Type, Category, Power, Accuracy, PP, Effect, Probability = row
      movesCursor.execute(sql_insert_moves_row, (Move, Type, Category, Power, Accuracy, PP, Effect, Probability))

  movesConn.commit()
  movesConn.close()

  #items.db
  print("Creating items.db")
  with open("items.csv", "r") as pk1:

    csvReader = csv.reader(pk1)
    next(csvReader)

    for row in csvReader:
      Item, Desc = row
      itemsCursor.execute(sql_insert_items_row, (Item, Desc))

  itemsConn.commit()
  itemsConn.close()
