from sqlalchemy import select

from core.models import UserToken
from core.db import get_sync_session


def get_user_token(user):
    '''Получение токена пользователя moneybox из БД'''
    session = get_sync_session()
    user_token = session.execute(
        select(UserToken).where(UserToken.user == user)
    )
    return user_token.scalars().first()


def save_user_token(user, token):
    '''Сохранение токена пользователя moneybox из БД'''
    new_user_token = UserToken(user=user, token=token)
    session = get_sync_session()
    session.add(new_user_token)
    session.commit()


def delete_user_token(user):
    '''Удаление токена пользователя moneybox из БД'''
    session = get_sync_session()
    user_token = session.execute(
        select(UserToken).where(UserToken.user == user)
    ).scalars().first()

    if user_token:
        session.delete(user_token)
        session.commit()
        return user_token.token
    return None
