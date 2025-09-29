from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import Resource
from .services.embeddings import embed_texts
from sqlalchemy import text

def run():
    db: Session = SessionLocal()
    samples = [
        ("https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Introduction", "MDN JS Intro", "JavaScript is a cross-platform..."),
        ("https://react.dev/learn", "React Docs — Learn", "Welcome to the React documentation..."),
    ]
    for url, title, content in samples:
        r = Resource(url=url, title=title, source="seed", content_text=content)
        db.add(r); db.commit(); db.refresh(r)
        vec = embed_texts([content])[0]
        db.execute(text("INSERT INTO embeddings(resource_id, embedding) VALUES (:rid, :vec)"), {"rid": r.id, "vec": vec})
        db.commit()
    db.close()

if __name__ == "__main__":
    run()
