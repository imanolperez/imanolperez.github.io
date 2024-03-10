#!/usr/bin/env python3

import pandas as pd
import numpy as np
import os
import urllib.request
import json
from tqdm.auto import tqdm

if __name__ == "__main__":
  library = pd.read_csv("library.raw.csv")
  library["cover"] = ""
  
  pbar = tqdm(library.iloc[::-1].iterrows(), total=len(library))

  for i, book in pbar:
    #if book["title"] != "Holy Bible":
    #  continue

    if np.isnan(book["ean_isbn13"]):
      isbn = ""
    else:
      isbn = str(int(book["ean_isbn13"]))

    pbar.set_description(f'{book["title"]} {isbn}')

    if len(isbn):
      cover_out = f"{isbn}.jpg"

      url_dir = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
      try:
        with urllib.request.urlopen(url_dir) as url:
          book_details = json.load(url)
  
          if book_details["totalItems"] == 0:
            print(f"ISBN {isbn} found {book_details['totalItems']} items")
            cover = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
  
          else:
            book_details = book_details["items"][0]["volumeInfo"]
  
            if "publishedDate" in book_details:
              library.loc[i, "publish_date"] = book_details["publishedDate"]
  
            if os.path.isfile(f"covers/{cover_out}"):
              library.loc[i, "cover"] = cover_out
              cover = None
              cover_out = None
              continue
  
            if "imageLinks" in book_details:
              cover = book_details["imageLinks"]["thumbnail"]
            else:
              cover = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
  
            # Update book info
            #if "authors" in book_details:
            #  library.loc[i, "creators"] = ", ".join(book_details["authors"])
            #if "title" in book_details:
            #  library.loc[i, "title"] = book_details["title"]
  
            if "publishedDate" in book_details:
              library.loc[i, "publish_date"] = book_details["publishedDate"]
      except:
        library.loc[i, "cover"] = cover_out
        print("Could not query Google")
    
    elif book["group"] == "Penguin Specials WWII":
      snumber = book["description"].split("\n")[0]
      snumber = "S" + snumber[1:].zfill(3)
      cover = f"http://www.penguinfirsteditions.com/Specials/{snumber}.jpg"
      cover_out = f"PENGUIN_{snumber}.jpg"

      if os.path.isfile(f"covers/{cover_out}"):
        library.loc[i, "cover"] = cover_out
        cover = None
        cover_out = None
        continue
    elif book["tags"] == "pelican philosophy series":
      snumber = book["description"].split("\n")[0].split()[0]
      snumber = "A" + snumber[1:].zfill(3)
      cover = f"http://www.penguinfirsteditions.com/pel/{snumber}.jpg"
      cover_out = f"PELICAN_{snumber}.jpg"

      if os.path.isfile(f"covers/{cover_out}"):
        library.loc[i, "cover"] = cover_out
        cover = None
        cover_out = None
        continue
    else:
      cover = None
      cover_out = None
      continue

    if cover is None:
      print(f"Cover is None")
      cover = None
      cover_out = None
      continue

    if "google" in cover:
      response = urllib.request.urlopen(cover)
      content = response.read()
      f = open(f"covers/{cover_out}", 'wb')
      f.write(content)
      f.close()
    elif cover.endswith(".jpg"):
      print(f"OpenLibrary cover for {isbn}")
      os.system(f"wget {cover} -O covers/{cover_out}")
    else:
      print(f"URL {cover} not recognised. Not wget-ing for safety")
      cover = None
      cover_out = None
      continue
    
    cover_out_path = f"covers/{cover_out}"
    if not os.path.isfile(cover_out_path):
      print(f"File {cover_out_path} for {book['title']} not created. Skipping")
      cover = None
      cover_out = None
      continue

    if os.path.getsize(cover_out_path) < 5:
      print(f"File {cover_out_path} for {book['title']} is empty. Removing")
      cover = None
      cover_out = None
      os.remove(cover_out_path)
      continue

    if cover_out is not None:
      library.loc[i, "cover"] = cover_out

    cover_out = None
    cover = None

  library.to_csv("library.csv", index=False)
