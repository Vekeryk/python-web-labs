#!/usr/bin/env python3
from http import cookies
import os
import cgi
import html

cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
if "count" in cookie:
  count = int(cookie.get("count").value) + 1
else:
  count = 1

form = cgi.FieldStorage()

name = html.escape(form.getfirst("name", ""))
surname = html.escape(form.getfirst("surname", ""))

courses = ["maths", "biology", "chemistry", "history"]
courses = [course for course in courses if form.getvalue(course)]

language = form.getvalue("language")

HTML = f'''<!DOCTYPE html>
<html lang="en-US">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
    <title>Result</title>
  </head>
  <body>
    <h1>Обробка даних форм!</h1>
    <p>Name: {name}</p>
    <p>Surname: {surname}</p>
    <p>Selected courses: {courses}</p>
    <p>Selected language: {language}</p>
    <p>Form count: {count}</p>
  </body>
</html>'''

print(f"Set-cookie: count={count}")
print("Content-type: text/html\r\n\r\n")
print(HTML)