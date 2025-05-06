import json
import pandas as pd


class DotDict(dict):
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            # Return an empty DotDict for missing attributes to avoid AttributeError
            self[attr] = DotDict()
            return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value
        
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            # Return an empty DotDict for missing keys to avoid KeyError
            self[key] = DotDict()
            return self[key]


class FCLRecord:
    def __init__(self, json_data):
        # Ensure all nested structures are properly initialized as DotDict
        self.fcl_listener = DotDict({
            "input": DotDict({
                "application": self._convert_to_dotdict(json_data.get("Application", {}))
            })
        })
        
        # Initialize messagelist if not present
        if "messagelist" not in self.fcl_listener.input.application:
            self.fcl_listener.input.application.messagelist = DotDict({
                "statuscode": "0",
                "description": "",
                "statusdescription": ""
            })

    def _convert_to_dotdict(self, data):
        """Recursively convert dictionaries to DotDict"""
        if isinstance(data, dict):
            result = DotDict()
            for key, value in data.items():
                result[key] = self._convert_to_dotdict(value)
            return result
        elif isinstance(data, list):
            return [self._convert_to_dotdict(item) for item in data]
        else:
            return data

def normalize(exchange_rates):
    if isinstance(exchange_rates, dict):
        exchange_rates = [exchange_rates]
    cleaned = [dict(rate) for rate in exchange_rates]
    return pd.DataFrame(cleaned)


# Load your JSON file
with open("fcl_input.txt", "r") as f:
    json_data = json.load(f)

# Create the record object
record = FCLRecord(json_data)

# Example usage:
try:
    fx_rates = normalize(
        record.fcl_listener.input.application.TBCBank.Request.GeneralInfo.ExchangeRates.ExchangeRate
    )
    NBGExchangeRates = fx_rates[fx_rates["ExchangeRateType"] == "NBG"]
    print("NBG Exchange Rates:")
    print(NBGExchangeRates.head())
except Exception as e:
    print(f"Error accessing exchange rates: {e}")