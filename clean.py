import os
import subprocess

if os.path.exists('prepro'):
    subprocess.run(["rm", "-r", "prepro"], check=True)

if os.path.exists('postpro'):
    subprocess.run(["rm", "-r", "postpro"], check=True)

if os.path.exists('pksprites'):
    subprocess.run(["rm", "-r", "pksprites"], check=True)

if os.path.exists('leads.csv'):
    os.remove('leads.csv')
if os.path.exists('metagame.csv'):
    os.remove('metagame.csv')
if os.path.exists('moveset.csv'):
    os.remove('moveset.csv')
if os.path.exists('basic.csv'):
    os.remove('basic.csv')

if os.path.exists('leads.db'):
    os.remove('leads.db')
if os.path.exists('metagame.db'):
    os.remove('metagame.db')
if os.path.exists('moveset.db'):
    os.remove('moveset.db')
if os.path.exists('basic.db'):
    os.remove('basic.db')

if os.path.exists('pokemon.db'):
    os.remove('pokemon.db')
if os.path.exists('abilities.db'):
    os.remove('abilities.db')
if os.path.exists('items.db'):
    os.remove('items.db')
if os.path.exists('moves.db'):
    os.remove('moves.db')
