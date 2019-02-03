# coding: utf-8

import datetime


class ChargeData:
    year = 0
    month = 0
    day = 0
    date = datetime.datetime(1970, 1, 1)
    is_new_signature = True
    user = ""
    shop = ""
    payment_method = ""
    charge = 0.0
    payment_fee = 0.0
    total_payment_amount = 0.0
    total_paying_time = 0
    current_paying_time = 0
    charge_for_this_month = 0.0
    charge_left_for_next_month = 0.0
    notes = ""

    def __str__(self):
        return "{}/{}/{} {}円 @ {}".format(self.year, self.month, self.day, self.charge, self.shop)
        #str(self.year) + "/" + str(self.month) + "/" + str(self.day) + " " + str(self.charge) + " 円 @ " + str(self.shop)

    def create_date(self):
        self.date = datetime.datetime(self.year, self.month, self.day)

    def to_dict(self):
        dict_ = {"Date": self.date,
                 "Charge": self.charge,
                 "Shop": self.shop
                 }

        return dict_
