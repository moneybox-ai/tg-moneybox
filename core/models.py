from sqlalchemy import Column, Integer, String, UniqueConstraint

from core.db import Base


class UserToken(Base):
    '''Модель для пары тг_юэер-токен_moneybox '''
    user = Column(Integer)
    token = Column(String)

    __table_args__ = (
            UniqueConstraint('user', 'token', name='unique_user_token'),
        )
