from langchain.tools import tool

from catalog.models import Product
from orders.models import Order

from langchain_huggingface import HuggingFaceEmbeddings
from pgvector.django import CosineDistance

embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

@tool
def search_products_tool(query: str, max_price: float = None) -> str:
    """Шукає товари за змістом (семантично). Використовуй для будь-яких запитів про товари."""
    query_vector = embeddings_model.embed_query(query)
    
    products = Product.objects.select_related('brand').order_by(
        CosineDistance('embedding', query_vector)
    )
    
    if max_price:
        products = products.filter(price__lte=max_price)
        
    top_products = products[:5]
        
    if not top_products.exists():
        return f"На жаль, товарів за запитом '{query}' не знайдено."
        
    result = "Ось що я знайшов (найбільш відповідні):\n"
    for p in top_products:
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