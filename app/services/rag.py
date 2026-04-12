from app.db.loader import search


def get_context(query: str) -> str:
    docs = search(query)

    if not docs:
        return ""

    return "\n\n".join(docs)