#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from pattern.web import Newsfeed, plaintext
from alchemyapi import AlchemyAPI

app = Flask(__name__)
reader = Newsfeed()
alchemyapi = AlchemyAPI()

LIFEHACKER = "http://feeds.gawker.com/lifehacker/vip"

items = []
for result in reader.search(LIFEHACKER)[:10]:
  clean_text = plaintext(result.text)
  response = alchemyapi.entities("text", result.text)

  entities = []
  for entity in response["entities"]:
    if entity.has_key("disambiguated"):
      dbpedia_uri = entity["disambiguated"]["dbpedia"]
    else:
      dbpedia_uri = None
    entities.append((entity["text"], dbpedia_uri))

  items.append(dict(title=result.title, url=result.url, text=clean_text, entities=entities))

@app.route('/')
def index():
  return render_template("index.html", items=items)

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
