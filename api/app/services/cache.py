import hashlib, json
from redis import Redis
from ..core.config import settings

r = Redis.from_url(settings.REDIS_URL)

def key_for(question: str, contexts: list) -> str:
    blob = json.dumps({"q": question, "ctx": [c.get("id") for c in contexts]}, sort_keys=True)
    return "tutor:" + hashlib.sha1(blob.encode()).hexdigest()
