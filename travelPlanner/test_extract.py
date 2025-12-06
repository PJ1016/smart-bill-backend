import os
import json
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# ---------------------------
# Environment configuration
# ---------------------------
AZURE_AI_PROJECT_ENDPOINT = "https://travel-memory-hub-ai1.services.ai.azure.com/api/projects/travel-memory-hub-ai"
AGENT_NAME = "travel-extract-agent"

# Init Azure project client
project_client = AIProjectClient(
    endpoint=AZURE_AI_PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

openai_client = project_client.get_openai_client()


def test_extract(image_url: str):
    agent = project_client.agents.get(agent_name=AGENT_NAME)

    payload = {
        "imageUrl": image_url
    }

    response = openai_client.responses.create(
        input=[
            {
                "role": "user",
                "content": json.dumps(payload)
            }
        ],
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}}
    )

    text = response.output_text
    print("RAW OUTPUT:", text)
    parsed = json.loads(text)
    print("PARSED JSON:", json.dumps(parsed, indent=2))


if __name__ == "__main__":
    TEST_IMAGE_URL = "https://cdn.pixabay.com/photo/2018/08/15/06/58/hawa-mahal-3601901_960_720.jpg"
    test_extract(TEST_IMAGE_URL)
