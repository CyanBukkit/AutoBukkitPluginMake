import requests

chat_id = ""
headers = {
    "Authorization": "Bearer 密钥",
    "Content-Type": "application/json"
}
url = "http://kimi.cyanbukkit.cn/v1/chat/completions"

def kimi_(content) -> str:
    data = {
        "model": "kimi",
        "conversation_id": "none",
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "use_search": True,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    print(f"得到请求体 {response.json()}")
    response_json = response.json()
    first_choice = response_json["choices"]
    last_choice = first_choice[-1]  # 使用负索引获取最后一个元素
    global chat_id
    chat_id = response_json["id"]
    message_content = last_choice["message"]["content"]
    return message_content

#
def kimi_continue(content) -> str:
    data = {
        "model": "kimi",
        "conversation_id": chat_id,
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "use_search": True,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    print(f"得到请求体 {response.json()}")
    response_json = response.json()
    first_choice = response_json["choices"]
    last_choice = first_choice[-1]  # 使用负索引获取最后一个元素
    message_content = last_choice["message"]["content"]
    return message_content
