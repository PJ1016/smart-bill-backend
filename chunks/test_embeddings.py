# test_embeddings.py

import asyncio
from embedding_utils import generate_embeddings

async def main():
    texts = [
        "Salary credited 65,000 rupees on June 1",
        "ATM withdrawal of 5,000 rupees on June 10",
        "Random unrelated sentence about weather"
    ]

    embeddings = await generate_embeddings(texts)

    print(f"Got {len(embeddings)} embeddings.")
    if embeddings:
        print(f"Each embedding length: {len(embeddings[0])}")
        print("First 5 numbers of first embedding:", embeddings[0][:5])

if __name__ == "__main__":
    asyncio.run(main())
