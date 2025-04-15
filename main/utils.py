import requests

def notify_bot(task):
    url = "http://localhost:8080/notify/"
    data = {
        "title": task.title,
        "deadline": task.deadline.isoformat()
    }
    headers = {"Authorization": "Bearer секрет"}
    requests.post(url, json=data, headers=headers, timeout=3)
    try:
        response = requests.post(url, json=data, timeout=3)
        if response.status_code != 200:
            print(f"Ошибка при отправке: {response.status_code} — {response.text}")
    except requests.RequestException as e:
        print(f"Ошибка соединения с ботом: {e}")