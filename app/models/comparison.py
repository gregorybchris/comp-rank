import datetime as dt
import uuid
import os

class Comparison():
    def __init__(self, item_a_id, item_b_id):
        self.id = None
        self.created_at = dt.datetime.now()
        self.winner_id = None
        self.comparison_key = gen_comparison_key()
        self.item_a_id = item_a_id
        self.item_b_id = item_b_id

    @staticmethod
    def gen_comparison_key():
        return str(uuid.UUID(bytes=os.urandom(16)))
