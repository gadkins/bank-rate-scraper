from pydantic import BaseModel
from typing import List, Tuple

def chunk_data(data: str, chunk_size: int) -> List[str]:
    """
    Splits a large string into smaller chunks of a specified maximum size.

    Args:
        data (str): The data to be chunked.
        chunk_size (int): The maximum size of each chunk.

    Returns:
        List[str]: A list of data chunks.
    """
    chunks = []
    for i in range(0, len(data), chunk_size):
        chunks.append(data[i:i + chunk_size])
    return chunks

def extract_with_llm(chunk: str) -> BankResponse:
    prompt = f"""
Extract the banking rate data from the following text and structure it according to the provided model.

Special instructions:
- If a property or object does not exist, do not include it in the output.
- Do not include 'www' or other subdomains in the bankRootDomain.
- If dividend rate is given, do not include interest rate.
- Do not convert percentage to decimal. I.e. if the rate is 0.55%, return 0.55 not 0.0055

Text:
{chunk}
"""
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output structured data."},
            {"role": "user", "content": prompt}
        ],
        response_format=BankResponse,  # Directly use the Pydantic model here
    )

    return response.choices[0].message.parsed  # This will be a Pydantic model instance