import pymysql.cursors
from hnhh_scraper import *
import os

# Initially add some data into the Songs and Artists tables
def add_data(pages=1):
  conn = pymysql.connect(host="localhost", port=8889, user="root", 
      password="root", db="Music", charset="utf8mb4",
      cursorclass=pymysql.cursors.DictCursor)

  insert_song_query = "INSERT INTO Songs(artist, song_name, features, genre, link, release_date) \
                      VALUES(%s, %s, %s, %s, %s, %s)"

  insert_artist_query = "INSERT INTO Artists(artist, genre) \
                        SELECT %s, %s \
                        FROM DUAL WHERE NOT EXISTS \
                        (SELECT * FROM Artists WHERE artist= %s)"

  scraper = HNHHScraper()
  for i in range(pages):
    song_list = scraper.scrape_songs(i)
    for song in song_list:
      with conn.cursor() as cursor:
        try:
          print("{} : {} : feat.{} : {}".format(song.get_artist(), song.get_song_name(), song.get_features(), song.get_link()))
          cursor.execute(insert_artist_query, (song.get_artist(), "Hip-Hop/Rap", song.get_artist()))
          cursor.execute(insert_song_query, (song.get_artist(), song.get_song_name(), 
          song.get_features(), "Hip-Hop/Rap", song.get_link(), song.get_release_date()))
          conn.commit()
        except:
          print("{} : {} : feat.{} : {}".format(song.get_artist(), song.get_song_name(), song.get_features(), song.get_link()))

  conn.close()

if __name__ == "__main__":
  add_data()