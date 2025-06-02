import pandas as pd

# Get target currency from input
target_currency = (
    record.fcl_listener.input.application.tbcbank.request.applicationdata.currency
)
# Process exchange rates
fx_rates = normalize(
    record.fcl_listener.input.application.tbcbank.request.generalinfo.exchangerates.exchangerate
)
NBGExchangeRates = fx_rates[fx_rates["ExchangeRateType"] == "NBG"]
applicants = record.fcl_listener.input.application.tbcbank.request.applicants.applicant

def exchange_rates_calculation(node_currency, target_currency):
    node_currency = str(node_currency).upper()
    target_currency = str(target_currency).upper()
    
    if node_currency == target_currency:
        return 1.0

    filtered_rates = NBGExchangeRates[
        (NBGExchangeRates["CurrencyCodeFrom"] == node_currency)
        & (NBGExchangeRates["CurrencyCodeTo"] == target_currency)
    ]
    
    if not filtered_rates.empty:
        rate = filtered_rates["CurrencyRateSell"].iloc[0]
        multiplicity = (
            filtered_rates["ExchangeRateMultiplicity"].iloc[0]
            if "ExchangeRateMultiplicity" in filtered_rates.columns
            else 1.0
        )
        return float(rate) / float(multiplicity)
    else:
        error_msg = f"No exchange rate found from {node_currency} to {target_currency}"
        record.fcl_listener.input.application.messagelist.statuscode = "3"
        record.fcl_listener.input.application.messagelist.description += f"#{error_msg}"
        record.fcl_listener.input.application.messagelist.statusdescription = "System Error"
        return None

def convert_fields(node, fields, node_currency, output_node):
    """Convert field values and assign to output fields"""
    if node_currency is None:
        return
    
    try:
        rate_to_gel = exchange_rates_calculation(node_currency, "GEL")
        rate_in_loan = exchange_rates_calculation(node_currency, target_currency)
    except Exception:
        return

    if rate_to_gel is None or rate_in_loan is None:
        return

    for field in fields:
        field_value = getattr(node, field.lower(), None)
        if field_value is not None:
            try:
                num_value = float(field_value)
                # Assign to output fields
                setattr(output_node, f"{field}GEL", num_value * rate_to_gel)
                setattr(output_node, f"{field}InLoanCurrency", num_value * rate_in_loan)
            except (ValueError, TypeError):
                pass

# Process all APM applications for each applicant
def process_apm_applications():
    for i in range(len(applicants)):
        applicant = applicants[i]
        output_applicant = record.fcl_listener.output.application.tbcbank.request.applicants.applicant[i]
        
        try:
            apm_applications = applicant.internaldatainfo.apmapplicationhistory.apmapplication
            output_apm_applications = output_applicant.internaldatainfo.apmapplicationhistory.apmapplication
            
            if apm_applications == -1:
                continue

            for j in range(len(apm_applications)):
                apm_app = apm_applications[j]
                output_apm_app = output_apm_applications[j]
                
                node_currency = apm_app.currency
                fields = [
                    "Amount",
                    "MonthlyPaymentAmount",
                    "MonthlyAmountPayment_Variable",
                    "LongTermMonthlyPaymentAmount"
                ]
                
                # Convert and assign values to output
                convert_fields(apm_app, fields, node_currency, output_apm_app)
                
        except AttributeError:
            continue

def process_securities(loan_path):
    print(f"=== Processing Securities in {loan_path} ===")
    for i in range(len(applicants)):
        applicant = applicants[i]
        try:
            # Navigate to the loans based on the provided path
            if loan_path == "internal":
                loans = applicant.internaldatainfo.basiccredithistory.loan
            elif loan_path == "bureau":
                loans = applicant.creditbureauinfo.basiccredithistory.loan
            else:
                print(f"Invalid loan path specified: {loan_path}")
                return
                
            if loans.GetNodeKey() == -1:
                print(f"Loans node is missing for Applicant {i} in {loan_path}")
                continue
                
            for j in range(len(loans)):
                loan = loans[j]
                try:
                    securities = loan.securities.security
                    if securities.GetNodeKey() == -1:
                        print(f"Securities node is missing for Loan {j}, Applicant {i}")
                        continue
                        
                    for k in range(len(securities)):
                        security = securities[k]
                        currency = security.currency
                        
                        try:
                            rate_to_gel = exchange_rates_calculation(currency, "GEL")
                            rate_in_loan = exchange_rates_calculation(currency, target_currency)
                            
                            if security.securityvalue is not None:
                                security.securityvaluegel = security.securityvalue * rate_to_gel
                                security.securityvalueinloancurrency = security.securityvalue * rate_in_loan
                        except Exception as e:
                            print(f"Error calculating rates for Security {k} in Loan {j}, Applicant {i}: {e}")
                            
                except AttributeError as e:
                    print(f"Error processing securities for Loan {j}, Applicant {i}: {e}")
        except AttributeError as e:
            print(f"Error accessing loans for Applicant {i}: {e}")

