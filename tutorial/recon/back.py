# !/usr/bin/env python
import sys
import os
import subprocess
from datetime import date
import sqlite3
import csv

class backProcess():

    def configurer_fichier (url) :
        today = date.today()
        filename = url + "-" + str(today) + ".txt"
        modules = {
            "recon/domains-hosts/google_site_web",
            "recon/domains-hosts/bing_domain_web",
            "recon/domains-hosts/netcraft"
        }

        target = open (filename, 'w')

        target.write("workspaces select "+ url + "-" + str(today) + '\n')
        #print("workspaces select"+ url + "-" + str(today) + '\n')
        for m in modules :
            target.write("use " + m + '\n')
            target.write("set SOURCE "+ url + '\n')
            target.write("run " + '\n')

        #print ("modules added to the file ")

        target.write("use recon/domains-hosts/brute_hosts" + '\n')
        target.write("set SOURCE " + url + '\n')
        target.write("run " + '\n')

        target.write("use recon/hosts-hosts/resolve" + '\n')
        target.write("set SOURCE default " + '\n')

        target.write("use reporting/csv " + '\n')
        target.write("run " + '\n')

        target.write("exit() " + '\n')

        target.close()

        #print ("file created")
        return filename

    def collecte_info_sqlite (url) :
        today = date.today()
        print("/root/.recon-ng/workspaces/"+ url + "-" + str(today) + "/data.db")
        aa = "/root/.recon-ng/workspaces/"+ url + "-" + str(today) + "/data.db"
        conn = sqlite3.connect(aa)
        cursor = conn.cursor()
        cursor.execute("""SELECT host,ip_address FROM hosts""")
        raws = cursor.fetchall()
        print (type(raws))
        for i in range(0,len(raws)):
            print (raws[i])
        print("all data collected")

    def collecte_info_csv (url):
        today = date.today()
        fp = open("/root/.recon-ng/workspaces/" + url + "-" + str(today) + "/results.csv")
        fcsv = csv.reader(fp)
        for ligne in fcsv:
            print(ligne[0] + ', ' + ligne[1] + ', ' + ligne[6])

    def globalProcess(url):


        pwd = os.getcwd()
        dir = os.path.join(pwd, '')

        filename = backProcess.configurer_fichier(url)

        respath = os.path.join(pwd, str(filename))

        subprocess.call('recon-ng -r ' + respath, shell=True)

        backProcess.collecte_info_sqlite(url)

        backProcess.collecte_info_csv(url)

        print ("done !")
