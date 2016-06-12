#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
analyze.py

Analyze the CSV file passed on the command line and output the model config file.
"""
import sys
import os
import csv
import sqlite3


def main(theFile):
    """
    Load and analyze.

   CREATE TABLE "model" ("title" CHAR(250), "description" TEXT, "copyright" CHAR(250), "author" CHAR(250), "contributors" TEXT)

    CREATE TABLE "record"
           (header  char(100), label char(250), datatype char(10), minlen int, maxlen int, "choices" TEXT, "regex" CHAR(250), "minval" FLOAT, "maxval" FLOAT, "valInclusive" BOOL, "url" CHAR(500))


    """

    conn = sqlite3.connect('analyze.sqlite')
    c = conn.cursor()

    data = []
    with open(theFile) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for h in reader.fieldnames:
            print('Adding: ', h)
            data.append((h,h,'String',0,0,'','',0,0,True,'',''))

    c.executemany("INSERT INTO csv VALUES (?,?,?,?,?)", data)
    conn.commit()
    conn.close()


    return


if __name__ == '__main__':
    csvFile = sys.argv[1:][0]
    main(csvFile)
    print("\n\nFinished! \nCreated: Model Config file for: " + csvFile + " .\n\n")
    sys.exit(0)

