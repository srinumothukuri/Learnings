import requests
import xlrd
import openpyxl
import pandas as pd
import logging
import subprocess
import time

class Utils:

    start_date = None
    end_date = None

    reports_base_url = "http://reports-server:8091/billing_reports/"
    generate_report = "?generateReport=true"
    skip_session_check = "&skipSessionCheck=true"
    skip_session_check_1 = "?skipSessionCheck=true"
    aggregator_id_param = "&aggregatorId="

    report_status = reports_base_url+"get_report_status/"
    ura_base_url = "http://ura-interface:8067/ura_interface/"
    efris_report_url = ura_base_url+"invoices_by_branch/{}/{}/true/{}"
    sim_sales_report_url = reports_base_url + \
        "get_sim_sales_report_interactive/{}/{}/{}/true/false"+skip_session_check_1
    sim_swap_report_url = reports_base_url + \
        "all_sim_swaps/{}/{}/{}/true"+skip_session_check_1
    mifi_sales_report_url = reports_base_url + \
        "get_mifi_sales_report_interactive/{}/{}/{}/false/true"+skip_session_check_1
    mifi_return_report_url = reports_base_url + \
        "user_product_return_report/{}/{}"+generate_report + \
        skip_session_check+aggregator_id_param+"{}"
    wallet_report_url = reports_base_url + \
        "get_etopup_sales_tax_report_ui_new/{}/{}/{}/false/" + \
        generate_report+skip_session_check
    voucher_sales_url = reports_base_url + \
        "get_voucher_sales_tax_report_ui_new/{}/{}/{}/false" + \
        generate_report+skip_session_check
    staff_report_url = reports_base_url + \
        "get_all_staff_recharge_request_tax_report_ui_interactive/{}/{}/false" + \
        generate_report+skip_session_check
    soft_recharge_report_url = reports_base_url + \
        "get_soft_recharge_tax_report_new/{}/{}/true/{}/false"+skip_session_check_1

    @staticmethod
    def get_soft_recharge_report_url(soft_reseller_txn_prefix):
        return Utils.soft_recharge_report_url.format(Utils.start_date, Utils.end_date, soft_reseller_txn_prefix)

    @staticmethod
    def get_staff_report_url():
        return Utils.staff_report_url.format(Utils.start_date, Utils.end_date)

    @staticmethod
    def get_voucher_sales_url(reseller_id):
        return Utils.voucher_sales_url.format(reseller_id, Utils.start_date, Utils.end_date)

    @staticmethod
    def get_wallet_report_url(reseller_id):
        return Utils.wallet_report_url.format(reseller_id, Utils.start_date, Utils.end_date)

    @staticmethod
    def get_file(file_name):
        command = "scp -i ~/keypair ubuntu@ura-interface:{} ~/".format(
            file_name)
        subprocess.check_output(command, shell=True)

    @staticmethod
    def get_mifi_return_report_url(reseller_id):
        return Utils.mifi_return_report_url.format(Utils.start_date, Utils.end_date, reseller_id)

    @staticmethod
    def get_efris_report_url(branch_id):
        return Utils.efris_report_url.format(Utils.start_date, Utils.end_date, branch_id)

    @staticmethod
    def get_sim_sales_report_url(reseller_id):
        return Utils.sim_sales_report_url.format(reseller_id, Utils.start_date, Utils.end_date)

    @staticmethod
    def get_api_call_response(url, requestMethods: str):
        if requestMethods == 'GET':
            return requests.get(url, headers={"SESSIONID": "", "API_KEY": ""})

    @staticmethod
    def get_sim_swap_report_url(reseller_id):
        return Utils.sim_swap_report_url.format(reseller_id, Utils.start_date, Utils.end_date)

    @staticmethod
    def get_mifi_sales_url(reseller_id):
        return Utils.mifi_sales_report_url.format(reseller_id, Utils.start_date, Utils.end_date)

    @staticmethod
    def create_work_book(data, sheet_name, file_name):
        book = openpyxl.Workbook()
        sheet = book.create_sheet(sheet_name)
        for row in data:
            sheet.append(row)
        book.save(file_name)

# 1st argument list of tuple

    @staticmethod
    def create_file(files: list, summary: list, file_name):
        Utils.create_work_book(summary, "Summary", file_name)
        with pd.ExcelWriter(file_name, engine='openpyxl', mode='a') as excel_writer:
            for file_details in files:
                report_file_name, sheet_name = file_details
                excel_file = pd.ExcelFile(report_file_name)
                df = excel_file.parse("Sheet 1")
                df.to_excel(excel_writer, sheet_name=sheet_name, index=False)
                excel_writer.save()
        excel_writer.close()

    @staticmethod
    def get_file_df(file_name):
        excel_file = pd.ExcelFile(file_name)
        return excel_file.parse("Sheet 1")

    @staticmethod
    def sum_amount(file_name, column_name):
        df = Utils.get_file_df(file_name)
        return df[' ' + column_name].sum()

    @staticmethod
    def get_report_data(url):
        print(url)
        response = Utils.get_api_call_response(
            url, requestMethods="GET")
        print(response)
        if response.status_code == 200:
            status = response.json()['status']
            report_status_url = Utils.report_status+"{}"+Utils.skip_session_check_1
            while status == None or status != 'success':
                time.sleep(10)
                if status == 'statusInProgress':
                    reportId = response.json()['reportId']
                    response = Utils.get_api_call_response(
                        url=report_status_url.format(reportId), requestMethods="GET")
                    status = response.json()['status']
                    logging.info(status)
                else:
                    print("Invalid State while collecting report")
                    break
        return response.json()
