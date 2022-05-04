#!/usr/bin/python3
# -*- coding: utf-8 -*-
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from PIL import ImageFont
import time
from threading import Thread
import requests
import json
import spotipy.util as util

def get_spotify_token():
    username = '咕谷酱'
    scope = 'user-read-playback-state'
    gettokne = util.prompt_for_user_token(username,scope,
                            client_id='xxxx',
                            client_secret='xxxx',
                            # 注意需要在自己的web app中添加redirect url
                            redirect_uri='https://gmoe.cc')
    return gettokne


token=get_spotify_token()
headers = {"Authorization": "Bearer {}".format(token)}


url = 'https://api.spotify.com/v1/me/player?market=ES'

#初始值
text_title ="None"
text_art = "None"
time_music = "00:00"
time_load_long = 5
start_music = "播放"
start_wath = False

def ms_to_hours(millis):
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    #hours = (millis / (1000 * 60 * 60)) % 24
    #hours = int(hours)
    #lay = millis - hours*1000 * 60 * 60 - minutes*1000 * 60 - seconds*1000
    if minutes == 0:
        minutes = "00"
    else:
        minutes = "0"+str(minutes)

    if len(str(seconds)) == 1:
        seconds = "0"+str(seconds)

    out_min = str(minutes)+":"+str(seconds)
    return(out_min)

def len_how(text):
    font = ImageFont.truetype("./MiSans-ExtraLight.ttf", 15, 0)
    width, height = font.getsize(text)
    if width >= 128:
        return True
    else:
        return False

def len_how_art(text):
    font = ImageFont.truetype("./MiSans-ExtraLight.ttf", 13, 0)
    width, height = font.getsize(text)
    if width >= 128:
        return True
    else:
        return False

def get_len_how_wh(text):
    font = ImageFont.truetype("./MiSans-ExtraLight.ttf", 15, 0)
    width, height = font.getsize(text)
    return width

def get_len_how_time(text):
    font = ImageFont.truetype("./MiSans-ExtraLight.ttf", 13, 0)
    width, height = font.getsize(text)
    return width

def get_len_how_wh_art(text):
    font = ImageFont.truetype("./MiSans-ExtraLight.ttf", 13, 0)
    width, height = font.getsize(text)
    return width

def get_len_how_hg(text):
    font = ImageFont.truetype("./MiSans-ExtraLight.ttf", 15, 0)
    width, height = font.getsize(text)
    return height

def load_oled():# 显示音乐函数
    global time_music
    global text_title
    global text_art
    global time_load_long
    global start_music
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial)
    font_title = ImageFont.truetype('./MiSans-ExtraLight.ttf', 15)
    font_info = ImageFont.truetype('./MiSans-ExtraLight.ttf', 13)
    font_start = ImageFont.truetype('./MiSans-ExtraLight.ttf', 13)
    while True:
        text_in = text_title
        get_ine = get_len_how_wh(text_in)
        get_hi = get_len_how_hg(text_in)

        get_ine_art = get_len_how_wh_art(text_art)

        x = 3
        zt = 1
        x_art = 3
        while zt:
            with canvas(device) as draw:
                #draw.rectangle(device.bounding_box, outline="white", fill="black")
                draw.rectangle(device.bounding_box, outline="white", fill="black")

                draw.rectangle((5,40, 122, 45), outline="white", fill="black")
                draw.rectangle((5,40, int(time_load_long), 45), outline="white", fill="white")

                draw.text((4, 46), start_music, fill="white", font=font_start)

                if len_how(text_in):
                    draw.text((x, -1), text_in, fill="white", font=font_title)
                    draw.text((124-get_len_how_time(time_music), 48), time_music, fill="white", font=font_info)

                    if len_how_art(text_art):#绘制歌手名字
                        draw.text((x_art,  get_hi-1), text_art, fill="white", font=font_info)
                        if x_art <= get_ine_art*-1:
                            x_art = 128
                        x_art -=2
                    else:
                        draw.text((1, get_hi-1), text_art, fill="white", font=font_info)

                    x-=2
                    
                    if x <= get_ine*-1:
                        x = 128
                    if text_in != text_title:
                        zt = 0
                else:
                    draw.text((3, -1), text_in, fill="white", font=font_title)
                    draw.text((124-get_len_how_time(time_music), 48), time_music, fill="white", font=font_info)
                    if len_how_art(text_art):
                        draw.text((x_art,  get_hi-1), text_art, fill="white", font=font_info)
                        if x_art <= get_ine_art*-1:
                            x_art = 128
                        x_art -=2
                    else:
                        draw.text((3, get_hi-1), text_art, fill="white", font=font_info)
                    
                    if text_in != text_title:
                        zt = 0

start = 1
start_wathe =1

thread_list = []
t1 = Thread(target=load_oled, args=())  # 定义线程t1
thread_list.append(t1)
for t in thread_list:
    t.setDaemon(True)
    t.start()

while True:
    try:
        response = requests.get(url, headers=headers)  # 在这里传入请求头
        get_load_json = json.loads(response.text)

        getlist_json = ""
        if len(get_load_json["item"]["artists"]) > 1:
            for music_art in range(len(get_load_json["item"]["artists"])):
                getlist_json += get_load_json["item"]["artists"][music_art]["name"]
                if music_art != len(get_load_json["item"]["artists"])-1:
                    getlist_json +=","
        else:
            getlist_json = get_load_json["item"]["artists"][0]["name"]

        text_art = getlist_json 
        #print(ms_to_hours(get_load_json["progress_ms"]),get_load_json["is_playing"]) 

        time_music = ms_to_hours(get_load_json["progress_ms"]) +"/"+ ms_to_hours(get_load_json["item"]["duration_ms"])
        time_load_long = str(round(round(get_load_json["progress_ms"] / get_load_json["item"]["duration_ms"] ,2)*116,0)+5)
        time_load_long = time_load_long[:len(time_load_long)-2]
        text_title = get_load_json["item"]["name"]
        if get_load_json["is_playing"]:
            start_music = "播放"
        else:
            start_music = "暂停"
        
        time.sleep(1)
    except Exception as err:
        token=get_spotify_token()
        headers = {"Authorization": "Bearer {}".format(token)}
        print(err)
