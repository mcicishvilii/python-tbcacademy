import logging
import pandas as pd

logger = logging.getLogger(__name__)

# Define fields to convert for each data path
APPLICATION_MIN_DATA_FIELDS = ['requestedamount', 'requestedrepayment']
LOAN_FIELDS = [
    'AccruedInsurance', 'AccruedInterest', 'AccruedPenalty', 'PaidPenalty',
    'InsurancePastDueAmount', 'InsurancePaymentAmount', 'InterestPastDueAmount',
    'InterestPaymentAmount', 'LimitAmount', 'MaxMonthlyPaymentAmount', 'PenaltyAmount',
    'OutstandingAmount', 'PastDueAmount', 'PrincipalPastDueAmount', 'PrincipalPaymentAmount',
    'RefinanceBalance', 'SAAccruedPenalty', 'TotalAmountToCover'
]
SECURITY_FIELDS = ['SecurityValue']
APM_APPLICATION_FIELDS = ['Amount', 'MonthlyPaymentAmount', 'MonthlyAmountPayment_Variable', 'LongTermMonthlyPaymentAmount']
ACCOUNT_PLEDGE_FIELDS = ['RestrictionAmount']
DEPOSIT_FIELDS = ['DepositAmount']
TRANSFER_FIELDS = ['Amount']
OTHER_LIABILITY_FIELDS = ['LimitAmount', 'OutstandingAmount', 'TotalRefinanceBalanceAmount', 'RefinanceBalance']
JOBINFO_FIELDS = ['IncomeAmount', 'VerifideIncome', 'Expense', 'NBGMaxNetIncome']

def convert_fields(items, currency_field=None, fixed_currency=None, fields_to_convert=None, fx_rates=None, target_currency=None, NBGExchangeRates=None):
    """
    Converts specified fields of each item in `items` to GEL and loan currency.
    
    :param items: List of objects (or a single object) to process.
    :param currency_field: Name of the field in each item that holds its currency (e.g., 'limitcurrency').
    :param fixed_currency: If provided, use this as the currency instead of looking up a field.
    :param fields_to_convert: List of field names to convert (e.g., ['LimitAmount', 'OutstandingAmount']).
    :param fx_rates: Exchange rates data.
    :param target_currency: The loan currency.
    :param NBGExchangeRates: Filtered exchange rates for NBG.
    """
    if not isinstance(items, list):
        items = [items]
    
    for item in items:
        # Determine the object's currency
        if currency_field is not None:
            if hasattr(item, currency_field):
                object_currency = getattr(item, currency_field)
            else:
                logger.error(f"Currency field '{currency_field}' not found in item")
                continue
        elif fixed_currency is not None:
            object_currency = fixed_currency
        else:
            logger.error("No currency source provided")
            continue
        
        # Calculate exchange rates
        try:
            rate_to_gel = ExchangeRates_Calculation(fx_rates, object_currency, "GEL", NBGExchangeRates)
            rate_in_loan = ExchangeRates_Calculation(fx_rates, object_currency, target_currency, NBGExchangeRates)
        except ValueError as e:
            logger.error(f"Error calculating exchange rates for {item}: {e}")
            continue
        
        # Convert each field
        for field in fields_to_convert or []:
            if hasattr(item, field) and getattr(item, field) is not None:
                setattr(item, field + 'gel', getattr(item, field) * rate_to_gel)
                setattr(item, field + 'inloancurrency', getattr(item, field) * rate_in_loan)

def ExchangeRates_Calculation(fx_rates, node_currency, target_currency, NBGExchangeRates):
    node_currency = str(node_currency).upper()
    target_currency = str(target_currency).upper()
    if node_currency == target_currency:
        return 1.0
    filtered_rates = NBGExchangeRates[
        (NBGExchangeRates["CurrencyCodeFrom"] == node_currency) &
        (NBGExchangeRates["CurrencyCodeTo"] == target_currency)
    ]
    if not filtered_rates.empty:
        return filtered_rates["CurrencyRateSell"].iloc[0]
    else:
        raise ValueError(f"Error: No exchange rate found from {node_currency} to {target_currency}.")

# Mock classes to simulate the data structure
class MockObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def GetNodeKey(self):
        return 1  # Simulate valid node

class MockList(list):
    def __init__(self, items):
        if isinstance(items, list):
            super().__init__(items)
        else:
            super().__init__([items])
    
    def GetNodeKey(self):
        return 1 if len(self) > 0 else -1

# Create mock exchange rates data
mock_fx_rates = pd.DataFrame([
    {"CurrencyCodeFrom": "USD", "CurrencyCodeTo": "GEL", "CurrencyRateSell": 2.65, "ExchangeRateType": "NBG"},
    {"CurrencyCodeFrom": "EUR", "CurrencyCodeTo": "GEL", "CurrencyRateSell": 2.85, "ExchangeRateType": "NBG"},
    {"CurrencyCodeFrom": "GEL", "CurrencyCodeTo": "USD", "CurrencyRateSell": 0.377, "ExchangeRateType": "NBG"},
    {"CurrencyCodeFrom": "GEL", "CurrencyCodeTo": "EUR", "CurrencyRateSell": 0.351, "ExchangeRateType": "NBG"},
    {"CurrencyCodeFrom": "USD", "CurrencyCodeTo": "EUR", "CurrencyRateSell": 0.93, "ExchangeRateType": "NBG"},
    {"CurrencyCodeFrom": "EUR", "CurrencyCodeTo": "USD", "CurrencyRateSell": 1.075, "ExchangeRateType": "NBG"},
])

