import requests

from Automation_task.pages.ProductPage import ProductPageFlow
from .data import test_data


def test_search_product(driver):
    page_flow = ProductPageFlow()
    page_flow.search_product(test_data['product'])
    assert test_data['product'] in page_flow.product_tittle


def test_search_product_price():
    headers = {"Content-Type": "application/json",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3)"
                             " AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6"}

    response = requests.get(url=test_data['api_search_url'].format(product=test_data['product']), headers=headers)
    assert response.status_code == 200
    response_data = response.json()['data']
    assert isinstance(response_data, dict)
    assert str(response_data['goods'][0]['price_pcs']) == test_data['product_price_USD']
    assert str(response_data['goods'][0]['price']) == test_data['product_price_UHA']
    assert test_data['product'] in response_data['goods'][0]['title']
