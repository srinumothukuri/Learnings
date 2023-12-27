import datetime
import pymysql
from report_preparator import ReportPreparator
import sys
from utils import Utils
import logging
from database import Database
class BootStrap:
     def __init__(self, data, basedir):
        self.data = data
        self.topic_name = None
        self.query_name = None
        self.topic_data = None
        self.query_data = None
        self.basedir = basedir
   
    billing_db = Database(query['billingrepo'], 'billing', 'access', 'billing')

    summary_data = []
    file_data = []
    header = ("ResellerName", "EfrisCount",
            "EfrisAmount", "BillingCount", "BillingAmount", "Match Status", "MisMatch Reason")


    def get_lyca_office_reseller_id(billing_cursor):
        query = "select lyca_digital_reseller_id from config_table"
        billing_cursor.execute(query)
        return billing_cursor.fetchall()[0][0]


    def get_api_key(billing_cursor):
        query = "select application_key from application_keys where application_name='OPS'"
        billing_cursor.execute(query)
        return billing_cursor.fetchall()[0][0]


    def get_reseller_information(billing_cursor):
        query = "select a.soft_reseller_txn_prefix,r.reseller_name,r.reseller_id,ura_branch_id,is_softagent,application_name from reseller_management r inner join user u on u.user_id=r.user_id and u.role_name='Reseller Aggregator' and u.is_active=1 and r.is_active=1 inner join application_keys a on a.reseller_id=r.reseller_id"
        billing_cursor.execute(query)
        return billing_cursor.fetchall()


    def start_reports_reconciliation(self):
        billing_cursor = billing_db.cursor()

        lyca_reseller_id = get_lyca_office_reseller_id(billing_cursor)
        api_key = get_api_key(billing_cursor)
        resellers_information = get_reseller_information(billing_cursor)

        reports_collection_data = []
        for reseller_information in resellers_information:
            soft_reseller_txn_prefix, reseller_name, reseller_id, branch_id, is_soft_reseller, application_name = reseller_information
            if branch_id is None:
                logging.info("Branch id not found for " + reseller_name)
                continue
            logging.info("Collecting for " + reseller_name)
            print(self.data)
            report_preparator = ReportPreparator(
                reseller_id, branch_id, self.data['start_date'], self.data['end_date'], bool(int.from_bytes(is_soft_reseller, 'big')), reseller_id == lyca_reseller_id, reseller_name, api_key, soft_reseller_txn_prefix)
            # report_preparator.start()
            report_preparator.run()
            reports_collection_data.append(report_preparator)

        summary_data.append(header)

        while reports_collection_data:
            report_collection_data = reports_collection_data.pop()
            if report_collection_data.status == "Started":
                reports_collection_data.append(report_collection_data)
            else:
                file_data.extend(report_collection_data.billing_file_names)
                file_data.extend(report_collection_data.efris_file_name)
                add_summary(report_collection_data,
                            report_collection_data.reseller_name)
        logging.info('*' * 20, "data", '*' * 20)
        logging.info(summary_data)
        logging.info(file_data)
        Utils.create_file(file_data, summary_data, self.data['start_date'] + ".xlsx")
        


    def add_summary(report_preparator: ReportPreparator, reseller_name):
        summary_data.append((reseller_name, report_preparator.efris_count,
                            report_preparator.efris_amount, report_preparator.billing_count, report_preparator.billing_amount, report_preparator.status, report_preparator.mismatch_reason))
