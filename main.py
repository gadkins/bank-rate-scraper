from scraper import extract_all_tables_from_html, convert_tables_to_csv
from llm_extraction import chunk_data, extract_with_llm
from pipeline import process_and_extract_tables
from utils import print_csv_tables, print_bank_responses_json, print_bank_response_as_json_by_domain

urls = [
    # List of URLs
    'https://www.simplicity.coop/rates',
    'https://www.bankofdeerfield.bank/resources/deposit-rates',
    'https://www.salemcoop.com/rates-fees/deposit-interest-rates/',
    'https://www.bankwithpremier.com/Current%20Deposit%20Interest%20Rates',
    'https://www.shrewsburycu.com/home/member-services/rates',
    'https://www.parkbank.bank/Pages/savings-cd.html',
    'https://www.parkbank.bank/Pages/p-checking.html',
    'https://www.parkbank.bank/Pages/rewards-checking.html',
    'https://www.bluffviewbank.com/personal/savings/cd-rates/',
    'https://www.bluffviewbank.com/personal/checking/checking-and-savings-rates/',
    'https://www.dcu.org/bank/certificates/regular-certificates.html',
    'https://www.dcu.org/bank/savings.html',
    'https://www.dcu.org/bank/checking.html',
    'https://www.dcu.org/bank/retirement/ira-savings.html',
    'https://www.firstiowa.bank/personal/cd-and-ira-rates',
    'https://www.firstiowa.bank/connect/rates',
    'https://www.firstiowa.bank/personal/checking',
    'https://www.huntington.com/Personal/savings-cds-overview/certificates-of-deposit',
    'https://www.huntington.com/Personal/savings-cds-overview/relationship-money-market-account',
    'https://www.huntington.com/Personal/checking/perks',
    'https://www.huntington.com/Personal/savings-cds-overview/money-market-ira',
    'https://www.huntington.com/Personal/savings-cds-overview/premier-savings-account',
    'https://verveacu.com/personal/product/savings/certificates/share-certificates/',
    'https://verveacu.com/personal/product/savings/money-market/',
    'https://verveacu.com/personal/product/checking/kickback-checking/',
    'https://verveacu.com/personal/product/savings/kickback-savings/',
    'https://verveacu.com/personal/product/savings/money-market/',
]

results, unsuccessful_urls = extract_all_tables_from_html(urls)
csv_tables_dict = convert_tables_to_csv(results)
extracted_data, unsuccessful_urls = process_and_extract_tables(csv_tables_dict, chunk_size=500)

# Print the CSV content for each URL
print_csv_tables(csv_tables_dict)

# Printing or further processing
print_bank_responses_json(extracted_data, num_to_print=10)
