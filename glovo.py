# Helper Functions
from statistics import median


# Safe float conversion function
def safe_float_conversion(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0

# Retrieve the list of applicants
try:
    applicants = record.system.application.tbcbank.request.applicants.applicant
except AttributeError as e:
    print("Applicants node not found in TBCBank - using an empty list")
    applicants = []

print("Start: TBC Other Transactions Median")

for i in range(len(applicants)):
    applicant = applicants[i]
    print(f"Processing Applicant {i+1}")

    # Retrieve SelfEmployedOtherTransactionHistory.OtherIncomeAmounts (multiple node)
    try:
        other_income_amounts = applicant.internaldatainfo.selfemployedothertransactionhistory.otherincomeamounts.otherincomeamount
        if other_income_amounts.GetNodeKey() == -1:
            print("Node is missing or empty")
        else:
            # Group transactions by periods
            grouped_periods = {}
            for k in range(len(other_income_amounts)):
                income = other_income_amounts[k]
                try:
                    period = getattr(income, 'period', None)
                    company = getattr(income, 'company', "")
                    amount = safe_float_conversion(getattr(income, 'amount', 0))
                    print(f"Period: {period}, Company: {company}, Amount: {amount}")
        
                    if period not in grouped_periods:
                        grouped_periods[period] = {"amount": 0.0, "companies": set()}
        
                    grouped_periods[period]["amount"] += amount
                    grouped_periods[period]["companies"].add(company)
                except Exception as e:
                    print(f"Error processing OtherIncomeAmount[{k}] for Applicant {i+1}: {e}")
    except AttributeError:
        print(f"Error: 'selfemployedothertransactionhistory.otherincomeamounts' node not found for Applicant {i+1}")
        continue
    # Save grouped results to OtherIncomeAmounts
    try:
        dm_other_income_amounts = []
        for period, data in grouped_periods.items():
            record.system.application.tbcbank.request.applicants.applicant[i].internaldatainfo.selfemployedothertransactionhistory.dmotherincomeamounts.otherincomeamount[period].amount=amount
            record.system.application.tbcbank.request.applicants.applicant[i].internaldatainfo.selfemployedothertransactionhistory.dmotherincomeamounts.otherincomeamount[period].company=company
            record.system.application.tbcbank.request.applicants.applicant[i].internaldatainfo.selfemployedothertransactionhistory.dmotherincomeamounts.otherincomeamount[period].period=period
    except AttributeError as e:
        print(f"Error saving grouped results for Applicant {i+1}: {e}")
        continue

    print("Grouped Periods:", grouped_periods)
    # Extract amounts by periods (Period_0 to Period_6)
    periods_data = {f"Period_{j}": 0.0 for j in range(7)}
    for entry in dm_other_income_amounts:
        period_key = entry.get("period")
        if period_key in periods_data:
            periods_data[period_key] = entry.get("amount", 0.0)
    print("Periods Data:", periods_data)

# --- Verification of Period Counts (New Section) ---
    six_month_period_count = 0
    for j in range(7): # Period_0 to Period_6 (6 months + current)
        period_key = f"Period_{j}"
        if period_key in periods_data and periods_data[period_key] >= 100:
            six_month_period_count += 1

    four_month_period_count = 0
    for j in range(5): # Period_0 to Period_4 (4 months + current)
        period_key = f"Period_{j}"
        if period_key in periods_data and periods_data[period_key] >= 100:
            four_month_period_count += 1

    is_period_0_or_1_valid = False # Flag for mandatory Period_0 or Period_1 >= 100
    if ("Period_0" in periods_data and periods_data["Period_0"] >= 100) or \
       ("Period_1" in periods_data and periods_data["Period_1"] >= 100):
        is_period_0_or_1_valid = True

    print(f"6-Month Period Count (>=100): {six_month_period_count}") # Debug print
    print(f"4-Month Period Count (>=100): {four_month_period_count}") # Debug print
    print(f"Period_0 or Period_1 Valid (>=100): {is_period_0_or_1_valid}") # Debug print

    periodicity = 0 # Default periodicity, will be updated based on conditions
    is_for_median_flags = [False] * len(periods_data)
    median_values = [] # Initialize median_values here as well

    # --- Median Calculation Logic (Existing Code - Adjusted with Count Checks) ---
    if six_month_period_count >= 5 and is_period_0_or_1_valid: # Check 6-month count AND mandatory period condition
        if ( # Original 6-month condition 1
            periods_data["Period_1"] >= 100 and periods_data["Period_6"] >= 100 and
            (periods_data["Period_0"] == 0 or periods_data["Period_0"] <= periods_data["Period_6"])
        ):
            median_values = [periods_data[f"Period_{j}"] for j in range(1, 7)]
            periodicity = 6
            is_for_median_flags[1:7] = [True] * 6

        elif ( # Original 6-month condition 2
            (periods_data["Period_6"] == 0 or periods_data["Period_6"] < 100) and
            periods_data["Period_0"] >= 100
        ):
            median_values = [periods_data[f"Period_{j}"] for j in range(6)]
            periodicity = 6
            is_for_median_flags[0:6] = [True] * 6

        elif ( # Original 6-month condition 3
            (periods_data["Period_1"] == 0 or periods_data["Period_1"] < 100) and
            periods_data["Period_0"] >= 100
        ):
            median_values = [periods_data[f"Period_{j}"] for j in [0, 2, 3, 4, 5, 6]]
            periodicity = 6
            is_for_median_flags[0] = True
            is_for_median_flags[2:7] = [True] * 5

        elif ( # Original 6-month condition 4
            periods_data["Period_1"] >= 100 and periods_data["Period_0"] >= 100 and
            periods_data["Period_6"] >= 100 and periods_data["Period_0"] > periods_data["Period_6"]
        ):
            median_values = [periods_data[f"Period_{j}"] for j in range(6)]
            periodicity = 6
            is_for_median_flags[0:6] = [True] * 6

        # --- 4-Month Median Calculation (moved into 'else if') ---
        elif four_month_period_count >= 3 and is_period_0_or_1_valid: # Check 4-month count AND mandatory period condition
            if ( # Original 4-month condition 1
                periods_data["Period_1"] >= 100 and periods_data["Period_4"] >= 100 and
                (periods_data["Period_0"] == 0 or periods_data["Period_0"] <= periods_data["Period_4"])
            ):
                median_values = [periods_data[f"Period_{j}"] for j in range(1, 5)]
                periodicity = 4
                is_for_median_flags[1:5] = [True] * 4

            elif ( # Original 4-month condition 2
                (periods_data["Period_4"] == 0 or periods_data["Period_4"] < 100) and
                periods_data["Period_0"] >= 100
            ):
                median_values = [periods_data[f"Period_{j}"] for j in range(4)]
                periodicity = 4
                is_for_median_flags[0:4] = [True] * 4

            elif ( # Original 4-month condition 3
                (periods_data["Period_1"] == 0 or periods_data["Period_1"] < 100) and
                periods_data["Period_0"] >= 100
            ):
                median_values = [periods_data[f"Period_{j}"] for j in [0, 2, 3, 4]]
                periodicity = 4
                is_for_median_flags[0] = True
                is_for_median_flags[2:5] = [True] * 3

            elif ( # Original 4-month condition 4
                periods_data["Period_1"] >= 100 and periods_data["Period_0"] >= 100 and
                periods_data["Period_4"] >= 100 and periods_data["Period_0"] > periods_data["Period_4"]
            ):
                median_values = [periods_data[f"Period_{j}"] for j in range(4)]
                periodicity = 4
                is_for_median_flags[0:4] = [True] * 4
        else: # Default case: no valid periods found (moved into the 'else' for the count check)
            median_values = []
            periodicity = None

    # Calculate the median if applicable
    calculated_median = None
    if len(median_values) > max(3, (periodicity or -1) - 1):
        calculated_median = median(median_values)

    print("Calculated Median:", calculated_median)
    # Save results to output nodes without directly modifying read-only attributes

    try:
        setattr(applicant.internaldatainfo.selfemployedothertransactionhistory, 'periodicity', periodicity)

        dm_other_income_amount_nodes = getattr(
            applicant.internaldatainfo.selfemployedothertransactionhistory.dmotherincomeamounts, 'otherincomeamount', [])
        if dm_other_income_amount_nodes.GetNodeKey() == -1:
            print("dm_other_income_amount_nodesis missing or empty")
        else:
            for k in range(len(dm_other_income_amount_nodes)):
                setattr(dm_other_income_amount_nodes[k], 'isformedian', "true" if is_for_median_flags[k] else "false")
    
            if calculated_median is not None:
                setattr(applicant.jobs, 'othertransactionattbcgel', calculated_median)
    
            period_income_check_sum = 0
            if "Period_0" in periods_data:
                if is_for_median_flags[0]:
                    period_income_check_sum += periods_data["Period_0"]
    
            # Verificar Period_1:
            if "Period_1" in periods_data:
                if is_for_median_flags[1]:
                    period_income_check_sum += periods_data["Period_1"]
    
            if calculated_median == 0 or period_income_check_sum==0 or period_income_check_sum / calculated_median < 0.9:
                setattr(applicant.jobs, 'ischeckothertransactionattbc', "false")
            else:
                setattr(applicant.jobs, 'ischeckothertransactionattbc', "true")
    except AttributeError as e:
        print(f"Error saving results for Applicant {i+1}: {e}")

print("TBC Other Transactions Median Calculation Completed.")