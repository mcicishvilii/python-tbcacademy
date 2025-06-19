# Extract Data
target_currency = record.system.application.tbcbank.request.applicationdata.currency
fx_rates = normalize(record.system.application.tbcbank.request.generalinfo.exchangerates.exchangerate)
NBGExchangeRates = fx_rates[fx_rates["ExchangeRateType"] == "NBG"]
applicants = record.system.application.tbcbank.request.applicants.applicant

# FX Rates Calculation Function
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
        return filtered_rates["CurrencyRateSell"].iloc[0].item()
    else:
        error_msg = f"No exchange rate found from {node_currency} to {target_currency}"
        print(error_msg)
        record.fcl_listener.output.application.messagelist.statuscode = "3"
        record.fcl_listener.output.application.messagelist.statusdescription = "System Error"
        return None

try:
    print("gelaa")
    rate_to_gel = ExchangeRates_Calculation(fx_rates, target_currency, "GEL", NBGExchangeRates)
except ValueError as e:
    print(f"Error calculating exchange rates for loan: {e}")
    rate_to_gel = None

# Convert the loan amounts to GEL
if rate_to_gel == None:
    return
if record.system.application.tbcbank.request.applicationdata.applicationmindata.requestedamount is not None:
    record.fcl_listener.output.application.tbcbank.request.applicationdata.applicationmindata.requestedamountgel = (record.system.application.tbcbank.request.applicationdata.applicationmindata.requestedamount * rate_to_gel)
if record.system.application.tbcbank.request.applicationdata.applicationmindata.requestedrepayment is not None:
    record.fcl_listener.output.application.tbcbank.request.applicationdata.applicationmindata.requestedrepaymentgel = (record.system.application.tbcbank.request.applicationdata.applicationmindata.requestedrepayment * rate_to_gel)

# Get the list of applicants
applicants = record.system.application.tbcbank.request.applicants.applicant
logger.info(f"Number of Applicants: {len(applicants)}")

