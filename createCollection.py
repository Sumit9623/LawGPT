
import qdrant_client
import os
client = qdrant_client.QdrantClient(os.getenv("QDRANT_HOST"),api_key=os.getenv("QDRANT_API_KEY"))
collection_config = qdrant_client.http.models.VectorParams(
        size=1536, # 768 for instructor-xl, 1536 for OpenAI
        distance=qdrant_client.http.models.Distance.COSINE
    )

client.recreate_collection(
    collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
    vectors_config=collection_config
)
