from models import Entry
from sqlalchemy import extract
from collections import defaultdict

def get_monthly_summary(month=None):
    from datetime import datetime
    if not month:
        month = datetime.today().month
    entries = Entry.query.filter(extract('month', Entry.date) == month).all()
    summary = defaultdict(float)
    for e in entries:
        key = f"{e.type.title()} - {e.category}"
        summary[key] += e.amount
    return summary