# Process internal loans
def process_loans(loan_path):
    print(f"=== Processing Loans in {loan_path} ===")
    for i in range(len(applicants)):
        applicant = applicants[i]
        try:
            # Navigate to the loans based on the provided path
            if loan_path == "internal":
                loans = applicant.internaldatainfo.basiccredithistory.loan
            elif loan_path == "bureau":
                loans = applicant.creditbureauinfo.basiccredithistory.loan
            else:
                print(f"Invalid loan path specified: {loan_path}")
                return
                
            if loans.GetNodeKey() == -1:
                print(f"Loans node is missing for Applicant {i} in {loan_path}")
                continue
                
            for j in range(len(loans)):
                loan = loans[j]
                currency = loan.limitcurrency
                
                fields = [
                    "AccruedInsurance", "AccruedInterest", "AccruedPenalty", "PaidPenalty",
                    "BusinessMonthlyPaymentAmount", "InsurancePastDueAmount", "InsurancePaymentAmount",
                    "InterestPastDueAmount", "InterestPaymentAmount", "LimitAmount",
                    "MonthlyPaymentAmount", "MaxMonthlyPaymentAmount", "PenaltyAmount",
                    "OutstandingAmount", "PastDueAmount", "PrincipalPastDueAmount",
                    "PrincipalPaymentAmount", "RefinanceBalance", "SAAccruedPenalty", "TotalAmountToCover"
                ]
                
                convert_fields(loan, fields, currency)
                
                # Add USD conversion specifically for OutstandingAmount if needed
                if loan.outstandingamount is not None:
                    try:
                        rate_to_usd = exchange_rates_calculation(currency, "USD")
                        if rate_to_usd is not None:
                            loan.outstandingamountusd = loan.outstandingamount * rate_to_usd
                    except Exception as e:
                        print(f"Error calculating USD rate for Loan {j}, Applicant {i}: {e}")
                
        except AttributeError as e:
            print(f"Error processing loans for Applicant {i}: {e}")

# Process account pledges
def process_account_pledges():
    print("=== Processing Account Pledges ===")
    for i in range(len(applicants)):
        applicant = applicants[i]
        try:
            accounts = applicant.internaldatainfo.accounts.account
            if accounts.GetNodeKey() == -1:
                print(f"Accounts node is missing for Applicant {i}")
                continue
                
            for j in range(len(accounts)):
                account = accounts[j]
                try:
                    currency = account.accountpledge.restrictioncurrency
                    if account.accountpledge.restrictionamount is not None:
                        rate_to_gel = exchange_rates_calculation(currency, "GEL")
                        rate_in_loan = exchange_rates_calculation(currency, target_currency)
                        
                        if rate_to_gel is not None:
                            account.accountpledge.restrictionamountgel = account.accountpledge.restrictionamount * rate_to_gel
                        if rate_in_loan is not None:
                            account.accountpledge.restrictionamountinloancurrency = account.accountpledge.restrictionamount * rate_in_loan
                except AttributeError as e:
                    print(f"Error processing account pledge for Account {j}, Applicant {i}: {e}")
        except AttributeError as e:
            print(f"Error accessing accounts for Applicant {i}: {e}")

# Process deposits
def process_deposits():
    print("=== Processing Deposits ===")
    for i in range(len(applicants)):
        applicant = applicants[i]
        try:
            deposits = applicant.internaldatainfo.deposits.depositinfo
            if deposits.GetNodeKey() == -1:
                print(f"Deposits node is missing for Applicant {i}")
                continue
                
            for j in range(len(deposits)):
                deposit = deposits[j]
                currency = deposit.depositcurrency
                
                if deposit.depositamount is not None:
                    rate_to_gel = exchange_rates_calculation(currency, "GEL")
                    rate_in_loan = exchange_rates_calculation(currency, target_currency)
                    
                    if rate_to_gel is not None:
                        deposit.depositamountgel = deposit.depositamount * rate_to_gel
                    if rate_in_loan is not None:
                        deposit.depositamountinloancurrency = deposit.depositamount * rate_in_loan
        except AttributeError as e:
            print(f"Error processing deposits for Applicant {i}: {e}")

