import requests
import json
import smtplib
import configparser
import sys

config = configparser.RawConfigParser()#load config parser
configFilePath = r'C:\Users\ccampagn\Documents\Python\weathertext\config.ini'#file path of config file
config.read(configFilePath)#read config file

try:
    fromaddr = config.get('file', 'from')#get fromaddr from file
    toaddrs = config.get('file', 'to')#get toaddrs from file
    username = config.get('file', 'username')#get username from file
    password = config.get('file', 'password')#get password from file
    mailserver = config.get('file', 'mailserver')#get mailserver from file
    apikey = config.get('file', 'apikey')#get apikey from file
except configparser.NoOptionError :#except with no options error
    print('could not read configuration file')#Error message if can't read 
    sys.exit(1)  #exit program on error
try:
    page = requests.get("https://api.weatherbit.io/v2.0/forecast/daily?city=Kendall+Park,NJ&units=I&days=1&key="+apikey)#request for api
    data=page.json()#parse data into dict
    weather={"temp":data["data"][0]["temp"],"maxtemp":data["data"][0]["max_temp"],"mintemp":data["data"][0]["min_temp"],"pop":data["data"][0]["pop"],"precip":data["data"][0]["precip"]}#create dict for result
except:#except with no options error
    print('Failed to retieve api data')#Error message if can't read 
    sys.exit(1)  #exit program on error
msg='''
Max Temp:'''+str(weather['maxtemp'])+"\n Min Temp:"+str(weather['mintemp'])+"\n Precip Chance:"+str(weather['pop'])+"\n Precip Amount:"+str(weather['precip'])#create the msg to be sent

server = smtplib.SMTP(mailserver)#set the mail server to be use
server.ehlo()#identify it self to mail server
server.starttls()#start secure connection
server.login(username,password)#login with username/password
server.sendmail(fromaddr, toaddrs, msg)#send mail using the msg
server.quit()#exit the server