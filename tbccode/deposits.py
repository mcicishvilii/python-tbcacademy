# Extract Data
target_currency = record.system.application.tbcbank.request.applicationdata.currency
fx_rates = normalize(record.system.application.tbcbank.request.generalinfo.exchangerates.exchangerate)
print(f"paxo {fx_rates}")
NBGExchangeRates = fx_rates[fx_rates["ExchangeRateType"] == "NBG"]
print(f"vaxo {NBGExchangeRates}")
applicants = record.system.application.tbcbank.request.applicants.applicant


try:
    print("gelaa")
    rate_to_gel = uf_currency_conversion_logic(fx_rates, target_currency, "GEL", NBGExchangeRates)
except ValueError as e:
    print(f"Error calculating exchange rates for loan: {e}")
    rate_to_gel = None

for i in range(len(applicants)):
    print(f"applicant {i}")
    applicant = applicants[i]
    try:
        # Inside the applicant loop (e.g., after processing loans)
        try:
            deposits = applicant.internaldatainfo.deposits.depositinfo
            if deposits.GetNodeKey() == -1:
                print(f"Deposits node missing for applicant {i}")
            else:
                for m in range(len(deposits)):
                    deposit = deposits[m]
                    try:
                        # Get deposit currency
                        node_currency = deposit.depositcurrency
                        print(f"Deposit {m} currency: {node_currency}")
                        
                        # Calculate conversion rates using the provided function
                        rate_in_loan = uf_currency_conversion_logic(fx_rates, node_currency, target_currency, NBGExchangeRates)
                        rate_to_gel = uf_currency_conversion_logic(fx_rates, node_currency, "GEL", NBGExchangeRates)
                        
                        # Skip if any exchange rate is missing
                        if None in (rate_to_gel, rate_in_loan):
                            print(f"Skipping deposit {m} - missing FX rates")
                            continue
                        
                        # Convert DepositAmount if it exists
                        if deposit.depositamount is not None:
                            print(f"Converting DepositAmount for deposit {m}")
                            deposit.depositamountgel = float(deposit.depositamount) * rate_to_gel
                            deposit.depositamountinloancurrency = float(deposit.depositamount) * rate_in_loan
                        
                    except ValueError as e:
                        print(f"FX error in deposit {m}: {e}")
                    except AttributeError as e:
                        print(f"Missing attribute in deposit {m}: {e}")
        except AttributeError as e:
            print(f"Error accessing Deposits: {e}")
                
    except AttributeError as e:
        logger.error(f"Error accessing loans for applicant {i}: {e}")
        continue  # Continue with next applicant