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
        try:
            accounts = applicant.internaldatainfo.accounts.account
            if accounts.GetNodeKey() == -1:
                print(f"Accounts node missing for applicant {i}")
            else:
                for m in range(len(accounts)):
                    account = accounts[m]
                    try:
                        # Access AccountPledge node directly (no loop needed)
                        pledge = account.accountpledge
                        if pledge.GetNodeKey() == -1:
                            print(f"AccountPledge missing for account {m}")
                            continue
                        
                        # Get pledge currency
                        node_currency = pledge.restrictioncurrency
                        print(f"AccountPledge currency for account {m}: {node_currency}")
                        
                        # Calculate conversion rates
                        rate_in_loan = uf_currency_conversion_logic(fx_rates, node_currency, target_currency, NBGExchangeRates)
                        rate_to_gel = uf_currency_conversion_logic(fx_rates, node_currency, "GEL", NBGExchangeRates)
                        
                        if None in (rate_to_gel, rate_in_loan):
                            print(f"Skipping AccountPledge for account {m} - missing FX rates")
                            continue
                        
                        # Process RestrictionAmount
                        if pledge.restrictionamount is not None:
                            try:
                                restriction_amount = float(pledge.restrictionamount)
                                pledge.restrictionamountgel = restriction_amount * rate_to_gel
                                pledge.restrictionamountinloancurrency = restriction_amount * rate_in_loan
                            except ValueError:
                                print(f"Invalid restrictionamount for account {m}: {pledge.restrictionamount}")
                                
                    except AttributeError as e:
                        print(f"Error accessing AccountPledge for account {m}: {e}")
                        
        except AttributeError as e:
            print(f"Error accessing Accounts: {e}")
        
    except AttributeError as e:
        logger.error(f"Error accessing loans for applicant {i}: {e}")
        continue  # Continue with next applicant