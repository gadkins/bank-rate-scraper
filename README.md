# Banking Rate Web Scraper with Generative AI

This repo implements a web scraping tool to extract publicly available banking rate information from a collection of bank websites.

## How it works

1. The web scraper BeautifulSoup is used to scrape HTML tags from a list of websites.
2. From the collected tags, we filter for `<table>` tags, discarding the rest.
3. These tables are converted into CSV to clean them up and reduce their character count.
4. Next the tables in CSV format are chunked to prepare them for sending to a large language model (LLM).
5. Along with the table chunks, a JSON schema is provided to the LLM to instruct it in what the data format should be in it's response.
6. Special instructions can be provided to the LLM to handle edge cases or other behavior not well defined in the JSON schema.
7. Once the LLM receives the table chunks, JSON schema, and special instructions, it responds with a list of JSON objects, per the schema.
8. After all JSON objects are returned from the LLM, a post-processing script aggregates and deduplicates the data.

## JSON Schema

The following JSON schema is provided to the LLM to format it's response:  

```json
{
    "type": "object",
    "properties": {
        "bankDomain": {
            "type": "string",
            "description": "The domain of the bank to which these account types belong."
        },
        "checkingAccounts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the checking account, e.g. Interest Checking, Senior Advantage Checking, etc."
                    },
                    "interestRate": {
                        "type": "number",
                        "description": "The interest rate of the checking account, if any."
                    },
                    "annualPercentageYield": {
                        "type": "number",
                        "description": "The annual percentage yield (APY) of the checking account."
                    },
                    "minimumBalanceToObtainAPY": {
                        "type": "number",
                        "description": "The minimum balance to obtain the annual percentage yield (APY)."
                    },
                    "minimumBalanceToOpen": {
                        "type": "number",
                        "description": "The minimum balance to open the checking account."
                    },
                    "minimumDailyBalance": {
                        "type": "number",
                        "description": "The minimum daily balance of the checking account to obtain APY or avoid fees."
                    },
                    "dividendRate": {
                        "type": "number",
                        "description": "The dividend rate of the checking account, if any."
                    },
                    "dividendFrequency": {
                        "type": "string",
                        "description": "The frequency at which dividends are paid, if at all, e.g. monthly, quarterly, annually, etc."
                    }
                },
                "required": [
                    "name",
                    "annualPercentageYield"
                ]
            }
        },
        "savingsAccounts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the savings account, e.g. Partnership Savings, Statement Savings, etc."
                    },
                    "interestRate": {
                        "type": "number",
                        "description": "The interest rate of the savings account, if any."
                    },
                    "annualPercentageYield": {
                        "type": "number",
                        "description": "The annual percentage yield (APY) of the savings account."
                    },
                    "minimumBalanceToObtainAPY": {
                        "type": "number",
                        "description": "The minimum balance to obtain the annual percentage yield (APY)."
                    },
                    "minimumBalanceToOpen": {
                        "type": "number",
                        "description": "The minimum balance to open the savings account."
                    },
                    "minimumDailyBalance": {
                        "type": "number",
                        "description": "The minimum daily balance of the savings account to obtain APY or avoid fees."
                    },
                    "dividendRate": {
                        "type": "number",
                        "description": "The dividend rate of the checking account, if any."
                    },
                    "dividendFrequency": {
                        "type": "string",
                        "description": "The frequency at which dividends are paid, if at all, e.g. monthly, quarterly, annually, etc."
                    },
                    "required": [
                        "name",
                        "annualPercentageYield"
                    ]
                }
            },
            "moneyMarketAccounts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name or tier of money market account, e.g. Tier 1 ($0.01 - $9,999.99), etc."
                        },
                        "interestRate": {
                            "type": "number",
                            "description": "The interest rate of the savings account, if any."
                        },
                        "annualPercentageYield": {
                            "type": "number",
                            "description": "The annual percentage yield (APY) of the savings account."
                        },
                        "minimumBalanceToObtainAPY": {
                            "type": "number",
                            "description": "The minimum balance to obtain the annual percentage yield (APY)."
                        },
                        "dividendRate": {
                            "type": "number",
                            "description": "The dividend rate of the checking account, if any."
                        },
                        "dividendFrequency": {
                            "type": "string",
                            "description": "The frequency at which dividends are paid, if at all, e.g. monthly, quarterly, annually, etc."
                        },
                        "minimumBalanceToOpen": {
                            "type": "number",
                            "description": "The minimum balance to open the savings account."
                        },
                        "minimumDailyBalance": {
                            "type": "number",
                            "description": "The minimum daily balance of the savings account to obtain APY or avoid fees."
                        }
                    },
                    "required": [
                        "name",
                        "annualPercentageYield"
                    ]
                }
            },
            "certificatesOfDeposit": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "term": {
                            "type": "string",
                            "description": "The term of the certificate of deposit, e.g. 6 months, 12 months, etc."
                        },
                        "interestRate": {
                            "type": "number",
                            "description": "The interest rate of the certificate of deposit, if any."
                        },
                        "annualPercentageYield": {
                            "type": "number",
                            "description": "The annual percentage yield (APY) of the certificate of deposit."
                        },
                        "minimumBalanceToObtainAPY": {
                            "type": "number",
                            "description": "The minimum balance to obtain the annual percentage yield (APY)."
                        },
                        "minimumBalanceToOpen": {
                            "type": "number",
                            "description": "The minimum balance to open the certificate of deposit."
                        },
                        "minimumDailyBalance": {
                            "type": "number",
                            "description": "The minimum daily balance of the certificate of deposit to obtain APY or avoid fees."
                        }
                    },
                    "required": [
                        "term",
                        "annualPercentageYield"
                    ]
                }
            },
            "individualRetirementAccounts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "term": {
                            "type": "string",
                            "description": "The term of the individual retirement account, e.g. 7 months, 12 months, etc."
                        },
                        "interestRate": {
                            "type": "number",
                            "description": "The interest rate of the individual retirement account, if any."
                        },
                        "annualPercentageYield": {
                            "type": "number",
                            "description": "The annual percentage yield (APY) of the individual retirement account."
                        },
                        "minimumBalanceToObtainAPY": {
                            "type": "number",
                            "description": "The minimum balance to obtain the annual percentage yield (APY)."
                        },
                        "minimumBalanceToOpen": {
                            "type": "number",
                            "description": "The minimum balance to open the individual retirement account."
                        },
                        "minimumDailyBalance": {
                            "type": "number",
                            "description": "The minimum daily balance of the individual retirement account to obtain APY or avoid fees."
                        }
                    },
                    "required": [
                        "term",
                        "annualPercentageYield"
                    ]
                }
            },
            "loans": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the loan, e.g. Auto Loan, Student Loan, 30-Year Fixed Rate Mortgage, etc."
                        },
                        "term": {
                            "anyOf": [
                                {
                                    "type": "integer"
                                },
                                {
                                    "type": "string"
                                }
                            ],
                            "description": "The term of the loan, e.g. 1-3 years, 7 years, etc."
                        },
                        "annualPercentageRate": {
                            "type": "number",
                            "description": "The Annual Percentage Rate (APR) of the loan. APR is the interest rate plus additional fees charged by the lender."
                        },
                        "minimumPayment": {
                            "type": "number",
                            "description": "The required minimum monthly payment for the loan."
                        },
                        "maximumLoanAmount": {
                            "type": "number",
                            "description": "The maximum loan amount that can be borrowed as a percentage of the collateral value."
                        },
                        "paymentPer1000Dollars": {
                            "type": "number",
                            "description": "The amount the borrower would pay per month for every $1,000 borrowed."
                        }
                    },
                    "required": [
                        "name",
                        "annualPercentageRate"
                    ]
                }
            },
            "creditCards": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the credit card, if applicable, e.g. Visa Platinum, Mastercard Gold, etc."
                        },
                        "annualPercentageRate": {
                            "type": "number",
                            "description": "The Annual Percentage Rate (APR) of the loan. APR is the interest rate plus additional fees charged by the lender."
                        },
                        "annualFee": {
                            "type": "number",
                            "description": "The annual fee charged by the credit card provider."
                        },
                        "doesEarnRewards": {
                            "type": "boolean",
                            "description": "Indicates whether the credit card earns rewards or not."
                        }
                    },
                    "required": [
                        "annualPercentageRate",
                        "annualFee"
                    ]
                }
            },
            "fees": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the fee, e.g. Overdraft Fee, Wire Transfer Fee, etc."
                        },
                        "feeAmount": {
                            "type": "number",
                            "description": "The fee amount."
                        },
                        "feeUnit": {
                            "type": "string",
                            "description": "The unit of the fee amount, e.g. 'per hour', 'per month', 'per ten', '%', etc."
                        },
                        "oneTime": {
                            "type": "boolean",
                            "description": "Indicates if the fee is a one-time fee."
                        },
                        "recurringInterval": {
                            "type": "string",
                            "description": "The interval for recurring fees, e.g. 'monthly', 'annually', etc. (if applicable).",
                            "enum": ["daily", "weekly", "monthly", "annually"]
                        }
                    },
                    "required": [
                        "name",
                        "feeAmount",
                        "feeUnit"
                    ],
                    "anyOf": [
                        {
                            "required": ["oneTime"]
                        },
                        {
                            "required": ["recurringInterval"]
                        }
                    ]
                }
            }
        }
    }
}
```
