#!/usr/bin/python3

import urllib.request
from bs4 import BeautifulSoup
import os
import pymysql
#import shutil
from urllib.parse import urljoin

def get_name(link):
    f_name = link
    start = f_name.find('/')
    while (start > -1) and (len (f_name[start+1:]) >2):
        f_name = f_name[start+1:]
        start = f_name.find('/') 
    if start > -1:
        f_name = f_name[:-1]
    return f_name

def download_file(download_url):
    f_name = get_name(download_url)
    sql = "SELECT EXISTS ( SELECT * FROM loaded WHERE (name,link) = ('%s', '%s'))" %(f_name, download_url)
    try:
        cursor.execute(sql)
    except:
        print("Error accessing DB")
        return
    data = cursor.fetchone()
    if data[0] == 0 :
        try:
            web_file = urllib.request.urlopen(download_url)
            local_file = open(f_name, 'wb')
            local_file.write(web_file.read())
            web_file.close()
            local_file.close()
        except :
            print ("COULDN'T LOAD FILE  "+download_url)
            return
        sql = "INSERT INTO loaded(`name`, `link`) VALUES ('%s', '%s')" % (f_name, download_url)
        try:
           cursor.execute(sql)
           db.commit()
        except:
           print("Error using DB")
           db.rollback()


def clear_db() :
    sql = "TRUNCATE TABLE seen;"
    try:
       cursor.execute(sql)
       db.commit()
    except:
       print("Error cleaning DB")
       db.rollback()    
#    sql = "TRUNCATE TABLE loaded;"
#    try:
#       cursor.execute(sql)
#       db.commit()
#    except:
#       print("Error cleaning DB")
#       db.rollback()    


def walk_through(url): #, w_t):
    try:
        html = urllib.request.urlopen(url)
    except :
        print ("COULDN'T CONNECT TO WEBSITE  "+url)
        return
    if (html.geturl() != url) :
        return
 #   w_t.write(url + '\n')
    sql = "INSERT INTO seen(name) VALUES ('%s')" % url
    try:
       cursor.execute(sql)
       db.commit()
    except:
       print("Error using DB")
       db.rollback()
    soup = BeautifulSoup(html, "lxml")
    for link in soup.find_all('a'):
        l1 = link.get('href')
        if (l1 != None) and ((l1.endswith('.pdf')) or (l1.endswith('.doc') or (l1.endswith('.docx')))) :
            l1 = urljoin(url, l1)
            download_file(l1)          
        else :
            if (l1 != None) and ((l1.endswith('.html')) or (l1.endswith('.htm')) or (l1.endswith('/'))) :
                if (l1.startswith('www')) or (l1.startswith('http')) :
                    if (l1.startswith(url)) :
                        l1 = l1
                    else :
                        continue
                l1 = urljoin(url, l1)
                sql = "SELECT EXISTS(SELECT 1 FROM seen WHERE name ='%s' LIMIT 1)" %l1
                try:
                    cursor.execute(sql)
                    data = cursor.fetchone()
                    if data[0] == 0:
                        walk_through(l1) #, w_t)
                except:
                    return 

# Open database connection
db = pymysql.connect("localhost","testuser","test123","websites" )
# prepare a cursor object using cursor() method
cursor = db.cursor()
clear_db()
f3 = open('sites.txt', 'r')
if not(os.path.isdir("library")):
#    shutil.rmtree("library")
    os.mkdir("library")
os.chdir('./'+"library")
for url in f3:
    if (url.isspace() == False) :
        print("----- starting: " + url)
        url = url[:-1]
        dirname = get_name(url)
        if not(os.path.isdir(dirname)):
            #shutil.rmtree(dirname)
            os.mkdir(dirname)
        os.chdir('./'+dirname)
#        r_m = open ("README.txt", 'w')
#        r_m.write("These files are downloaded from the website "+url)
#        r_m.close()
#        w_t = open ("WayThrough.txt", 'w')
        walk_through(url)#, w_t)
#        w_t.close()
        os.chdir('../')
f3.close()
# disconnect from server
db.close()
print ("READY")
