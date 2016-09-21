#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    data_gen.py

    S3Model 3.0.0 (and later) data instance generator.

    Copyright (C) 2016 Data Insights, Inc., All Rights Reserved.
"""
import sys, getopt, csv
from datetime import datetime

def main(count):
   print("""
    S3Model data generator for the semantics demo.

    Copyright (C) 2016 Data Insights, Inc., All Rights Reserved.
    See the file README.md for usage.
   """)

   print("Creating " +count+ " copies of each of the three example data instances.")
   f1 = open("data/ccd-7af79fef-9a2b-4f5f-8a94-a3655b4f4e37.xml",'r')
   f2 = open("data/ccd-a44dba62-f284-477e-a52e-9b491dbb5328.xml",'r')
   f3 = open("data/ccd-d382c66e-c4b3-4add-b4f2-f10eb655d7e3.xml",'r')
   ex1 = f1.read()
   ex2 = f2.read()
   ex3 = f3.read()
   f1.close()
   f2.close()
   f3.close()

   for n in range(0,int(count)):
      out1 = open('data/f4e37-'+str(n).zfill(12)+'.xml','w')
      out2 = open('data/b5328-'+str(n).zfill(12)+'.xml','w')
      out3 = open('data/5d7e3-'+str(n).zfill(12)+'.xml','w')
      out1.write(ex1)
      out2.write(ex2)
      out3.write(ex3)
      out1.close()
      out2.close()
      out3.close()

   print("\n\n Finished generating the copies.\n\n")

if __name__ == "__main__":
   if len(sys.argv) < 2:
      print('\nYou must include a number greater that zero on the commandline. \n\n')
   else:
      count = sys.argv[1:][0]
      if count.isdigit():
         main(count)
      else:
         print('\nYou must include a number greater that zero on the commandline. \n\n')


