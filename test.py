import requests

response = requests.get('https://dog.ceo/api/breeds/image/random')

if response:

    json_data = response.json()

    img_response = requests.get(json_data['message'])

with open('husky.jpg', 'wb') as f:

    f.write(img_response.content)



