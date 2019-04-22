class Song:
  def __init__(self, song_name, artist, features, release_date, link):
    self.song_name = song_name
    self.artist = artist
    self.features = features        # List object (possibly empty)
    self.release_date = release_date
    self.link = link
  
  def get_song_name(self):
    return self.song_name

  def get_artist(self):
    return self.artist

  def get_release_date(self):
    return self.release_date

  def get_link(self):
    return self.link
  
  def get_features(self):
    return self.features