# Process transfer amounts
def process_transfer_amounts():
    print("=== Processing Transfer Amounts ===")
    for i in range(len(applicants)):
        applicant = applicants[i]
        try:
            transfers = applicant.internaldatainfo.transfertransactionhistory.transferamounts.transferamount
            if transfers.GetNodeKey() == -1:
                print(f"Transfers node is missing for Applicant {i}")
                continue
                
            for j in range(len(transfers)):
                transfer = transfers[j]
                currency = transfer.currency
                
                if transfer.amount is not None:
                    rate_to_gel = exchange_rates_calculation(currency, "GEL")
                    if rate_to_gel is not None:
                        transfer.amountgel = transfer.amount * rate_to_gel
        except AttributeError as e:
            print(f"Error processing transfers for Applicant {i}: {e}")

# Process other liabilities
def process_other_liabilities():
    print("=== Processing Other Liabilities ===")
    for i in range(len(applicants)):
        applicant = applicants[i]
        try:
            liabilities = applicant.otherliabilities.otherliability
            if liabilities.GetNodeKey() == -1:
                print(f"Other liabilities node is missing for Applicant {i}")
                continue
                
            for j in range(len(liabilities)):
                liability = liabilities[j]
                currency = liability.limitcurrency
                fields = ["LimitAmount", "OutstandingAmount", "TotalRefinanceBalanceAmount", "RefinanceBalance"]
                convert_fields(liability, fields, currency)
        except AttributeError as e:
            print(f"Error processing other liabilities for Applicant {i}: {e}")

# Process job information
def process_job_info():
    print("=== Processing Job Information ===")
    for i in range(len(applicants)):
        applicant = applicants[i]
        try:
            jobs = applicant.jobs.jobinfo
            if jobs.GetNodeKey() == -1:
                print(f"Jobs node is missing for Applicant {i}")
                continue
                
            for j in range(len(jobs)):
                job = jobs[j]
                currency = job.incomecurrency
                
                fields = ["IncomeAmount", "BonusIncomeAmount", "VerifiedIncome"]
                convert_fields(job, fields, currency)
                
                # Special handling for ModelA income
                if job.incomegel_modela is not None:
                    try:
                        rate_in_loan = exchange_rates_calculation("GEL", target_currency)
                        if rate_in_loan is not None:
                            job.incomeinloancurrency_modela = job.incomegel_modela * rate_in_loan
                    except Exception as e:
                        print(f"Error calculating ModelA rates for Job {j}, Applicant {i}: {e}")
                        
        except AttributeError as e:
            print(f"Error processing jobs for Applicant {i}: {e}")

# Process application securities
def process_application_securities():
    print("=== Processing Application Securities ===")
    try:
        securities = record.system.application.tbcbank.request.applicationdata.securities.security
        if securities.GetNodeKey() == -1:
            print("Application securities node is missing")
            return
            
        for i in range(len(securities)):
            security = securities[i]
            currency = security.currency
            
            if security.securityvalue is not None:
                rate_to_gel = exchange_rates_calculation(currency, "GEL")
                rate_in_loan = exchange_rates_calculation(currency, target_currency)
                
                if rate_to_gel is not None:
                    security.securityvaluegel = security.securityvalue * rate_to_gel
                if rate_in_loan is not None:
                    security.securityvalueinloancurrency = security.securityvalue * rate_in_loan
    except AttributeError as e:
        print(f"Error processing application securities: {e}")

# Process collateral liabilities
def process_collateral_liabilities():
    print("=== Processing Collateral Liabilities ===")
    try:
        liabilities = record.system.application.tbcbank.request.applicationdata.collateralliabilities.collateralliability
        if liabilities.GetNodeKey() == -1:
            print("Collateral liabilities node is missing")
            return
            
        for i in range(len(liabilities)):
            liability = liabilities[i]
            currency = liability.currency
            
            if liability.limitamount is not None:
                rate_in_loan = exchange_rates_calculation(currency, target_currency)
                if rate_in_loan is not None:
                    liability.limitamountinloancurrency = liability.limitamount * rate_in_loan
    except AttributeError as e:
        print(f"Error processing collateral liabilities: {e}")

process_apm_applications()
process_securities("internal")  
process_securities("bureau")   
process_loans("internal")       
process_loans("bureau")         
process_account_pledges()
process_deposits()
process_transfer_amounts()
process_other_liabilities()
process_job_info()
process_application_securities()
process_collateral_liabilities()