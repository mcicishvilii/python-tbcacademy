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
                        node_currency = loan.limitcurrency
                        if not node_currency:
                            print(f"Skipping loan {j} - missing LimitCurrency")
                            continue
                        
                        print(f"Loan {j} currency: {node_currency}")
                        
                        # Calculate conversion rates
                        rate_in_loan = uf_currency_conversion_logic(fx_rates, node_currency, target_currency, NBGExchangeRates)
                        rate_to_gel = uf_currency_conversion_logic(fx_rates, node_currency, "GEL", NBGExchangeRates)
                        
                        # Skip if exchange rates are unavailable
                        if None in (rate_to_gel, rate_in_loan):
                            print(f"Skipping loan {j} - missing FX rates")
                            continue
                        
                        # Fields to convert
                        fields_to_convert = [
                            "accruedpenalty",
                            "limitamount",
                            "monthlypaymentamount",
                            "maxmonthlypaymentamount",
                            "outstandingamount",
                            "pastdueamount",
                            "principalpastdueamount",
                            "refinancebalance"
                        ]
                        
                        # Convert each field if present and not None
                        for field in fields_to_convert:
                            if hasattr(loan, field) and getattr(loan, field) is not None:
                                try:
                                    amount = float(getattr(loan, field))
                                    setattr(loan, field + "gel", amount * rate_to_gel)
                                    setattr(loan, field + "inloancurrency", amount * rate_in_loan)
                                    print(f"Converted {field} for loan {j}")
                                except ValueError:
                                    print(f"Invalid value for {field} in loan {j}: {getattr(loan, field)}")
                        
                    except AttributeError as e:
                        print(f"Error accessing loan {j} data: {e}")
                    except ValueError as e:
                        print(f"Value error in loan {j}: {e}")
        except AttributeError as e:
            print(f"Error accessing Loans for applicant {i}: {e}")
                        
    except AttributeError as e:
        print(f"Error processing applicant {i}: {e}")