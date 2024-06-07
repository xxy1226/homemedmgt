import pymongo

mymongo = pymongo.MongoClient('localhost', 27017)
mydb = mymongo['xxiablog']
mycol = mydb['posts']

myquery = {'title': 'Python Insert', 'tag': 'it'}

mycol.insert_one(myquery)