# Mock data setup - Replace the real data extraction with mocks
target_currency = "GEL"  # Mock target currency
fx_rates = mock_fx_rates  # Mock exchange rates
NBGExchangeRates = fx_rates[fx_rates["ExchangeRateType"] == "NBG"]

# Mock ApplicationMinData
application_mindata = MockObject(
    requestedamount=10000,
    requestedrepayment=12000
)

# Mock Applicants with nested structures
mock_security1 = MockObject(currency="USD", SecurityValue=2000)
mock_security2 = MockObject(currency="EUR", SecurityValue=1500)

mock_loan = MockObject(
    limitcurrency="USD",
    LimitAmount=5000,
    OutstandingAmount=3000,
    AccruedInterest=100,
    securities=MockObject(security=MockList([mock_security1, mock_security2]))
)

mock_apm_application = MockObject(
    currency="EUR",
    Amount=8000,
    MonthlyPaymentAmount=500
)

mock_account = MockObject(
    accountpledge=MockObject(
        restrictioncurrency="USD",
        RestrictionAmount=1000
    )
)

mock_deposit = MockObject(
    depositcurrency="EUR",
    DepositAmount=5000
)

mock_transfer = MockObject(
    currency="USD",
    Amount=200
)

mock_other_liability = MockObject(
    limitcurrency="EUR",
    LimitAmount=3000,
    OutstandingAmount=2500
)

mock_jobinfo = MockObject(
    incomecurrency="USD",
    IncomeAmount=3000,
    VerifideIncome=2800,
    Expense=1500,
    incomegel_modela=7500  # Special field for conversion
)

# Create mock applicant structure
mock_applicant = MockObject(
    internaldatainfo=MockObject(
        basiccredithistory=MockObject(loan=MockList([mock_loan])),
        apmapplicationhistory=MockObject(apmapplication=MockList([mock_apm_application])),
        accounts=MockObject(account=MockList([mock_account])),
        deposits=MockObject(depositinfo=MockList([mock_deposit])),
        transfertransactionhistory=MockObject(
            transferamounts=MockObject(transferamount=MockList([mock_transfer]))
        )
    ),
    creditbureauinfo=MockObject(
        basiccredithistory=MockObject(loan=MockList([mock_loan]))
    ),
    otherliabilities=MockObject(otherliability=MockList([mock_other_liability])),
    jobs=MockObject(jobinfo=MockList([mock_jobinfo]))
)

applicants = MockList([mock_applicant])

logger.info("=== Starting Currency Conversion Processing ===")

# Process ApplicationMinData
convert_fields(
    application_mindata,
    fixed_currency=target_currency,
    fields_to_convert=APPLICATION_MIN_DATA_FIELDS,
    fx_rates=fx_rates,
    target_currency=target_currency,
    NBGExchangeRates=NBGExchangeRates
)

