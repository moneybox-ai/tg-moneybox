import os

from dotenv import load_dotenv
from openapi_client.api.expenses_api import ExpensesApi
from openapi_client.api_client import ApiClient
from openapi_client import Configuration
from consts import expense_url

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TOKEN')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')


headers = {
     "Authorization": f'token: {AUTH_TOKEN}',
     "Content-Type": "application/json"
}


def initialize_expenses_api():
    config = Configuration()
    config.access_token = f'Token {AUTH_TOKEN}'
    config.host = expense_url
    api_client = ApiClient(configuration=config, header_name='Authorization', header_value=headers['Authorization'])
    expenses_api = ExpensesApi(api_client)
    return expenses_api
