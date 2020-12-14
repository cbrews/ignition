# API Documentation
The Ignition library exposes a package `ignition` that contains all of the functionality for interfacing with Gemini capsules.

* [ignition](#ignition)
* [ignition.BaseResponse](#ignitionbaseresponse)
* [ignition.InputResponse](#ignitioninputresponse)
* [ignition.SuccessResponse](#ignitionsuccessresponse)
* [ignition.RedirectResponse](#ignitionredirectresponse)
* [ignition.TempFailureResponse](#ignitiontempfailureresponse)
* [ignition.PermFailureResponse](#ignitionpermfailureresponse)
* [ignition.ClientCertRequiredResponse](#ignitionclientcertrequiredresponse)
* [ignition.ErrorResponse](#ignitionerrorresponse)

## ignition
*Source Code: [src/\_\_init\_\_.py](../src/__init__.py)*

Load this with
```python
import ignition
```

This class cannot be instantiated directly.

### Methods

#### request(url: string, referer: string = None, timeout: float = None) -> ignition.BaseResponse
Given a *url* to a Gemini capsule, this performs a request to the specified url and returns a response (as a subclass of [ignition.BaseResponse](#ignitionbaseresponse)) with the details associated to the response.  This is the interface that most users should use.

If a *referer* is provided, a dynamic URL is constructed by ignition to send a request to. (*referer* expectes a fully qualified url as returned by `ignition.BaseResponse.url` or (less prefered) `ignition.url()`). Typically, in order to simplify the browsing experience, you should pass the previously requested URL as the referer to simplify URL construction logic.

*See `ignition.url()` for details around url construction with a referer.*

If a *timeout* is provided, this will specify the client timeout (in seconds) for this request.  The default is 30 seconds.  See also `ignition.set_default_timeout` to change the default timeout.

If a *ca_cert* is provided, the certificate will be sent to the server as a CA CERT.  You will need to provide the paths to both the certificate and the key in this case.

Depending on the response from the server, as per Gemini specification, the corresponding response type will be returned.

* If the response status begins with "1", the response type is `INPUT`, and will return a response of type [ignition.InputResponse](#ignitioninputresponse).
* If the response status begins with "2", the response type is `STATUS`, and will return a response of type [ignition.SuccessResponse](#ignitionsuccessresponse).
* If the response status begins with "3", the response type is `REDIRECT`, and will return a response of type [ignition.RedirectResponse](#ignitionredirectresponse).
* If the response status begins with "4", the response type is `TEMPORARY FAILURE`, and will return a response of type [ignition.TempFailureResponse](#ignitiontempfailureresponse).
* If the response status begins with "5", the response type is `PERMANENT FAILURE`, and will return a response of type [ignition.PermFailureResponse](#ignitionpermfailureresponse).
* If the response status begins with "6", the response type is `CLIENT CERTIFICATE REQUIRED`, and will return a response of type [ignition.ClientCertRequiredResponse](#ignitionclientcertrequiredresponse).
* If *no valid response* can be returned, ignition assigns a response type of "0" and returns a response of type [ignition.ErrorResponse](#ignitionerrorresponse).

Parameters:
* url: `string`
* referer: `string` (optional)
* timeout: `float` (optional)
* ca_cert: `Tuple(cert_file, key_file)` (optional)

Returns: `[ignition.BaseResponse](#ignitionbaseresponse)`

#### url(url: string, referer: string = None) -> string
Given a *url* to a Gemini capsule, this returns a standardized, fully-qualified url to the Gemini capsule.  If a *referer* is provided, a dynamic URL is constructed by ignition to send a request to.  This logic follows URL definition behavior outlined in [RFC-3986](https://tools.ietf.org/html/rfc3986).

This allows for the bulk of URL generation logic to be handled without ignition as opposed to within the business logic of the client.  Here are some sample use cases:

*Use Case 1: Automatically populate URL protocol*
```python
ignition.url('//gemini.circumlunar.space') # => gemini://gemini.circumlunar.space
```

*Use Case 2: Navigate to an absolute path*
```python
ignition.url('/home', 'gemini://gemini.circumlunar.space') # => gemini://gemini.circumlunar.space/home
```

*Use Case 3: Navigate to a relative path*
```python
ignition.url('2', 'gemini://gemini.circumlunar.space/home') # => gemini://gemini.circumlunar.space/home/2
```

*Use Case 4: Resolve paths with navigation*
```python
ignition.url('../fun/', 'gemini://gemini.circumlunar.space/home/work/') # => gemini://gemini.circumlunar.space/home/fun/
```

*Note:* if the user's intent is to generate a url to a Gemini capsule and then make a request, ignition recommends that you just provide the *url* and *referer* to `ignition.request()`, as that function encapsulates all of the logic within this method when making a request.  If you want to retrieve a URL from an already processed request, it is recommended to use `ignition.BaseResponse.url`, as that will store the URL that was actually used.  This method is only intended for use in constructing a URL but not generating a request.

Parameters:
* url: `string`
* referer: `string` (optional)

Returns: `string`

#### set_default_timeout(timeout: float)
Set the default timeout (in seconds) for all requests made via ignition.  The default timeout is 30 seconds.

Parameters:
* timeout: `float`

#### set_default_hosts_file(hosts_file: string)
Set the default host file location where all of the certificate fingerprints are stored in order to support Trust-On-First-Use (TOFU) validation.  By default, this file is stored in the same directory as your project in a file named `.known_hosts`.  This can be updated to any readable location but should be stored somewhere persistent for security purposes.

The format of this file is very similar to (but not identical to) the SSH `known_hosts` file.

Parameters:
* hosts_file: `string`

### Constants

#### RESPONSE_STATUS_INPUT = "1"
Possible value for `ignition.BaseResponse.status`, and will appear in any response types of `ignition.InputResponse`.  As per the Gemini documentation, this means that the requested resource requires a line of textual user input. The same resource should then be requested again with the user's input included as a query component.

See `RESPONSE_STATUSDETAIL_INPUT*` for additional detailed responses for each potential response type.

#### RESPONSE_STATUS_SUCCESS = "2"
Possible value for `ignition.BaseResponse.status`, and will appear in any response types of `ignition.SuccessResponse`.

See `RESPONSE_STATUSDETAIL_SUCCESS*` for additional detailed responses for each potential response type.  As per the Gemini documentation, the request was handled successfully and a response body is included, following the response header. The META line is a MIME media type which applies to the response body.

#### RESPONSE_STATUS_REDIRECT = "3"
Possible value for `ignition.BaseResponse.status`, and will appear in any response types of `ignition.RedirectResponse`.  As per the Gemini documentation, the server is redirecting the client to a new location for the requested resource.  The URL may be absolute or relative.  The redirect should be considered temporary (unless specied otherwise in the detailed status), i.e. clients should continue to request the resource at the original address and should not performance convenience actions like automatically updating bookmarks.

There is currently no support for automatically following redirects in Ignition.

See `RESPONSE_STATUSDETAIL_REDIRECT*` for additional detailed responses for each potential response type.

#### RESPONSE_STATUS_TEMP_FAILURE = "4"
Possible value for `ignition.BaseResponse.status`, and will appear in any response types of `ignition.TempFailureResponse`.  As per the Gemini documentation, the request has failed. The nature of the failure is temporary, i.e. an identical request MAY succeed in the future.

See `RESPONSE_STATUSDETAIL_TEMP_FAILURE*` for additional detailed responses for each potential response type.

#### RESPONSE_STATUS_PERM_FAILURE = "5"
Possible value for `ignition.BaseResponse.status`, and will appear in any response types of `ignition.PermFailureResponse`.  As per the Gemini documentation, the request has failed.  The nature of the failure is permanent, i.e. identical future requests will reliably fail for the same reason.  Automatic clients such as aggregators or indexing crawlers should not repeat this request.

See `RESPONSE_STATUSDETAIL_PERM_FAILURE*` for additional detailed responses for each potential response type.

#### RESPONSE_STATUS_CLIENTCERT_REQUIRED = "6"
Possible value for `ignition.BaseResponse.status`, and will appear in any response types of `ignition.ClientCertRequiredResponse`.  As per the Gemini documentation, the requested resource requires a client certificate to access. If the request was made without a certificate, it should be repeated with one. If the request was made with a certificate, the server did not accept it and the request should be repeated with a different certificate.

See `RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED*` for additional detailed responses for each potential response type.

#### RESPONSE_STATUS_ERROR = "0"
Possible value for `ignition.BaseResponse.status`, and will appear in any response types of `ignition.ErrorResponse`.  This status indicates that there was an error on transmission with the host and the request could not be completed.  These response types are specific to Ignition because they are beyond the scope of the Gemini protocol and typically indicate an error with networking or communication between the client and the host.

See `RESPONSE_STATUSDETAIL_ERROR*` for additional detailed responses for each potential response type.

---

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

#### RESPONSE_STATUSDETAIL_ERROR_NETWORK = "00"
This is a detailed status message for response type 0x (ERROR).

This is a custom error type outside of the scope of the Gemini protocol.  00 errors represent any errors that occur at the network level, and prevented the client from making any connection with external services.  See the message-level details in the `response.data()` to get additional information.

#### RESPONSE_STATUSDETAIL_ERROR_DNS = "01"
This is a detailed status message for response type 0x (ERROR).

This is a custom error type outside of the scope of the Gemini protocol.  01 errors represent any errors at the DNS level.  See the message-level details in the `response.data()` to get additional information.

#### RESPONSE_STATUSDETAIL_ERROR_HOST = "02"
This is a detailed status message for response type 0x (ERROR).

This is a custom error type outside of the scope of the Gemini protocol.  02 errors represent any errors connecting to the host (timeout, refused, etc.).  See the message-level details in the `response.data()` to get additional information.

#### RESPONSE_STATUSDETAIL_ERROR_TLS = "03"
This is a detailed status message for response type 0x (ERROR).

This is a custom error type outside of the scope of the Gemini protocol.  03 errors represent any errors associated with TLS/SSL, including handshake errors, certificate expired errors, and security errors like certificate rejection errors.  See the message-level details in the `response.data()` to get additional information.

#### RESPONSE_STATUSDETAIL_ERROR_PROTOCOL = "04"
This is a detailed status message for response type 0x (ERROR).

This is a custom error type outside of the scope of the Gemini protocol.  04 errors represent any errors where a secure message is received from the server, but it does not conform to the Gemini protocol requirements and cannot be processed.  See the message-level details in the `response.data()` to get additional information.

---

## ignition.BaseResponse
*Source Code: [src/response.py](../src/response.py)*

This class cannot be instantiated directly.

### Subclasses

[InputResponse](#ignitioninputresponse), [SuccessResponse](#ignitionsuccessresponse), [RedirectResponse](#ignitionredirectresponse), [TempFailureResponse](#ignitiontempfailureresponse), [PermFailureResponse](#ignitionpermfailureresponse), [ClientCertRequiredResponse](#ignitionclientcertrequiredresponse), [ErrorResponse](#ignitionerrorresponse)

### Members

#### basic_status
*type: `string` (length: 1 character)*

`basic_status` returns the raw one-character status response.  It will be one of the following values:

* `ignition.RESPONSE_STATUS_INPUT` = "1"
* `ignition.RESPONSE_STATUS_SUCCESS` = "2"
* `ignition.RESPONSE_STATUS_REDIRECT` = "3"
* `ignition.RESPONSE_STATUS_TEMP_FAILURE` = "4"
* `ignition.RESPONSE_STATUS_PERM_FAILURE` = "5"
* `ignition.RESPONSE_STATUS_CLIENTCERT_REQUIRED` = "6"
* `ignition.RESPONSE_STATUS_ERROR` = "0"

It is not recommended to use this value, and instead leverage the `BaseResponse.is_a()` to check the response type; however, this option has been made available if preferred.

#### status
*type: `string` (length: 2 characters)*

`status` returns the raw detailed two-character status response.  This is useful when providing specific behavior depending on the response.  The response will be one of the following values:

* `ignition.RESPONSE_STATUSDETAIL_ERROR_NETWORK` = "00"
* `ignition.RESPONSE_STATUSDETAIL_ERROR_DNS` = "01"
* `ignition.RESPONSE_STATUSDETAIL_ERROR_HOST` = "02"
* `ignition.RESPONSE_STATUSDETAIL_ERROR_TLS` = "03"
* `ignition.RESPONSE_STATUSDETAIL_ERROR_PROTOCOL` = "04"
* `ignition.RESPONSE_STATUSDETAIL_INPUT` = "10"
* `ignition.RESPONSE_STATUSDETAIL_INPUT_SENSITIVE` = "11"
* `ignition.RESPONSE_STATUSDETAIL_SUCCESS` = "20"
* `ignition.RESPONSE_STATUSDETAIL_REDIRECT_TEMPORARY` = "30"
* `ignition.RESPONSE_STATUSDETAIL_REDIRECT_PERMANENT` = "31"
* `ignition.RESPONSE_STATUSDETAIL_TEMP_FAILURE` = "40"
* `ignition.RESPONSE_STATUSDETAIL_TEMP_FAILURE_UNAVAILABLE` = "41"
* `ignition.RESPONSE_STATUSDETAIL_TEMP_FAILURE_CGI` = "42"
* `ignition.RESPONSE_STATUSDETAIL_TEMP_FAILURE_PROXY` = "43"
* `ignition.RESPONSE_STATUSDETAIL_TEMP_FAILURE_SLOW_DOWN` = "44"
* `ignition.RESPONSE_STATUSDETAIL_PERM_FAILURE` = "50"
* `ignition.RESPONSE_STATUSDETAIL_PERM_FAILURE_NOT_FOUND` = "51"
* `ignition.RESPONSE_STATUSDETAIL_PERM_FAILURE_GONE` = "52"
* `ignition.RESPONSE_STATUSDETAIL_PERM_FAILURE_PROXY_REFUSED` = "53"
* `ignition.RESPONSE_STATUSDETAIL_PERM_FAILURE_BAD_REQUEST` = "59"
* `ignition.RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED` = "60"
* `ignition.RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED_NOT_AUTHORIZED` = "61"
* `ignition.RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED_NOT_VALID` = "62"

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

* [ignition.ErrorResponse](#ignitionerrorresponse)
* [ignition.InputResponse](#ignitioninputresponse)
* [ignition.SuccessResponse](#ignitionsuccessresponse)
* [ignition.RedirectResponse](#ignitionredirectresponse)
* [ignition.TempFailureResponse](#ignitiontempfailureresponse)
* [ignition.PermFailureResponse](#ignitionpermfailureresponse)
* [ignition.ClientCertRequiredResponse](#ignitionclientcertrequiredresponse)

Returns: `string`

#### success() -> boolean
Utility method to check if the response was successful, defined by a status response of `20`.

This is useful if you just need to confirm that the message contains a body or not.

Returns: `boolean`

#### is_a(response_class_type: class) -> bool
Utility method to qualify the response type.  The response type from a request will be one of: ignition.ErrorResponse, ignition.InputResponse, ignition.SuccessResponse, ignition.RedirectResponse, ignition.TempFailureResponse, ignition.TempFailureResponse, ignition.PermFailureResponse, ignition.ClientCertRequiredResponse.  This will return `true` if the response type matches the current object type.

This is recommended for use when routing behavior based on a response.

*Note: This only qualifies the `basic_status` of a response.  For any additional behavior it is required to check the `BaseResponse.status` for detailed status.*

Parameters:
* response_class_type: `ignition.BaseResponse` class

Returns: `boolean`


---


## ignition.InputResponse
**Extends [ignition.BaseResponse](#ignitionbaseresponse)**

*Source Code: [src/response.py](../src/response.py)*

This class cannot be instantiated directly.

### Members

#### basic_status
*type: `string` (length: 1 character)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse)

`basic_status` returns the raw one-character status response.  In the case of the `InputResponse`, this value will always be:

* `ignition.RESPONSE_STATUS_INPUT` = "1"

It is not recommended to use this value, and instead leverage the `InputResponse.is_a()` to check the response type; however, this option has been made available if preferred.

#### status
*type: `string` (length: 2 characters)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse)

`status` returns the raw detailed two-character status response.  This is useful when providing specific behavior depending on the response.  In the case of the `InputResponse`, this value will always be one of:

* `ignition.RESPONSE_STATUSDETAIL_INPUT` = "10"
* `ignition.RESPONSE_STATUSDETAIL_INPUT_SENSITIVE` = "11"

This member SHOULD be used to facilitate status-specific behavior by a client.

#### meta
*type: `string` (length <= 1024 characters)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

#### raw_body
*type: `bytes`*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

#### url
*type: `string`*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

### Methods

#### data() -> string
This returns the prompt to display to the user in order to request the textual user input, which was provided as part of the META response to the user in the header.

Returns: `string`

#### success() -> boolean
Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

Returns: `boolean`

#### is_a(response_class_type: class) -> boolean
Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

Returns: `boolean`


---


## ignition.SuccessResponse
**Extends [ignition.BaseResponse](#ignitionbaseresponse)**

*Source Code: [src/response.py](../src/response.py)*

This class cannot be instantiated directly.

### Members

#### basic_status
*type: `string` (length: 1 character)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse)

`basic_status` returns the raw one-character status response.  In the case of the `SuccessResponse`, this value will always be:

* `ignition.RESPONSE_STATUS_SUCCESS` = "2"

It is not recommended to use this value, and instead leverage the `SuccessResponse.is_a()` to check the response type; however, this option has been made available if preferred.

#### status
*type: `string` (length: 2 characters)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse)

`status` returns the raw detailed two-character status response.  This is useful when providing specific behavior depending on the response.  In the case of the `SuccessResponse`, this value will always be:

* `ignition.RESPONSE_STATUSDETAIL_SUCCESS` = "20"

This member SHOULD be used to facilitate status-specific behavior by a client.

#### meta
*type: `string` (length <= 1024 characters)*

In the context of a success response, this will include additional information including Mime Type and encoding.  This is useful for a SuccessResponse.

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

#### raw_body
*type: `bytes`*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

#### url
*type: `string`*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

### Methods

#### data() -> string
Returns the full request body in the Success response, encoded according to the META mime type.  Note: this function does not do any additional formatting of the response payload beyond mapping the encoding.

Returns: `string`

#### success() -> boolean
Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

Returns: `boolean`

#### is_a(response_class_type: class) -> boolean
Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

Returns: `boolean`


---


## ignition.RedirectResponse
**Extends [ignition.BaseResponse](#ignitionbaseresponse)**

*Source Code: [src/response.py](../src/response.py)*

This class cannot be instantiated directly.

### Members

#### basic_status
*type: `string` (length: 1 character)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse)

`basic_status` returns the raw one-character status response.  In the case of the `RedirectResponse`, this value will always be:

* `ignition.RESPONSE_STATUS_REDIRECT` = "3"

It is not recommended to use this value, and instead leverage the `RedirectResponse.is_a()` to check the response type; however, this option has been made available if preferred.

#### status
*type: `string` (length: 2 characters)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse)

`status` returns the raw detailed two-character status response.  This is useful when providing specific behavior depending on the response.  In the case of the `RedirectResponse`, this value will always be one of:

* `ignition.RESPONSE_STATUSDETAIL_REDIRECT_TEMPORARY` = "30"
* `ignition.RESPONSE_STATUSDETAIL_REDIRECT_PERMANENT` = "31"

This member SHOULD be used to facilitate status-specific behavior by a client.

#### meta
*type: `string` (length <= 1024 characters)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

#### raw_body
*type: `bytes`*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

#### url
*type: `string`*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

### Methods

#### data() -> string
Returns the new url location for the requested response based on the META value for the Redirect response.

Returns: `string`

#### success() -> boolean
Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

Returns: `boolean`

#### is_a(response_class_type: class) -> boolean
Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

Returns: `boolean`


---


## ignition.TempFailureResponse
**Extends [ignition.BaseResponse](#ignitionbaseresponse)**

*Source Code: [src/response.py](../src/response.py)*

This class cannot be instantiated directly.

### Members

#### basic_status
*type: `string` (length: 1 character)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse)

`basic_status` returns the raw one-character status response.  In the case of the `TempFailureResponse`, this value will always be:

* `ignition.RESPONSE_STATUS_TEMP_FAILURE` = "4"

It is not recommended to use this value, and instead leverage the `TempFailureResponse.is_a()` to check the response type; however, this option has been made available if preferred.

#### status
*type: `string` (length: 2 characters)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse)

`status` returns the raw detailed two-character status response.  This is useful when providing specific behavior depending on the response.  In the case of the `TempFailureResponse`, this value will always be one of:

* `ignition.RESPONSE_STATUSDETAIL_TEMP_FAILURE` = "40"
* `ignition.RESPONSE_STATUSDETAIL_TEMP_FAILURE_UNAVAILABLE` = "41"
* `ignition.RESPONSE_STATUSDETAIL_TEMP_FAILURE_CGI` = "42"
* `ignition.RESPONSE_STATUSDETAIL_TEMP_FAILURE_PROXY` = "43"
* `ignition.RESPONSE_STATUSDETAIL_TEMP_FAILURE_SLOW_DOWN` = "44"

This member SHOULD be used to facilitate status-specific behavior by a client.

#### meta
*type: `string` (length <= 1024 characters)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

#### raw_body
*type: `bytes`*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

#### url
*type: `string`*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

### Methods

#### data() -> string
Returns the contents of the META field to provide additional information regarding the failure to the user.

Returns: `string`

#### success() -> boolean
Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

Returns: `boolean`

#### is_a(response_class_type: class) -> boolean
Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

Returns: `boolean`


---


## ignition.PermFailureResponse
**Extends [ignition.BaseResponse](#ignitionbaseresponse)**

*Source Code: [src/response.py](../src/response.py)*

This class cannot be instantiated directly.

### Members

#### basic_status
*type: `string` (length: 1 character)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse)

`basic_status` returns the raw one-character status response.  In the case of the `PermFailureResponse`, this value will always be:

* `ignition.RESPONSE_STATUS_PERM_FAILURE` = "5"

It is not recommended to use this value, and instead leverage the `PermFailureResponse.is_a()` to check the response type; however, this option has been made available if preferred.

#### status
*type: `string` (length: 2 characters)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse)

`status` returns the raw detailed two-character status response.  This is useful when providing specific behavior depending on the response.  In the case of the `PermFailureResponse`, this value will always be one of:

* `ignition.RESPONSE_STATUSDETAIL_PERM_FAILURE` = "50"
* `ignition.RESPONSE_STATUSDETAIL_PERM_FAILURE_NOT_FOUND` = "51"
* `ignition.RESPONSE_STATUSDETAIL_PERM_FAILURE_GONE` = "52"
* `ignition.RESPONSE_STATUSDETAIL_PERM_FAILURE_PROXY_REFUSED` = "53"
* `ignition.RESPONSE_STATUSDETAIL_PERM_FAILURE_BAD_REQUEST` = "59"

This member SHOULD be used to facilitate status-specific behavior by a client.

#### meta
*type: `string` (length <= 1024 characters)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

#### raw_body
*type: `bytes`*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

#### url
*type: `string`*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

### Methods

#### data() -> string
Returns the contents of the META field to provide additional information regarding the failure to the user.

Returns: `string`

#### success() -> boolean
Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

Returns: `boolean`

#### is_a(response_class_type: class) -> boolean
Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

Returns: `boolean`


---


## ignition.ClientCertRequiredResponse
**Extends [ignition.BaseResponse](#ignitionbaseresponse)**

*Source Code: [src/response.py](../src/response.py)*

This class cannot be instantiated directly.

### Members

#### basic_status
*type: `string` (length: 1 character)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse)

`basic_status` returns the raw one-character status response.  In the case of the `ClientCertRequiredResponse`, this value will always be:

* `ignition.RESPONSE_STATUS_CLIENTCERT_REQUIRED` = "6"

It is not recommended to use this value, and instead leverage the `ClientCertRequiredResponse.is_a()` to check the response type; however, this option has been made available if preferred.

#### status
*type: `string` (length: 2 characters)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse)

`status` returns the raw detailed two-character status response.  This is useful when providing specific behavior depending on the response.  In the case of the `ClientCertRequiredResponse`, this value will always be one of:

* `ignition.RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED` = "60"
* `ignition.RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED_NOT_AUTHORIZED` = "61"
* `ignition.RESPONSE_STATUSDETAIL_CLIENTCERT_REQUIRED_NOT_VALID` = "62"

This member SHOULD be used to facilitate status-specific behavior by a client.

#### meta
*type: `string` (length <= 1024 characters)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

#### raw_body
*type: `bytes`*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

#### url
*type: `string`*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

### Methods

#### data() -> string
Returns the additional information on certificate requirements, or the reason that the certificate was rejected.  These are the contents of the META field for a Client Certificate Required response.

Returns: `string`

#### success() -> boolean
Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

Returns: `boolean`

#### is_a(response_class_type: class) -> boolean
Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

Returns: `boolean`


---


## ignition.ErrorResponse
**Extends [ignition.BaseResponse](#ignitionbaseresponse)**

*Source Code: [src/response.py](../src/response.py)*

This class cannot be instantiated directly.

### Members

#### basic_status
*type: `string` (length: 1 character)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse)

`basic_status` returns the raw one-character status response.  In the case of the `ErrorResponse`, this value will always be:

* `ignition.RESPONSE_STATUS_ERROR` = "0"

It is not recommended to use this value, and instead leverage the `ErrorResponse.is_a()` to check the response type; however, this option has been made available if preferred.

#### status
*type: `string` (length: 2 characters)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse)

`status` returns the raw detailed two-character status response.  This is useful when providing specific behavior depending on the response.  In the case of the `ErrorResponse`, this value will always be one of:

* `ignition.RESPONSE_STATUSDETAIL_ERROR_NETWORK` = "00"
* `ignition.RESPONSE_STATUSDETAIL_ERROR_DNS` = "01"
* `ignition.RESPONSE_STATUSDETAIL_ERROR_HOST` = "02"
* `ignition.RESPONSE_STATUSDETAIL_ERROR_TLS` = "03"
* `ignition.RESPONSE_STATUSDETAIL_ERROR_PROTOCOL` = "04"

This member SHOULD be used to facilitate status-specific behavior by a client.

#### meta
*type: `string` (length <= 1024 characters)*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

#### raw_body
*type: `bytes`*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

#### url
*type: `string`*

Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

### Methods

#### data() -> string
Provides an error message related to the Error failure type as defined by ignition.  See failure constants as defined in the `status` field for full details on each error type.

Returns: `string`

#### success() -> boolean
Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

Returns: `boolean`

#### is_a(response_class_type: class) -> boolean
Extended from [ignition.BaseResponse](#ignitionbaseresponse). See parent class for full details.

Returns: `boolean`
