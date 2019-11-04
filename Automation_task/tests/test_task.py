import requests

from Automation_task.pages.ProductPage import ProductPage
from .data import test_data
from .config import api_search_url


def test_search_product(driver):
    page = ProductPage()
    page.search_product(test_data['product'])
    assert page.product_title.endswith(test_data['product'])


def test_search_product_price():
    headers = {"Content-Type": "application/json",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3)"
                             " AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6"}

    response = requests.get(url=api_search_url.format(product=test_data.get('product')), headers=headers)
    assert response.status_code == 200
    response_data = response.json()['data']
    assert isinstance(response_data, dict)
    assert response_data['goods'][0]['price_pcs'] == test_data.get('product_price_USD')
    assert response_data['goods'][0]['price'] == test_data.get('product_price_UHA')
    assert test_data.get('product') in response_data['goods'][0]['title']
