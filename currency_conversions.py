import json


def get_nested(data, path):
    """Retrieve a nested value from dicts/lists given a dot-separated path."""
    keys = path.split('.')
    for key in keys:
        if isinstance(data, list):
            try:
                index = int(key)
                data = data[index]
            except (ValueError, IndexError):
                return None
        else:
            data = data.get(key)
        if data is None:
            return None
    return data


def get_exchange_rate(rates, from_curr, to_curr):
    """Get exchange rate from from_curr to to_curr using NBG rates."""
    if from_curr == to_curr:
        return 1.0
    for rate in rates:
        if (
            rate.get('CurrencyCodeFrom') == from_curr and
            rate.get('CurrencyCodeTo')   == to_curr and
            rate.get('ExchangeRateType') == 'NBG'
        ):
            multiplicity = float(rate.get('ExchangeRateMultiplicity', 1))
            rate_value   = float(rate.get('CurrencyRateSell', 0))
            return rate_value / multiplicity
    return None


# Load input JSON
with open('input_data.json') as f:
    input_data = json.load(f)

exchange_rates = input_data.get('ExchangeRates', {}).get('ExchangeRate', [])

# Determine the target loan currency for "InLoanCurrency" conversions
loan_currency_path = 'Application.TBCBank.Request.ApplicationData.Currency'
loan_currency = get_nested(input_data, loan_currency_path)

conversion_tasks = [
    {
        "base_path": "Application.TBCBank.Request.ApplicationData.ApplicationMinData",
        "fields": ["RequestedAmount", "RequestedRepayment"],
        "currency_path": "Application.TBCBank.Request.ApplicationData.Currency",
    },
    {
        "base_path": "Application.TBCBank.Request.Applicants.Applicant.InternalDataInfo.BasicCreditHistory.Loan",
        "fields": [
            "AccruedInsurance",
            "AccruedInterest",
            "AccruedPenalty",
            "PaidPenalty",
            "BusinessMonthlyPaymentAmount",
            "InsurancePastDueAmount",
            "InsurancePaymentAmount",
            "InterestPastDueAmount",
            "InterestPaymentAmount",
            "LimitAmount",
            "MonthlyPaymentAmount",
            "MaxMonthlyPaymentAmount",
            "PenaltyAmount",
            "OutstandingAmount",
            "PastDueAmount",
            "PrincipalPastDueAmount",
            "PrincipalPaymentAmount",
            "RefinanceBalance",
            "SAAccruedPenalty",
            "TotalAmountToCover",
        ],
        "currency_path": "Application.TBCBank.Request.Applicants.Applicant.InternalDataInfo.BasicCreditHistory.Loan.LimitCurrency",
    },
    {
        "base_path": "Application.TBCBank.Request.Applicants.Applicant.InternalDataInfo.BasicCreditHistory.Loan.Securities.Security",
        "fields": ["SecurityValue"],
        "currency_path": "Application.TBCBank.Request.Applicants.Applicant.InternalDataInfo.BasicCreditHistory.Loan.Securities.Security.Currency",
    },
    {
        "base_path": "Application.TBCBank.Request.Applicants.Applicant.InternalDataInfo.APMApplicationHistory.APMApplication",
        "fields": [
            "Amount",
            "MonthlyPaymentAmount",
            "MonthlyAmountPayment_Variable",
            "LongTermMonthlyPaymentAmount",
        ],
        "currency_path": "Application.TBCBank.Request.Applicants.Applicant.InternalDataInfo.APMApplicationHistory.APMApplication.Currency",
    },
    {
        "base_path": "Application.TBCBank.Request.Applicants.Applicant.InternalDataInfo.Accounts.Account.AccountPledge",
        "fields": ["RestrictionAmount"],
        "currency_path": "Application.TBCBank.Request.Applicants.Applicant.InternalDataInfo.Accounts.Account.AccountPledge.RestrictionCurrency",
    },
    {
        "base_path": "Application.TBCBank.Request.Applicants.Applicant.InternalDataInfo.Deposits.DepositInfo",
        "fields": ["DepositAmount"],
        "currency_path": "Application.TBCBank.Request.Applicants.Applicant.InternalDataInfo.Deposits.DepositInfo.DepositCurrency",
    },
    {
        "base_path": "Application.TBCBank.Request.Applicants.Applicant.InternalDataInfo.TransferTransactionHistory.TransferAmounts.TransferAmount",
        "fields": ["Amount"],
        "currency_path": "Application.TBCBank.Request.Applicants.Applicant.InternalDataInfo.TransferTransactionHistory.TransferAmounts.TransferAmount.Currency",
    },
    {
        "base_path": "Application.TBCBank.Request.Applicants.Applicant.CreditBureauInfo.BasicCreditHistory.Loan",
        "fields": [
            "AccruedPenalty",
            "LimitAmount",
            "MonthlyPaymentAmount",
            "MaxMonthlyPaymentAmount",
            "OutstandingAmount",
            "PastDueAmount",
            "PrincipalPastDueAmount",
            "RefinanceBalance",
        ],
        "currency_path": "Application.TBCBank.Request.Applicants.Applicant.CreditBureauInfo.BasicCreditHistory.Loan.LimitCurrency",
    },
    {
        "base_path": "Application.TBCBank.Request.Applicants.Applicant.CreditBureauInfo.BasicCreditHistory.Loan.Securities.Security",
        "fields": ["SecurityValue"],
        "currency_path": "Application.TBCBank.Request.Applicants.Applicant.CreditBureauInfo.BasicCreditHistory.Loan.Securities.Security.Currency",
    },
    {
        "base_path": "Application.TBCBank.Request.Applicants.Applicant.OtherLiabilities.OtherLiability",
        "fields": [
            "LimitAmount",
            "MonthlyPaymentAmount",
            "OutstandingAmount",
            "TotalRefinanceBalanceAmount",
            "RefinanceBalance",
        ],
        "currency_path": "Application.TBCBank.Request.Applicants.Applicant.OtherLiabilities.OtherLiability.LimitCurrency",
    },
    {
        "base_path": "Application.TBCBank.Request.Applicants.Applicant.Jobs.JobInfo",
        "fields": ["IncomeAmount", "VerifideIncome", "Expense", "NBGMaxNetIncome"],
        "currency_path": "Application.TBCBank.Request.Applicants.Applicant.Jobs.JobInfo.IncomeCurrency",
    },
    {
        "base_path": "Application.TBCBank.Request.Applicants.Applicant.VerifiedIncome",
        "fields": ["VerifideIncome"],
        "currency_path": "Application.TBCBank.Request.Applicants.Applicant.VerifiedIncome.IncomeCurrency",
    },
]

