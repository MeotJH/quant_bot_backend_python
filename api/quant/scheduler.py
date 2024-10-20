from apscheduler.schedulers.background import BackgroundScheduler
from api.quant.services import QuantService

class QuantScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.quant_service = QuantService()

    def start(self):
        self.scheduler.add_job(self.quant_service.check_and_notify, 'interval', minutes=30)
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()