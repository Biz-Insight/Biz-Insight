import requests

API_KEY = "****"
ENDPOINT = "https://api.openai.com/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def get_corp_summary(corp_name, approx_words=50, model="gpt-3.5-turbo-16k"):
    message_content = (
        f"Provide a concise and informative summary about {corp_name} "
        f"corporation in approximately {approx_words} words in Korean translation."
    )

    data = {
        "model": model,
        "messages": [{"role": "user", "content": message_content}],
    }

    response = requests.post(ENDPOINT, headers=HEADERS, json=data)
    response.raise_for_status()

    corp_summary = response.json()["choices"][0]["message"]["content"].strip()

    return corp_summary
