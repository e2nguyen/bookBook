import csv
import os
from application import db
from models import *

def main():
  f = open('books2.csv')
  booksReader = csv.reader(f)
  for isbn, title, author, year in booksReader:
    book = Book(isbn=isbn,title=title,author=author,year=year)
    db.add(book)
  # In cases of large datasets, expect a delay in committing as with books.csv
  # estimated time to commit ~20 mins
  db.commit()
  f.close()

if __name__ == "__main__":
  main()
