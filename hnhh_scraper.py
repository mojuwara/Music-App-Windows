from requests import get
from bs4 import BeautifulSoup
from Song import *
import datetime

class HNHHScraper:
  def __init__(self):
    self.url = "https://www.hotnewhiphop.com/songs/" #/page_number/
    self.excluded = {",", "&"}

  """ Creates and returns a list of song objects for all songs on the page. """
  def scrape_songs(self, page_num=0):
    song_list = []
    url = self.url + str(page_num) + "/"
    response = get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")

    # Loop for each song on the current page
    for song in content.findAll("div", {"class" : "grid-item song"}):
      throwback = False
      song_name = song.find("a", {"class" : "cover-title grid-item-title"}).text.strip()

      # May be a song made by a group of artists
      for group in song.findAll("div", {"class" : "grid-item-artists"}):
        artists = group.findAll("em", {"class" : "default-artist"})
        main_artists = "".join([individual.text.strip() + " " for individual in artists]).strip()

        # Extract feature artist(s) if any
        features_list = []
        for feature in group.findAll("em", {"class" : "no-bold"}):
          if feature not in self.excluded:
            features_list.append(feature.text.strip()) 
        features_list = ", ".join(features_list)

      # Extract the release date of the song & find out if this is a throwback
      for meta_data in song.findAll("div", {"class" : "grid-item-meta-info hidden-md-down"}):
        for tag in meta_data.findAll("span", {"class" : "song-review"}):
          if (tag.text == "THROWBACK"):
            throwback = True
        for time in meta_data.findAll("span", {"class" : "grid-item-time song pull-right"}):
          release_date = self.format_date(time.findAll("span")[0].text.strip())

      # Extract the link to the song page
      prefix = "https://www.hotnewhiphop.com"
      for link in song.findAll("a", {"class" : "cover-title grid-item-title"}, href=True):
        song_page = prefix + link["href"]
      
      # Append to song list
      if (not throwback):
        song_list.append(Song(song_name, main_artists, features_list, release_date, song_page))
      else:
        print("Throwback:\t {} : {} : {}".format(main_artists, song_name, song_page))

    # Return list of Song objects
    return song_list

  # Given a string (ex: 'Apr 15, 2019', '13 h') returns it as 'YYYY-MM-DD'
  def format_date(self, date):
    # True assuming that songs are scraped at the end of the day)
    if (len(date) <= 4): 
      return str(datetime.date.today())

    month_dict = {"Jan" : "01", "Feb" : "02", "Mar" : "03", "Apr" : "04", 
                  "May" : "05", "Jun" : "06", "Jul" : "07", "Aug" : "08", 
                  "Sep" : "09", "Oct" : "10", "Nov" : "11", "Dec" : "12"}

    date = date.replace(",", "")
    date = date.split()
    date[0] = month_dict[date[0]]
    return date[2] + "-" + date[0] + "-" + date[1]