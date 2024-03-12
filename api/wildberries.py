import requests


def get_info_about_product(product_article: int):
    """
    Выполняем запрос к API card.wb.ru, получаем JSON и достаем из него название товара, цену и оценку,
    а также считаем количество на всех складах
    """

    request = requests.get(
        f'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={product_article}')

    all_stocks_quantity = 0
    products = request.json().get('data').get('products')[0]

    for product in products.get('sizes'):
        for stock in product.get('stocks'):
            all_stocks_quantity += stock['qty']

    product_name = products.get('name')
    product_price = int(products.get('salePriceU') / 100)
    product_rating = products.get('reviewRating')
    return all_stocks_quantity, product_name, product_price, product_rating
