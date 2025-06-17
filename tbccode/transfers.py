# Extract Data
target_currency = record.system.application.tbcbank.request.applicationdata.currency
fx_rates = normalize(record.system.application.tbcbank.request.generalinfo.exchangerates.exchangerate)
NBGExchangeRates = fx_rates[fx_rates["ExchangeRateType"] == "NBG"]
applicants = record.system.application.tbcbank.request.applicants.applicant

for i in range(len(applicants)):
    print(f"applicant {i}")
    applicant = applicants[i]
    try:
        try:
            loans = applicant.creditbureauinfo.basiccredithistory.loan
            if loans.GetNodeKey() == -1:
                print(f"Loans node missing for applicant {i}")
            else:
                for j in range(len(loans)):
                    loan = loans[j]
                    try:
                        securities = loan.securities.security
                        if securities.GetNodeKey() == -1:
                            print(f"Securities node missing for loan {j}")
                        else:
                            for k in range(len(securities)):
                                security = securities[k]
                                try:
                                    node_currency = security.currency
                                    if not node_currency:
                                        print(f"Skipping security {k} - missing Currency")
                                        continue
                                    
                                    print(f"Security {k} currency: {node_currency}")
                                    
                                    rate_in_loan = uf_currency_conversion_logic(fx_rates, node_currency, target_currency, NBGExchangeRates)
                                    rate_to_gel = uf_currency_conversion_logic(fx_rates, node_currency, "GEL", NBGExchangeRates)
                                    
                                    if None in (rate_to_gel, rate_in_loan):
                                        print(f"Skipping security {k} - missing FX rates")
                                        continue
                                    
                                    if security.securityvalue is not None:
                                        try:
                                            amount = float(security.securityvalue)
                                            security.securityvaluegel = amount * rate_to_gel
                                            security.securityvalueinloancurrency = amount * rate_in_loan
                                            print(f"Converted SecurityValue for security {k}")
                                        except ValueError:
                                            print(f"Invalid SecurityValue for security {k}: {security.securityvalue}")
                                    
                                except AttributeError as e:
                                    print(f"Error accessing security {k} data: {e}")
                    except AttributeError as e:
                        print(f"Error accessing Securities for loan {j}: {e}")
        except AttributeError as e:
            print(f"Error accessing Loans for applicant {i}: {e}")
                        
    except AttributeError as e:
        print(f"Error processing applicant {i}: {e}")