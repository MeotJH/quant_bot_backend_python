from apscheduler.schedulers.background import BackgroundScheduler
from api.quant.services import QuantService
import logging
from apscheduler.schedulers.base import SchedulerNotRunningError

logger = logging.getLogger(__name__)

class QuantScheduler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QuantScheduler, cls).__new__(cls)
            cls._instance.scheduler = BackgroundScheduler()
            cls._instance.quant_service = QuantService()
        return cls._instance

    def start(self):
        if not self.scheduler.running:
            self.scheduler.add_job(self.quant_service.check_and_notify, 'interval', minutes=30)
            self.scheduler.start()
            logger.info("Quant Scheduler started")
        else:
            logger.info("Quant Scheduler is already running")

    def shutdown(self):
        if self.scheduler.running:
            logger.info("Shutting down Quant Scheduler")
            self.scheduler.shutdown()
        else:
            logger.warning("Quant Scheduler is not running")
