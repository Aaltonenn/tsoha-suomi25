from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from flask import render_template
from app import app
from db import db
import functions


@app.route("/")
def home():
    subjectarea = functions.getsubjectareas()
    try:
        userid = functions.getuserid(session["username"])[0]
        follows = functions.getfollows(userid)
        newfollows = []
        for follow in follows:
            newfollows.append(follow[0])
        threadtitles = functions.getthreadtitles(newfollows)
        followslist = []
        i=0
        while i<len(newfollows):
            followslist.append([newfollows[i],threadtitles[i]])
            i=i+1
        return render_template("index.html", count=len(subjectarea), subjectarea=subjectarea, followslist=followslist)

    except:
        return render_template("index.html", count=len(subjectarea), subjectarea=subjectarea)
        
    
@app.route("/loginpage")
def loginpage():
    return render_template("loginpage.html")

@app.route("/subjectarea/<string:shortname>")
def subjectarea(shortname):
    subjectarea = functions.getsubjectarea(shortname)
    threads = functions.getthreads(subjectarea[0])
    return render_template("subjectarea.html", threads=threads, subjectareaname=subjectarea[1])
    
@app.route("/thread/<int:id>")
def thread(id):
    thread = functions.getthread(id)
    threadtitle = thread[1]
    threadstarter = functions.getusername(thread[2])[0]
    threadcontent = thread[3]
    comments = functions.getcommentsofthread(id)
    isfollowed = functions.checkfollow(session["id"], id)
    return render_template("thread.html", threadtitle=threadtitle, threadstarter=threadstarter, threadcontent=threadcontent, count=len(comments), comments=comments, threadid=id, isfollowed=isfollowed)


@app.route("/login",methods=["POST"])
def login():
    username = str(request.form["username"])
    password = str(request.form["password"])
    result = functions.logingetuser(username, password)
    if result == 1 or result == 0:
        id = functions.getuserid(username)
        session["username"] = username
        session["id"] = id[0]
        session["admin"] = result
        
        return redirect("/")
    elif result == "Käyttäjää ei löydy":
        return result
    elif result == "Väärä salasana":
        return result
    else:
        return "Kriittinen virhe"

@app.route("/signinpage")
def signinpage():
    return render_template("signinpage.html")

@app.route("/signinnew", methods=["POST"])
def signinnew():
    username = str(request.form["username"])
    password = str(request.form["password"])
    if len(username) >= 30:
        return "Käyttäjänimi on liian pitkä"
    if len(password) <= 8:
        return "Salasana on liian lyhyt"
    admin = int(request.form["admin"])
    functions.adduser(username, password, admin)
    return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/user/<int:id>")
def userpage(id):
    if id == session["id"]:
        users = functions.getuserinfo()
        found = users[0]
        for user in users:
            if user[1]==id:
                found = user
        if found[2] == 1:
            admin = "ylläpitäjä."
        elif found[2] == 0:
            admin = "tavallinen käyttäjä."
        return render_template("user.html", username=found[0],admin=admin)
    else:
        return "SINULLA EI OLE OIKEUKSIA OLLA TÄÄLLÄ!!"

@app.route("/newthread")
def newthread():
    subjectareas = functions.getsubjectareas()
    return render_template("newthread.html", subjectareas=subjectareas)

@app.route("/sendthread", methods=["POST"])
def sendthread():
    subjectareastring = request.form["subjectarea"]
    subjectarea = list(subjectareastring.strip("()").split(", "))
    subjectarea[1] = subjectarea[1].replace("'", "")
    subjectarea[2] = subjectarea[2].replace("'", "")
    title = str(request.form["title"])
    content = str(request.form["content"])
    subjectareashortname = subjectarea[2]
    userid= session["id"]
    if len(title) >= 100:
        return "Otsikko on liian pitkä"
    if len(content) >= 5000:
        return "Viesti on liian pitkä"
    functions.addthread(userid, subjectarea[0], title, content)
    return redirect(f"/subjectarea/{subjectareashortname}")

@app.route("/newsubjectarea")
def newsubjectarea():
    return render_template("newsubjectarea.html")

@app.route("/sendsubjectarea", methods=["POST"])
def sendsubjectarea():
    subjectareaname = request.form["subjectareaname"]
    if len(subjectareaname) >= 50:
        return "Keskustelualueen aiheen nimi on liian pitkä"
    subjectareashortname = str(request.form["subjectareashortname"])
    if len(subjectareashortname) >= 20:
        return "Keskustelualueen lyhytnimi on liian pitkä"
    functions.addsubjectarea(subjectareaname, subjectareashortname)
    return redirect("/subjectarea/subjectareashortname")

@app.route("/newcomment/<int:id>")
def newcomment(id):
    return render_template("newcomment.html",threadid=id)

@app.route("/sendcomment/<int:id>", methods=["POST"])
def sendcomment(id):
    comment = request.form["content"]
    userid = session["id"]
    threadid = id
    username = session["username"]   
    if len(comment) >= 5000:
        return "Kommentti on liian pitkä" 
    functions.addcomment(userid,threadid,comment, username)
    return redirect(f"/thread/{threadid}")

@app.route("/follow/<int:id>")
def follow(id):
    functions.addfollow(session["id"], id)
    return redirect(f"/thread/{id}")

@app.route("/unfollow/<int:id>")
def unfollow(id):
    functions.unfollow(session["id"], id)
    return redirect(f"/thread/{id}")

