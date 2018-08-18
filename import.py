import csv
import os
#import application 
from application import db
from models import *


#os.environ['DATABASE_URL'] = 'postgres://smermoelyzzldc:66f83b65535532a207d4dfc35cbe6fb4edebed9c1c756c4e762b240c1ca5b9c9@ec2-54-235-212-58.compute-1.amazonaws.com:5432/dgcc2ibvmkqp1i'

#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker

#engine = create_engine(os.getenv('postgres://smermoelyzzldc:66f83b65535532a207d4dfc35cbe6fb4edebed9c1c756c4e762b240c1ca5b9c9@ec2-54-235-212-58.compute-1.amazonaws.com:5432/dgcc2ibvmkqp1i'))
#db = scoped_session(sessionmaker(bind=engine))

def main():
  f = open('books.csv')
  booksReader = csv.reader(f)
  for isbn, title, author, year in booksReader:
    book = Book(isbn=isbn,title=title,author=author,year=year)
    #print(book)
    db.add(book)
    db.commit()
  print('committing')
  #db.commit()
  f.close()

if __name__ == "__main__":
  main()
