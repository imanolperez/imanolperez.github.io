#!/usr/bin/env python3

import pandas as pd
import os

def get_cover(book):
  if book["title"] == "Signatures in machine learning and finance":
    return "covers/imanol.jpg"

  cover = f'covers/{book["cover"]}'
  if not os.path.isfile(cover) or os.path.getsize(cover) < 1000:
    cover = 'covers/missing.png'

  return cover

def add_groups(html, library):
  print(library["group"].unique())
  groups = sorted(library["group"].unique())
  
  sep = "&nbsp;&nbsp;<small>●</small>&nbsp;&nbsp;"
  groups_html = sep.join([f"<nobr><a href='#{group}'>{group}</a></nobr>" for group in groups])
  html = html.replace("{NAV}", groups_html)

  return html

def add_nbooks(html, library):
  return html.replace("{N_BOOKS}", str(len(library)))

def add_acquisitions(html, library):
  acquisitions_html = ""
  for _, book in library.iloc[::-1].head(3).iterrows():
    acquisitions_html += (
        '<!-- book -->\n'
        '    <div style="text-align: center; padding-bottom: 20px;">\n'
        f'      <a href="#{book["title"]}"><img src="{get_cover(book)}" width="150"></a>\n'
        '    </div>\n'
        '<!-- end of book -->\n'
        '\n\n'
      )
      
  return html.replace("{ACQUISITIONS}", acquisitions_html)


def add_books(html, library):
  groups = sorted(library["group"].unique())
  books_html = ""
  for group in groups:
    books_html += f'<h2 id="{group}">{group}</h2>\n'
    
    _books = library[library["group"] == group]
    _books = _books.sort_values(by=["last_name", "first_name", "title"])
    for _, book in _books.iterrows():
      books_html += (
        f'<!-- book -->\n'
        f'<article class="bookitem" id="{book["title"]}">\n'
        f'  <div class="row">\n'
        f'    <div class="col cover">\n'
        f'      <a href="#{book["title"]}">\n'
        f'        <img src="{get_cover(book)}" onload="imageLoaded(this)" width="100" style="min-width: 50px;">\n'
        f'      </a>'
        f'    </div>\n'
        f'    <div class="col-10">\n'
        f'      <h3><a href="#{book["title"]}">{book["title"]}</a></h3>\n'
        f'      <p><small>{book["creators"]}<br>{str(book["publish_date"]).split("-")[0]}</small></p>\n'
        f'    </div>\n'
        f'  </div>\n'
        f' </article>\n'
        f' <!-- end of book -->\n'
        f'\n\n'
      )

  return html.replace("{BOOKS}", books_html)


if __name__ == "__main__":
  with open("index.base.html", "r") as f:
    html = f.read()

  library = pd.read_csv("library.csv")
  print(library.head())
  
  html = add_nbooks(html, library)
  html = add_groups(html, library)
  html = add_acquisitions(html, library)
  html = add_books(html, library)

  with open("index.html", "w") as f:
    f.write(html)


