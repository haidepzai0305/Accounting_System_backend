from datetime import datetime

from backend.models import JournalEntry, db, ChartOfAccounts
from backend.utils.id_generator import generate_id


def create_journal_entry(transaction_id, date, description, debit, credit, amount):

    journal = JournalEntry(
        journal_id=generate_id("JNL"),
        transaction_id=transaction_id,
        period=date.strftime('%Y-%m'),
        date=date,
        description=description,
        account_debit=debit,
        account_credit=credit,
        amount=amount,
        status='posted',
        is_system_generated=True,
        posted_at=datetime.utcnow()
    )

    db.session.add(journal)

    debit_account = ChartOfAccounts.query.filter_by(code=debit).first()
    credit_account = ChartOfAccounts.query.filter_by(code=credit).first()

    if debit_account:
        debit_account.balance += amount

    if credit_account:
        credit_account.balance -= amount

    return journal