import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")

def analyze_logs(logs):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": [
                {"role": "system", "content": "You are a DevOps expert."},
                {"role": "user", "content": f"Analyze this CI/CD error log and give root cause + fix:\n{logs}"}
            ]
        }
    )

    data = response.json()

    print("🔍 Full API Response:\n", data)   # DEBUG

    if "choices" not in data:
        return "❌ AI failed: " + str(data)

    return data["choices"][0]["message"]["content"]


if __name__ == "__main__":
    if not os.path.exists("error.log"):
        print("❌ error.log not found")
        exit()

    with open("error.log", "r") as f:
        logs = f.read()

    print("📄 Logs:\n", logs)   # DEBUG

    result = analyze_logs(logs)

    print("\n✅ AI Analysis:\n")
    print(result)