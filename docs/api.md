# API Documentation
The Titan2 library exposes a package `titan2` that contains all of the functionality for interfacing with Gemini capsules.

* [titan2](#titan2)
* [titan2.BaseResponse](#titan2baseresponse)
* [titan2.InputResponse](#titan2inputresponse)
* [titan2.SuccessResponse](#titan2successresponse)
* [titan2.RedirectResponse](#titan2redirectresponse)
* [titan2.TempFailureResponse](#titan2tempfailureresponse)
* [titan2.PermFailureResponse](#titan2permfailureresponse)
* [titan2.ClientCertRequiredResponse](#titan2clientcertrequiredresponse)
* [titan2.ErrorResponse](#titan2errorresponse)

## titan2
*Source Code: [src/\_\_init\_\_.py](../src/__init__.py)*

This class cannot be instantiated directly.

### Methods

#### request(url: string, referer: string = None, timeout: float = None) -> titan2.BaseResponse
Given a *url* to a Gemini capsule, this performs a request to the specified url and returns a response (as a subclass of [titan2.BaseResponse](#titan2baseresponse)) with the details associated to the response.  This is the interface that most users should use.

If a *referer* is provided, a dynamic URL is constructed by titan2 to send a request to. (*referer* expectes a fully qualified url as returned by `titan2.BaseResponse.url` or (less prefered) `titan2.url()`). Typically, in order to simplify the browsing experience, you should pass the previously requested URL as the referer to simplify URL construction logic.

*See `titan2.url()` for details around url construction with a referer.*

If a *timeout* is provided, this will specify the client timeout (in seconds) for this request.  The default is 30 seconds.  See also `titan2.set_default_timeout` to change the default timeout.

Depending on the response from the server, as per Gemini specification, the corresponding response type will be returned.

* If the response status begins with "1", the response type is `INPUT`, and will return a response of type [titan2.InputResponse](#titan2inputresponse).
* If the response status begins with "2", the response type is `STATUS`, and will return a response of type [titan2.SuccessResponse](#titan2successresponse).
* If the response status begins with "3", the response type is `REDIRECT`, and will return a response of type [titan2.RedirectResponse](#titan2redirectresponse).
* If the response status begins with "4", the response type is `TEMPORARY FAILURE`, and will return a response of type [titan2.TempFailureResponse](#titan2tempfailureresponse).
* If the response status begins with "5", the response type is `PERMANENT FAILURE`, and will return a response of type [titan2.PermFailureResponse](#titan2permfailureresponse).
* If the response status begins with "6", the response type is `CLIENT CERTIFICATE REQUIRED`, and will return a response of type [titan2.ClientCertRequiredResponse](#titan2clientcertrequiredresponse).
* If *no valid response* can be returned, titan2 assigns a response type of "0" and returns a response of type [titan2.ErrorResponse](#titan2errorresponse).

Parameters:
* url: `string`
* referer: `string` (optional)
* timeout: `float` (optional)

Returns: `[titan2.BaseResponse](#titan2baseresponse)`

#### url(url: string, referer: string = None) -> string
Given a *url* to a Gemini capsule, this returns a standardized, fully-qualified url to the Gemini capsule.  If a *referer* is provided, a dynamic URL is constructed by titan2 to send a request to.  This logic follows URL definition behavior outlined in [RFC-3986](https://tools.ietf.org/html/rfc3986).

This allows for the bulk of URL generation logic to be handled without titan2 as opposed to within the business logic of the client.  Here are some sample use cases:

*Use Case 1: Automatically populate URL protocol*
```python
titan2.url('//gemini.circumlunar.space') # => gemini://gemini.circumlunar.space
```

*Use Case 2: Navigate to an absolute path*
```python
titan2.url('/home', 'gemini://gemini.circumlunar.space') # => gemini://gemini.circumlunar.space/home
```

*Use Case 3: Navigate to a relative path*
```python
titan2.url('2', 'gemini://gemini.circumlunar.space/home') # => gemini://gemini.circumlunar.space/home/2
```

*Use Case 4: Resolve paths with navigation*
```python
titan2.url('../fun/', 'gemini://gemini.circumlunar.space/home/work/') # => gemini://gemini.circumlunar.space/home/fun/
```

*Note:* if the user's intent is to generate a url to a Gemini capsule and then make a request, titan2 recommends that you just provide the *url* and *referer* to `titan2.request()`, as that function encapsulates all of the logic within this method when making a request.  If you want to retrieve a URL from an already processed request, it is recommended to use `titan2.BaseResponse.url`, as that will store the URL that was actually used.  This method is only intended for use in constructing a URL but not generating a request.

Parameters:
* url: `string`
* referer: `string` (optional)

Returns: `string`

#### set_default_timeout(timeout: float)
Set the default timeout (in seconds) for all requests made via titan2.  The default timeout is 30 seconds.

Parameters:
* timeout: `float`

#### set_default_hosts_file(hosts_file: string)
Set the default host file location where all of the certificate fingerprints are stored in order to support Trust-On-First-Use (TOFU) validation.  By default, this file is stored in the same directory as your project in a file named `.known_hosts`.  This can be updated to any readable location but should be stored somewhere persistent for security purposes.

The format of this file is very similar to (but not identical to) the SSH `known_hosts` file.

Parameters:
* hosts_file: `string`

### Constants

#### RESPONSE_STATUS_INPUT = "1"
Possible value for `titan2.BaseResponse.status`, and will appear in any response types of `titan2.InputResponse`.  As per the Gemini documentation, this means that the requested resource requires a line of textual user input. The same resource should then be requested again with the user's input included as a query component.

See `RESPONSE_STATUSDETAIL_INPUT*` for additional detailed responses for each potential response type.

#### RESPONSE_STATUS_SUCCESS = "2"
Possible value for `titan2.BaseResponse.status`, and will appear in any response types of `titan2.SuccessResponse`.

See `RESPONSE_STATUSDETAIL_SUCCESS*` for additional detailed responses for each potential response type.  As per the Gemini documentation, the request was handled successfully and a response body is included, following the response header. The META line is a MIME media type which applies to the response body.

#### RESPONSE_STATUS_REDIRECT = "3"
Possible value for `titan2.BaseResponse.status`, and will appear in any response types of `titan2.RedirectResponse`.  As per the Gemini documentation, the server is redirecting the client to a new location for the requested resource.  The URL may be absolute or relative.  The redirect should be considered temporary (unless specied otherwise in the detailed status), i.e. clients should continue to request the resource at the original address and should not performance convenience actions like automatically updating bookmarks.

There is currently no support for automatically following redirects in Titan2.

See `RESPONSE_STATUSDETAIL_REDIRECT*` for additional detailed responses for each potential response type.

#### RESPONSE_STATUS_TEMP_FAILURE = "4"
Possible value for `titan2.BaseResponse.status`, and will appear in any response types of `titan2.TempFailureResponse`.  As per the Gemini documentation, the request has failed. The nature of the failure is temporary, i.e. an identical request MAY succeed in the future.

See `RESPONSE_STATUSDETAIL_TEMP_FAILURE*` for additional detailed responses for each potential response type.

#### RESPONSE_STATUS_PERM_FAILURE = "5"
Possible value for `titan2.BaseResponse.status`, and will appear in any response types of `titan2.PermFailureResponse`.  As per the Gemini documentation, the request has failed.  The nature of the failure is permanent, i.e. identical future requests will reliably fail for the same reason.  Automatic clients such as aggregators or indexing crawlers should not repeat this request.

See `RESPONSE_STATUSDETAIL_PERM_FAILURE*` for additional detailed responses for each potential response type.

#### RESPONSE_STATUS_CLIENTCERT_REQUIRED = "6"
Possible value for `titan2.BaseResponse.status`, and will appear in any response types of `titan2.ClientCertRequiredResponse`.  As per the Gemini documentation, the requested resource requires a client certificate to access. If the request was made without a certificate, it should be repeated with one. If the request was made with a certificate, the server did not accept it and the request should be repeated with a different certificate.

See `RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED*` for additional detailed responses for each potential response type.

#### RESPONSE_STATUS_ERROR = "0"
Possible value for `titan2.BaseResponse.status`, and will appear in any response types of `titan2.ErrorResponse`.  This status indicates that there was an error on transmission with the host and the request could not be completed.  These response types are specific to Titan2 because they are beyond the scope of the Gemini protocol and typically indicate an error with networking or communication between the client and the host.

See `RESPONSE_STATUSDETAIL_ERROR*` for additional detailed responses for each potential response type.

#### RESPONSE_STATUSDETAIL_INPUT = "10"
This is a detailed status message for response type 1x (INPUT).

As per the Gemini specification, this is the default response type and no special handling should be applied beyond what's handled by the INPUT response.

See `RESPONSE_STATUS_INPUT` for additional details.

#### RESPONSE_STATUSDETAIL_INPUT_SENSITIVE = "11"
This is a detailed status  message for response type 1x (INPUT).

As per the Gemini specification, the client should request user input but should not echo that input to the screen, and keep it protected as if it were a password.

See `RESPONSE_STATUS_INPUT` for additional details.

#### RESPONSE_STATUSDETAIL_SUCCESS = "20"
This is a detailed status message for response type 2x (SUCCESS).

As per the Gemini specification, this is the default response type and no special handling should be applied beyond what's handled by the SUCCESS response.

See `RESPONSE_STATUS_SUCCESS` for additional details.

#### RESPONSE_STATUSDETAIL_REDIRECT_TEMPORARY = "30"
This is a detailed status message for response type 3x (REDIRECT).

As per the Gemini specification, this is the default response type and no special handling should be applied beyond what's handled by the REDIRECT response.

See `RESPONSE_STATUS_REDIRECT` for additional details.

#### RESPONSE_STATUSDETAIL_REDIRECT_PERMANENT = "31"
This is a detailed status message for response type 3x (REDIRECT).

As per the Gemini specification, the specified redirect is permanent.  All indexes should be updated to avoid sending requests to the old URL.

See `RESPONSE_STATUS_REDIRECT` for additional details.

#### RESPONSE_STATUSDETAIL_TEMP_FAILURE = "40"
This is a detailed status message for response type 4x (TEMPORARY FAILURE).

As per the Gemini specification, this is the default response type and no special handling should be applied beyond what's handled by the TEMPORARY FAILURE response.

See `RESPONSE_STATUS_TEMP_FAILURE` for additional details.

#### RESPONSE_STATUSDETAIL_TEMP_FAILURE_UNAVAILABLE = "41"
This is a detailed status message for response type 4x (TEMPORARY FAILURE).

As per the Gemini specification, this represents a temporary failure due to a server issue.  The request should be retried at a later time.

See `RESPONSE_STATUS_TEMP_FAILURE` for additional details.

#### RESPONSE_STATUSDETAIL_TEMP_FAILURE_CGI = "42"
This is a detailed status message for response type 4x (TEMPORARY FAILURE).

As per the Gemini specification, this represents a temporary failure of a CGI script.  The request should be retried at a later time.

See `RESPONSE_STATUS_TEMP_FAILURE` for additional details.

#### RESPONSE_STATUSDETAIL_TEMP_FAILURE_PROXY = "43"
This is a detailed status message for response type 4x (TEMPORARY FAILURE).

As per the Gemini specification, this represents a temporary failure of a network proxy.  The request should be retried at a later time.

See `RESPONSE_STATUS_TEMP_FAILURE` for additional details.

#### RESPONSE_STATUSDETAIL_TEMP_FAILURE_SLOW_DOWN = "44"
This is a detailed status message for response type 4x (TEMPORARY FAILURE).

As per the Gemini specification, this represents temporary failure due to rate limiting.  The meta value will be an integer number of seconds which the client must wait before another request is made to this server.

See `RESPONSE_STATUS_TEMP_FAILURE` for additional details.

#### RESPONSE_STATUSDETAIL_PERM_FAILURE = "50"
This is a detailed status message for response type 5x (PERMANENT FAILURE).

As per the Gemini specification, this is the default response type and no special handling should be applied beyond what's handled by the PERMANENT FAILURE response.

See `RESPONSE_STATUS_PERM_FAILURE` for additional details.

#### RESPONSE_STATUSDETAIL_PERM_FAILURE_NOT_FOUND = "51"
This is a detailed status message for response type 5x (PERMANENT FAILURE).

As per the Gemini specification, the resource was not found.

See `RESPONSE_STATUS_PERM_FAILURE` for additional details.

#### RESPONSE_STATUSDETAIL_PERM_FAILURE_GONE = "52"
This is a detailed status message for response type 5x (PERMANENT FAILURE).

As per the Gemini specification, the resources was permanently removed.

See `RESPONSE_STATUS_PERM_FAILURE` for additional details.

#### RESPONSE_STATUSDETAIL_PERM_FAILURE_PROXY_REFUSED = "53"
This is a detailed status message for response type 5x (PERMANENT FAILURE).

As per the Gemini specification, the requested domain is not served by this server and the server does not accept proxy requests.

See `RESPONSE_STATUS_PERM_FAILURE` for additional details.

#### RESPONSE_STATUSDETAIL_PERM_FAILURE_BAD_REQUEST = "59"
This is a detailed status message for response type 5x (PERMANENT FAILURE).

As per the Gemini specification, the server could not process the client's request.  Please fix and try again.

See `RESPONSE_STATUS_PERM_FAILURE` for additional details.

#### RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED = "60"
This is a detailed status message for response type 6x (CLIENT CERTIFICATE REQUIRED).

As per the Gemini specification, this is the default response type and no special handling should be applied beyond what's handled by the CLIENT CERTIFICATE REQUIRED response.

See `RESPONSE_STATUS_CLIENTCERT_REQUIRED` for additional details.

#### RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED_NOT_AUTHORIZED = "61"
This is a detailed status message for response type 6x (CLIENT CERTIFICATE REQUIRED).

As per the Gemini specification, the supplied client certificate is not authorized.

See `RESPONSE_STATUS_CLIENTCERT_REQUIRED` for additional details.

#### RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED_NOT_VALID = "62"
This is a detailed status message for response type 6x (CLIENT CERTIFICATE REQUIRED).

As per the Gemini specification, the supplied client certificate is not valid.

See `RESPONSE_STATUS_CLIENTCERT_REQUIRED` for additional details.

#### RESPONSE_STATUSDETAIL_ERROR_UNKNOWN_HOST = "00"
This is a detailed status message for response type 0x (ERROR).

This error occurs when the server for the supplied hostname in the request cannot be resolved into an IP address.  This is typically a DNS-level error.

See `RESPONSE_STATUS_CLIENTCERT_REQUIRED` for additional details.  These response types are specific to Titan2 because they are beyond the scope of the Gemini protocol and typically indicate an error with networking or communication between the client and the host.

#### RESPONSE_STATUSDETAIL_ERROR_TIMEOUT = "01"
This is a detailed status message for response type 0x (ERROR).

This error occurs when the connection between the client and server take longer than expected.  In this case, the server may be hanging, or it may be required to increase the timeout on the client.  See `titan2.set_default_timeout()` for details around how to adjust the timeout on the client.

See `RESPONSE_STATUS_CLIENTCERT_REQUIRED` for additional details.  These response types are specific to Titan2 because they are beyond the scope of the Gemini protocol and typically indicate an error with networking or communication between the client and the host.

#### RESPONSE_STATUSDETAIL_ERROR_REFUSED = "02"
This is a detailed status message for response type 0x (ERROR).

This error occurs when a hostname can be resolved for a server, but the host refuses connection to the client.  This may be due to a incorrect port number or a firewall on the server.

See `RESPONSE_STATUS_CLIENTCERT_REQUIRED` for additional details.  These response types are specific to Titan2 because they are beyond the scope of the Gemini protocol and typically indicate an error with networking or communication between the client and the host.

#### RESPONSE_STATUSDETAIL_ERROR_HOST_ERROR = "03"
This is a detailed status message for response type 0x (ERROR).

This error occurs when there is some other error resolving the hostname via DNS.  This is more or less the catch-all for other DNS-level errors.

See `RESPONSE_STATUS_CLIENTCERT_REQUIRED` for additional details.  These response types are specific to Titan2 because they are beyond the scope of the Gemini protocol and typically indicate an error with networking or communication between the client and the host.

#### RESPONSE_STATUSDETAIL_ERROR_RESET = "04"
This is a detailed status message for response type 0x (ERROR).

This error occurs when the TCP connection to the server is reset by the remote computer.

See `RESPONSE_STATUS_CLIENTCERT_REQUIRED` for additional details.  These response types are specific to Titan2 because they are beyond the scope of the Gemini protocol and typically indicate an error with networking or communication between the client and the host.

#### RESPONSE_STATUSDETAIL_ERROR_SSL_HANDSHAKE = "05"
This is a detailed status message for response type 0x (ERROR).

This error occurs when the SSL handshake fails; this would typically be due to an error in the SSL certificate or protocol.

See `RESPONSE_STATUS_CLIENTCERT_REQUIRED` for additional details.  These response types are specific to Titan2 because they are beyond the scope of the Gemini protocol and typically indicate an error with networking or communication between the client and the host.

#### RESPONSE_STATUSDETAIL_ERROR_SSL_EXPIRED_CERT = "06"
This is a detailed status message for response type 0x (ERROR).

This error occurs if the server returns a certificate that is expired.  In this case, the SSL handshake is aborted and the connection is closed.

See `RESPONSE_STATUS_CLIENTCERT_REQUIRED` for additional details.  These response types are specific to Titan2 because they are beyond the scope of the Gemini protocol and typically indicate an error with networking or communication between the client and the host.

#### RESPONSE_STATUSDETAIL_ERROR_SSL_TOFU_REJECT = "07"
This is a detailed status message for response type 0x (ERROR).

This error occurs when the server responds with an unrecognized certificate before that certificate is expired.  Titan2 implements a Trust-On-First-Use paradigm; so if the server certificate is not recognized (and not supposed to be expired) after an initial request, the connection will be aborted and closed by the client.

See `RESPONSE_STATUS_CLIENTCERT_REQUIRED` for additional details.  These response types are specific to Titan2 because they are beyond the scope of the Gemini protocol and typically indicate an error with networking or communication between the client and the host.

#### RESPONSE_STATUSDETAIL_ERROR_BAD_RESPONSE = "08"
This is a detailed status message for response type 0x (ERROR).

This error occurs when the server returns a response that does not match the Gemini protocol requirements.  In this case, Titan2 aborts processing and closes the connection.

See `RESPONSE_STATUS_CLIENTCERT_REQUIRED` for additional details.  These response types are specific to Titan2 because they are beyond the scope of the Gemini protocol and typically indicate an error with networking or communication between the client and the host.


---


## titan2.BaseResponse
*Source Code: [src/response.py](../src/response.py)*

This class cannot be instantiated directly.

### Subclasses

[InputResponse](#titan2inputresponse), [SuccessResponse](#titan2successresponse), [RedirectResponse](#titan2redirectresponse), [TempFailureResponse](#titan2tempfailureresponse), [PermFailureResponse](#titan2permfailureresponse), [ClientCertRequiredResponse](#titan2clientcertrequiredresponse), [ErrorResponse](#titan2errorresponse)

### Members

#### basic_status
*type: `string` (length: 1 character)*

`basic_status` returns the raw one-character status response.  It will be one of the following values:

* `titan2.RESPONSE_STATUS_INPUT` = "1"
* `titan2.RESPONSE_STATUS_SUCCESS` = "2"
* `titan2.RESPONSE_STATUS_REDIRECT` = "3"
* `titan2.RESPONSE_STATUS_TEMP_FAILURE` = "4"
* `titan2.RESPONSE_STATUS_PERM_FAILURE` = "5"
* `titan2.RESPONSE_STATUS_CLIENTCERT_REQUIRED` = "6"
* `titan2.RESPONSE_STATUS_ERROR` = "0"

It is not recommended to use this value, and instead leverage the `BaseResponse.is_a()` to check the response type; however, this option has been made available if preferred.

#### status
*type: `string` (length: 2 characters)*

`status` returns the raw detailed two-character status response.  This is useful when providing specific behavior depending on the response.  The response will be one of the following values:

* `titan2.RESPONSE_STATUSDETAIL_ERROR_UNKNOWN_HOST` = "00"
* `titan2.RESPONSE_STATUSDETAIL_ERROR_TIMEOUT` = "01"
* `titan2.RESPONSE_STATUSDETAIL_ERROR_REFUSED` = "02"
* `titan2.RESPONSE_STATUSDETAIL_ERROR_HOST_ERROR` = "03"
* `titan2.RESPONSE_STATUSDETAIL_ERROR_RESET` = "04"
* `titan2.RESPONSE_STATUSDETAIL_ERROR_SSL_HANDSHAKE` = "05"
* `titan2.RESPONSE_STATUSDETAIL_ERROR_SSL_EXPIRED_CERT` = "06"
* `titan2.RESPONSE_STATUSDETAIL_ERROR_SSL_TOFU_REJECT` = "07"
* `titan2.RESPONSE_STATUSDETAIL_ERROR_BAD_RESPONSE` = "08"
* `titan2.RESPONSE_STATUSDETAIL_INPUT` = "10"
* `titan2.RESPONSE_STATUSDETAIL_INPUT_SENSITIVE` = "11"
* `titan2.RESPONSE_STATUSDETAIL_SUCCESS` = "20"
* `titan2.RESPONSE_STATUSDETAIL_REDIRECT_TEMPORARY` = "30"
* `titan2.RESPONSE_STATUSDETAIL_REDIRECT_PERMANENT` = "31"
* `titan2.RESPONSE_STATUSDETAIL_TEMP_FAILURE` = "40"
* `titan2.RESPONSE_STATUSDETAIL_TEMP_FAILURE_UNAVAILABLE` = "41"
* `titan2.RESPONSE_STATUSDETAIL_TEMP_FAILURE_CGI` = "42"
* `titan2.RESPONSE_STATUSDETAIL_TEMP_FAILURE_PROXY` = "43"
* `titan2.RESPONSE_STATUSDETAIL_TEMP_FAILURE_SLOW_DOWN` = "44"
* `titan2.RESPONSE_STATUSDETAIL_PERM_FAILURE` = "50"
* `titan2.RESPONSE_STATUSDETAIL_PERM_FAILURE_NOT_FOUND` = "51"
* `titan2.RESPONSE_STATUSDETAIL_PERM_FAILURE_GONE` = "52"
* `titan2.RESPONSE_STATUSDETAIL_PERM_FAILURE_PROXY_REFUSED` = "53"
* `titan2.RESPONSE_STATUSDETAIL_PERM_FAILURE_BAD_REQUEST` = "59"
* `titan2.RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED` = "60"
* `titan2.RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED_NOT_AUTHORIZED` = "61"
* `titan2.RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED_NOT_VALID` = "62"

This member SHOULD be used to facilitate status-specific behavior by a client.

#### meta
*type: `string` (length <= 1024 characters)*

`meta` is the raw meta field returned in the response header from the Gemini server.  In general, it is NOT RECOMMENDED to use this in favor of `BaseResponse.data()` method to retrieve the meta field for non-20 responses, but this can be used if preferred.

#### raw_body
*type: `bytes`*

`raw_body` is the raw bytestring stored in the response, before encoding.  This response SHOULD only be used for debug purposes, but it is typically preferred to use `BaseResponse.data()` for success messages as this will decode the response body according to the charset provided in the response META.

#### url
*type: `string`*

Returns the fully qualified URL of the request after processing.  This value MAY be passed to subsequent responses in the `referer` field in order to help to construct fully qualified URLs on the request.

### Methods

#### data() -> string
Returns the user-facing data for each method.  This is method is unique for each response type.

* [titan2.ErrorResponse](#titan2errorresponse)
* [titan2.InputResponse](#titan2inputresponse)
* [titan2.SuccessResponse](#titan2successresponse)
* [titan2.RedirectResponse](#titan2redirectresponse)
* [titan2.TempFailureResponse](#titan2tempfailureresponse)
* [titan2.PermFailureResponse](#titan2permfailureresponse)
* [titan2.ClientCertRequiredResponse](#titan2clientcertrequiredresponse)

Returns: `string`

#### success() -> boolean
Utility method to check if the response was successful, defined by a status response of `20`.

This is useful if you just need to confirm that the message contains a body or not.

Returns: `boolean`

#### is_a(response_class_type: class) -> bool
Utility method to qualify the response type.  The response type from a request will be one of: titan2.ErrorResponse, titan2.InputResponse, titan2.SuccessResponse, titan2.RedirectResponse, titan2.TempFailureResponse, titan2.TempFailureResponse, titan2.PermFailureResponse, titan2.ClientCertRequiredResponse.  This will return `true` if the response type matches the current object type.

This is recommended for use when routing behavior based on a response.

*Note: This only qualifies the `basic_status` of a response.  For any additional behavior it is required to check the `BaseResponse.status` for detailed status.*

Parameters:
* response_class_type: `titan2.BaseResponse` class

Returns: `boolean`


---


## titan2.InputResponse
**Extends [titan2.BaseResponse](#titan2baseresponse)**

*Source Code: [src/response.py](../src/response.py)*

This class cannot be instantiated directly.

### Members

#### basic_status
*type: `string` (length: 1 character)*

Extended from [titan2.BaseResponse](#titan2baseresponse)

`basic_status` returns the raw one-character status response.  In the case of the `InputResponse`, this value will always be:

* `titan2.RESPONSE_STATUS_INPUT` = "1"

It is not recommended to use this value, and instead leverage the `InputResponse.is_a()` to check the response type; however, this option has been made available if preferred.

#### status
*type: `string` (length: 2 characters)*

Extended from [titan2.BaseResponse](#titan2baseresponse)

`status` returns the raw detailed two-character status response.  This is useful when providing specific behavior depending on the response.  In the case of the `InputResponse`, this value will always be one of:

* `titan2.RESPONSE_STATUSDETAIL_INPUT` = "10"
* `titan2.RESPONSE_STATUSDETAIL_INPUT_SENSITIVE` = "11"

This member SHOULD be used to facilitate status-specific behavior by a client.

#### meta
*type: `string` (length <= 1024 characters)*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

#### raw_body
*type: `bytes`*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

#### url
*type: `string`*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

### Methods

#### data() -> string
This returns the prompt to display to the user in order to request the textual user input, which was provided as part of the META response to the user in the header.

Returns: `string`

#### success() -> boolean
Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

Returns: `boolean`

#### is_a(response_class_type: class) -> boolean
Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

Returns: `boolean`


---


## titan2.SuccessResponse
**Extends [titan2.BaseResponse](#titan2baseresponse)**

*Source Code: [src/response.py](../src/response.py)*

This class cannot be instantiated directly.

### Members

#### basic_status
*type: `string` (length: 1 character)*

Extended from [titan2.BaseResponse](#titan2baseresponse)

`basic_status` returns the raw one-character status response.  In the case of the `SuccessResponse`, this value will always be:

* `titan2.RESPONSE_STATUS_SUCCESS` = "2"

It is not recommended to use this value, and instead leverage the `SuccessResponse.is_a()` to check the response type; however, this option has been made available if preferred.

#### status
*type: `string` (length: 2 characters)*

Extended from [titan2.BaseResponse](#titan2baseresponse)

`status` returns the raw detailed two-character status response.  This is useful when providing specific behavior depending on the response.  In the case of the `SuccessResponse`, this value will always be:

* `titan2.RESPONSE_STATUSDETAIL_SUCCESS` = "20"

This member SHOULD be used to facilitate status-specific behavior by a client.

#### meta
*type: `string` (length <= 1024 characters)*

In the context of a success response, this will include additional information including Mime Type and encoding.  This is useful for a SuccessResponse.

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

#### raw_body
*type: `bytes`*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

#### url
*type: `string`*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

### Methods

#### data() -> string
Returns the full request body in the Success response, encoded according to the META mime type.  Note: this function does not do any additional formatting of the response payload beyond mapping the encoding.

Returns: `string`

#### success() -> boolean
Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

Returns: `boolean`

#### is_a(response_class_type: class) -> boolean
Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

Returns: `boolean`


---


## titan2.RedirectResponse
**Extends [titan2.BaseResponse](#titan2baseresponse)**

*Source Code: [src/response.py](../src/response.py)*

This class cannot be instantiated directly.

### Members

#### basic_status
*type: `string` (length: 1 character)*

Extended from [titan2.BaseResponse](#titan2baseresponse)

`basic_status` returns the raw one-character status response.  In the case of the `RedirectResponse`, this value will always be:

* `titan2.RESPONSE_STATUS_REDIRECT` = "3"

It is not recommended to use this value, and instead leverage the `RedirectResponse.is_a()` to check the response type; however, this option has been made available if preferred.

#### status
*type: `string` (length: 2 characters)*

Extended from [titan2.BaseResponse](#titan2baseresponse)

`status` returns the raw detailed two-character status response.  This is useful when providing specific behavior depending on the response.  In the case of the `RedirectResponse`, this value will always be one of:

* `titan2.RESPONSE_STATUSDETAIL_REDIRECT_TEMPORARY` = "30"
* `titan2.RESPONSE_STATUSDETAIL_REDIRECT_PERMANENT` = "31"

This member SHOULD be used to facilitate status-specific behavior by a client.

#### meta
*type: `string` (length <= 1024 characters)*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

#### raw_body
*type: `bytes`*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

#### url
*type: `string`*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

### Methods

#### data() -> string
Returns the new url location for the requested response based on the META value for the Redirect response.

Returns: `string`

#### success() -> boolean
Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

Returns: `boolean`

#### is_a(response_class_type: class) -> boolean
Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

Returns: `boolean`


---


## titan2.TempFailureResponse
**Extends [titan2.BaseResponse](#titan2baseresponse)**

*Source Code: [src/response.py](../src/response.py)*

This class cannot be instantiated directly.

### Members

#### basic_status
*type: `string` (length: 1 character)*

Extended from [titan2.BaseResponse](#titan2baseresponse)

`basic_status` returns the raw one-character status response.  In the case of the `TempFailureResponse`, this value will always be:

* `titan2.RESPONSE_STATUS_TEMP_FAILURE` = "4"

It is not recommended to use this value, and instead leverage the `TempFailureResponse.is_a()` to check the response type; however, this option has been made available if preferred.

#### status
*type: `string` (length: 2 characters)*

Extended from [titan2.BaseResponse](#titan2baseresponse)

`status` returns the raw detailed two-character status response.  This is useful when providing specific behavior depending on the response.  In the case of the `TempFailureResponse`, this value will always be one of:

* `titan2.RESPONSE_STATUSDETAIL_TEMP_FAILURE` = "40"
* `titan2.RESPONSE_STATUSDETAIL_TEMP_FAILURE_UNAVAILABLE` = "41"
* `titan2.RESPONSE_STATUSDETAIL_TEMP_FAILURE_CGI` = "42"
* `titan2.RESPONSE_STATUSDETAIL_TEMP_FAILURE_PROXY` = "43"
* `titan2.RESPONSE_STATUSDETAIL_TEMP_FAILURE_SLOW_DOWN` = "44"

This member SHOULD be used to facilitate status-specific behavior by a client.

#### meta
*type: `string` (length <= 1024 characters)*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

#### raw_body
*type: `bytes`*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

#### url
*type: `string`*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

### Methods

#### data() -> string
Returns the contents of the META field to provide additional information regarding the failure to the user.

Returns: `string`

#### success() -> boolean
Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

Returns: `boolean`

#### is_a(response_class_type: class) -> boolean
Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

Returns: `boolean`


---


## titan2.PermFailureResponse
**Extends [titan2.BaseResponse](#titan2baseresponse)**

*Source Code: [src/response.py](../src/response.py)*

This class cannot be instantiated directly.

### Members

#### basic_status
*type: `string` (length: 1 character)*

Extended from [titan2.BaseResponse](#titan2baseresponse)

`basic_status` returns the raw one-character status response.  In the case of the `PermFailureResponse`, this value will always be:

* `titan2.RESPONSE_STATUS_PERM_FAILURE` = "5"

It is not recommended to use this value, and instead leverage the `PermFailureResponse.is_a()` to check the response type; however, this option has been made available if preferred.

#### status
*type: `string` (length: 2 characters)*

Extended from [titan2.BaseResponse](#titan2baseresponse)

`status` returns the raw detailed two-character status response.  This is useful when providing specific behavior depending on the response.  In the case of the `PermFailureResponse`, this value will always be one of:

* `titan2.RESPONSE_STATUSDETAIL_PERM_FAILURE` = "50"
* `titan2.RESPONSE_STATUSDETAIL_PERM_FAILURE_NOT_FOUND` = "51"
* `titan2.RESPONSE_STATUSDETAIL_PERM_FAILURE_GONE` = "52"
* `titan2.RESPONSE_STATUSDETAIL_PERM_FAILURE_PROXY_REFUSED` = "53"
* `titan2.RESPONSE_STATUSDETAIL_PERM_FAILURE_BAD_REQUEST` = "59"

This member SHOULD be used to facilitate status-specific behavior by a client.

#### meta
*type: `string` (length <= 1024 characters)*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

#### raw_body
*type: `bytes`*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

#### url
*type: `string`*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

### Methods

#### data() -> string
Returns the contents of the META field to provide additional information regarding the failure to the user.

Returns: `string`

#### success() -> boolean
Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

Returns: `boolean`

#### is_a(response_class_type: class) -> boolean
Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

Returns: `boolean`


---


## titan2.ClientCertRequiredResponse
**Extends [titan2.BaseResponse](#titan2baseresponse)**

*Source Code: [src/response.py](../src/response.py)*

This class cannot be instantiated directly.

### Members

#### basic_status
*type: `string` (length: 1 character)*

Extended from [titan2.BaseResponse](#titan2baseresponse)

`basic_status` returns the raw one-character status response.  In the case of the `ClientCertRequiredResponse`, this value will always be:

* `titan2.RESPONSE_STATUS_CLIENTCERT_REQUIRED` = "6"

It is not recommended to use this value, and instead leverage the `ClientCertRequiredResponse.is_a()` to check the response type; however, this option has been made available if preferred.

#### status
*type: `string` (length: 2 characters)*

Extended from [titan2.BaseResponse](#titan2baseresponse)

`status` returns the raw detailed two-character status response.  This is useful when providing specific behavior depending on the response.  In the case of the `ClientCertRequiredResponse`, this value will always be one of:

* `titan2.RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED` = "60"
* `titan2.RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED_NOT_AUTHORIZED` = "61"
* `titan2.RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED_NOT_VALID` = "62"

This member SHOULD be used to facilitate status-specific behavior by a client.

#### meta
*type: `string` (length <= 1024 characters)*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

#### raw_body
*type: `bytes`*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

#### url
*type: `string`*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

### Methods

#### data() -> string
Returns the additional information on certificate requirements, or the reason that the certificate was rejected.  These are the contents of the META field for a Client Certificate Required response.

Returns: `string`

#### success() -> boolean
Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

Returns: `boolean`

#### is_a(response_class_type: class) -> boolean
Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

Returns: `boolean`


---


## titan2.ErrorResponse
**Extends [titan2.BaseResponse](#titan2baseresponse)**

*Source Code: [src/response.py](../src/response.py)*

This class cannot be instantiated directly.

### Members

#### basic_status
*type: `string` (length: 1 character)*

Extended from [titan2.BaseResponse](#titan2baseresponse)

`basic_status` returns the raw one-character status response.  In the case of the `ErrorResponse`, this value will always be:

* `titan2.RESPONSE_STATUS_ERROR` = "0"

It is not recommended to use this value, and instead leverage the `ErrorResponse.is_a()` to check the response type; however, this option has been made available if preferred.

#### status
*type: `string` (length: 2 characters)*

Extended from [titan2.BaseResponse](#titan2baseresponse)

`status` returns the raw detailed two-character status response.  This is useful when providing specific behavior depending on the response.  In the case of the `ErrorResponse`, this value will always be one of:

* `titan2.RESPONSE_STATUSDETAIL_ERROR_UNKNOWN_HOST` = "00"
* `titan2.RESPONSE_STATUSDETAIL_ERROR_TIMEOUT` = "01"
* `titan2.RESPONSE_STATUSDETAIL_ERROR_REFUSED` = "02"
* `titan2.RESPONSE_STATUSDETAIL_ERROR_HOST_ERROR` = "03"
* `titan2.RESPONSE_STATUSDETAIL_ERROR_RESET` = "04"
* `titan2.RESPONSE_STATUSDETAIL_ERROR_SSL_HANDSHAKE` = "05"
* `titan2.RESPONSE_STATUSDETAIL_ERROR_SSL_EXPIRED_CERT` = "06"
* `titan2.RESPONSE_STATUSDETAIL_ERROR_SSL_TOFU_REJECT` = "07"
* `titan2.RESPONSE_STATUSDETAIL_ERROR_BAD_RESPONSE` = "08"

This member SHOULD be used to facilitate status-specific behavior by a client.

#### meta
*type: `string` (length <= 1024 characters)*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

#### raw_body
*type: `bytes`*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

#### url
*type: `string`*

Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

### Methods

#### data() -> string
Provides an error message related to the Error failure type as defined by titan2.  See failure constants as defined in the `status` field for full details on each error type.

Returns: `string`

#### success() -> boolean
Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

Returns: `boolean`

#### is_a(response_class_type: class) -> boolean
Extended from [titan2.BaseResponse](#titan2baseresponse). See parent class for full details.

Returns: `boolean`