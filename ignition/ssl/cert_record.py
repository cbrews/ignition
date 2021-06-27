'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
'''

import datetime

from ..exceptions import CertRecordParseException
from ..globals import *


class CertRecord:
  '''
  Manages a single Certificate Record with a hostfile, signature, and expiration
  '''
  hostname: str
  fingerprint: str
  expiration: datetime.datetime

  def __init__(self, hostname: str, fingerprint: str, expiration: datetime.datetime):
    '''
    Generate a CertRecord from logic; passing in the hostname, fingerprint, and expiration
    '''
    self.hostname = hostname
    self.fingerprint = fingerprint
    self.expiration = expiration

  @classmethod
  def from_string(cls, host_string: str):
    '''
    Generate a CertRecord from a string in the format:
    [HOSTNAME] [SSH-ALGORITHM PUBLIC_KEY];EXPIRES=[YYYY-MM-DDTHH:mm:ss.SSSZ]
    '''
    try:
      hostname, fingerprint_with_expiration = host_string.strip().split(' ', maxsplit=1)
      fingerprint, expiration = fingerprint_with_expiration.split(';EXPIRES=')
      expiration_datetime = datetime.datetime.fromisoformat(expiration)

      return CertRecord(hostname, fingerprint, expiration_datetime)
    except Exception as e:
      raise CertRecordParseException() from e

  def to_string(self):
    '''
    Converts a CertRecord to a string in the format:
    [HOSTNAME] [SSH-ALGORITHM PUBLIC_KEY];EXPIRES=[YYYY-MM-DDTHH:mm:ss.SSSZ]
    '''
    return self.hostname + ' ' + self.fingerprint + ';EXPIRES=' + self.expiration.isoformat() + EOL

  def is_expired(self):
    '''
    Returns true if the expiration date on the cert record is before now
    '''
    return self.expiration < self.now()

  def now(self):
    '''
    Utility function to get current datetime, extracted for testing purposes
    Returns datetime
    '''
    return datetime.datetime.now()