for task in conversion_tasks:
    base = task['base_path']
    fields = task['fields']
    curr_path = task['currency_path']

    orig_curr = get_nested(input_data, curr_path)
    if orig_curr is None:
        print(f"Warning: Currency not found at {curr_path}")
        continue

    parent = get_nested(input_data, base)
    if parent is None:
        print(f"Warning: Base path {base} not found")
        continue

    items = parent if isinstance(parent, list) else [parent]
    for item in items:
        for field in fields:
            if field not in item:
                continue
            val = item[field]
            if val is None:
                continue
            try:
                num = float(val) if isinstance(val, str) else val
            except (ValueError, TypeError):
                print(f"Warning: Cannot convert {field}='{val}' to number")
                continue

            rate_gel = get_exchange_rate(exchange_rates, orig_curr, 'GEL')
            if rate_gel is not None:
                item[field + 'GEL'] = round(num * rate_gel, 2)

            if loan_currency:
                rate_loan = get_exchange_rate(exchange_rates, orig_curr, loan_currency)
                if rate_loan is not None:
                    item[field + 'InLoanCurrency'] = round(num * rate_loan, 2)

# === CUSTOM LOOPS FOR SECURITIES ===
# 1) InternalDataInfo.BasicCreditHistory.Loan → Securities.Security
loan_list = get_nested(input_data, 'Application.TBCBank.Request.Applicants.Applicant.InternalDataInfo.BasicCreditHistory.Loan')
if isinstance(loan_list, list):
    for loan in loan_list:
        sec = loan.get('Securities', {}).get('Security')
        if isinstance(sec, dict):
            curr = sec.get('Currency')
            val  = sec.get('SecurityValue')
            if curr and val is not None:
                try:
                    num = float(val)
                except (ValueError, TypeError):
                    continue
                rg = get_exchange_rate(exchange_rates, curr, 'GEL')
                if rg is not None:
                    sec['SecurityValueGEL'] = round(num * rg, 2)
                if loan_currency:
                    rl = get_exchange_rate(exchange_rates, curr, loan_currency)
                    if rl is not None:
                        sec['SecurityValueInLoanCurrency'] = round(num * rl, 2)

# 2) CreditBureauInfo.BasicCreditHistory.Loan → Securities.Security
cb_loans = get_nested(input_data, 'Application.TBCBank.Request.Applicants.Applicant.CreditBureauInfo.BasicCreditHistory.Loan')
if isinstance(cb_loans, list):
    for loan in cb_loans:
        sec = loan.get('Securities', {}).get('Security')
        if isinstance(sec, dict):
            curr = sec.get('Currency')
            val  = sec.get('SecurityValue')
            if curr and val is not None:
                try:
                    num = float(val)
                except (ValueError, TypeError):
                    continue
                rg = get_exchange_rate(exchange_rates, curr, 'GEL')
                if rg is not None:
                    sec['SecurityValueGEL'] = round(num * rg, 2)
                if loan_currency:
                    rl = get_exchange_rate(exchange_rates, curr, loan_currency)
                    if rl is not None:
                        sec['SecurityValueInLoanCurrency'] = round(num * rl, 2)

# Write out the augmented JSON
with open('output.json', 'w') as f:
    json.dump(input_data, f, indent=4)

print('✅ Conversion complete. Results saved to output.json.')
