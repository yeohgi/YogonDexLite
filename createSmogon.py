import sqlite3
import os
import csv
import dask
dask.config.set({'dataframe.query-planning': True})
import dask.dataframe as dd

def createDB():

  if os.path.exists('leads.db'):
    os.remove('leads.db')
    print("leads.db deleted successfully")
  else:
    print("leads.db does not exist")

  if os.path.exists('metagame.db'):
    os.remove('metagame.db')
    print("metagame.db deleted successfully")
  else:
    print("metagame.db does not exist")

  if os.path.exists('moveset.db'):
    os.remove('moveset.db')
    print("moveset.db deleted successfully")
  else:
    print("moveset.db does not exist")

  if os.path.exists('basic.db'):
    os.remove('basic.db')
    print("basic.db deleted successfully")
  else:
    print("basic.db does not exist")
      
  sql_create_lead_table = """ CREATE TABLE IF NOT EXISTS leads (
      Year INT,
      Month INT,
      Format TEXT,
      Rank INT,
      Pokemon TEXT,
      Usage FLOAT,
      Raw TEXT,
      Percent FLOAT
  ); """

  sql_create_metagame_table = """ CREATE TABLE IF NOT EXISTS metagame (
      Year INT,
      Month INT,
      Format TEXT,
      Meta TEXT,
      Percent FLOAT,
      Stall FLOAT
  ); """

  sql_create_moveset_table = """ CREATE TABLE IF NOT EXISTS moveset (
      Year INT,
      Month INT,
      Format TEXT,
      Pokemon TEXT,
      Raw INT,
      Abilities TEXT,
      Items TEXT,
      Spreads TEXT,
      Moves TEXT,
      Teammates TEXT
  ); """

  sql_create_basic_table = """ CREATE TABLE IF NOT EXISTS basic (
      Year INT,
      Month INT,
      Format TEXT,
      Rank INT,
      Pokemon TEXT,
      Usage FLOAT,
      Raw INT,
      Raw_Percent FLOAT,
      Real INT,
      Real_Percent FLOAT
  );"""

  sql_insert_lead_row = """
    INSERT INTO leads (Year, Month, Format, Rank, Pokemon, Usage, Raw, Percent)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  """

  sql_insert_metagame_row = """
      INSERT INTO metagame (Year, Month, Format, Meta, Percent, Stall)
        VALUES (?, ?, ?, ?, ?, ?)
  """

  sql_insert_moveset_row = """
      INSERT INTO moveset (Year, Month, Format, Pokemon, Raw, Abilities, Items, Spreads, Moves, Teammates)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  """

  sql_insert_basic_row = """
      INSERT INTO basic (Year, Month, Format, Rank, Pokemon, Usage, Raw, Raw_Percent, Real, Real_Percent)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  """

  leadsConn = sqlite3.connect('leads.db')
  metagameConn = sqlite3.connect('metagame.db')
  movesetConn = sqlite3.connect('moveset.db')
  basicConn = sqlite3.connect('basic.db')

  leadsCursor = leadsConn.cursor()
  metagameCursor = metagameConn.cursor()
  movesetCursor = movesetConn.cursor()
  basicCursor = basicConn.cursor()

  leadsCursor.execute(sql_create_lead_table)
  metagameCursor.execute(sql_create_metagame_table)
  movesetCursor.execute(sql_create_moveset_table)
  basicCursor.execute(sql_create_basic_table)

  #leads
  print("Creating leads.csv")
  with open("leads.csv", "w") as pk1:
    pk1.write("Year,Month,Format,Rank,Pokemon,Usage,Raw,Percent\n")
    for folder in os.listdir('postpro'):
      for file in os.listdir(f'postpro/{folder}/leads/'):
        with open("./postpro/" + folder + "/leads/" + file, "r") as pk2:
          year = folder.split('-')[0]
          month = folder.split('-')[1]
          if(len(folder.split('-')) > 2):
            month += '-' + folder.split('-')[2]
          format = file.split('.')[0]
          pk2.readline()
          for line in pk2:
            pk1.write(year + ',' + month + ',' + format + ',' + line)

  sortLeads = ['Year', 'Month','Format','Rank']
  df = dd.read_csv('leads.csv', low_memory=False)
  dfSorted = df.sort_values(sortLeads).compute()
  dfSorted.to_csv('leads.csv', index=False)

  #leads.db
  print("Creating leads.db")
  with open("leads.csv", "r") as pk1:

    csvReader = csv.reader(pk1)
    next(csvReader)

    for row in csvReader:
      year, month, format_, rank, pokemon, usage, raw, percent = row
      leadsCursor.execute(sql_insert_lead_row, (year, month, format_, rank, pokemon, usage, raw, percent))

  leadsConn.commit()
  leadsConn.close()

  #metagame
  print("Creating metagame.csv")
  with open("metagame.csv", "w") as pk1:
    pk1.write("Year,Month,Format,Meta,Percent,Stall\n")
    for folder in os.listdir('postpro'):
      for file in os.listdir(f'postpro/{folder}/metagame/'):
        with open("./postpro/" + folder + "/metagame/" + file, "r") as pk2:
          year = folder.split('-')[0]
          month = folder.split('-')[1]
          if(len(folder.split('-')) > 2):
            month += '-' + folder.split('-')[2]
          format = file.split('.')[0]
          pk2.readline()
          for line in pk2:
            pk1.write(year + ',' + month + ',' + format + ',' + line)

  sortMetagame = ['Year', 'Month','Format']
  df = dd.read_csv('metagame.csv', low_memory=False)
  dfSorted = df.sort_values(sortMetagame).compute()
  dfSorted.to_csv('metagame.csv', index=False)

  #metagame.db
  print("Creating metagame.db")
  with open("metagame.csv", "r") as pk1:

    csvReader = csv.reader(pk1)
    next(csvReader)

    for row in csvReader:
      year, month, format_, meta, percent, stall = row
      metagameCursor.execute(sql_insert_metagame_row, (year, month, format_, meta, percent, stall))

  metagameConn.commit()
  metagameConn.close()

  #moveset
  print("Creating moveset.csv")
  with open("moveset.csv", "w") as pk1:
    pk1.write("Year,Month,Format,Pokemon,Raw,Abilities,Items,Spreads,Moves,Teammates\n")
    for folder in os.listdir('postpro'):
      for file in os.listdir(f'postpro/{folder}/moveset/'):
        with open("./postpro/" + folder + "/moveset/" + file, "r") as pk2:
          year = folder.split('-')[0]
          month = folder.split('-')[1]
          if(len(folder.split('-')) > 2):
            month += '-' + folder.split('-')[2]
          format = file.split('.')[0]
          pk2.readline()
          for line in pk2:
            pk1.write(year + ',' + month + ',' + format + ',' + line)


  sortMoveset = ['Year', 'Month','Format','Raw']
  df = dd.read_csv('moveset.csv', low_memory=False)
  dfSorted = df.sort_values(sortMoveset).compute()
  dfSorted.to_csv('moveset.csv', index=False)

  #moveset.db
  print("Creating moveset.db")
  with open("moveset.csv", "r") as pk1:

    csvReader = csv.reader(pk1)
    next(csvReader)

    for row in csvReader:
      year, month, format_, pokemon, raw, abilities, items, spreads, moves, teammates = row
      movesetCursor.execute(sql_insert_moveset_row, (year, month, format_, pokemon, raw, abilities, items, spreads, moves, teammates))

  movesetConn.commit()
  movesetConn.close()


  #basic
  print("Creating basic.csv")
  with open("basic.csv", "w") as pk1:
    pk1.write("Year,Month,Format,Rank,Pokemon,Usage,Raw,Raw_Percent,Real,Real_Percent\n")
    for folder in os.listdir('postpro'):
      for file in os.listdir(f'postpro/{folder}'):
        if file.endswith('.txt'):
          with open("./postpro/" + folder + "/" + file, "r") as pk2:
            year = folder.split('-')[0]
            month = folder.split('-')[1]
            if(len(folder.split('-')) > 2):
              month += '-' + folder.split('-')[2]
            format = file.split('.')[0]
            pk2.readline()
            for line in pk2:
              pk1.write(year + ',' + month + ',' + format + ',' + line)

  sortBasic = ['Year', 'Month','Format','Rank']
  df = dd.read_csv('basic.csv', low_memory=False)
  dfSorted = df.sort_values(sortBasic).compute()
  dfSorted.to_csv('basic.csv', index=False)
      
  #basic.db
  print("Creating basic.db")
  with open("basic.csv", "r") as pk1:

    csvReader = csv.reader(pk1)
    next(csvReader)

    for row in csvReader:
      year, month, format_, rank, pokemon, usage, raw, raw_percent, real, real_percent = row
      basicCursor.execute(sql_insert_basic_row, (year, month, format_, rank, pokemon, usage, raw, raw_percent, real, real_percent))

  basicConn.commit()
  basicConn.close()
     




