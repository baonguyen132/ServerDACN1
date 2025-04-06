import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="dacn1"
)
mycursor = db.cursor()

def importData(sql,val):

    mycursor.execute(sql, val)
    db.commit()

def exportData(sql, val, fetch_all=False):
    mycursor.execute(sql, val)
    return mycursor.fetchall() if fetch_all else mycursor.fetchone()
