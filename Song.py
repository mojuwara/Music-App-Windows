class Song:
  def __init__(self, song_name, artist, features_string, release_date, link, features_list):
    self.song_name = song_name
    self.artist = artist
    self.features_string = features_string        # String object (possibly empty)
    self.release_date = release_date
    self.link = link
    self.features_list = features_list            # List object (possibly empty)
  
  def get_song_name(self):
    return self.song_name

  def get_artist(self):
    return self.artist

  def get_release_date(self):
    return self.release_date

  def get_link(self):
    return self.link
  
  def get_features_string(self):
    return self.features_string

  def get_features_list(self):
    return self.features_list