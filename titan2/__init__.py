from .request import Request
from .session_manager import SessionManager
from .globals import *

def request(url):
  return Request(url).send()

def session_manager():
  return SessionManager()