import os
import json
from typing import Any, Dict, List
from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

# ENV VARS (set these in .env or your environment)
AZURE_AI_PROJECT_ENDPOINT = os.getenv("AZURE_EXISTING_AIPROJECT_ENDPOINT")
AZURE_AI_EXTRACT_AGENT_NAME = "travel-extract-agent"
AZURE_AI_CHAT_AGENT_NAME = "travel-chat-agent"

if not AZURE_AI_PROJECT_ENDPOINT:
    raise RuntimeError("AZURE_EXISTING_AIPROJECT_ENDPOINT is not set")

# Single project client (reused)
_project_client = AIProjectClient(
    endpoint=AZURE_AI_PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

_openai_client = _project_client.get_openai_client()


def _get_agent(agent_name: str):
    return _project_client.agents.get(agent_name=agent_name)


def call_extract_agent(image_url: str) -> Dict[str, Any]:
    """
    Calls the travel-extract-agent with an image URL.
    The agent returns JSON string with:
    { placeName, city, category, notes, aiDescription }
    """
    agent = _get_agent(AZURE_AI_EXTRACT_AGENT_NAME)

    # We send a single user message where content is JSON including the imageUrl.
    # Your agent instructions know how to interpret this.
    payload = {
        "imageUrl": image_url
    }

    response = _openai_client.responses.create(
        input=[
            {
                "role": "user",
                "content": json.dumps(payload),
            }
        ],
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )

    # In the code sample they used response.output_text (string).
    # That should be the JSON string we want to parse.
    text = response.output_text
    return json.loads(text)


def call_chat_agent(memories: List[Dict[str, Any]], question: str) -> Dict[str, Any]:
    """
    Calls the travel-chat-agent with a list of memories and a question.
    Agent returns:
    {
      "responseText": "...",
      "matches": [ ...subset of memories... ]
    }
    """
    agent = _get_agent(AZURE_AI_CHAT_AGENT_NAME)

    payload = {
        "memories": memories,
        "question": question,
    }

    response = _openai_client.responses.create(
        input=[
            {
                "role": "user",
                "content": json.dumps(payload),
            }
        ],
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )

    text = response.output_text
    return json.loads(text)
