from db import db
from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy.sql import text

def getsubjectareas():
    sql = text("SELECT id, subjectarea, shortname FROM subjectarea")
    result = db.session.execute(sql)
    return result.fetchall()

def getsubjectarea(shortname):
    sql = text("SELECT id, subjectarea, shortname FROM subjectarea WHERE shortname=:shortname")
    result = db.session.execute(sql, {"shortname":shortname})
    return result.fetchone()

def getthreads(id):
    sql = text("Select id, userid, subjectarea, title, content FROM threads WHERE subjectarea=:id")
    result = db.session.execute(sql,{"id":id})
    return result.fetchall()

def getthreadtitles(idlist):
    namelist = []
    for id in idlist:
        sql = text("Select title FROM threads WHERE id=:id")
        result = db.session.execute(sql, {"id":id})
        result = result.fetchone()
        for title in result:
            namelist.append(title)
    return namelist

def getthread(threadid):
    sql = text("Select id, title, userid, content FROM threads WHERE id=:threadid")
    result = db.session.execute(sql, {"threadid":threadid})
    return result.fetchone()

def getusername(userid):
    sql = text("Select username FROM users WHERE id=:userid")
    resultusername = db.session.execute(sql, {"userid":userid})
    return resultusername.fetchone()

def getuserid(username):
    sql = text("Select id FROM users WHERE username=:username")
    resultid = db.session.execute(sql, {"username":username})
    return resultid.fetchone()

def getallusers():
    sql = text("Select username, id, password, admin From users")
    return db.session.execute(sql).fetchall()
    
def getuserinfo():
    sql = text("Select username,id, admin FROM users")
    return db.session.execute(sql).fetchall()

def logingetuser(username, password):
    sql = text("Select admin, password FROM users where username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return "Käyttäjää ei löydy"
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            return user[0]
        else:
            return "Väärä salasana"


def getcommentsofthread(threadid):
    sql = text("SELECT id, userid, threadid, time, content, username FROM comments WHERE threadid=:threadid")
    return db.session.execute(sql, {"threadid":threadid}).fetchall()

def addthread(userid, subjectarea, title, content):
    sql = text("INSERT INTO threads (userid, subjectarea, title, content) VALUES (:userid, :subjectarea, :title, :content);")
    db.session.execute(sql,{"userid":userid, "subjectarea":subjectarea, "title":title, "content":content})
    db.session.commit()
    return 

def addsubjectarea(subjectareaname, subjectareashortname):
    sql = text("INSERT INTO subjectarea (subjectarea, shortname) VALUES (:subjectareaname, :subjectareashortname);")
    db.session.execute(sql, {"subjectareaname": subjectareaname, "subjectareashortname":subjectareashortname})
    db.session.commit()
    return 

def addcomment(userid, threadid, content, username):
    sql = text("INSERT INTO comments (userid, threadid, time, content, username) VALUES (:userid, :threadid, NOW(), :content, :username)")
    db.session.execute(sql, {"userid":userid, "threadid": threadid, "content": content, "username": username})
    db.session.commit()
    return

def adduser(username, password, admin):
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password, admin) VALUES (:username, :hash_value, :admin)")
    db.session.execute(sql, {"username":username, "hash_value":hash_value, "admin": admin})
    db.session.commit()
    return

def getfollows(userid):
    sql = text("SELECT threadid FROM follows WHERE userid=:userid")
    return db.session.execute(sql,{"userid":userid}).fetchall()

def addfollow(userid, threadid):
    sql = text("INSERT INTO follows (userid, threadid) VALUES (:userid, :threadid)")
    db.session.execute(sql, {"userid":userid, "threadid":threadid})
    db.session.commit()
    return

def checkfollow(userid, threadid):
    sql = text("SELECT userid, threadid FROM follows WHERE threadid=:threadid AND userid=:userid")
    result = db.session.execute(sql,{"userid":userid, "threadid":threadid}).fetchone()
    if result != None:
        return True
    else: 
        return False
    
def unfollow(userid, threadid):
    sql = text("DELETE FROM follows WHERE userid =:userid and threadid =:threadid")
    db.session.execute(sql,{"userid":userid, "threadid":threadid})
    db.session.commit()
    return

def deletesubjectarea(shortname):
    sql = text("DELETE FROM subjectarea WHERE shortname=:shortname")
    db.session.execute(sql, {"shortname":shortname})
    db.session.commit()
    return

def deletethread(id):
    sql = text("DELETE FROM threads WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return

def deletecomment(id):
    sql = text("DELETE FROM comments WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return