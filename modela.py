applicants = record.system.application.tbcbank.request.applicants.applicant

is_income_approved_by_photo = False
income_model_limit = float("inf")
max_min_loan_amount = None

# minloan
try:
    product_policies = (
        record.system.application.tbcbank.request.productpolicycatalogue.productpolicy
    )

    if product_policies is None:
        print("ProductPolicyCatalogue.ProductPolicy node is None")
    elif (
        hasattr(product_policies, "GetNodeKey") and product_policies.GetNodeKey() == -1
    ):
        print("ProductPolicyCatalogue.ProductPolicy node missing (key -1)")
    else:
        policies_list = []
        try:
            policies_list = [product_policies[i] for i in range(len(product_policies))]
        except TypeError:
            policies_list = [product_policies]

        valid_min_loans = []
        for policy in policies_list:
            try:
                if hasattr(policy, "minloanamount"):
                    valid_min_loans.append(policy.minloanamount)
            except AttributeError as e:
                print(f"Error accessing MinLoanAmount: {e}")

        if valid_min_loans:
            max_min_loan_amount = max(valid_min_loans)
            print(
                f"Found {len(valid_min_loans)} MinLoanAmount values. Using maximum: {max_min_loan_amount}"
            )
        else:
            print("No valid MinLoanAmount values found in any policy")

except AttributeError as e:
    print(f"Error accessing ProductPolicyCatalogue: {e}")

if max_min_loan_amount is None:
    max_min_loan_amount = 0
    print(f"Using default MinLoanAmount: {max_min_loan_amount}")


# income by photo
for i in range(len(applicants)):
    print(f"applicant {i}")
    applicant = applicants[i]
    try:
        jobs = applicant.jobs.jobinfo
        if jobs.GetNodeKey() == -1:
            print(f"Jobs node missing for applicant {i}")
        else:
            for n in range(len(jobs)):
                job = jobs[n]
                try:
                    applicant_incomes = job.applicantincome
                    if applicant_incomes.GetNodeKey() == -1:
                        print(f"ApplicantIncome node missing for job {n}")
                    else:
                        for p in range(len(applicant_incomes)):
                            applicant_income = applicant_incomes[p]
                            try:
                                is_income_approved_by_photo = (
                                    applicant_income.isincomeapprovedbyphoto
                                )
                            except AttributeError as e:
                                print(
                                    f"Error accessing applicant income {p} in job {n} data: {e}"
                                )
                except AttributeError as e:
                    print(f"Error accessing ApplicantIncome for job {n}: {e}")
    except AttributeError as e:
        print(f"Error accessing Jobs for applicant {i}: {e}")

# income model limit
try:
    internal_data = applicant.internaldatainfo
    if internal_data.GetNodeKey() == -1:
        print(f"InternalDataInfo missing for applicant {i}")
    else:
        try:
            transaction_history = internal_data.selfemployedtransactionhistory
            if transaction_history.GetNodeKey() == -1:
                print(f"SelfEmployedTransactionHistory missing for applicant {i}")
            else:
                try:
                    income_model_limit = transaction_history.incomemodellimit
                    print(f"IncomeModelLimit for applicant {i}: {income_model_limit}")

                except AttributeError as e:
                    print(f"Error accessing IncomeModelLimit for applicant {i}: {e}")
        except AttributeError as e:
            print(
                f"Error accessing SelfEmployedTransactionHistory for applicant {i}: {e}"
            )
except AttributeError as e:
    print(f"Error accessing InternalDataInfo for applicant {i}: {e}")


# jobinfo > 1

