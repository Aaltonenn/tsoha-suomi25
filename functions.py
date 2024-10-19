from db import db
from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy.sql import text

def getsubjectareas():
    result = db.session.execute(text("SELECT id, subjectarea, shortname FROM subjectarea"))
    return result.fetchall()

def getsubjectarea(shortname):
    result = db.session.execute(text(f"SELECT id, subjectarea, shortname FROM subjectarea WHERE shortname='{shortname}'"))
    return result.fetchone()

def getthreads(id):
    result = db.session.execute(text(f"Select id, userid, subjectarea, title, content FROM threads WHERE subjectarea='{id}'"))
    return result.fetchall()

def getthreadtitles(idlist):
    namelist = []
    for id in idlist:
        result = db.session.execute(text(f"Select title FROM threads WHERE id='{id}'"))
        result = result.fetchone()
        for title in result:
            namelist.append(title)
    return namelist

def getthread(threadid):
    result = db.session.execute(text(f"Select id, title, userid, content FROM threads WHERE id={threadid}"))
    return result.fetchone()

def getusername(userid):
    resultusername = db.session.execute(text(f"Select username FROM users WHERE id={userid}"))
    return resultusername.fetchone()

def getuserid(username):
    resultid = db.session.execute(text(f"Select id FROM users WHERE username='{username}'"))
    return resultid.fetchone()

def getallusers():
    return db.session.execute(text("Select username, id, password, admin From users")).fetchall()
    
def getuserinfo():
    return db.session.execute(text("Select username,id, admin FROM users")).fetchall()

def logingetuser(username, password):
    sql = text("Select admin, password FROM users where username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    print(user)
    print(user)
    print(user)
    print(user)
    print(user)
    if not user:
        return "Käyttäjää ei löydy"
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            return user[0]
        else:
            return "Väärä salasana"


def getcommentsofthread(threadid):
    return db.session.execute(text(f"SELECT userid, threadid, time, content, username FROM comments WHERE threadid={threadid}")).fetchall()

def addthread(userid, subjectarea, title, content):
    db.session.execute(text(f"INSERT INTO threads (userid, subjectarea, title, content) VALUES ({userid}, {subjectarea}, '{title}', '{content}');"))
    db.session.commit()
    return 

def addsubjectarea(subjectareaname, subjectareashortname):
    db.session.execute(text(f"INSERT INTO subjectarea (subjectarea, shortname) VALUES ('{subjectareaname}', '{subjectareashortname}');"))
    db.session.commit()
    return 

def addcomment(userid, threadid, content, username):
    db.session.execute(text(f"INSERT INTO comments (userid, threadid, time, content, username) VALUES ({userid}, {threadid}, NOW(), '{content}', '{username}')"))
    db.session.commit()
    return

def adduser(username, password, admin):
    hash_value = generate_password_hash(password)
    db.session.execute(text(f"INSERT INTO users (username, password, admin) VALUES ('{username}', '{hash_value}', {admin})"))
    db.session.commit()
    return

def getfollows(userid):
    return db.session.execute(text(f"SELECT threadid FROM follows WHERE userid={userid}")).fetchall()

def addfollow(userid, threadid):
    db.session.execute(text(f"INSERT INTO follows (userid, threadid) VALUES ({userid}, {threadid})"))
    db.session.commit()
    return

def checkfollow(userid, threadid):
    result = db.session.execute(text(f"SELECT userid, threadid FROM follows WHERE threadid={threadid} AND userid={userid}")).fetchone()
    if result != None:
        return True
    else: 
        return False
    
def unfollow(userid, threadid):
    db.session.execute(text(f"DELETE FROM follows WHERE userid = {userid} and threadid = {threadid}"))
    db.session.commit()
    return