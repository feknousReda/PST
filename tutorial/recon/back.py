# !/usr/bin/env python
import sys
import os
import subprocess
from datetime import date
import sqlite3
import csv


class backProcess():

    def configurer_fichier (url, selected_modules) :
        today = date.today()
        filename = url + "-" + str(today) + ".txt"
        modules = {
            "recon/domains-hosts/google_site_web",
            "recon/domains-hosts/bing_domain_web",
            "recon/domains-hosts/netcraft",
            "recon/domains-hosts/hackertarget",
            "recon/domains-hosts/brute_hosts"

        }

        with open (filename, 'w') as target:

            target.write("workspaces select "+ url + "-" + str(today) + '\n')
        #print("workspaces select"+ url + "-" + str(today) + '\n')
            for m in selected_modules :
                target.write("use " + "recon/domains-hosts/" + m + '\n')
                target.write("set SOURCE "+ url + '\n')
                target.write("run " + '\n')

        #print ("modules added to the file ")

            target.write("use recon/hosts-hosts/resolve" + '\n')
            target.write("set SOURCE default " + '\n')

            target.write("use reporting/csv " + '\n')
            target.write("run " + '\n')

            target.write("exit() " + '\n')

            #target.close()

        #print ("file created")
        return filename

    def collecte_info_sqlite (url,selected_modules) :
        today = date.today()
        print("/root/.recon-ng/workspaces/"+ url + "-" + str(today) + "/data.db")
        aa = "/root/.recon-ng/workspaces/"+ url + "-" + str(today) + "/data.db"
        conn = sqlite3.connect(aa)
        cursor = conn.cursor()
        strmoduls = "module = 'hackertarget' OR module = 'netcraft'"
        strmoduls = ""
        for m in selected_modules:
            strmoduls = strmoduls + "module = '" + m + "' OR "
        strmoduls = strmoduls[:-3]
        cursor.execute("""SELECT host,ip_address,module FROM hosts WHERE %s""" %strmoduls)
        raws = cursor.fetchall()
        print (type(raws))
        for i in range(0,len(raws)):
            print (raws[i])
        print("all data collected")
        return raws

    def collecte_info_csv (url):
        today = date.today()
        fp = open("/root/.recon-ng/workspaces/" + url + "-" + str(today) + "/results.csv")
        fcsv = csv.reader(fp)
        for ligne in fcsv:
            print(ligne[0] + ', ' + ligne[1] + ', ' + ligne[6])
        return fcsv
    def globalProcess(url, selected_modules):


        pwd = os.getcwd()
        dir = os.path.join(pwd, '')

        filename = backProcess.configurer_fichier(url, selected_modules)

        respath = os.path.join(pwd, str(filename))

        while True:
            try:
                subprocess.call('recon-ng -r ' + respath, shell=True)
                break
            except ValueError:
                print('Recon-ng is not working')

        raws = backProcess.collecte_info_sqlite(url,selected_modules)

        fcsv = backProcess.collecte_info_csv(url)

        print ("done !")
        return raws
