import requests as reqs


# Send an HTTP GET request to the specified URL

def req(response):
    # response = requests.get(url)
    # Print request headers
    print("\n\nRequest Headers:")
    print("\n\nUser-Agent:", response.request.headers.get('User-Agent'))
    print("\n\nHost:", response.request.headers.get('Host'))
    print("\n\nAccept:", response.request.headers.get('Accept'))
    print("\n\nAuthorization:", response.request.headers.get('Authorization'))
    print("\n\nCookie:", response.request.headers.get('Cookie'))
    print("\n\nReferer:", response.request.headers.get('Referer'))
    print("\n\nCache-Control:", response.request.headers.get('Cache-Control'))

def res(response):
    # Print response headers
    print("\n\nResponse Headers:")
    print("\n\nServer:", response.headers.get('Server'))
    print("\n\nContent-Type:", response.headers.get('Content-Type'))
    print("\n\nContent-Length:", response.headers.get('Content-Length'))
    print("\n\nLocation:", response.headers.get('Location'))
    print("\n\nSet-Cookie:", response.headers.get('Set-Cookie'))
    print("\n\nETag:", response.headers.get('ETag'))
    print("\n\nCache-Control:", response.headers.get('Cache-Control'))

if __name__ == "__main__":
    url = input("\n\tPlease Enter the url:- ")  # Replace with the desired URL
    response = reqs.get(url)
    req(response)
    res(response)
