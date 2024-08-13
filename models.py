from typing import List, Union
from pydantic import BaseModel

class CheckingAccountResponse(BaseModel):
    name: str
    interestRate: float
    annualPercentageYield: Union[float, None]
    minimumBalanceToObtainAPY: Union[float, None]
    minimumBalanceToOpen: Union[float, None]
    minimumDailyBalance: Union[float, None]
    dividendRate: Union[float, None]
    dividendFrequency: Union[str, None]

class SavingsAccountResponse(BaseModel):
    name: str
    interestRate: Union[float, None]
    annualPercentageYield: float
    minimumBalanceToObtainAPY: Union[float, None]
    minimumBalanceToOpen: Union[float, None]
    minimumDailyBalance: Union[float, None]
    dividendRate: Union[float, None]
    dividendFrequency: Union[str, None]

class MoneyMarketAccountResponse(BaseModel):
    name: str
    interestRate: Union[float, None]
    annualPercentageYield: float
    minimumBalanceToObtainAPY: Union[float, None]
    dividendRate: Union[float, None]
    dividendFrequency: Union[str, None]
    minimumBalanceToOpen: Union[float, None]
    minimumDailyBalance: Union[float, None]

class CertificateOfDepositResponse(BaseModel):
    term: str
    interestRate: Union[float, None]
    annualPercentageYield: float
    minimumBalanceToObtainAPY: Union[float, None]
    minimumBalanceToOpen: Union[float, None]
    minimumDailyBalance: Union[float, None]

class IndividualRetirementAccountResponse(BaseModel):
    term: str
    interestRate: Union[float, None]
    annualPercentageYield: float
    minimumBalanceToObtainAPY: Union[float, None]
    minimumBalanceToOpen: Union[float, None]
    minimumDailyBalance: Union[float, None]

class LoanResponse(BaseModel):
    name: str
    term: Union[Union[int, str], None]
    annualPercentageRate: float
    minimumPayment: Union[float, None]
    maximumLoanAmount: Union[float, None]
    paymentPer1000Dollars: Union[float, None]

class CreditCardResponse(BaseModel):
    name: Union[str, None]
    annualPercentageRate: float
    annualFee: Union[float, None]
    doesEarnRewards: Union[bool, None]

class FeeResponse(BaseModel):
    name: str
    feeAmount: float
    feeUnit: str
    oneTime: Union[bool, None]
    recurringInterval: Union[str, None]

class BankResponse(BaseModel):
    bankRootDomain: str
    checkingAccounts: Union[List[CheckingAccountResponse], None]
    savingsAccounts: Union[List[SavingsAccountResponse], None]
    moneyMarketAccounts: Union[List[MoneyMarketAccountResponse], None]
    certificatesOfDeposit: Union[List[CertificateOfDepositResponse], None]
    individualRetirementAccounts: Union[List[IndividualRetirementAccountResponse], None]
    loans: Union[List[LoanResponse], None]
    creditCards: Union[List[CreditCardResponse], None]
    fees: Union[List[FeeResponse], None]