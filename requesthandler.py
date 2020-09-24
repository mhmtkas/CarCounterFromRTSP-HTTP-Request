from flask import Flask
import subprocess
import json
import os
import time
import shlex

app = Flask(__name__)


def rtsp():
    subprocess.Popen(["sh", "rtsp.sh"], cwd="/home/mkas/Desktop")


def m3u8():
    subprocess.Popen(["sh", "m3u8.sh"], cwd="/home/mkas/Desktop")


def http():
    subprocess.Popen(["sh", "http.sh"], cwd="/home/mkas/Desktop")


def ngrok():
    subprocess.Popen(["sh", "ngrok.sh"], cwd="/home/mkas/Desktop")


@app.route("/Start", methods=['POST'])
def home():
    rtsp()
    time.sleep(2)
    m3u8()
    time.sleep(2)
    http()
    time.sleep(2)
    ngrok()
    time.sleep(2)

    os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")

    with open('tunnels.json') as data_file:
        datajson = json.load(data_file)

    msg = "ngrok URL's: \n'"
    for i in datajson['tunnels']:
        msg = msg + i['public_url'] + '\n'
    link = msg.split('\n')
    return "Stream Link:  "+link[2]+"/PitonArge.m3u8"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

