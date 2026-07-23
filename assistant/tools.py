from langchain.tools import tool

from catalog.models import Product
from orders.models import Order

@tool
def search_products_tool(query: str, max_price: float = None) -> str:
    """Шукає товари в базі даних магазину за назвою. Використовуй цей інструмент для пошуку кросівок, одягу тощо."""
    products = Product.objects.filter(name__icontains=query)
    
    if max_price:
        products = products.filter(price__lte=max_price)
        
    if not products.exists():
        return f"На жаль, товарів за запитом '{query}' не знайдено."
        
    result = "Ось що я знайшов:\n"
    for p in products[:5]:
        result += f"- {p.name} (Бренд: {p.brand.name}), Ціна: {p.price} грн.\n"
        
    return result

@tool
def check_order_status_tool(order_id: int) -> str:
    """Перевіряє статус замовлення за його ID. Використовуй це, коли питають про статус замовлення."""
    try:
        order = Order.objects.get(id=order_id)
        status_map = {
            'pending': 'Очікує на оплату ⏳',
            'paid': 'Оплачено та готується до відправки ✅',
            'cancelled': 'Скасовано ❌'
        }
        human_status = status_map.get(order.status, order.status)
        return f"Статус замовлення №{order_id}: {human_status}."
    except Order.DoesNotExist:
        return f"Замовлення з номером {order_id} не знайдено в базі."