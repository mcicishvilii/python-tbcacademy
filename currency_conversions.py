import json


def get_nested(data, path):
    keys = path.split(".")
    for key in keys:
        if isinstance(data, list):
            try:
                index = int(key)
                data = data[index]
            except (ValueError, IndexError):
                return None
        else:
            data = data.get(key, None)
        if data is None:
            return None
    return data


def get_exchange_rate(rates, from_curr, to_curr):
    if from_curr == to_curr:
        return 1.0
    for rate in rates:
        if (
            rate["CurrencyCodeFrom"] == from_curr
            and rate["CurrencyCodeTo"] == to_curr
            and rate["ExchangeRateType"] == "NBG"
        ):
            multiplicity = float(rate["ExchangeRateMultiplicity"])
            rate_value = float(rate["CurrencyRateSell"])
            return rate_value / multiplicity
    return None


with open("input_data.json") as f:
    input_data = json.load(f)

exchange_rates = input_data["ExchangeRates"]["ExchangeRate"]

loan_currency_path = "Application.TBCBank.Request.ApplicationData.Currency"
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
    base_path = task["base_path"]
    fields = task["fields"]
    currency_path = task["currency_path"]

    original_currency = get_nested(input_data, currency_path)
    if original_currency is None:
        print(f"Warning: Currency not found at {currency_path}")
        continue

    parent = get_nested(input_data, base_path)
    if parent is None:
        print(f"Warning: Base path {base_path} not found")
        continue

    if isinstance(parent, list):
        for item in parent:
            for field in fields:
                if field in item:
                    value = item[field]
                    if value is None:
                        continue

                    try:
                        numeric_value = (
                            float(value) if isinstance(value, str) else value
                        )
                    except (ValueError, TypeError):
                        print(
                            f"Warning: Could not convert {field} value '{value}' to number"
                        )
                        continue

                    rate_to_gel = get_exchange_rate(
                        exchange_rates, original_currency, "GEL"
                    )
                    if rate_to_gel is not None:
                        item[field + "GEL"] = round(numeric_value * rate_to_gel, 2)
                    else:
                        print(
                            f"Warning: No rate from {original_currency} to GEL for {field}"
                        )

                    rate_to_loan = get_exchange_rate(
                        exchange_rates, original_currency, loan_currency
                    )
                    if rate_to_loan is not None:
                        item[field + "InLoanCurrency"] = round(
                            numeric_value * rate_to_loan, 2
                        )
                    else:
                        print(
                            f"Warning: No rate from {original_currency} to {loan_currency} for {field}"
                        )
    else:
        for field in fields:
            if field in parent:
                value = parent[field]
                if value is None:
                    continue

                try:
                    numeric_value = float(value) if isinstance(value, str) else value
                except (ValueError, TypeError):
                    print(
                        f"Warning: Could not convert {field} value '{value}' to number"
                    )
                    continue

                rate_to_gel = get_exchange_rate(
                    exchange_rates, original_currency, "GEL"
                )
                if rate_to_gel is not None:
                    parent[field + "GEL"] = round(numeric_value * rate_to_gel, 2)
                else:
                    print(
                        f"Warning: No rate from {original_currency} to GEL for {field}"
                    )

                rate_to_loan = get_exchange_rate(
                    exchange_rates, original_currency, loan_currency
                )
                if rate_to_loan is not None:
                    parent[field + "InLoanCurrency"] = round(
                        numeric_value * rate_to_loan, 2
                    )
                else:
                    print(
                        f"Warning: No rate from {original_currency} to {loan_currency} for {field}"
                    )

with open("output.json", "w") as f:
    json.dump(input_data, f, indent=4)

print("✅ Conversion complete. Results saved to output.json.")
