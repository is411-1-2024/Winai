import requests

url = 'https://mentor2code.com/'
conn = requests.get(url)

print(conn.status_code)

data = conn.content
print(data[:50])

for key in conn.headers:
    print("{} : {}".format(key, conn.headers[key]))