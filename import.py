from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import os, csv

engine=create_engine(os.getenv("DATABASE_URL"))

#the 'scoped session' ensures that different users interacts in separate manner with db
db = scoped_session(sessionmaker(bind=engine))

#Read and parse books information
file = open("books.csv")
reader = csv.reader(file)


for isbn , title, author, year in reader:
	db.execute("INSERT INTO books(isbn, title, author, year) VALUES(:isbn, :title, :author, :year)",
		{"isbn":isbn, 
		"title":title,
		"author":author,
		"year":year })

	print("Added book {} to database".format(title))
	db.commit()

