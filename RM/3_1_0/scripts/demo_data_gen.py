#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
data_gen.py
Can be used to create multiple copies of DM based data files to use for examples or stress testing your RDF store.
Pass the number of copies per example on the commandline.
    
Copyright (C) 2016 - 2018 Data Insights, Inc., All Rights Reserved.
"""
import sys, getopt, csv
from datetime import datetime

def main(count):
   print("""
    S3Model data generator for the semantics demo.

    Copyright (C) 2016 - 2018 Data Insights, Inc., All Rights Reserved.
    See the file README.md for usage.
   """)

   print("Creating " + count + " copies of each of the three example data instances.")
   f1 = open("data/instance1.xml",'r')
   f2 = open("data/instance2.xml",'r')
   f3 = open("data/instance3.xml",'r')
   ex1 = f1.read()
   ex2 = f2.read()
   ex3 = f3.read()
   f1.close()
   f2.close()
   f3.close()

   for n in range(0,int(count)):
      out1 = open('data/1-'+str(n).zfill(12)+'.xml','w')
      out2 = open('data/2-'+str(n).zfill(12)+'.xml','w')
      out3 = open('data/3-'+str(n).zfill(12)+'.xml','w')
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


