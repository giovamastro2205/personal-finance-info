
import os
import time
import jwt
import requests

app_id = os.environ["ENABLE_BANKING_APP_ID"].strip()
private_key = os.environ["ENABLE_BANKING_PRIVATE_KEY"].replace("\\n", "\n").strip()

now = int(time.time())
token = jwt.encode(
    {
        "iss": "enablebanking.com",
        "aud": "api.enablebanking.com",
        "iat": now,
        "exp": now + 600
    },
    private_key,
    algorithm="RS256",
    headers={"typ": "JWT", "kid": app_id}
)

response = requests.get(
    "https://api.enablebanking.com/application",
    headers={"Authorization": f"Bearer {token}"},
    timeout=25
)
response.raise_for_status()

data = response.json()

print("Connessione API: OK")
print("Campi disponibili:", sorted(data.keys()))

sessions = data.get("sessions")
if isinstance(sessions, list):
    print("Sessioni disponibili:", len(sessions))
else:
    print("Elenco sessioni non presente nella risposta.")
