import requests

url = "https://www.sample.com/"  # Replace with the desired URL

# Send an HTTP GET request to the specified URL
response = requests.get(url)

# Print request headers
print("Request Headers:")
print("User-Agent:", response.request.headers.get('User-Agent'))
print("Host:", response.request.headers.get('Host'))
print("Accept:", response.request.headers.get('Accept'))
print("Authorization:", response.request.headers.get('Authorization'))
print("Cookie:", response.request.headers.get('Cookie'))
print("Referer:", response.request.headers.get('Referer'))
print("Cache-Control:", response.request.headers.get('Cache-Control'))

# Print response headers
print("\nResponse Headers:")
print("Server:", response.headers.get('Server'))
print("Content-Type:", response.headers.get('Content-Type'))
print("Content-Length:", response.headers.get('Content-Length'))
print("Location:", response.headers.get('Location'))
print("Set-Cookie:", response.headers.get('Set-Cookie'))
print("ETag:", response.headers.get('ETag'))
print("Cache-Control:", response.headers.get('Cache-Control'))
