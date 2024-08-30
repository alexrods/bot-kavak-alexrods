import os
import time
import logging
from pinecone import Pinecone
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

PINECONE_APIKEY = os.environ['PINECONE_APIKEY']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

embeddings_client = OpenAI(api_key=OPENAI_API_KEY)

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pc = Pinecone(api_key=PINECONE_APIKEY)
index = pc.Index("kavak-test")

def get_embedding(text: str, model: str = "text-embedding-3-small"):
    """
    Generate an embedding for a given text using the specified model.

    Args:
        text (str): The text to be converted into an embedding.
        model (str): The model to use for generating the embedding. Defaults to "text-embedding-3-small".

    Returns:
        list: The embedding vector generated for the input text.

    Raises:
        Exception: Propagates any unexpected exceptions that occur during the API call.
    """
    text = text.replace("\n", " ")
    while True:
        try:
            embedding = embeddings_client.embeddings.create(input=[text], model=model).data[0].embedding
            return embedding
        except Exception as e: 
            if "Rate limit reached" in str(e):
                logger.warning("Rate limit reached. Waiting 5 seconds before retrying...")
                time.sleep(5) 
            else:
                logger.error(f"Unexpected error: {e}")
                raise e


def inventory_search(query: str) -> str:
    """
    Perform an inventory search based on a query by generating an embedding and querying the index.

    Args:
        query (str): The search query input by the user.

    Returns:
        str: A string summarizing the matching cars in the inventory.

    Raises:
        Exception: Propagates any unexpected exceptions that occur during the search.

    # TO DO: Numeric filter, by price, year, km, etc ...
    """
    query_embedding = get_embedding(query)
    results = index.query(
        vector=query_embedding,
        top_k=10,  
        include_metadata=True
    )

    search_result = "Autos en inventario: "
    for match in results['matches']:
        search_result += f"{match['metadata']}, "

    return search_result

