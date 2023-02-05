from faker import Faker
import time
from datetime import datetime
import random
import ipaddress
import mysql.connector
import pandas as pd
dbconn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="",
    database="cn"
)

mycursor = dbconn.cursor()
if(dbconn):
    frame = pd.read_sql("select * from access", dbconn)
    pd.set_option('display.expand_frame_repr', False)
    print(frame)
    #frame.set_index(['ip', frame.index], inplace=True)  # in-place
    frametest = frame.groupby('ip')[['time','area','url','bytesent','useragent']].agg(list).reset_index()
    print(frametest)
    result = frametest.to_csv('file1.csv')
    print(result)