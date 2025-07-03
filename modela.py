def safe_float_conversion(value):
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0

applicants = record.system.application.tbcbank.request.applicants.applicant

for appl in range(len(applicants)):
    applicant = applicants[appl]
    transfer_sum = 0
    country_grouped = {}
    all_median_periods = []
 
    transferamounts = applicant.internaldatainfo.transfertransactionhistory.transferamounts.transferamount
    if transferamounts.GetNodeKey() == -1:
        applicant.jobs.transferattbcgel = 0.0
        applicant.jobs.ischecktransferattbc = "false"
        continue
    else:
        for ind in range(len(transferamounts)):
            transferamount = transferamounts[ind]
            period = transferamount.period
            country = transferamount.country
            currency = transferamount.currency
            amountgel = transferamount.amountgel
            source = transferamount.source       
            key = (country, period)
    
            if country not in country_grouped:
                country_grouped[country] = {}
            if period not in country_grouped[country]:
                country_grouped[country][period] = {
                    "AmountGEL": 0.0,
                    "Country": country,
                    "Period": period,
                    "Sources": set()
                }
    
            country_grouped[country][period]["AmountGEL"] += amountgel
            country_grouped[country][period]["Sources"].add(source)   
            print(country_grouped)
            
        for i, (country, periods_dict) in enumerate(country_grouped.items()):
            dmtransferamount = applicant.internaldatainfo.transfertransactionhistory.dmtransferamounts[i]
    
            for j, (period, data) in enumerate(sorted(periods_dict.items())):
                try:
                    transfer = dmtransferamount.transferamount[j]
                except IndexError:
                    print(f"[WARNING] No transferamount[{j}] available to write.")
                    break
                transfer.period = int(data["Period"])       
                transfer.amountgel = data["AmountGEL"]    
                transfer.country = data["Country"]
                transfer.source = "/".join(sorted(data["Sources"]))

    dm_transfer_amounts = applicant.internaldatainfo.transfertransactionhistory.dmtransferamounts
    if dm_transfer_amounts.GetNodeKey() == -1:
        continue
    else:
        for dt in range(len(dm_transfer_amounts)):
            transfer_amounts = dm_transfer_amounts[dt].transferamount
            transfer_periods = [0.0] * 7
            transfer_sources = [""] * 7
            
            if transfer_amounts.GetNodeKey() == -1:
                continue
            else:
                for t in range(len(transfer_amounts)):
                    transmfer = transfer_amounts[t]
                    if transmfer.GetNodeKey() == -1:
                        continue
                    else:
                        try:
                            period = int(transmfer.period)
                            amount = float(transmfer.amountgel) if transmfer.amountgel is not None else 0.0
                            source = transmfer.source if transmfer.source else ""
                            if 0 <= period <= 6:
                                transfer_periods[period] = amount
                                transfer_sources[period] = source
                        except Exception as e:
                            print(f"Error processing TransferAmount for Applicant {appl+1}, item {t+1}: {e}")
                
                def count_valid_periods(periods_slice):
                    return sum(1 for income in periods_slice if income >= 100)
                
                count_1_6 = count_valid_periods(transfer_periods[1:7])
                count_0_5 = count_valid_periods(transfer_periods[0:6])
                
                has_period_0_or_1 = transfer_periods[0] >= 100 or transfer_periods[1] >= 100
                    
                periodicity = 0
                median_values = []
                median_periods_to_use = []
                
                if count_1_6 >= 5 and has_period_0_or_1:
                    periodicity = 6
                elif count_0_5 >= 5 and has_period_0_or_1:
                    periodicity = 6
                else:
                    periodicity = 0
                
                if periodicity == 6:
                    if (transfer_periods[1] >= 100 and transfer_periods[6] >= 100 and 
                        (transfer_periods[0] == 0 or transfer_periods[0] <= transfer_periods[6])):
                        median_values = transfer_periods[1:7]
                        median_periods_to_use = list(range(1, 7))
                    elif (transfer_periods[6] < 100 and transfer_periods[0] >= 100):
                        median_values = transfer_periods[0:6]
                        median_periods_to_use = list(range(0, 6))
                    elif (transfer_periods[1] < 100 and transfer_periods[0] >= 100):
                        median_values = [transfer_periods[0]] + transfer_periods[2:7]
                        median_periods_to_use = [0] + list(range(2, 7))
                    elif (transfer_periods[0] >= 100 and transfer_periods[1] >= 100 and 
                          transfer_periods[6] >= 100 and transfer_periods[0] > transfer_periods[6]):
                        median_values = transfer_periods[0:6]
                        median_periods_to_use = list(range(0, 6))
                    else:
                        median_values = transfer_periods[1:7]
                        median_periods_to_use = list(range(1, 7))
                    
                    filtered_median_values = [val for val in median_values if val >= 100]
                    
                    if filtered_median_values:
                        calculated_median = round_down_2(calculate_median(filtered_median_values))
                        transfer_sum += calculated_median
                        
                        for period_idx in median_periods_to_use:
                            if transfer_periods[period_idx] >= 100:
                                all_median_periods.append({
                                    "period": period_idx,
                                    "amountgel": transfer_periods[period_idx],
                                    "source": transfer_sources[period_idx],
                                    "isformedian": True
                                })
                
                try:
                    dm_transfer_amounts[dt].periodicity = periodicity
                    print(f"Set periodicity {periodicity} for country group {dt}")
                except Exception as e:
                    print(f"Error updating periodicity for Applicant {appl+1}, DM {dt+1}: {e}")
    
    try:
        dmtransferdetails = applicant.internaldatainfo.transfertransactionhistory.dmtransferdetails
        
        for idx, median_data in enumerate(all_median_periods):
            try:
                transfer_detail = dmtransferdetails.transferamount[idx]
                transfer_detail.period = median_data["period"]
                transfer_detail.amountgel = median_data["amountgel"]
                transfer_detail.source = median_data["source"]
                transfer_detail.isformedian = "true"
            except IndexError:
                print(f"[WARNING] No transferamount[{idx}] available in DMTransferDetails.")
                break
            except Exception as e:
                print(f"Error setting DMTransferDetails for Applicant {appl+1}, item {idx}: {e}")
                
    except Exception as e:
        print(f"Error accessing DMTransferDetails for Applicant {appl+1}: {e}")
    
    try:
        applicant.jobs.transferattbcgel = transfer_sum
        if transfer_sum >= 100:
            applicant.jobs.ischecktransferattbc = "true"
        else:
            applicant.jobs.ischecktransferattbc = "false"
        print(f"Final transfer sum: {transfer_sum}")
    except AttributeError as e:
        print(f"Error updating Jobs fields for Applicant {appl+1}: {e}")