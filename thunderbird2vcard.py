#! /usr/bin/python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Author:   Fabien Marteau <fabien.marteau@armadeus.com>
# Created:  20/08/2014
#-----------------------------------------------------------------------------
""" class thunderbird2vcard
"""

import sys
import shlex


def formatphonenum(phone_string):
    return phone_string.replace(" ",'').replace('.', '')

if __name__ == "__main__":
    filein = open(sys.argv[1], "r")
    champs = [value.strip() for value in filein.readline().split(",")]
    print(str(champs))
    print(str(len(champs)) + " champs")

    contacts = []
    for line in filein:
        line = line.strip().replace(",",", ")  #XXX Garder les champs vide !
        myshlex = shlex.shlex(line, posix=True)
        myshlex.whitespace = ","
        myshlex.quotes = '"'
        myshlex.whitespace_split = True
        record = [value.strip() for value in list(myshlex)]
        contacts.append(dict(zip(champs, record)))
    filein.close()

    fileout = open(sys.argv[2], "w")
    for record in contacts:
        fileout.write("BEGIN:VCARD\n")
        fileout.write("VERSION:4.0\n")
        fileout.write("n:" + record.get("Last Name", '') +
                      ";" + record.get("First Name", '') +
                      ";;;;\n")
        if record["Display Name"] == '':
            fileout.write("fn:" + record.get("First Name", '') +
                          " " + record.get("Last Name", '') + "\n")
        else:
            fileout.write("fn:" + record.get("Display Name", '') + "\n")
        
        if record.get("Primary Email", '') != '':
            fileout.write("email;type=internet,home,pref:" +
                          record["Primary Email"] + "\n")
        if record.get("Secondary Email", '') != '':
            fileout.write("email;type=internet,home,pref:" +
                          record["Secondary Email"] + "\n")

        value = record.get("Work Phone", '')
        if value != '':
            fileout.write("tel;type=work:" +
                          formatphonenum(value) +
                          "\n")
        value = record.get("Home Phone", '')
        if value != '':
            fileout.write("tel;type=home:" +
                          formatphonenum(value) +
                          "\n")
        value = record.get("Mobile Number", '')
        if value != '':
            fileout.write("tel;type=cell:" +
                          formatphonenum(value) +
                          "\n")
        #home address
        homeadress = record.get("Home Address", '') +\
                     " " +\
                     record.get("Home Address 2", '')

        fileout.write("adr;type=home:;;" +
                      homeadress.strip() +
                      ";" +
                      record.get("Home City", '') +
                      ";" +
                      record.get("Home State", '') +
                      ";" +
                      record.get("Home ZipCode", '') +
                      ";" +
                      record.get("Home Country", '') +
                      "\n")

        #home address
        workadress = record.get("Work Address", '') +\
                     " " +\
                     record.get("Work Address 2", '')

        fileout.write("adr;type=home:;;" +
                      workadress.strip() +
                      ";" +
                      record.get("Work City", '') +
                      ";" +
                      record.get("Work State", '') +
                      ";" +
                      record.get("Work ZipCode", '') +
                      ";" +
                      record.get("Work Country", '') +
                      "\n")
        fileout.write("END:VCARD\n")
    fileout.close()
