#!/usr/bin/python3
# -*- coding: utf-8 -*-  

import cgi  
import cgitb  
import sqlite3  
  
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
cgitb.enable()  
  
print("Content-type: text/html; charset=utf-8")
print("Pragma: no-cache")
print("Cache-Control: no-cache")
print()  
print('''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"> 
<html lang="ja"> 
<head> 
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=UTF-8"> 
<META HTTP-EQUIV="Pragma" CONTENT="no-cache"> 
<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache"> 
<title>python message board</title> 

<style type="text/css">
body {
    color: black;
	background-color: white;
	}
</style>

</head> 
<body> 
<form method="POST" action="./pyboard3.py"> 
<table> 
<tr> 
  <td><b>Name</b></td> 
  <td><input type="text" name="name" size="10" value=""></td> 
</tr> 
<tr> 
  <td><b>Title</b></td> 
  <td><input type="text" name="title" size="20" value=""></td> 
</tr> 
<tr> 
  <td><b>Comment / Message</b></td> 
  <td><textarea cols="20" rows="5" name="comment"></textarea></td> 
</tr> 

<tr> 
  <td><b>URL</b></td> 
  <td><input type="text" name="url"></td> 
</tr> 

<tr> 
  <td colspan="2"><input type="submit" value="Post"><input type="reset" value="Reset"></td> 
</tr> 
</table> 
</form> 
''')
  
  
con = sqlite3.connect("board.db")  
try:  
  # Database Creation
  con.executescript("""create table boardtbl(regdate timestamp,name varchar(10),title varchar(30),comment varchar(100),url text);""")  
except:  
  print  
finally:  
  # If there is input, insert data to database
  form = cgi.FieldStorage()  
#  print( form["name"].value )
  if "name" in form:
    # if name is specified, insert data
    name = form["name"].value
    title = form["title"].value
    comment = form["comment"].value
    url = form["url"].value
    cur = con.cursor()
    try:  
      cur.execute("insert into boardtbl values(datetime('now','localtime'),?,?,?,?)",(cgi.escape(name),cgi.escape(title),cgi.escape(comment),cgi.escape(url)))  
      con.commit()  
    except:  
      con.rollback()  
    finally:  
      cur.close()  
  
  # display messages
  con.row_factory = sqlite3.Row  
  cur = con.cursor()  
  try:
    cur.execute("select * from boardtbl order by regdate desc")  
    print("<dl>")
    for each in cur.fetchall():

      print('<dt><hr />')
      print('Title:', each['title'])
      print('Name:' , each['name'])
      print('Date:', each['regdate'])
      print('URL: <a href=', each['url'], '>', each['url'], '</a>')
      print('<dt><br>')
      print('<dd>', each['comment'], '</dd>')

    print("</dl>")
  finally:  
    cur.close()  
    con.close()  
  print("</body></html>")
