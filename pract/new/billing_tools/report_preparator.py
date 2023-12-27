from _thread import start_new_thread
from utils import Utils
import xlrd
import xlwt
import threading
import traceback
import time
import json
import subprocess
import logging
import datetime
import pymysql
from database import Database

ura_db = Database(query['billingrepo'], 'billing', 'access', 'ura')

# class ReportPreparator(threading.Thread):


class ReportPreparator:

    # change to future tasks
    def __init__(self, reseller_id, branch_id, start_date, end_date, soft_reseller: bool, lyca_office: bool, reseller_name, api_key, soft_reseller_txn_prefix):
        # threading.Thread.__init__(self)
        self.reseller_id = reseller_id
        self.branch_id = branch_id
        Utils.start_date = start_date
        Utils.end_date = end_date
        self.soft_reseller = soft_reseller
        self.lyca_office = lyca_office
        self.billing_report_finished = False
        self.efris_report_finished = False
        self.billing_file_names = []
        self.efris_file_name = []
        self.billing_count = 0
        self.billing_amount = 0
        self.efris_count = 0
        self.efris_amount = 0
        self.status = 'Started'
        self.soft_reseller_txn_prefix = soft_reseller_txn_prefix
        self.reseller_name = reseller_name
        self.api_key_header = {"API_KEY": api_key}
        self.mismatch_reason = ""

    def create_efris_data(self):
        url = Utils.get_efris_report_url(self.branch_id)

        response_json = Utils.get_report_data(url)
        if response_json is None:
            logging.error(
                "Failed generating efris report for " + self.reseller_name)
            return
        json_data = json.dumps(response_json)
        if 'fileName' in json_data:
            self.efris_count += (response_json['entriesCount']-1)
            file_name = response_json['fileName']
            Utils.get_file(file_name)
            file_name = file_name.replace("efris_reports/", "")
            self.efris_amount += Utils.sum_amount(
                file_name, "TotalAmount")
            self.efris_file_name.append(
                (file_name, self.reseller_name+" Efris"))
            self.efris_report_finished = True

    def add_sim_sales_report(self):
        column_names = ["SalePrice", "SpecialNumberPrice"]
        url = Utils.get_sim_sales_report_url(self.reseller_id)
        json = Utils.get_report_data(url=url)
        self.summarize_billing_report(
            json, column_names, self.reseller_name+" "+"SIM Sales Report")

    def add_sim_swap_report(self):
        column_names = ["SIMPrice"]
        url = Utils.get_sim_swap_report_url(self.reseller_id)

        json = Utils.get_report_data(url=url)
        self.summarize_billing_report(
            json, column_names, self.reseller_name+" "+"SIM Swap Report")

    def add_mifi_sales_report(self):
        column_names = ["SalePrice"]
        url = Utils.get_mifi_sales_url(self.reseller_id)

        json = Utils.get_report_data(url=url)
        self.summarize_billing_report(
            json, column_names, self.reseller_name+" "+"MIFI Sales Report")

    def add_mifi_return_report(self):
        column_names = ["Amount"]
        url = Utils.get_mifi_return_report_url(self.reseller_id)

        json = Utils.get_report_data(url=url)
        self.summarize_billing_report(
            json, column_names, self.reseller_name+" "+"Product Return Report")

    def add_wallet_sales_tax_report(self):
        column_names = ["SalePrice"]
        url = Utils.get_wallet_report_url(self.reseller_id)

        json = Utils.get_report_data(url=url)
        self.summarize_billing_report(
            json, column_names, self.reseller_name+" "+"ETopup Sales Report")

    def add_voucher_sales_report(self):
        column_names = ["SalePrice"]
        url = Utils.get_voucher_sales_url(self.reseller_id)

        json = Utils.get_report_data(url=url)
        self.summarize_billing_report(
            json, column_names, self.reseller_name+" "+"Voucher Sales Report")

    def add_staff_recharge_report(self):
        column_names = ["BundlePrice", "ETopupAmount"]
        url = Utils.get_staff_report_url()

        json = Utils.get_report_data(url)
        self.summarize_billing_report(
            json, column_names, self.reseller_name+" "+"Staff Recharge Report")

    def add_soft_recharge_tax_report(self):
        column_names = ['BundlePrice']
        url = Utils.get_soft_recharge_report_url(self.soft_reseller_txn_prefix)

        json = Utils.get_report_data(url)
        self.summarize_billing_report(
            json, column_names, self.reseller_name+" "+"Sales Tax Report")

    def summarize_billing_report(self, response_json, column_names, sheet_name):
        json_data = json.dumps(response_json)
        if 'fileName' in json_data:
            self.billing_count += (response_json['entriesCount']-1)
            file_name = response_json['fileName']+".xls"
            for column_name in column_names:
                self.billing_amount += Utils.sum_amount(
                    file_name, column_name)
            self.billing_file_names.append(
                (file_name, sheet_name))

    def run(self):
        self.start_reports_collection()

    def start_reports_collection(self):
        try:
            if self.soft_reseller and not self.lyca_office:
                self.add_soft_recharge_tax_report()
            else:
                self.add_voucher_sales_report()
                self.add_wallet_sales_tax_report()
                self.add_mifi_return_report()
                self.add_mifi_sales_report()
                self.add_sim_sales_report()
                self.add_sim_swap_report()
                if self.lyca_office:
                    self.add_staff_recharge_report()
                self.billing_report_finished = True
            self.create_efris_data()
            self.update_report_status()
        except Exception:
            traceback.print_exc()
            logging.error("Exception")
            self.status = "Error Generating Report"

    def update_report_status(self):
        if self.efris_amount == self.billing_amount:
            self.status = "Match"
        else:
            #self.add_mis_match_reason()
            self.status = "MisMatch"

    @staticmethod
    def is_invoice_recorded_on_same_date(fdn) -> bool:
        ura_cursor = ura_db.cursor()
        query = "select invoice_date,invoice_recorded_on from ura_invoice_details where ura_invoice_no='{}'".format(
            fdn)
        ura_cursor.execute(query)
        return ura_cursor.fetchall()

    def add_mis_match_reason(self):
        billing_fdns = []
        for file_name in self.billing_file_names:
            print(file_name)
            df = Utils.get_file_df(file_name[0])
            print(list(df.columns.values))
            fdns = df[' FiscalInvoiceNo'].tolist()
            if fdns:
                billing_fdns.extend(fdns)

        billing_fdns = set(billing_fdns)
        efris_df = Utils.get_file_df(self.efris_file_name[0][0])
        efris_fdns = df[' FiscalInvoiceNo'].tolist()
        efris_fdns = set(efris_fdns)
        present_in_billing_not_in_efris = billing_fdns.difference(efris_fdns)
        print(present_in_billing_not_in_efris)
        if present_in_billing_not_in_efris:
            for fdn in present_in_billing_not_in_efris:
                invoice_dates = ReportPreparator.is_invoice_recorded_on_same_date(
                    str(fdn).strip())
                invoice_date, invoice_recorded_on = invoice_dates[0]
                if invoice_date.strftime("%d") != invoice_recorded_on.strftime("%d"):
                    self.mismatch_reason += str(fdn)+" --> Invoice Recored in efris on " + \
                        invoice_recorded_on
