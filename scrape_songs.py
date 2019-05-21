import pymysql.cursors
from hnhh_scraper import *
import os

# Initially add some data into the Songs and Artists tables
def add_data(pages=1):
  conn = pymysql.connect(host="localhost", port=3306, user="root", 
      password="", db="Music", charset="utf8mb4",
      cursorclass=pymysql.cursors.DictCursor)

  insert_song_query = "INSERT INTO Songs(artist, song_name, features, genre, link, release_date) \
                      VALUES(%s, %s, %s, %s, %s, %s)"

  insert_artist_query = "INSERT INTO Artists(artist, genre) \
                        SELECT %s, %s \
                        FROM DUAL WHERE NOT EXISTS \
                        (SELECT * FROM Artists WHERE artist= %s)"

  insert_collab_query = "INSERT INTO Collaborations(main_artist, feature, songID) \
      VALUES (%s, %s, %s)"

  song_id_query = "SELECT songID FROM Songs WHERE link = %s"

  scraper = HNHHScraper()
  for i in range(pages):
    song_list = scraper.scrape_songs(i)
    for song in song_list:
      with conn.cursor() as cursor:
        try:
          cursor.execute(insert_artist_query, (song.get_artist(), "Hip-Hop/Rap", song.get_artist()))
          cursor.execute(insert_song_query, (song.get_artist(), song.get_song_name(), 
              song.get_features_string(), "Hip-Hop/Rap", song.get_link(), song.get_release_date()))
          
          cursor.execute(song_id_query, (song.get_link()))
          id = int(cursor.fetchone()["songID"])
          for feature in song.get_features_list():
            cursor.execute(insert_artist_query, (feature, "Hip-Hop/Rap", feature))
            cursor.execute(insert_collab_query, (song.get_artist(), feature, id))
          notify_users(song)
          conn.commit()
        except:
          print("{} : {} : feat.{} : {}".format(song.get_artist(), song.get_song_name(), song.get_features_string(), song.get_link()))

  conn.close()

""" 
Given a song object, this function will will notify all people 
who happen to like a certain artist that is involved in that song,
"""

def notify_users(song):
  """
  1) Query database to find all the phone numbers stored.
  2) for each number, Check if a feature or main artist is liked by that person
  3) If so, notify them and move on to the next person,
  The text will be the title of that song as a hyper link(hopefully).
  """
  pass

  
if __name__ == "__main__":
  add_data()