# Process each applicant
for i, applicant in enumerate(applicants):
    logger.info(f"Processing Applicant {i}")

    # Process InternalDataInfo Loans
    loans = applicant.internaldatainfo.basiccredithistory.loan
    if loans.GetNodeKey() != -1:
        # Convert each loan individually
        for loan in loans:
            convert_fields(
                loan,  # Pass individual loan, not the list
                currency_field='limitcurrency',
                fields_to_convert=LOAN_FIELDS,
                fx_rates=fx_rates,
                target_currency=target_currency,
                NBGExchangeRates=NBGExchangeRates
            )
        # Process securities within loans
        for loan in loans:
            securities = loan.securities.security
            if securities.GetNodeKey() != -1:
                # Convert each security individually
                for security in securities:
                    convert_fields(
                        security,  # Pass individual security, not the list
                        currency_field='currency',
                        fields_to_convert=SECURITY_FIELDS,
                        fx_rates=fx_rates,
                        target_currency=target_currency,
                        NBGExchangeRates=NBGExchangeRates
                    )
    else:
        logger.warning(f"Loans node missing for Applicant {i}")

    # Process APMApplications
    apmapplications = applicant.internaldatainfo.apmapplicationhistory.apmapplication
    if apmapplications.GetNodeKey() != -1:
        for apm in apmapplications:
            convert_fields(
                apm,
                currency_field='currency',
                fields_to_convert=APM_APPLICATION_FIELDS,
                fx_rates=fx_rates,
                target_currency=target_currency,
                NBGExchangeRates=NBGExchangeRates
            )
    else:
        logger.warning(f"APMApplications node missing for Applicant {i}")

    # Process AccountPledge
    accounts = applicant.internaldatainfo.accounts.account
    if accounts.GetNodeKey() != -1:
        for account in accounts:
            if hasattr(account, 'accountpledge'):
                convert_fields(
                    account.accountpledge,
                    currency_field='restrictioncurrency',
                    fields_to_convert=ACCOUNT_PLEDGE_FIELDS,
                    fx_rates=fx_rates,
                    target_currency=target_currency,
                    NBGExchangeRates=NBGExchangeRates
                )
    else:
        logger.warning(f"Accounts node missing for Applicant {i}")

    # Process Deposits
    deposits = applicant.internaldatainfo.deposits.depositinfo
    if deposits.GetNodeKey() != -1:
        for deposit in deposits:
            convert_fields(
                deposit,
                currency_field='depositcurrency',
                fields_to_convert=DEPOSIT_FIELDS,
                fx_rates=fx_rates,
                target_currency=target_currency,
                NBGExchangeRates=NBGExchangeRates
            )
    else:
        logger.warning(f"Deposits node missing for Applicant {i}")

    # Process TransferAmounts
    transfers = applicant.internaldatainfo.transfertransactionhistory.transferamounts.transferamount
    if transfers.GetNodeKey() != -1:
        for transfer in transfers:
            convert_fields(
                transfer,
                currency_field='currency',
                fields_to_convert=TRANSFER_FIELDS,
                fx_rates=fx_rates,
                target_currency=target_currency,
                NBGExchangeRates=NBGExchangeRates
            )
    else:
        logger.warning(f"TransferAmounts node missing for Applicant {i}")

    # Process CreditBureauInfo Loans
    cb_loans = applicant.creditbureauinfo.basiccredithistory.loan
    if cb_loans.GetNodeKey() != -1:
        for loan in cb_loans:
            convert_fields(
                loan,
                currency_field='limitcurrency',
                fields_to_convert=LOAN_FIELDS,
                fx_rates=fx_rates,
                target_currency=target_currency,
                NBGExchangeRates=NBGExchangeRates
            )
        for loan in cb_loans:
            securities = loan.securities.security
            if securities.GetNodeKey() != -1:
                for security in securities:
                    convert_fields(
                        security,
                        currency_field='currency',
                        fields_to_convert=SECURITY_FIELDS,
                        fx_rates=fx_rates,
                        target_currency=target_currency,
                        NBGExchangeRates=NBGExchangeRates
                    )
    else:
        logger.warning(f"CreditBureau Loans node missing for Applicant {i}")

    # Process OtherLiabilities
    otherliabilities = applicant.otherliabilities.otherliability
    if otherliabilities.GetNodeKey() != -1:
        for liability in otherliabilities:
            convert_fields(
                liability,
                currency_field='limitcurrency',
                fields_to_convert=OTHER_LIABILITY_FIELDS,
                fx_rates=fx_rates,
                target_currency=target_currency,
                NBGExchangeRates=NBGExchangeRates
            )
    else:
        logger.warning(f"OtherLiabilities node missing for Applicant {i}")

    # Process JobInfo
    jobinfos = applicant.jobs.jobinfo
    if jobinfos.GetNodeKey() != -1:
        for jobinfo in jobinfos:
            convert_fields(
                jobinfo,
                currency_field='incomecurrency',
                fields_to_convert=JOBINFO_FIELDS,
                fx_rates=fx_rates,
                target_currency=target_currency,
                NBGExchangeRates=NBGExchangeRates
            )
        # Handle special case for incomegel_modela
        for jobinfo in jobinfos:
            if hasattr(jobinfo, 'incomegel_modela') and jobinfo.incomegel_modela is not None:
                try:
                    rate_from_gel_to_loan = ExchangeRates_Calculation(fx_rates, "GEL", target_currency, NBGExchangeRates)
                    jobinfo.incomeinloancurrency_modela = jobinfo.incomegel_modela * rate_from_gel_to_loan
                except ValueError as e:
                    logger.error(f"Error converting incomegel_modela for Applicant {i}: {e}")
    else:
        logger.warning(f"JobInfo node missing for Applicant {i}")

logger.info("=== End of Currency Conversion Processing ===")

# Test the results - Print some converted values to verify
print("=== Testing Results ===")
print(f"Application Min Data - Requested Amount GEL: {getattr(application_mindata, 'requestedamountgel', 'Not converted')}")
print(f"Loan Limit Amount GEL: {getattr(mock_loan, 'LimitAmountgel', 'Not converted')}")
print(f"Job Info Income Amount GEL: {getattr(mock_jobinfo, 'IncomeAmountgel', 'Not converted')}")
print(f"Security Value GEL: {getattr(mock_security1, 'SecurityValuegel', 'Not converted')}")
print(f"APM Application Amount GEL: {getattr(mock_apm_application, 'Amountgel', 'Not converted')}")
print(f"Deposit Amount GEL: {getattr(mock_deposit, 'DepositAmountgel', 'Not converted')}")

# Print all attributes of mock_loan to see what was actually converted
print(f"\nMock loan attributes: {[attr for attr in dir(mock_loan) if not attr.startswith('_')]}")
print(f"Mock jobinfo attributes: {[attr for attr in dir(mock_jobinfo) if not attr.startswith('_')]}")