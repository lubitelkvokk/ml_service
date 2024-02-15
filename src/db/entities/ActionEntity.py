from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey

from db_init import Base


class DBAction(Base):
    __tablename__ = "actions"
    # table_args = {'extend_existing': True}

    action_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"))
    action_type = Column(String(255), nullable=False)
    change_cash = Column(Integer, nullable=False)
    action_date = Column(DateTime(timezone=True), default=func.now())
