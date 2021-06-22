'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
'''

import cryptography
from cryptography import x509
from cryptography.hazmat.backends import default_backend


class CertWrapper:
  '''
  Certificate as defined by x509
  '''
  certificate: cryptography.x509.Certificate
  '''
  Certificate fingerprint, to be used in TOFU handling and response
  '''
  public_key_fingerprint: str

  def __init__(self, certificate: cryptography.x509.Certificate):
    '''
    Constructor
    '''
    self.certificate = certificate

  def expiration(self) -> str:
    '''
    Access function for certificate expiration date
    '''
    return self.certificate.not_valid_after

  def fingerprint(self) -> str:
    '''
    Extracts the public key & expiration date from the cert,
    and returns the public key openssh fingerprint
    '''
    return self.certificate.public_key().public_bytes(
      cryptography.hazmat.primitives.serialization.Encoding.OpenSSH,
      cryptography.hazmat.primitives.serialization.PublicFormat.OpenSSH
    ).decode('utf-8')

  @classmethod
  def parse(cls, raw_certificate: bytes):
    '''
    Takes as input the raw certificate (originally from the TCP socket)
    Returns a certificate wrapper
    '''
    x509_certificate = x509.load_der_x509_certificate(raw_certificate, default_backend())
    return CertWrapper(x509_certificate)
