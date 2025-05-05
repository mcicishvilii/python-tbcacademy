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

# Determine the target loan currency for "InLoanCurrency" conversions (absolute path)
loan_currency_path = 'Application.TBCBank.Request.ApplicationData.Currency'
loan_currency = get_nested(input_data, loan_currency_path)

# Conversion tasks for fields, with per-item currency where appropriate
conversion_tasks = [
    # APM applications
    {
        'base_path': 'Application.TBCBank.Request.Applicants.Applicant.InternalDataInfo.APMApplicationHistory.APMApplication',
        'fields': ['Amount', 'MonthlyPaymentAmount', 'MonthlyAmountPayment_Variable', 'LongTermMonthlyPaymentAmount'],
        'currency_path': 'Application.TBCBank.Request.Applicants.Applicant.InternalDataInfo.APMApplicationHistory.APMApplication.Currency'
    },
    # BasicCreditHistory.Loans (InternalDataInfo)
    {
        'base_path': 'Application.TBCBank.Request.Applicants.Applicant.InternalDataInfo.BasicCreditHistory.Loan',
        'fields': [
            'AccruedInsurance', 'AccruedInterest', 'AccruedPenalty', 'PaidPenalty',
            'BusinessMonthlyPaymentAmount', 'InsurancePastDueAmount', 'InsurancePaymentAmount',
            'InterestPastDueAmount', 'InterestPaymentAmount', 'LimitAmount',
            'MonthlyPaymentAmount', 'MaxMonthlyPaymentAmount', 'PenaltyAmount',
            'OutstandingAmount', 'PastDueAmount', 'PrincipalPastDueAmount',
            'PrincipalPaymentAmount', 'RefinanceBalance', 'SAAccruedPenalty', 'TotalAmountToCover'
        ],
        'currency_subpath': 'LimitCurrency'
    },
    # BasicCreditHistory.Loans (CreditBureauInfo)
    {
        'base_path': 'Application.TBCBank.Request.Applicants.Applicant.CreditBureauInfo.BasicCreditHistory.Loan',
        'fields': [
            'AccruedPenalty', 'LimitAmount', 'MonthlyPaymentAmount', 'MaxMonthlyPaymentAmount',
            'OutstandingAmount', 'PastDueAmount', 'PrincipalPastDueAmount', 'RefinanceBalance'
        ],
        'currency_subpath': 'LimitCurrency'
    },
    # Other tasks here: Accounts.AccountPledge, Deposits, TransferAmounts, OtherLiabilities, Jobs, VerifiedIncome
    # [... add as before with either 'currency_path' or 'currency_subpath' depending on list or single]
]

def convert_fields(parent, fields, orig_curr):
    for field in fields:
        if field not in parent:
            continue
        val = parent[field]
        if val is None:
            continue
        try:
            num = float(val) if isinstance(val, str) else val
        except (ValueError, TypeError):
            print(f"Warning: Cannot convert {field}='{val}' to number")
            continue

        rate_gel = get_exchange_rate(exchange_rates, orig_curr, 'GEL')
        if rate_gel is not None:
            parent[field + 'GEL'] = round(num * rate_gel, 2)
        if loan_currency:
            rate_loan = get_exchange_rate(exchange_rates, orig_curr, loan_currency)
            if rate_loan is not None:
                parent[field + 'InLoanCurrency'] = round(num * rate_loan, 2)

for task in conversion_tasks:
    base = task['base_path']
    fields = task['fields']
    curr_path = task.get('currency_path')
    curr_sub = task.get('currency_subpath')

    parent = get_nested(input_data, base)
    if parent is None:
        print(f"Warning: Base path {base} not found")
        continue

    items = parent if isinstance(parent, list) else [parent]
    for item in items:
        if curr_sub:
            orig_curr = item.get(curr_sub)
        else:
            orig_curr = get_nested(input_data, curr_path)
        if orig_curr is None:
            print(f"Warning: Currency not found for task at {base} (item)")
            continue

        convert_fields(item, fields, orig_curr)

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