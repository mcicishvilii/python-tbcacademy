# def get_exchange_rate(rates, from_curr, to_curr):
#     if from_curr == to_curr:
#         return 1.0
#     for rate in rates:
#         if (
#             rate["CurrencyCodeFrom"] == from_curr
#             and rate["CurrencyCodeTo"] == to_curr
#             and rate["ExchangeRateType"] == "NBG"
#         ):
#             multiplicity = float(rate["ExchangeRateMultiplicity"])
#             rate_value = float(rate["CurrencyRateSell"])
#             return rate_value / multiplicity
#     return None

# def convert_currency_values(record, logger):
#     try:
#         # Get exchange rates
#         exchange_rates = record.system.exchangerates.exchangerate
        
#         # Get target currency (loan currency)
#         target_currency = record.system.application.tbcbank.request.applicationdata.currency
#         logger.info(f"Target currency: {target_currency}")
        
#         # Get applicants
#         applicants = record.system.application.tbcbank.request.applicants.applicant
        
#         for appl in range(len(applicants)):
#             applicant = applicants[appl]
#             logger.info(f"Processing applicant: {appl}")
            
#             try:
#                 # Process InternalDataInfo loans
#                 loans = applicant.internaldatainfo.basiccredithistory.loan
#                 if loans.GetNodeKey() == -1:
#                     logger.info(f"No loans found for applicant {appl} in InternalDataInfo")
#                 else:
#                     for loan in loans:
#                         currency = loan.limitcurrency
#                         convert_fields(loan, [
#                             "AccruedInsurance", "AccruedInterest", "AccruedPenalty", "PaidPenalty",
#                             "BusinessMonthlyPaymentAmount", "InsurancePastDueAmount", "InsurancePaymentAmount",
#                             "InterestPastDueAmount", "InterestPaymentAmount", "LimitAmount", "MonthlyPaymentAmount",
#                             "MaxMonthlyPaymentAmount", "PenaltyAmount", "OutstandingAmount", "PastDueAmount",
#                             "PrincipalPastDueAmount", "PrincipalPaymentAmount", "RefinanceBalance",
#                             "SAAccruedPenalty", "TotalAmountToCover"
#                         ], currency, exchange_rates, target_currency, logger)
                        
#                         # Process securities
#                         if hasattr(loan, 'securities') and hasattr(loan.securities, 'security'):
#                             security = loan.securities.security
#                             sec_currency = security.currency
#                             convert_fields(security, ["SecurityValue"], sec_currency, exchange_rates, target_currency, logger)
                
#                 # Process APM Applications
#                 if hasattr(applicant.internaldatainfo, 'apmapplicationhistory'):
#                     apm_apps = applicant.internaldatainfo.apmapplicationhistory.apmapplication
#                     if apm_apps.GetNodeKey() != -1:
#                         currency = apm_apps.currency
#                         convert_fields(apm_apps, [
#                             "Amount", "MonthlyPaymentAmount", "MonthlyAmountPayment_Variable",
#                             "LongTermMonthlyPaymentAmount"
#                         ], currency, exchange_rates, target_currency, logger)
                
#                 # Process other sections similarly...
#                 # (Add similar blocks for Accounts, Deposits, TransferTransactionHistory, etc.)
                
#             except Exception as e:
#                 logger.error(f"Error processing applicant {appl}: {str(e)}")
#                 continue
                
#     except Exception as e:
#         logger.error(f"Error in currency conversion: {str(e)}")
#         raise

# def convert_fields(node, fields, original_currency, exchange_rates, target_currency, logger):
#     for field in fields:
#         if hasattr(node, field):
#             value = getattr(node, field)
#             if value is None:
#                 continue
            
#             try:
#                 numeric_value = float(value)
#             except (ValueError, TypeError):
#                 logger.warning(f"Could not convert {field} value '{value}' to number")
#                 continue
            
#             # Convert to GEL
#             rate_to_gel = get_exchange_rate(exchange_rates, original_currency, "GEL")
#             if rate_to_gel is not None:
#                 setattr(node, f"{field}GEL", round(numeric_value * rate_to_gel, 2))
#             else:
#                 logger.warning(f"No rate from {original_currency} to GEL for {field}")
            
#             # Convert to target currency
#             if original_currency != target_currency:
#                 rate_to_target = get_exchange_rate(exchange_rates, original_currency, target_currency)
#                 if rate_to_target is not None:
#                     setattr(node, f"{field}InLoanCurrency", round(numeric_value * rate_to_target, 2))
#                 else:
#                     logger.warning(f"No rate from {original_currency} to {target_currency} for {field}")