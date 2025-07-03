applicants = record.system.application.tbcbank.request.applicants.applicant

transfer_sources = ["TRANSFER_TBC", "TRANSFER_CB", "TRANSFER_TBC/CB"]

for i in range(len(applicants)):
    applicant = applicants[i]
    try:
        jobs = applicant.jobs

        if jobs.GetNodeKey() == -1:
            logger.error(
                "jobs node is missing or empty - does not meet basic requirements."
            )
        else:
            if (
                jobs.ischecksalaryatrs == GDS_TRUE
                and jobs.ischecksalaryattbc == GDS_TRUE
                and jobs.ischeckselfincomeothertransactionattbc == GDS_TRUE
                and jobs.ischeckrentattbc == GDS_TRUE
            ):

                tbc_sum = (
                    jobs.salaryattbcgel
                    + jobs.selfincomeothertransactionnetattbcgel
                    + jobs.rentattbcgel
                )
                rs_salary = jobs.salaryatrsgel

                if tbc_sum > rs_salary:
                    jobs.checkincomesource = "TBC_COMBINED"
                else:
                    jobs.checkincomesource = "RS_INCOME"

            else:
                if jobs.ischecksalaryattbc == GDS_TRUE:
                    jobs.checkincomesource = "TBC_MEDIAN_SALARY"
                elif jobs.ischeckrentattbc == GDS_TRUE:
                    jobs.checkincomesource = "TBC_RENT"
                elif jobs.ischecksalaryatrs == GDS_TRUE:
                    jobs.checkincomesource = "RS_INCOME"
                elif jobs.ischeckselfincometransactionattbc == GDS_TRUE:
                    jobs.checkincomesource = "TBC_MEDIAN_SALARY"
                elif jobs.ischeckselfincomeothertransactionattbc == GDS_TRUE:
                    jobs.checkincomesource = "TBC_MEDIAN_SALARY"
                else:
                    jobs.checkincomesource = "TBC_RENT"

            if (
                jobs.ischecktransferattbc == GDS_TRUE
                and jobs.checkincomesource in transfer_sources
            ):
                amounts = (
                    applicant.internaldatainfo.transfertransactionhistory.dmtransferdetails.transferamount
                )
                transfers = [
                    amount for amount in amounts if amount.isformedian == GDS_TRUE
                ]
                sources = set(t.source for t in transfers)

                if sources == {"TBC"}:
                    jobs.checkincomesource = "TRANSFER_TBC"
                elif sources == {"CB"}:
                    jobs.checkincomesource = "TRANSFER_CB"
                else:
                    jobs.checkincomesource = "TRANSFER_TBC/CB"

            if jobs.ischeckselfincomeothertransactionattbc == GDS_TRUE:
                otherincomeamounts = (
                    applicant.internaldatainfo.selfemployedtransactionhistory.selfemployedothertransactionhistory.dmotherincomeamounts.otherincomeamount
                )
                filtered_amounts = []
                for k in range(len(otherincomeamounts)):
                    amount = otherincomeamounts[k]
                    if amount.isformedian == GDS_TRUE:
                        filtered_amounts.append(amount)
                sources = set(amount.source for amount in filtered_amounts)
                if len(sources) == 1:
                    single_source = next(iter(sources))
                    if single_source in ["Glovo", "Wolt", "Yandex", "Bolt"]:
                        jobs.selfincomeothertransactionsource = single_source

    except AttributeError as e:
        logger.error(f"Error accessing jobs or transfer details for applicant {i}: {e}")
