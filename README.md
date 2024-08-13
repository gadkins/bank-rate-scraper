# Bank Rate Web Scraper with Generative AI

This repo implements a web scraping tool to extract publicly available banking rate information from a collection of bank websites.

## Implementation Roadmap

- [x] The web scraper BeautifulSoup is used to scrape HTML tags from a list of websites.
- [x] From the collected tags, we filter for `<table>`, `<h1>`, and `<h2>` tags, discarding the rest.
- [x] These tables are converted into CSV to clean them up and reduce their character count using custom functions.  
- [x] The CSV tables are then chunked to prepare them for sending to a large language model (LLM).
- [x] Along with the table chunks, a structured schema (Pydantic object) is provided to the LLM to instruct it on how the data should be formatted in it's response.
- [x] Special instructions can be provided to the LLM to handle edge cases or other behavior not well defined in the Pydantic object schema.
- [x] Once the LLM receives the table chunks, structured schema response format, and special instructions, it responds with a list of JSON objects containing the banking rates, per the schema (OpenAI Python SDK now supports enfocing a `response_format` such as a Pydantic object. The SDK handles converting the data type to a supported JSON schema, deserializing the JSON response into the typed data structure automatically, and parsing refusals if they arise. See [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)).
- [x] After all JSON objects are returned from the LLM, a post-processing script aggregates and deduplicates the data.
- [ ] A post-processing [validation pipeline](#output-validation) is used to check that the LLM outputs are accurate.  
- [ ] The validated data is then stored in a database (likely NoSQL) for use in downstream tasks
- [ ] An API is created to serve the data

## Structured Output

We expect the LLM to respond with the following structured output (in JSON format):   

<details>
  <summary>Show JSON schema</summary>

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
</details>

## Output Validation

We will create a human-in-the-loop evaluation pipeline to reduce the likelihood of errors, We'll use the following steps to validate the output of the LLM:

### 1. Rules-based Evaluation  
- Create a set of heuristics and rules to sanity check the model's output. E.g. if a field was previously not empty, it should be non-empty again.  
- We can use `deepdiff` to compare current and former JSON object states to determine what changed from last state  

### 2. Model-graded Evaluation  
- Ask an advanced LLM (like GPT-4o) to grade the output of the other model. This step can be broken down into a multi-agent pipeline, where one agent checks format and the other checks values.  
- Reprompt the model to correct any errors or omissions  
- Flag any entries that are below a certain confidence threshold for human evaluation

### 3. Human Evaluation  
- After rules-based and model-graded evaluation, send flagged entries to a human for evaluation  
- The human evaluator will then enter data manually into the FileMaker database

## Usage

To run the application, follow these steps:

### Clone the repository

```bash
git clone https://github.com/gadkins/bank-rate-scraper.git
```

### Configure the environment

Rename the `.env.example` file to `.env`:  

```bash
cp .env.example .env
```

Replace `OPENAI_API_KEY=your-api-key` with your API key from OpenAI (Get your API key [here](https://platform.openai.com/api-keys)).:  

### Create a virtual environment

```bash
# Create a virtual environment
python3 -m venv myenv

# Activate a virtual environment
source myenv/bin/activate
```
### Install dependencies

```bash
# Now you can install packages in an isolated venv, e.g...
pip3 install -r requirements.txt
```

### Run the script

Then run the following command:

```python
python3 main.py
```