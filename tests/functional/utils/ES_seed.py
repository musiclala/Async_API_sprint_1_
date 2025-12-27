import json
from pathlib import Path

from elasticsearch import AsyncElasticsearch


def _load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


async def recreate_index(es: AsyncElasticsearch, index: str, mapping_path: str) -> None:
    body = _load_json(mapping_path)
    if await es.indices.exists(index=index):
        await es.indices.delete(index=index)
    await es.indices.create(index=index, body=body)


async def seed_docs(es: AsyncElasticsearch, index: str, docs_path: str) -> None:
    docs = _load_json(docs_path)
    for d in docs:
        await es.index(index=index, id=d["id"], document=d)
    await es.indices.refresh(index=index)