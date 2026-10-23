# Elasticsearch mapping notes

The assessment requires three indices: `East India_chunks`, `East India_entities`, and `East India_relations`. Use index names consistently and quote them in shell commands if needed. Final vector dimensions and quantisation settings must be selected only after inspecting the supplied embedding model and Elasticsearch version.

## Chunk index starter mapping

Do not apply until you have chosen the actual embedding model and replaced `EMBEDDING_DIMENSION` with its real output dimension.

```json
{
  "mappings": {
    "properties": {
      "chunk_id": {"type": "keyword"},
      "doc_id": {"type": "keyword"},
      "text": {"type": "text", "analyzer": "english"},
      "source": {"type": "keyword"},
      "page": {"type": "integer"},
      "char_start": {"type": "integer"},
      "char_end": {"type": "integer"},
      "entity_ids": {"type": "keyword"},
      "embedding": {"type": "dense_vector", "dims": EMBEDDING_DIMENSION, "index": true, "similarity": "cosine", "index_options": {"type": "hnsw", "m": 16, "ef_construction": 100}}
    }
  }
}
```

Replace the placeholder with an integer before using JSON. Check compatibility with the assessor's exact Elasticsearch version.
