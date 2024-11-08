from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from api.quant.services import QuantService
import logging
from apscheduler.schedulers.base import SchedulerNotRunningError
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from pytz import timezone

logger = logging.getLogger(__name__)

class QuantScheduler:
    _instance = None

    def __new__(cls, app: Flask = None):
        if cls._instance is None:
            cls._instance = super(QuantScheduler, cls).__new__(cls)
            cls._instance.scheduler = BackgroundScheduler()
            cls._instance.quant_service = QuantService()
            cls._instance.app = app
        return cls._instance

    def start(self):
        if not self.scheduler.running:
            # 한국 시간 밤 10:30과 11:30에 실행
            self.scheduler.add_job(
                self._run_check_and_notify, 
                trigger=CronTrigger(hour='22', minute=30),
                #trigger=IntervalTrigger(seconds=10),
                timezone=timezone('Asia/Seoul')
            )
            self.scheduler.start()
            logger.info("Quant Scheduler started, will run daily at 10:30 PM and 11:30 PM KST")
        else:
            logger.info("Quant Scheduler is already running")

    def _run_check_and_notify(self):
        with self.app.app_context():
            self.quant_service.check_and_notify()

    def shutdown(self):
        if self.scheduler.running:
            logger.info("Shutting down Quant Scheduler")
            self.scheduler.shutdown(wait=False)
        else:
            logger.warning("Quant Scheduler is not running")
