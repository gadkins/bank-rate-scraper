from collections import defaultdict
from typing import List, Dict, Union
from urllib.parse import urlparse

def merge_bank_responses(responses: List[BankResponse]) -> BankResponse:
    """
    Merges a list of BankResponse objects into a single BankResponse object.

    Args:
        responses (List[BankResponse]): A list of BankResponse objects to merge.

    Returns:
        BankResponse: A merged BankResponse object.
    """
    if not responses:
        return None

    merged_response = BankResponse(
        bankRootDomain=responses[0].bankRootDomain,
        checkingAccounts=[],
        savingsAccounts=[],
        moneyMarketAccounts=[],
        certificatesOfDeposit=[],
        individualRetirementAccounts=[],
        loans=[],
        creditCards=[],
        fees=[]
    )

    for response in responses:
        if response.checkingAccounts:
            merged_response.checkingAccounts.extend(response.checkingAccounts)
        if response.savingsAccounts:
            merged_response.savingsAccounts.extend(response.savingsAccounts)
        if response.moneyMarketAccounts:
            merged_response.moneyMarketAccounts.extend(response.moneyMarketAccounts)
        if response.certificatesOfDeposit:
            merged_response.certificatesOfDeposit.extend(response.certificatesOfDeposit)
        if response.individualRetirementAccounts:
            merged_response.individualRetirementAccounts.extend(response.individualRetirementAccounts)
        if response.loans:
            merged_response.loans.extend(response.loans)
        if response.creditCards:
            merged_response.creditCards.extend(response.creditCards)
        if response.fees:
            merged_response.fees.extend(response.fees)

    return merged_response

def merge_responses_by_domain(responses: List[BankResponse]) -> Dict[str, BankResponse]:
    """
    Merges BankResponse objects that share the same root domain.

    Args:
        responses (List[BankResponse]): A list of BankResponse objects.

    Returns:
        Dict[str, BankResponse]: A dictionary where the keys are root domains and the values are merged BankResponse objects.
    """
    domain_responses = defaultdict(list)

    for response in responses:
        domain_responses[response.bankRootDomain].append(response)

    merged_responses = {
        domain: merge_bank_responses(responses)
        for domain, responses in domain_responses.items()
    }

    return merged_responses