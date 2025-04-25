import requests, json

"""
def notify_bot(task):
    url = "http://localhost:8080/notify/"
    data = {
        "title": task.title,
        "deadline": task.deadline.isoformat()
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Bearer secret"
    }
    try:
        response = requests.post(
            "http://localhost:8080/notify/",
            data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
            headers=headers
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Ошибка при отправке уведомления боту:", e)
"""