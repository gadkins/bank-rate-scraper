from scraper import extract_all_tables_from_html, convert_tables_to_csv
from llm_extraction import chunk_data, extract_with_llm
from merger import merge_bank_responses, merge_responses_by_domain
from typing import List, Dict, Tuple
from collections import defaultdict

def process_and_extract_tables(
    csv_tables_dict: Dict[str, List[str]],
    chunk_size: int
) -> Tuple[List[BankResponse], List[str]]:
    """
    Processes the CSV tables and extracts structured data using OpenAI's API,
    returning a list of merged BankResponse objects and a list of unsuccessful URLs.

    Args:
        csv_tables_dict (Dict[str, List[str]]): Dictionary where keys are URLs and values are lists of CSV tables.
        chunk_size (int): The size of the data chunks to be processed.

    Returns:
        Tuple[List[BankResponse], List[str]]: A tuple containing a list of merged BankResponse objects and a list of unsuccessful URLs.
    """
    url_responses: Dict[str, List[BankResponse]] = defaultdict(list)
    unsuccessful_urls: List[str] = []

    for url, csv_tables in csv_tables_dict.items():
        if not csv_tables:
            unsuccessful_urls.append(url)
            continue

        start_time = time.time()
        combined_csv = ''.join(csv_tables)
        chunks = chunk_data(combined_csv, chunk_size)

        for chunk in chunks:
            extracted_data_chunk = extract_with_llm(chunk)
            url_responses[url].append(extracted_data_chunk)

        end_time = time.time()
        processing_time = end_time - start_time

        print(f"Processing time for {url}: {processing_time:.2f} seconds")

    # Merge responses by URL
    merged_url_responses = [
        merge_bank_responses(responses) for responses in url_responses.values()
    ]

    # Merge responses by root domain
    final_merged_responses = list(merge_responses_by_domain(merged_url_responses).values())

    return final_merged_responses, unsuccessful_urls
