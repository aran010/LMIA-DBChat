from apscheduler.schedulers.background import BackgroundScheduler
from config import tenant_config

scheduler = BackgroundScheduler()

def reindex_job():
    print("Running scheduled re-index...")
    # call ingestion logic

def start_scheduler():
    # Example scheduling. In a real app, parse cron format from sync_schedule
    scheduler.add_job(reindex_job, 'cron', hour=2, minute=0)
    scheduler.start()
