# swagger_client.DefaultApi

All URIs are relative to *https://virtserver.swaggerhub.com/DellVMProjec/VMDBUser/1.0.0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**example_get**](DefaultApi.md#example_get) | **GET** /example | Server example operation
[**ping_get**](DefaultApi.md#ping_get) | **GET** /ping | Server heartbeat operation

# **example_get**
> example_get()

Server example operation

This is an example operation to show how security is applied to the call.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: password
configuration = swagger_client.Configuration()
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.DefaultApi(swagger_client.ApiClient(configuration))

try:
    # Server example operation
    api_instance.example_get()
except ApiException as e:
    print("Exception when calling DefaultApi->example_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[password](../README.md#password)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ping_get**
> ping_get()

Server heartbeat operation

This operation shows how to override the global security defined above, as we want to open it up for all users.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()

try:
    # Server heartbeat operation
    api_instance.ping_get()
except ApiException as e:
    print("Exception when calling DefaultApi->ping_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

