# Extract Data
target_currency = record.system.application.tbcbank.request.applicationdata.currency
fx_rates = normalize(record.system.application.tbcbank.request.generalinfo.exchangerates.exchangerate)
NBGExchangeRates = fx_rates[fx_rates["ExchangeRateType"] == "NBG"]
min_data = record.system.application.tbcbank.request.applicationdata.applicationmindata

try:
    rate_to_gel = uf_currency_conversion_logic(fx_rates, target_currency, "GEL", NBGExchangeRates)
except ValueError as e:
    print(f"Error calculating exchange rates for min_data: {e}")
    rate_to_gel = None

try:
    rate_in_min_data = uf_currency_conversion_logic(fx_rates, target_currency, target_currency, NBGExchangeRates)
    rate_to_gel = uf_currency_conversion_logic(fx_rates, target_currency, "GEL", NBGExchangeRates)
except ValueError as e:
    pass
    # log an error

if min_data.requestedamount is not None:    
    min_data.requestedamountgel = float(min_data.requestedamount) * rate_to_gel
    #min_data.requestedamountinloancurrency = float(min_data.requestedamount) * rate_in_min_data

#  RequestedRepayment

if min_data.requestedrepayment is not None:
    min_data.requestedrepaymentgel = float(min_data.requestedrepayment) * rate_to_gel
    #min_data.requestedrepaymentinloancurrency = float(min_data.requestedrepayment) * rate_in_min_data
