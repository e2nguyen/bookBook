import csv
import os
from application import db
from models import *

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
