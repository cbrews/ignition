'''
This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL
was not distributed with this file, You can obtain one
at http://mozilla.org/MPL/2.0/.
'''


class RemoteCertificateExpired(Exception):
  '''
  An exception type to handle expired certificates from the remote server.
  This should throw if the remote certificate expiration date
  '''


class TofuCertificateRejection(Exception):
  '''
  An exception type handle TOFU (trust-on-first-use rejection).
  '''


class CertRecordParseException(Exception):
  '''
  An exception triggered on cert record parsing.
  '''


class GeminiResponseParseError(Exception):
  '''
  Raised when the gemini protocol data response cannot be parsed.
  '''
