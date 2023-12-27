import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from postpaid_autorenewal import PostpaidAutorenewalCheck
import datetime
from shelve_read_writer import ShelveReadWriter
from app import app


# not working
@app.before_request
def init():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=run_postpaid_autorenewal_check,
                      trigger="interval", months=1)
    scheduler.start()


def run_postpaid_autorenewal_check():
    postpaid_autorenewal = PostpaidAutorenewalCheck()
    postpaid_autorenewal.check_and_retry_autorenewal()
    if not postpaid_autorenewal.errors:
        print("No errors found at "+str(datetime.datetime.now()))
    else:
        postpaid_error_shelve = ShelveReadWriter(
            postpaid_autorenewal.errors, postpaid_autorenewal.file_name)
        postpaid_error_shelve.write_data()
