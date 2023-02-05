from faker import Faker
import time
from datetime import datetime
import random
import ipaddress
import mysql.connector

dbconn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="",
    database="cn"
)

mycursor = dbconn.cursor()
if(dbconn):
    print("Connected")


fake = Faker()

bytessent = random.randint(1000, 16000)
dt = datetime.now()
str_date_time = dt.strftime("%d/%b/%Y:%H:%M:%S")
ip = fake.ipv4()
country = fake.country()
ua = fake.user_agent()
method = ["POST", "GET"]

def user():
    request_url = ["GET /registration HTTP/1.1", "GET /login HTTP/1.1", "POST /api/login HTTP/1.1",
                   "POST /api/registration HTTP/1.1", "GET /redeem HTTP/1.1", "POST /api/redeem/verification HTTP/1.1"]
    global str_date_time
    bytessent = random.randint(1000, 16000)

    print("Staring session for LEGIT USER....")
    print("User logged In....")
    uriuser = random.choice(request_url)
    print(ip + " ~ " + str_date_time + " ~ " + country + " ~ " + uriuser + " ~ " + str(bytessent) + " ~ " + ua)
    stmt = "INSERT INTO access(ip, time, area, url, useragent, bytesent) VALUES(%s, %s, %s, %s, %s, %s)"
    values = (ip, str_date_time, country, uriuser, ua, str(bytessent))
    mycursor.execute(stmt, values)
    dbconn.commit()

    for x in range(5, random.randint(10,20)):
        dt = datetime.now()
        delay = random.randint(2, 6)
        bytessent = random.randint(1000, 16000)
        str_date_time = dt.strftime("%d/%b/%Y:%H:%M:%S")
        print("User visiting " + str(delay) + " Seconds")
        print(ip + " ~ " + str_date_time + " ~ " + country + " ~ " + random.choice(
            method) + " /" + fake.uri_path() + " HTTP/1.1" + " ~ " + str(bytessent) + " ~ " + ua)
        uri = random.choice(method) + " /" + fake.uri_path() + " HTTP/1.1"
        stmt = "INSERT INTO access(ip, time, area, url, useragent, bytesent) VALUES(%s, %s, %s, %s, %s, %s)"
        values = (ip, str_date_time, country, uri, ua, str(bytessent))
        mycursor.execute(stmt, values)
        dbconn.commit()
        time.sleep(delay)

    print("Session ended")

def attacker():
    # ATTACKER
    print("ATTACK\n")

    request_url_pattern_1 = ["GET /login HTTP/1.1", "POST /api/login HTTP/1.1",
                             "POST /api/redeem/verification HTTP/1.1"]
    request_url_pattern_2 = ["GET /login HTTP/1.1", "POST /api/login HTTP/1.1"]
    patterns = [request_url_pattern_1, request_url_pattern_2]

    #0 = same ip - multiple req
    #1 = ip within range
    scenario = [0,1]

    scene = random.choice(scenario)

    #subnet = str(ip1) +"."+ str(ip2) +"."+ str(ip3) +"."+ str(ip4)
    #subnet = "192.168.0.0/32"
    #print(subnet)
    cls = fake.ipv4_network_class()
    bytessent = random.randint(2500, 5000)

    dt = datetime.now()
    delay = random.randint(1, 2)
    str_date_time = dt.strftime("%d/%b/%Y:%H:%M:%S")
    p = random.choice(patterns)

    if(scene == 0):
        ip = fake.ipv4_public(address_class=cls)
        for x in range(1, random.randint(1,15)):
            for i in range(0, len(p)):
                print("User visiting " + str(delay) + " Seconds")
                print(ip + " ~ " + str_date_time + " ~ " + country + " ~ " + p[i] + " ~ " + str(bytessent) + " ~ " + ua)
                stmt = "INSERT INTO access(ip, time, area, url, useragent, bytesent) VALUES(%s, %s, %s, %s, %s, %s)"
                values = (ip, str_date_time, country, p[i], ua, str(bytessent))
                mycursor.execute(stmt, values)
                dbconn.commit()
                time.sleep(delay)
    else:
        ip = fake.ipv4_public()
        ip1 = str(ip).split(".")[0]
        ip2 = str(ip).split(".")[1]
        ip3 = str(ip).split(".")[2]
        for x in range(1, random.randint(5,20)):
            ip = ip1 + "." + ip2 + "." + ip3 + "." + str(random.randint(0,255))
            #ips = [str(ip) for ip in ipaddress.IPv4Network(subnet)]
            #print(ips)
            #ip = random.choice(ips)
            #ip = fake.ipv4_public(address_class=cls)
            #print(ip)

            p = random.choice(patterns)
            for i in range(0, len(p)):
                print("User visiting " + str(delay) + " Seconds")
                print(ip + " ~ " + str_date_time + " ~ " + country + " ~ " + p[i] + " ~ " + str(bytessent) + " ~ " + ua)
                stmt = "INSERT INTO access(ip, time, area, url, useragent, bytesent) VALUES(%s, %s, %s, %s, %s, %s)"
                values = (ip, str_date_time, country, p[i], ua, str(bytessent))
                mycursor.execute(stmt, values)
                dbconn.commit()
                time.sleep(delay)
        print("Session ended")

while True:
    types = [0, 1]
    type = random.choice(types)
    
    if(type == 0):
        print(type)
        user()
    else:
        print(type)
        attacker()