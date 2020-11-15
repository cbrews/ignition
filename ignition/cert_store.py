'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one 
at http://mozilla.org/MPL/2.0/.
'''

import cryptography
from cryptography import x509
import datetime
from typing import Dict, Tuple

from .globals import *

class RemoteCertificateExpired(Exception):
  '''
  An exception type to handle expired certificates from the remote server.
  This should throw if the remote certificate expiration date 
  '''
  pass

class TofuCertificateRejection(Exception):
  '''
  An exception type handle TOFU (trust-on-first-use rejection).
  '''
  pass

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
  def from_string(self, host_string: str):
    '''
    Generate a CertRecord from a string in the format:
    [HOSTNAME] [SSH-ALGORITHM PUBLIC_KEY];EXPIRES=[YYYY-MM-DDTHH:mm:ss.SSSZ]
    '''
    hostname, fingerprint_with_expiration = host_string.strip().split(' ', maxsplit=1)
    fingerprint, expiration = fingerprint_with_expiration.split(';EXPIRES=')
    expiration_datetime = datetime.datetime.fromisoformat(expiration)

    return CertRecord(hostname, fingerprint, expiration_datetime)

  def to_string(self):
    '''
    Converts a CertRecord to a string in the format:
    [HOSTNAME] [SSH-ALGORITHM PUBLIC_KEY];EXPIRES=[YYYY-MM-DDTHH:mm:ss.SSSZ]
    '''
    return self.hostname + ' ' + self.fingerprint + ';EXPIRES=' + self.expiration.isoformat() + CRLF

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

class CertStore:
  '''
  Data structure to store the certificates across visited hosts
  '''

  __hosts_file: str
  __cert_store_data: Dict[str, CertRecord]

  def __init__(self, hosts_file):
    '''
    Initializes a new cert store with a specified file to store the certificate fingerprint & expiration dates
    '''
    self.__cert_store_data = {}
    self.__hosts_file = hosts_file

  def set_hosts_file(self, hosts_file):
    '''
    Updates the specified file for certificate fingerprint storage
    '''
    self.__hosts_file = hosts_file

  def validate_tofu_or_add(self, hostname: str, raw_certificate: bytes) -> bool:
    '''
    Given the hostname & correspoding certificate, this function:
    1. Checks to see if the certificate is expired (if so, it throws a RemoteCertificateExpired exception)
    2. Fetches a corresponding stored certificate record from the client to implement a TOFU check:
      a. If there is a local cert record, and it's not expired, and it matches the passed certificate, return success
      b. If there is not a local cert record, save the certificate record locally, and return success
      c. If there is a local cert record, but it's expired, save the certificate record locally, and return success
      d. If there is a local cert record, and it's not expired, but it does not match the passed certificate, throw TofuCertificateRejection
    '''
    fingerprint, expiration = self.__parse_raw_certificate(raw_certificate)
    remote_cert_record = CertRecord(hostname, fingerprint, expiration)

    if remote_cert_record.is_expired():
      raise RemoteCertificateExpired

    local_cert_record = self.__get_cert_record(hostname)

    if local_cert_record and not local_cert_record.is_expired() and local_cert_record.fingerprint != remote_cert_record.fingerprint:
      raise TofuCertificateRejection

    self.__add_cert_record(remote_cert_record)
    return True

  def __parse_raw_certificate(self, raw_certificate: bytes) -> Tuple[str, str]:
    '''
    Takes as input the raw certificate from the TCP socket
    Extracts the public key & expiration date from the cert
    Returns a public key openssh fingerprint
    '''
    cert = x509.load_der_x509_certificate(raw_certificate)
    expiration = cert.not_valid_after
    public_key_fingerprint = cert.public_key().public_bytes(
      cryptography.hazmat.primitives.serialization.Encoding.OpenSSH,
      cryptography.hazmat.primitives.serialization.PublicFormat.OpenSSH
    ).decode('utf-8')

    return (public_key_fingerprint, expiration)

  def __get_cert_record(self, hostname: str) -> CertRecord:
    '''
    Fetch the corresponding CertRecord for passed hostname from the local storage (file)
    TODO: smarter loading logic
    '''
    self.__load()
    return self.__cert_store_data.get(hostname, None)

  def __add_cert_record(self, cert_record: CertRecord):
    '''
    Add a CertRecord for the corresponding hostname to local storage (file) and save to file
    TODO: smarter saving logic
    '''
    self.__cert_store_data[cert_record.hostname] = cert_record
    self.__save()
    return self

  def __load(self):
    '''
    Reloads the hosts file from storage and copies that into memory
    '''
    file_lines = []
    try:
      with open(self.__hosts_file, 'r') as f:
        file_lines = f.readlines()
    except FileNotFoundError:
      file_lines = []
    
    cert_records = [CertRecord.from_string(l) for l in file_lines]

    for c in cert_records:
      self.__cert_store_data[c.hostname] = c

    return self

  def __save(self):
    '''
    Saves the full set of host records back to file
    '''
    with open(self.__hosts_file, 'w') as f:
      for c in self.__cert_store_data.values():
        f.write(c.to_string())
    
    return self
