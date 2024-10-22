from api.quant.entities import Quant
from api import db

class QuantRepository:
    def get_all_active_quants(self):
        return Quant.query.filter_by(notification=True).all()

    def update_quant_status(self, quant, new_status):
        quant.current_status = new_status
        db.session.commit()