from email.policy import default
from itertools import count
from flask import Flask, render_template, request , url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import os
import redis
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

redis_host = 'host.docker.internal'
redis_port = 6379


def redis_init():
    try:
        print("-----------------------------------sucess connecting---------------------------------------")
        r = redis.StrictRedis(host = redis_host, port= redis_port, decode_responses= True)
        #val = r.exists("count")
        #print("bruh if it exisst then {val} ",val)
        r.set("num1","0")
        r.set("num2","1")
        r.set("num3","1")
        r.set("count","0")
        name = os.environ.get['NAME']
        r.set("name",name)
        val = r.get("count")
        #print("val is {val}",val)
    except Exception as e:
        print("some issue ")
        print(e)

def redis_string():
    try:
        r = redis.StrictRedis(host = redis_host, port= redis_port, decode_responses= True)
        r.set("message", "Hello, world!")
        msg = r.get("message")
        print(msg)
    except Exception as e:
        print("bruh zone")
        print(e)

@app.route('/' , methods = ['POST','GET'])
def index():
    count = 0
    num = 0
    name = "BRUH"
    try:
        #print("good zone")
        r = redis.StrictRedis(host = redis_host, port= redis_port, decode_responses= True)
        r.incr("count")
        count = r.get("count")
        #print(f"val is {count}")
        if count=="1":
            name = r.get("name")
            num = r.get("num1")
            #print(f"count and num is {count} {num}")
        elif count=="2":
            name = r.get("name")
            num = r.get("num2")
        else:
            num = r.get("num3")
            name = r.get("name")
            r.set("num1",r.get("num2"))
            r.incrby("num3",r.get("num2"))
            r.set("num2",num)
        #return redirect('/')
    except Exception as e:
        print("bruh zone")
        print(e)    
    print("rendering templates")
    return render_template('index.html',count = count,num = num,name = name)

if __name__ == "__main__":
    redis_init()
    app.run(host='0.0.0.0',debug = True)
    
