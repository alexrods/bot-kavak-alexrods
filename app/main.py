from fastapi import FastAPI
from .api.models import MessageResponse, MessageRequest
from .llm.get_responses import bot_response

app = FastAPI(docs_url="/docs")

@app.post("/api/v1/bot")
def kavak_bot(request: MessageRequest) -> MessageResponse:
    """
    Endpoint that processes a message request and returns a bot response.

    Args:
        request (MessageRequest): The incoming request containing the user's message.

    Returns:
        MessageResponse: The response from the bot based on the user's message.
    """
    response_text = bot_response(request.message)
    return MessageResponse(response=response_text)
