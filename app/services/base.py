import datetime

from app.models.mixins import DonationMixIn


def close_donation_or_project(obj: DonationMixIn) -> DonationMixIn:
    obj.fully_invested = True
    obj.invested_amount = obj.full_amount
    obj.close_date = datetime.datetime.now()
    return obj
