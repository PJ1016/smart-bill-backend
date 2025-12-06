# embedding_utils.py

import os
from typing import List

from dotenv import load_dotenv

# IMPORTANT: you'll need semantic-kernel installed:
# pip install "semantic-kernel[azure]"

from semantic_kernel.connectors.ai.azure_ai_inference import AzureAIInferenceTextEmbedding

load_dotenv()


def get_embedding_model() -> AzureAIInferenceTextEmbedding:
    """
    Create and return an AzureAIInferenceTextEmbedding client
    using environment variables:
    - AZURE_AI_INFERENCE_ENDPOINT
    - AZURE_AI_INFERENCE_KEY
    - AZURE_AI_EMBEDDING_MODEL
    """
    endpoint = os.getenv("AZURE_AI_INFERENCE_ENDPOINT")
    key = os.getenv("AZURE_AI_INFERENCE_KEY")
    model_id = os.getenv("AZURE_AI_EMBEDDING_MODEL")

    if not endpoint or not key or not model_id:
        raise ValueError(
            "Missing one of AZURE_AI_INFERENCE_ENDPOINT / "
            "AZURE_AI_INFERENCE_KEY / AZURE_AI_EMBEDDING_MODEL in .env"
        )

    embedding_model = AzureAIInferenceTextEmbedding(
        endpoint=endpoint,
        api_key=key,
        ai_model_id=model_id,
    )
    return embedding_model


async def generate_embeddings(chunks: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of text chunks.
    Returns a list of embedding vectors, one per chunk.
    """
    if not chunks:
        return []

    model = get_embedding_model()
    embeddings: List[List[float]] = await model.generate_embeddings(chunks)
    return embeddings