# Process by applicants, loans
for i in range(len(applicants)):
    print(f"applicant {i}")
    applicant = applicants[i]
    try:
        loans = applicant.internaldatainfo.basiccredithistory.loan
        if loans.GetNodeKey() == -1:
            print("Node is missing or empty")
            logger.error("loans node is missing or empty - does not meet basic requirements.")
        else:
            for j in range(len(loans)):
                loan = loans[j]
                try:
                    # Get the currency for this specific loan (LimitCurrency)
                    node_currency = record.system.application.tbcbank.request.applicants.applicant[i].internaldatainfo.basiccredithistory.loan[j].limitcurrency
                    print(f"gelo {node_currency}")
                    
                    # Calculate exchange rates from the loan's currency
                    rate_in_loan = ExchangeRates_Calculation(fx_rates, node_currency, target_currency, NBGExchangeRates)
                    rate_to_gel = ExchangeRates_Calculation(fx_rates, node_currency, "GEL", NBGExchangeRates)
                    
                    print(f"Rate to loan currency: {rate_in_loan}, Rate to GEL: {rate_to_gel}")
                except ValueError as e:
                    print(f"Error calculating exchange rates for loan: {e}")
                    continue  # Skip this loan if exchange rates can't be calculated
                
                # Skip if any rate is None
                if rate_to_gel is None or rate_in_loan is None:
                    print(f"Skipping loan {j} for applicant {i} - missing exchange rates")
                    continue
                
                # AccruedInsurance
                if loan.accruedinsurance is not None:
                    print("Converting AccruedInsurance")
                    loan.accruedinsurancegel = float(loan.accruedinsurance) * rate_to_gel
                    loan.accruedinsuranceinloancurrency = float(loan.accruedinsurance) * rate_in_loan

                # AccruedInterest
                if loan.accruedinterest is not None:
                    print("Converting AccruedInterest")
                    loan.accruedinterestgel = float(loan.accruedinterest) * rate_to_gel
                    loan.accruedinterestinloancurrency = float(loan.accruedinterest) * rate_in_loan

                # AccruedPenalty
                if loan.accruedpenalty is not None:
                    print("Converting AccruedPenalty")
                    loan.accruedpenaltygel = float(loan.accruedpenalty) * rate_to_gel
                    loan.accruedpenaltyinloancurrency = float(loan.accruedpenalty) * rate_in_loan

                # PaidPenalty
                if loan.paidpenalty is not None:
                    print("Converting PaidPenalty")
                    loan.paidpenaltygel = float(loan.paidpenalty) * rate_to_gel
                    loan.paidpenaltyinloancurrency = float(loan.paidpenalty) * rate_in_loan

                # BusinessMonthlyPaymentAmount
                if loan.businessmonthlypaymentamount is not None:
                    print("Converting BusinessMonthlyPaymentAmount")
                    loan.businessmonthlypaymentamountgel = float(loan.businessmonthlypaymentamount) * rate_to_gel
                    loan.businessmonthlypaymentamountinloancurrency = float(loan.businessmonthlypaymentamount) * rate_in_loan

                # InsurancePastDueAmount
                if loan.insurancepastdueamount is not None:
                    print("Converting InsurancePastDueAmount")
                    loan.insurancepastdueamountgel = float(loan.insurancepastdueamount) * rate_to_gel
                    loan.insurancepastdueamountinloancurrency = float(loan.insurancepastdueamount) * rate_in_loan

                # InsurancePaymentAmount
                if loan.insurancepaymentamount is not None:
                    print("Converting InsurancePaymentAmount")
                    loan.insurancepaymentamountgel = float(loan.insurancepaymentamount) * rate_to_gel
                    loan.insurancepaymentamountinloancurrency = float(loan.insurancepaymentamount) * rate_in_loan

                # InterestPastDueAmount
                if loan.interestpastdueamount is not None:
                    print("Converting InterestPastDueAmount")
                    loan.interestpastdueamountgel = float(loan.interestpastdueamount) * rate_to_gel
                    loan.interestpastdueamountinloancurrency = float(loan.interestpastdueamount) * rate_in_loan

                # InterestPaymentAmount
                if loan.interestpaymentamount is not None:
                    print("Converting InterestPaymentAmount")
                    loan.interestpaymentamountgel = float(loan.interestpaymentamount) * rate_to_gel
                    loan.interestpaymentamountinloancurrency = float(loan.interestpaymentamount) * rate_in_loan

                # LimitAmount
                if loan.limitamount is not None:
                    print("Converting LimitAmount")
                    loan.limitamountgel = float(loan.limitamount) * rate_to_gel
                    loan.limitamountinloancurrency = float(loan.limitamount) * rate_in_loan

                # MonthlyPaymentAmount
                if loan.monthlypaymentamount is not None:
                    print("Converting MonthlyPaymentAmount")
                    loan.monthlypaymentamountgel = float(loan.monthlypaymentamount) * rate_to_gel
                    loan.monthlypaymentamountinloancurrency = float(loan.monthlypaymentamount) * rate_in_loan

                # MaxMonthlyPaymentAmount
                if loan.maxmonthlypaymentamount is not None:
                    print("Converting MaxMonthlyPaymentAmount")
                    loan.maxmonthlypaymentamountgel = float(loan.maxmonthlypaymentamount) * rate_to_gel
                    loan.maxmonthlypaymentamountinloancurrency = float(loan.maxmonthlypaymentamount) * rate_in_loan

                # PenaltyAmount
                if loan.penaltyamount is not None:
                    print("Converting PenaltyAmount")
                    loan.penaltyamountgel = float(loan.penaltyamount) * rate_to_gel
                    loan.penaltyamounntinloancurrency = float(loan.penaltyamount) * rate_in_loan

                # OutstandingAmount
                if loan.outstandingamount is not None:
                    print("Converting OutstandingAmount")
                    loan.outstandingamountgel = float(loan.outstandingamount) * rate_to_gel
                    loan.outstandingamountinloancurrency = float(loan.outstandingamount) * rate_in_loan

                # PastDueAmount
                if loan.pastdueamount is not None:
                    print("Converting PastDueAmount")
                    loan.pastdueamountgel = float(loan.pastdueamount) * rate_to_gel
                    loan.pastdueamountinloancurrency = float(loan.pastdueamount) * rate_in_loan

                # PrincipalPastDueAmount
                if loan.principalpastdueamount is not None:
                    print("Converting PrincipalPastDueAmount")
                    loan.principalpastdueamountgel = float(loan.principalpastdueamount) * rate_to_gel
                    loan.principalpastdueamountinloancurrency = float(loan.principalpastdueamount) * rate_in_loan

                # PrincipalPaymentAmount
                if loan.principalpaymentamount is not None:
                    print("Converting PrincipalPaymentAmount")
                    loan.principalpaymentamountgel = float(loan.principalpaymentamount) * rate_to_gel
                    loan.principalpaymentamountinloancurrency = float(loan.principalpaymentamount) * rate_in_loan

                # RefinanceBalance
                if loan.refinancebalance is not None:
                    print("Converting RefinanceBalance")
                    loan.refinancebalancegel = float(loan.refinancebalance) * rate_to_gel
                    loan.refinancebalanceinloancurrency = float(loan.refinancebalance) * rate_in_loan

                # SAAccruedPenalty
                if loan.saaccruedpenalty is not None:
                    print("Converting SAAccruedPenalty")
                    loan.saaccruedpenaltygel = float(loan.saaccruedpenalty) * rate_to_gel
                    loan.saaccruedpenaltyinloancurrency = float(loan.saaccruedpenalty) * rate_in_loan

                # TotalAmountToCover
                if loan.totalamounttocover is not None:
                    print("Converting TotalAmountToCover")
                    loan.totalamounttocovergel = float(loan.totalamounttocover) * rate_to_gel
                    loan.totalamounttocoverinloancurrency = float(loan.totalamounttocover) * rate_in_loan

    except AttributeError as e:
        logger.error(f"Error accessing loans for applicant {i}: {e}")
        continue  # Continue with next applicant