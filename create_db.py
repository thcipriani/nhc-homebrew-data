#!/usr/bin/env python

import os
import sys
import json
import subprocess
from tempfile import mkstemp
import sqlite3

reload(sys)
sys.setdefaultencoding("utf-8")

db_filename = 'nhc.db'
db_is_new = not os.path.exists(db_filename)
conn = sqlite3.connect(db_filename)

# cookies
headers = sys.argv[1]

base = os.path.dirname(__file__)
winner_html = os.path.join(base, 'tmp', 'winners.html')

# using pup because this started as a Makefile :\
go_path = os.path.join(os.getenv('GOPATH'), 'bin')
pup = os.path.join(go_path, 'pup')

def fill_db():
    with open(os.path.join(base, 'tmp', 'id_list.txt'), 'r') as file:
        for line in file.readlines():
            line = line.strip()

            entry = "%s -i 4 '#%s " % (pup, line)
            suffix = " json{}' < %s" % winner_html

            title = json.loads(subprocess.check_output(entry + '.entry-title a' + suffix, shell=True))
            style = json.loads(subprocess.check_output(entry + 'h3[itemprop="recipeCuisine"] a' + suffix, shell=True))
            year = json.loads(subprocess.check_output(entry + '.year' + suffix, shell=True))
            vol = json.loads(subprocess.check_output(entry + '.specs span[itemprop="recipeYield"]' + suffix, shell=True))

            (_, tmp_file) = mkstemp()

            print "Grabbing %s" % title.get('text')

            curl = 'curl %s -o %s -s %s' % (headers, tmp_file, title.get('href'))
            subprocess.check_output(curl, shell=True)

            cmd = "%s '%s' < %s" % (pup, 'div[itemprop="ingredients"] ul json{}', tmp_file)
            ingredients = json.loads(subprocess.check_output(cmd, shell=True))

            if len(ingredients) == 0:
                cmd = "%s '%s' < %s" % (pup, 'div[itemprop="ingredients"] ol json{}', tmp_file)
                ingredients = json.loads(subprocess.check_output(cmd, shell=True))
                if len(ingredients) == 0:
                    ingredients = {}

            cmd = "%s '%s' < %s" % (pup, 'ul.specs json{}', tmp_file)
            specs = json.loads(subprocess.check_output(cmd, shell=True))

            if len(specs) == 0:
                cmd = "%s '%s' < %s" % (pup, 'ol.specs json{}', tmp_file)
                specs = json.loads(subprocess.check_output(cmd, shell=True))

            cmd = "%s '%s' < %s" % (pup, 'div[itemprop="recipeInstructions"] ol json{}', tmp_file)
            instructions = json.loads(subprocess.check_output(cmd, shell=True))

            if len(instructions) == 0:
                cmd = "%s '%s' < %s" % (pup, 'div[itemprop="recipeInstructions"] ul json{}', tmp_file)
                instructions = json.loads(subprocess.check_output(cmd, shell=True))
                if len(instructions) == 0:
                    instructions = {}

            os.remove(tmp_file)

            ingredients_md = "".join(["* %s\n" % li.get('text') for li in ingredients.get('children', {})])
            specs_md = "".join(["* %s\n" % li.get('text') for li in specs.get('children', [])])
            instructions_md = "".join(["* %s\n" % li.get('text') for li in instructions.get('children', {})])

            if ingredients_md == '':
                ingredients_md = None

            if specs_md == '':
                specs_md = None

            if instructions_md == '':
                instructions_md = None

            sql_insert = """
            insert into recipes (name, style, year, vol, ingredients, specs, instructions)
            values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')
            """ % ( title.get('text'), style.get('text'), year.get('text'), vol.get('text'), ingredients_md, specs_md, instructions_md)

            print "Inserting %s" % title.get('text')
            conn.execute(sql_insert)
            conn.commit()

    conn.close()


def check_db():
    if db_is_new:
        print 'Need to create schema'
        with open('nhc_schema.sql', 'rt') as f:
            schema = f.read()
        conn.executescript(schema)

if __name__ == '__main__':
    check_db()
    fill_db()

