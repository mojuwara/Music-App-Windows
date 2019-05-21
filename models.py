import pymysql.cursors
import hashlib

# Return True if log in credentials are in the database.
def is_user(username, password):
  able_to_login = False

  conn = pymysql.connect(host="localhost", port=3306, user="root", 
      password="", db="Music", charset="utf8mb4", 
      cursorclass=pymysql.cursors.DictCursor)

  check_query = "SELECT username, password \
            FROM Users \
            WHERE (username, password) = (%s, %s)"
  with conn.cursor() as cursor:
    cursor.execute(check_query, (username, hashlib.sha256(password.encode()).hexdigest()))
    able_to_login = True if cursor.fetchone() is not None else False
    
  conn.commit()
  conn.close()
  return able_to_login

# Return True if a user was able to register. Username is not already being used.
def is_now_registered(username, password):
  able_to_register = False
  conn = pymysql.connect(host="localhost", port=3306, user="root", 
      password="", db="Music", charset="utf8mb4", 
      cursorclass=pymysql.cursors.DictCursor)

  exists_query = "SELECT username \
                  FROM Users \
                  WHERE username = %s"

  insert_query = "INSERT INTO Users(username, password) \
                  VALUES (%s, %s)"

  with conn.cursor() as cursor:
    cursor.execute(exists_query, (username))
    if (cursor.fetchone() is None):
      cursor.execute(insert_query, (username, hashlib.sha256(password.encode()).hexdigest()))
      able_to_register = True
  
  conn.commit()
  conn.close()
  return able_to_register

# Given a list of artists the user likes, 
# it will insert this relationship into the "Likes" table in the database
def store_new_artists(username, artist_list):
  conn = pymysql.connect(host="localhost", port=3306, user="root", 
      password="", db="Music", charset="utf8mb4",
      cursorclass=pymysql.cursors.DictCursor)
  
  store_query = "INSERT INTO Likes(username, artist) \
                  VALUES (%s, %s)"

  with conn.cursor() as cursor:
    for artist in artist_list:
      cursor.execute(store_query, (username, artist))
  conn.commit()
  conn.close() 

""" 
    Returns a list, that contains a list for every artist liked by the user, 
    where the first element is a dictionary of {'artist': value},
    And the second element is a LIST, that contains DICTIONARIE(S), 
    of each song involving that artist
"""
def search_new_songs(username):
  conn = pymysql.connect(host="localhost", port=3306, user="root", 
      password="", db="Music", charset="utf8mb4", 
      cursorclass=pymysql.cursors.DictCursor)

  songs_query = "SELECT * FROM Songs WHERE artist IN \
	                  (SELECT artist FROM Likes WHERE username = %s)\
                OR songID IN \
	                  (SELECT songID FROM Collaborations WHERE feature IN \
     	                  (SELECT artist FROM Likes WHERE username = %s))\
                ORDER BY release_date DESC;"

  with conn.cursor() as cursor:
    cursor.execute(songs_query, (username, username))
    results = cursor.fetchall()

  conn.commit()
  conn.close()
  return results

# Get artists that are currently neither disliked or liked by the user
def search_neutral_artists(username):
  neutral_artists_query = "SELECT artist FROM Artists \
                          WHERE artist NOT IN \
                                (SELECT artist FROM Likes WHERE username = %s) \
				                  and artist NOT IN \
                                (SELECT artist FROM Dislikes WHERE username = %s)"
  
  conn = pymysql.connect(host="localhost", port=3306, user="root", 
      password="", db="Music", charset="utf8mb4", 
      cursorclass=pymysql.cursors.DictCursor)

  with conn.cursor() as cursor:
    cursor.execute(neutral_artists_query, (username, username))
    results = cursor.fetchall()

  conn.commit()
  conn.close()
  return results

# Takes a username and list of artists the user does not like,
# and then adds them to the Dislike table so songs made by them don't show up 
def dislike(username, artists):
  conn = pymysql.connect(host="localhost", port=3306, user="root", 
      password="", db="Music", charset="utf8mb4", 
      cursorclass=pymysql.cursors.DictCursor)
      
  dislike_query = "INSERT INTO Dislikes(username, artist)\
                  VALUES (%s, %s)"

  with conn.cursor() as cursor:
    try:
      for artist in artists:
        cursor.execute(dislike_query, (username, artist))
    except:
      print("Could not dislike your selected artists.")

  conn.commit()
  conn.close()
      
# Get artists liked by the user
def get_liked_artists(username):
  conn = pymysql.connect(host="localhost", port=3306, user="root", 
      password="", db="Music", charset="utf8mb4", 
      cursorclass=pymysql.cursors.DictCursor)

  liked_artists_query = "SELECT artist FROM Likes \
                        WHERE username = %s"
  
  with conn.cursor() as cursor:
    cursor.execute(liked_artists_query, (username))
    results = cursor.fetchall()

  conn.commit()
  conn.close()
  return results
  
# Given a list of artists the user no longer likes
# this will remove them from the liked table
def remove_from_liked(username, artists):
  conn = pymysql.connect(host="localhost", port=3306, user="root", 
      password="", db="Music", charset="utf8mb4", 
      cursorclass=pymysql.cursors.DictCursor)

  remove_artist_query = "DELETE FROM Likes WHERE username=%s AND artist=%s"

  with conn.cursor() as cursor:
    for artist in artists:
      cursor.execute(remove_artist_query, (username, artist))

  conn.commit()
  conn.close()

# Get a list of dictionaries of all the artists the user does not like
def get_disliked_artists(username):
  conn = pymysql.connect(host="localhost", port=3306, user="root", 
      password="", db="Music", charset="utf8mb4", 
      cursorclass=pymysql.cursors.DictCursor)

  disliked_artist_query = "SELECT artist FROM Dislikes WHERE username = %s"

  with conn.cursor() as cursor:
      cursor.execute(disliked_artist_query, (username))
      results = cursor.fetchall()

  conn.commit()
  conn.close()
  return results

# Given a list of artists, will remove the user, artist pair from the Dislikes table
def remove_from_disliked(username, artists):
  conn = pymysql.connect(host="localhost", port=3306, user="root", 
    password="", db="Music", charset="utf8mb4", 
    cursorclass=pymysql.cursors.DictCursor)

  remove_artist_query = "DELETE FROM Dislikes WHERE username=%s AND artist=%s"

  with conn.cursor() as cursor:
    for artist in artists:
      cursor.execute(remove_artist_query, (username, artist))

  conn.commit()
  conn.close()

