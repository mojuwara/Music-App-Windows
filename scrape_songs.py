import pymysql.cursors
from hnhh_scraper import *
import os

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from secret import gmail_pass



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
  new_songs = []
  for i in range(pages):
    song_list = scraper.scrape_songs(i)
    notify_users(song_list)
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
          new_songs.append(song)
          conn.commit()
        except:
          print("{} : {} : feat.{} : {}".format(song.get_artist(), song.get_song_name(), song.get_features_string(), song.get_link()))
  notify_users(new_songs)
  conn.close()

""" 
Given a list of song objects, this function will will notify all people 
who happen to like certain artist that are involved in new songs
"""
def notify_users(song_list):
  """
  1) Query database to find all the email stored.
  2) for each email, Check if a feature or main artist is liked by that person
  3) If so, notify them and move on to the next person,
  The text will be the title of that song as a hyper link(hopefully).
  """
  conn = pymysql.connect(host="localhost", port=3306, user="root", 
      password="", db="Music", charset="utf8mb4",
      cursorclass=pymysql.cursors.DictCursor)

  get_subscribers_query = "SELECT * FROM users WHERE email IS NOT NULL"
  liked_artists_query = "SELECT artist FROM Likes WHERE username = %s"

  with conn.cursor() as cursor:
    cursor.execute(get_subscribers_query)
    subscribers = cursor.fetchall()
    for person in subscribers:
      cursor.execute(liked_artists_query, (person["username"]))
      liked_artists = set(row["artist"] for row in cursor.fetchall())
      content = ""
      for song in song_list:
        artists_on_song = set(song.get_features_list()).union(set(song.get_artist()))
        if len(liked_artists.intersection(artists_on_song)) > 0:
          if song.get_features_string() != "":
            content += "<a href={} target='_blank'>{} - {} feat. {}</a><br><br>".format(song.get_link(),
                song.get_artist(), song.get_song_name(), song.get_features_string())
          else:
            content += "<a href={} target='_blank'>{} - {}</a><br><br>".format(song.get_link(),
                song.get_artist(), song.get_song_name())
      send_email(person["email"], content)
  
  conn.close()


def send_email(receiver, contents):
  port = 465
  sender = "momusicapp@gmail.com"
  password = gmail_pass

  message = MIMEMultipart("alternative")
  message["Subject"] = "New Music"
  message["From"] = sender
  message["To"] = receiver 

  contents = MIMEText(contents, "html")
  message.attach(contents)
  
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    if message.as_string() != "":
      server.login("momusicapp@gmail.com", password)
      server.sendmail(sender, receiver, message.as_string())


if __name__ == "__main__":
  add_data()