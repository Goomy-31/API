import requests
url = "https://kknma-34-23-221-145.run.pinggy-free.link/"


response_get = requests.get(url + "/")
print("Thông tin của API: ", response_get.json())

response_get = requests.get(url + "/health")
print("Trạng thái hoạt động của hệ thống: ", response_get.json())

payload = {"text": "once upon a time"}
response_post = requests.post(url + "/predict", json=payload)
print("Kết quả GPT-2: ", response_post.json())