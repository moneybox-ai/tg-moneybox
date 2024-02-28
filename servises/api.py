import logging

from openapi_client import ApiClient, Configuration, WalletsApi, CurrencyApi


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_api(api, mb_token):
    config = Configuration()
    config.access_token = mb_token
    config.host = "http://localhost"
    api_client = ApiClient(configuration=config,
                           header_name='Authorization',
                           header_value=mb_token)
    return api(api_client)


def get_wallets(mb_token):
    api = get_api(WalletsApi, mb_token)
    wallets = ''
    try:
        wallets = api.wallet_list().results
    except Exception as e:
        logger.error(e, exc_info=True)
    return wallets


def get_currency(mb_token):
    api = get_api(CurrencyApi, mb_token)
    currency = ''
    try:
        currency = api.currency_list().results
    except Exception as e:
        logger.error(e, exc_info=True)
    return currency
