#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from pattern.web import Newsfeed, plaintext
#from alchemyapi import AlchemyAPI

app = Flask(__name__)
reader = Newsfeed()
#alchemyapi = AlchemyAPI()

LIFEHACKER = "http://feeds.gawker.com/lifehacker/vip"

items = []
for result in reader.search(LIFEHACKER)[:10]:
  clean_text = plaintext(result.text, keep={'h1':[], 'h2':[], 'strong':[], 'a':['href']})
  items.append(dict(title=result.title, url=result.url, text=clean_text))

print type(items), len(items)

@app.route('/')
def index():
  return render_template("index.html", name="PERICO", items=items)

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
