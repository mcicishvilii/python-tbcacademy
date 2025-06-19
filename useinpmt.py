from datetime import datetime, timedelta
import logging

applicants = record.system.application.tbcbank.request.applicants.applicant
# Input data tbc
is_closed = GDS_False
customer_role = ""
start_date = datetime(1970, 1, 1)

application_date = datetime(1970,1,1)

is_own_funds_refinancing = GDS_False
refinance_flag = GDS_False
new_outstanding_amount = 20
product_category = "TBC_RETAIL_STANDARD"
new_limit_amount = 20
ce_borrowing_share = 20
number_of_payments_left = 39
close_date_scheduled = datetime(2022,1,14)
# Input data securities
close_date_real = None
product_name = "LOANTYPE_PAWNLOAN"
security_type = "GUARANTEETYPE_MOVABLE"
periodicity_of_payments = "MonthlyInstalments30Days"
# input data apm
apm_application_date = datetime(2021,11,15)
apm_decision_status = "APPROVE"
apm_is_in_progress = GDS_True
# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Process by applicants, loans
for i in range(len(applicants)):
    print(f"applicant {i}")
    applicant = applicants[i]
    try:
        loans = applicant.internaldatainfo.basiccredithistory.loan
        if loans.GetNodeKey() == -1:
            print("Node is missing or empty")
            logger.error("loans node is missing or empty - does not meet basic requirements.")
        else:
            for j in range(len(loans)):
                loan = loans[j]
                try:
                    is_closed = loan.isclosed
                    customer_role = loan.customerrole
                    start_date = loan.startdate
                    is_own_funds_refinancing = loan.isownfundsrefinancing
                    refinance_flag = loan.refinanceflag
                    # new_outstanding_amount = loan.newoutstandingamount
                    product_category = loan.productcategory
                    print(f"product_category = {product_category}")
                    
                except ValueError as e:
                    print(f"Error calculating exchange rates for loan: {e}")
    except AttributeError as e:
        logger.error(f"Error accessing loans for applicant {i}: {e}")            


# '''  tbc '''
# start_date_dt = start_date
# application_date_dt = application_date
# close_date_scheduled_dt = close_date_scheduled

# disqualifying_conditions = [
#     is_closed == GDS_True,
#     customer_role == "CLIENT_ROLE_GUARANTOR" and start_date_dt < datetime(2019, 1, 1),
#     is_own_funds_refinancing,
#     refinance_flag and new_outstanding_amount == 0 and product_category in ["TBC_RETAIL_STANDARD", "TBC_BUSINESS_STANDARD"],
#     refinance_flag and new_limit_amount == 0 and product_category in ["TBC_RETAIL_REVOLVER", "TBC_BUSINESS_REVOLVER"],
#     product_category == "CASH_COVER",
#     ce_borrowing_share == 0 and product_category != "TBC_RETAIL_REVOLVER",
#     product_category == "TBC_RETAIL_STANDARD"
#     and number_of_payments_left < 2
#     and close_date_scheduled_dt < (application_date_dt + timedelta(days=30)),
# ]

# use_in_pmt = not any(disqualifying_conditions)

# print(use_in_pmt)

# ''' securities '''

# start_date_dt = start_date
# application_date_dt = application_date
# close_date_scheduled_dt = close_date_scheduled

# disqualifying_conditions = [
#     is_closed == GDS_True,
#     close_date_real is not None,
#     customer_role == "CLIENT_ROLE_GUARANTOR" and start_date_dt < datetime(2019, 1, 1),
#     is_own_funds_refinancing,
#     refinance_flag and new_outstanding_amount == 0 and product_category in ["CB_RETAIL_STANDARD", "CB_BUSINESS_STANDARD"],
#     refinance_flag and new_limit_amount == 0 and product_category == "CB_RETAIL_REVOLVER",
#     product_name == "LOANTYPE_PAWNLOAN" and security_type != "GUARANTEETYPE_REALESTATE",
#     ce_borrowing_share == 0 and product_category != "CB_RETAIL_REVOLVER",
#     product_category == "CB_RETAIL_STANDARD"
#     and number_of_payments_left < 2
#     and periodicity_of_payments == "MonthlyInstalments30Days"
#     and close_date_scheduled_dt < (application_date_dt + timedelta(days=30)),
# ]

# use_in_pmt = not any(disqualifying_conditions)

# print(use_in_pmt)

# ''' apm '''

# # Convert date strings to datetime objects
# application_date_dt = application_date
# apm_application_date_dt = apm_application_date

# # Check conditions
# is_within_90_days = (application_date_dt - apm_application_date_dt).days < 90
# is_decision_approved = apm_decision_status == "APPROVE"
# is_in_progress = apm_is_in_progress == GDS_True

# # Final decision
# active_apm_application = is_within_90_days and is_decision_approved and is_in_progress

# # Save result
# APMApplicationHistory_APMApplication_ActiveApmApplication = active_apm_application

# print(active_apm_application)
