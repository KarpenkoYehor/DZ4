import requests

url = 'https://booking-ntoj.onrender.com/api/v1/productentitiestool-ui-admin/partner/getAll?authuser=0'
headers = {
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'pragma': 'no-cache',
    'z-currency': 'USD',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'content-type': 'application/json',
    'cache-control': 'no-cache',
    'Referer': 'https://admin.spaceship.net/',
    'z-lang': 'en-US',
    'sec-ch-ua-platform': '"macOS"'
}

response = requests.post(url, headers=headers)
print(response.json())  # Виведе відповідь сервера

