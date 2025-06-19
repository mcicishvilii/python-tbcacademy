# Extract Data
target_currency = record.system.application.tbcbank.request.applicationdata.currency
fx_rates = normalize(
    record.system.application.tbcbank.request.generalinfo.exchangerates.exchangerate
)
NBGExchangeRates = fx_rates[fx_rates["ExchangeRateType"] == "NBG"]
applicants = record.system.application.tbcbank.request.applicants.applicant


try:
    rate_to_gel = uf_currency_conversion_logic(
        fx_rates, target_currency, "GEL", NBGExchangeRates
    )
except ValueError as e:
    print(f"Error calculating exchange rates for loan: {e}")
    rate_to_gel = None

for i in range(len(applicants)):
    print(f"applicant {i}")
    applicant = applicants[i]
    try:
        try:
            apm_applications = (
                applicant.internaldatainfo.apmapplicationhistory.apmapplication
            )
            if apm_applications.GetNodeKey() == -1:
                print(f"APMApplications node missing for applicant {i}")
            else:
                for l in range(len(apm_applications)):
                    apm_app = apm_applications[l]
                    try:
                        node_currency = apm_app.currency
                        print(f"APMApplication {l} currency: {node_currency}")

                        # Calculate exchange rates
                        rate_in_loan = uf_currency_conversion_logic(
                            fx_rates, node_currency, target_currency, NBGExchangeRates
                        )
                        rate_to_gel = uf_currency_conversion_logic(
                            fx_rates, node_currency, "GEL", NBGExchangeRates
                        )
                        if None in (rate_to_gel, rate_in_loan):
                            print(f"Skipping APMApplication {l} - missing FX rates")
                            continue

                        if apm_app.amount is not None:
                            apm_app.amountgel = float(apm_app.amount) * rate_to_gel
                            apm_app.amountinloancurrency = (float(apm_app.amount) * rate_in_loan)
                        
                        if apm_app.monthlypaymentamount is not None:
                            apm_app.monthlypaymentamountgel = float(apm_app.monthlypaymentamount) * rate_to_gel
                            apm_app.monthlypaymentamountinloancurrency = (float(apm_app.monthlypaymentamount) * rate_in_loan)
                        
                        if apm_app.monthlyamountpayment_variable is not None:
                            apm_app.monthlyamountpayment_variablegel = float(apm_app.monthlyamountpayment_variable) * rate_to_gel
                            apm_app.monthlyamountpayment_variableinloancurrency = (float(apm_app.monthlyamountpayment_variable) * rate_in_loan)
                        
                        if apm_app.longtermmonthlypaymentamount is not None:
                            apm_app.longtermmonthlypaymentamountgel = float(apm_app.longtermmonthlypaymentamount) * rate_to_gel
                            apm_app.longtermmonthlypaymentamountinloancurrency = (float(apm_app.longtermmonthlypaymentamount) * rate_in_loan)    
                    except ValueError as e:
                        print(f"FX error in APMApplication {l}: {e}")
                    except AttributeError as e:
                        print(f"Missing attribute in APMApplication {l}: {e}")

        except AttributeError as e:
            print(f"Error accessing APMApplications: {e}")

    except AttributeError as e:
        logger.error(f"Error accessing loans for applicant {i}: {e}")
        continue  # Continue with next applicant
