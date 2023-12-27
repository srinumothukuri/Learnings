import pymysql
from database import Database
import datetime
import requests


class PostpaidAutorenewalCheck:

    date_format = "%Y-%m-%d"
    file_prefix = "/home/ubuntu/postpaid_auto_renewal_failures/"

    def __init__(self):
        self.billing_db_conn = Database(
            'billingrepo', 'billing', 'access', 'billing')
        self.spal_db_conn = Database(
            'spalapirepo', 'billing', 'access', 'spal')
        self.errors = []
        self.file_name = file_prefix + \
            datetime.striptime(datetime.datetime.now(), date_format)

    def get_auto_renewal_failed_recharges(self):
        billing_cursor = self.billing_db_conn.cursor()
        billing_cursor.execute(
            'select subscription_token from postpaid_subscription_record ps inner join subscription s on s.subscription_id=ps.subscription_id and s.is_deleted=0 and s.is_active=1 and ps.is_deleted=0 and ps.expiry_date < now()')
        return billing_cursor.fetchall()

    def is_auto_renewal_successful(self, sub_token):
        billing_cursor = self.billing_db_conn.cursor()
        billing_cursor.execute(
            'select auto_renewal_state from postpaid_subscription_record where subscription_token="{}"'.format(sub_token))
        status = billing_cursor.fetchall()[0][0]
        if status and status == 'Complete':
            spal_cursor = self.spal_db_conn.cursor()
            spal_cursor.execute(
                'select validity_date > now() from postpaid_subscription_record where subscription_id="{}"'.format(sub_token))
            spal_auto_renewal = spal_cursor.fetchall()
            if not spal_auto_renewal:
                self.errors.append(
                    {'PostpaidSubscriptionToken': sub_token, "ErrorMessage": "Record Not found in spal"})
            else:
                is_expired = not spal_auto_renewal[0][0]
                if is_expired:
                    self.errors.append(
                        {'PostpaidSubscriptionToken': sub_token, "ErrorMessage": "Validity update failed in spal"})

    def check_and_retry_autorenewal(self):
        subscription_tokens = get_auto_renewal_failed_recharges()
        url = 'http://scheduler:8087/autorenewal_postpaid_subscription_record/'
        for subscription_token in subscription_tokens:
            sub_token = subscription_token[0]
            try:
                requests.post(url + sub_token)
                is_auto_renewal_successful(sub_token)
            except:
                self.errors.append({'PostpaidSubscriptionToken': sub_token,
                                   "ErrorMessage": "Error while Retrying autorenewal"})
                traceback.print_exc()
