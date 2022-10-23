import telebot
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import time
import requests
import json

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
client = gspread.authorize(creds)
bot = telebot.TeleBot("YOURBOTTOKEN")

def ceksentimen(chat):
    url = "https://ramnaufal.herokuapp.com/sentiment/simple"
    headers = {"Content-Type": "application/json", "accept": "application/json"}
    data = {"sentence": chat}
    response = requests.post(url, headers=headers, json=data)
    responnya = response.json()
    return responnya['sentiment'], responnya['score']

@bot.message_handler(commands=['start','kill','off','matikan','stop','alert'])
def handle_command(message):
    now = datetime.now()
    dt_string = now.strftime('%Y-%m-%d %H:%M')
    msg = message.text
    grupnama = message.chat.title
    fromfirstname = message.from_user.first_name
    datalist = [dt_string,msg,grupnama,fromfirstname]
    sheet = client.open("IDS Group Tele").worksheet('seranganbot')
    sheet.append_row(datalist)
    print(datalist)
    print("Serangan data has been added!")
    bot.reply_to(message, "Ini IDS bos.\njgn macem macem! udh nyala!\nSelamat kamu masuk log percobaan serangan!mampus!\n👹👹😈😈😈👾👾")

@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
    if(message.content_type == 'text'):
        now = datetime.now()
        dt_string = now.strftime('%Y-%m-%d %H:%M')
        msg = message.text
        msgid = message.message_id
        idgrup = message.chat.id
        gruptipe = message.chat.type
        grupnama = message.chat.title
        formid = message.from_user.id
        formbot = message.from_user.is_bot
        fromfirstname = message.from_user.first_name
        fromusername = message.from_user.username
        frombahasa = message.from_user.language_code
        klasifikasichat, skorklasifikasi = ceksentimen(msg)
        datalist = [dt_string,msgid,msg,idgrup,gruptipe,grupnama,formid,formbot,fromfirstname,fromusername,frombahasa,klasifikasichat,skorklasifikasi]
        sheet = client.open("IDS Group Tele").worksheet('logmonitoring')
        sheet.append_row(datalist)
        print(datalist)
        print("Data has been added!")

print("IDS is running")
bot.polling()
