from mongoengine import connect, Document, ListField, StringField, URLField
from pymongo import MongoClient
import pprint
client = MongoClient(host="localhost", port=27017)
connect(db="rptutorials", host="localhost", port=27017)


class Tutorial(Document):
    title = StringField(required=True, max_length=70)
    author = StringField(required=True, max_length=20)
    contributors = ListField(StringField(max_length=20))
    url = URLField(required=True)


tutorial1 = Tutorial(
    title="Beautiful Soup: Build a Web Scraper With Python",
    author="Martin",
    contributors=["Aldren", "Geir Arne", "Jaya", "Joanna", "Mike"],
    url="https://realpython.com/beautiful-soup-web-scraper-python/")
tutorial1.save()
print(tutorial1.title, tutorial1.author, tutorial1.contributors, tutorial1.url)
tutorial2 = Tutorial()
tutorial2.title = "Working With JSON Data in Python"
tutorial2.author = "Alex"
tutorial2.contributors = ["Aldren", "Jon", "Joanna"]
tutorial2.url = "https://realpython.com/convert-python-string-to-int/"
tutorial2.save()
print(tutorial2.title, tutorial2.author, tutorial2.contributors, tutorial2.url)
db = client.rptutorials
print(db)
tutorial3 = {
    "title": "Working With JSON Data in Python",
    "author": "Lucas",
    "contributors": [
        "Aldren",
        "Dan",
        "Joanna"
    ],
    "url": "https://realpython.com/python-json/"
}
tutorial = db.tutorial
print(tutorial)
result = tutorial.insert_one(tutorial3)
print(tutorial3)
print(f"One tutorial: {result.inserted_id}")
tutorial4 = {
    "title": "Python's Requests Library (Guide)",
    "author": "Alex",
    "contributors": [
        "Aldren",
        "Brad",
        "Joanna"
    ],
    "url": "https://realpython.com/python-requests/"
}
tutorial5 = {
    "title": "Object-Oriented Programming (OOP) in Python 3",
    "author": "David",
    "contributors": [
        "Aldren",
        "Joanna",
        "Jacob"
    ],
    "url": "https://realpython.com/python3-object-oriented-programming/"
}
new_result = tutorial.insert_many([tutorial4, tutorial5])
print(tutorial4, tutorial5)
print(f"Multiple tutorials: {new_result.inserted_ids}")
for doc in tutorial.find():
    pprint.pprint(doc)
jon_tutorial = tutorial.find_one({"author": "Jon"})
pprint.pprint(jon_tutorial)
with MongoClient() as client:
    db = client.rptutorials
    for doc in db.tutorial.find():
        pprint.pprint(doc)