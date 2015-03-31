#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    data_gen.py

    MLHIM 2.4.6 (and later) data instance generator for the semantics demo.

    Copyright (C) 2014 Timothy W. Cook tim@mlhim.org

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import sys, getopt, csv
from datetime import datetime

def main(count):
   print("""
    MLHIM data generator for the semantics demo.

    Copyright (C) 2014, Timothy W. Cook
    See the file README.md for usage.

    This program comes with ABSOLUTELY NO WARRANTY;
    This is free software, and you are welcome to redistribute it
    under certain conditions. See the LICENSE for details.
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


