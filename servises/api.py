import logging

from openapi_client import ApiClient, Configuration, WalletsApi, CurrencyApi
from config import api_host

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_api(api, mb_token):
    '''Создание API клиента'''
    config = Configuration()
    config.access_token = mb_token
    config.host = api_host
    api_client = ApiClient(configuration=config,
                           header_name='Authorization',
                           header_value=mb_token)
    return api(api_client)


def get_wallets(mb_token) -> dict:
    '''Получение списка кошельков пользователя'''
    api = get_api(WalletsApi, mb_token)
    wallets = {}
    try:
        wallets_db = api.wallet_list().results
        for item in wallets_db:
            wallets[item.id] = item
    except Exception as e:
        logger.error(e, exc_info=True)
    return wallets


def get_currency(mb_token) -> list:
    '''Получение списка доступных валют'''
    api = get_api(CurrencyApi, mb_token)
    currency = []
    try:
        currency = api.currency_list().results
    except Exception as e:
        logger.error(e, exc_info=True)
    return currency
