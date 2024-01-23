import requests
import json
from mcstatus import JavaServer

for un in range(116,117):
    for deux in range(1,256):
        for trois in range(1,256):
            for quatre in range(1,256):
                ip = str(un)+'.'+str(deux)+'.'+str(trois)+'.'+str(quatre)+':25565'
                try:
                    server = JavaServer.lookup(ip)
                    status = server.status()
                    print(ip, '| ON')
                    f=open("IP.txt", "w", encoding='utf-8')
                    f.write(ip,"\n")
                    f.close()
                except:
                    print(ip,'| OFF')