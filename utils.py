import json
from typing import List

# Print the CSV content for each URL
def print_csv_tables(csv_tables_dict):
    for url, csv_tables in csv_tables_dict.items():
        print(f"CSV Tables from {url}:")
        for i, csv_table in enumerate(csv_tables):
            print(f"Table {i+1}:")
            print(csv_table)
            print()  # Print a newline for better readability

def print_bank_responses_json(bank_responses: List[BankResponse], num_to_print: int) -> None:
    """
    Prints the specified number of BankResponse objects in JSON format.

    Args:
        bank_responses (List[BankResponse]): A list of BankResponse objects to print.
        num_to_print (int): The number of BankResponse objects to print.
    """
    for i, bank_response in enumerate(bank_responses[:num_to_print]):
        print(json.dumps(bank_response.dict(), indent=4))
        print("\n" + "-" * 40 + "\n")

def normalize_domain(domain: str) -> str:
    """
    Normalizes the domain by removing the 'www.' prefix if it exists.

    Args:
        domain (str): The domain to normalize.

    Returns:
        str: The normalized domain.
    """
    if domain.startswith("www."):
        return domain[4:]
    return domain

def print_bank_response_as_json_by_domain(bank_responses: List[BankResponse], domain: str) -> None:
    """
    Prints the BankResponse object in JSON format for the specified bankRootDomain.

    Args:
        bank_responses (List[BankResponse]): A list of BankResponse objects to search through.
        domain (str): The bankRootDomain or www subdomain of the BankResponse object to print.
    """
    normalized_domain = normalize_domain(domain)

    for bank_response in bank_responses:
        normalized_response_domain = normalize_domain(bank_response.bankRootDomain)

        if normalized_response_domain == normalized_domain:
            print(json.dumps(bank_response.dict(), indent=4))
            print("\n" + "-" * 40 + "\n")
            return

    print(f"No BankResponse found for domain: {domain}")