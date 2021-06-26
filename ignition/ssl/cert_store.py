'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
'''

import logging
from typing import Dict

from ..exceptions import CertRecordParseException, RemoteCertificateExpired, TofuCertificateRejection
from .cert_record import CertRecord
from .cert_wrapper import CertWrapper

logger = logging.getLogger(__name__)


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

  def get_hosts_file(self):
    '''
    Returns the currently set hosts file location
    '''
    return self.__hosts_file

  def validate_tofu_or_add(self, hostname: str, cert: CertWrapper) -> bool:
    '''
    Given the hostname & correspoding certificate, this function:
    1. Checks to see if the certificate is expired (if so, it throws a RemoteCertificateExpired exception)
    2. Fetches a corresponding stored certificate record from the client to implement a TOFU check:
      a. If there is a local cert record, and it's not expired, and it matches the passed certificate, return success
      b. If there is not a local cert record, save the certificate record locally, and return success
      c. If there is a local cert record, but it's expired, save the certificate record locally, and return success
      d. If there is a local cert record, and it's not expired, but it does not match the passed certificate, throw TofuCertificateRejection
    '''
    remote_cert_record = CertRecord(hostname, cert.fingerprint(), cert.expiration())

    if remote_cert_record.is_expired():
      raise RemoteCertificateExpired

    local_cert_record = self.__get_cert_record(hostname)

    if local_cert_record and not local_cert_record.is_expired() and local_cert_record.fingerprint != remote_cert_record.fingerprint:
      raise TofuCertificateRejection

    self.__add_cert_record(remote_cert_record)
    return True

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

    for file_line in file_lines:
      cert_record = self.__load_record(file_line)
      if cert_record is not None:
        self.__cert_store_data[cert_record.hostname] = cert_record

    return self

  def __load_record(self, file_line):
    try:
      return CertRecord.from_string(file_line)
    except CertRecordParseException:
      logger.warning(f"Invalid TOFU record encountered: '{file_line.strip()}'. This record has been skipped.")
      return None

  def __save(self):
    '''
    Saves the full set of host records back to file
    '''
    with open(self.__hosts_file, 'w') as f:
      for c in self.__cert_store_data.values():
        f.write(c.to_string())

    return self
