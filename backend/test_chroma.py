from app.services.vector_store_service import VectorStoreService

vector_store = VectorStoreService()

print(vector_store.collection.name)