from django.db.models.signals import pre_save
from django.dispatch import receiver
from langchain_huggingface import HuggingFaceEmbeddings
from .models import Product

# Модель завантажиться один раз при старті сервера
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

@receiver(pre_save, sender=Product)
def generate_product_embedding(sender, instance, **kwargs):
    text_to_embed = instance.get_semantic_text()
    vector = embeddings_model.embed_query(text_to_embed)
    instance.embedding = vector
