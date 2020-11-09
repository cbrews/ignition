from .request import Request

class SessionManager:
  def __init__(self, timeout=None, homepage='//gemini.circumlunar.space/', max_history=50):
    self.__session_history = []
    self.__ca_certs = {}
    self.__max_history = max_history
    self.__timeout = timeout
    self.__homepage = homepage
  
  def start(self):
    return self.request(self.__homepage)

  def request(self, url):
    req = self.__create_request_object(url)
    response = req.send()
    self.__add_to_history(url)
    return response

  def history(self):
    return self.__session_history

  def __add_to_history(self, url):
    self.__session_history.insert(0, url)

    if len(self.__session_history) > self.__max_history:
      self.__session_history = self.__session_history[0:self.__max_history / 2]

  def __create_request_object(self, url):
    if len(self.__session_history) == 0:
      return Request(url, timeout=self.__timeout)
    return Request(url, referer=self.__session_history[0], timeout=self.__timeout)