applicants = record.system.application.tbcbank.request.applicants.applicant
for i in range(len(applicants)):
    applicant = applicants[i]
    expense_rate = applicant.internaldatainfo.selfemployedtransactionhistory.selfemployedothertransactionhistory.expense
    print(f"xvicha {expense_rate}")
    try:
        jobs = applicant.jobs
        if jobs.GetNodeKey() == -1:
            logger.error("jobs node is missing or empty - does not meet basic requirements.")
        else:
            total_net_disposable_income = 0.0
            total_self_income_other_net = 0.0  # For SelfIncomeOtherTransactionNetAtTBCGEL
            
            try:
                jobinfos = jobs.jobinfo
                if jobinfos.GetNodeKey() == -1:
                    logger.error("jobinfos node is missing or empty - does not meet basic requirements.")
                else:
                    for j in range(len(jobinfos)):
                        jobinfo = jobinfos[j]
                        try:
                            jobinfo_net_disposable_income = 0.0
                            
                            try:
                                applicant_incomes = jobinfo.applicantincome
                                if applicant_incomes.GetNodeKey() == -1:
                                    logger.error(f"applicant_incomes node is missing or empty for jobinfo {j} - does not meet basic requirements.")
                                else:
                                    for k in range(len(applicant_incomes)):
                                        income = applicant_incomes[k]
                                        try:
                                            income_amount = float(income.incomeamountgel) if income.incomeamountgel else 0.0
                                            nbg_expense_rate = float(income.nbgexpenserate) if income.nbgexpenserate else 0.0
                                            expense = float(income.expense) if income.expense else 0.0
                                            
                                            income_expense_by_rate = income_amount * nbg_expense_rate
                                            max_expense_1 = max(income_expense_by_rate, expense)
                                            net_income_part1 = income_amount - max_expense_1
                                            
                                            self_income_transaction = float(jobs.selfincometransactionattbcgel) if jobs.selfincometransactionattbcgel else 0.0
                                            if self_income_transaction > 3000:
                                                self_income_transaction = 3000.0
                                            max_expense_2 = max(expense, income_expense_by_rate)
                                            net_income_part2 = self_income_transaction - max_expense_2
                                            
                                            net_disposable_income = min(net_income_part1, net_income_part2)
                                            
                                            jobinfo_net_disposable_income += net_disposable_income
                                                                                        
                                        except (AttributeError, ValueError) as e:
                                            logger.error(f"Error accessing income {k} for jobinfo {j} applicant {i}: {e}")
                                    
                                    total_net_disposable_income += jobinfo_net_disposable_income
                            
                            except AttributeError as e:
                                logger.error(f"Error accessing applicant_incomes for jobinfo {j} applicant {i}: {e}")
                            
                            try:
                                self_income_other = jobs.selfincomeothertransactionattbcgel if jobs.selfincomeothertransactionattbcgel is not None else 0.0
                                print(self_income_other)
                                net_other_income = self_income_other * (1 - expense_rate)
                                
                                print(f"[Applicant {i}][JobInfo {j}] net_other_income={net_other_income}")
                                total_self_income_other_net += net_other_income
                                print(f"[Applicant {i}][JobInfo {j}] total_self_income_other_net={total_self_income_other_net}")
                            except (AttributeError, ValueError) as e:
                                logger.error(f"Error calculating SelfIncomeOtherTransactionNetAtTBCGEL for jobinfo {j}: {e}")
                        except AttributeError as e:
                            print(f"Error accessing jobinfo {j} for applicant {i}: {e}")
                    
                    jobs.selfincometransactionnetattbcgel = total_net_disposable_income
                    jobs.selfincomeothertransactionnetattbcgel = total_self_income_other_net
                    
                    print(f"[Applicant {i}] total_self_income_other_net={total_self_income_other_net}")
                    
            except AttributeError as e:
                logger.error(f"Error accessing jobinfos for applicant {i}: {e}")
    except AttributeError as e:
        logger.error(f"Error accessing jobs for applicant {i}: {e}")
