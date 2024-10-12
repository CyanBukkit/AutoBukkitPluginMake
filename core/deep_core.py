import requests

headers = {
    "Authorization": "Bearer <KEY> ",
    "Content-Type": "application/json"
}

url = "http://deep.cyanbukkit.cn/v1/chat/completions"

def deep_seek_code(content) -> str:
    data = {
        "model": "deepseek_code",
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    print(f"得到请求体 {response.json()}")
    response_json = response.json()
    first_choice = response_json["choices"]
    last_choice = first_choice[-1]  # 使用负索引获取最后一个元素
    message_content = last_choice["message"]["content"]
    return message_content

def deep_seek_chat(content) -> str:
    data = {
        "model": "deepseek_chat",
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    print(f"得到请求体 {response.json()}")
    response_json = response.json()
    first_choice = response_json["choices"]
    last_choice = first_choice[-1]  # 使用负索引获取最后一个元素
    message_content = last_choice["message"]["content"]
    return message_content