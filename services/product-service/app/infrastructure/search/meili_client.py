from __future__ import annotations

import uuid
from typing import Any

import meilisearch
from meilisearch.index import Index

from app.infrastructure.config import settings

INDEX_NAME = "products"

_client_instance: MeiliSearchClient | None = None


class MeiliSearchClient:
    def __init__(self) -> None:
        self._client = meilisearch.Client(
            settings.MEILISEARCH_URL,
            settings.MEILISEARCH_KEY,
        )
        self._index: Index | None = None

    def _get_index(self) -> Index:
        if self._index is None:
            self._index = self._client.index(INDEX_NAME)
            self._index.update_filterable_attributes(["category_id", "price", "stock"])
            self._index.update_sortable_attributes(["price", "name", "stock"])
        return self._index

    def index_product(self, product: Any) -> Any:
        doc = {
            "id": str(product.id),
            "name": product.name,
            "description": product.description or "",
            "price": product.price,
            "stock": product.stock,
            "image_url": product.image_url or "",
            "category_id": str(product.category_id) if product.category_id else None,
            "api_url": product.api_url or "",
            "quota_limit": product.quota_limit,
            "rate_limit": product.rate_limit,
        }
        return self._get_index().add_documents([doc], primary_key="id")

    def delete_product(self, product_id: uuid.UUID) -> Any:
        return self._get_index().delete_document(str(product_id))

    def search(
        self,
        query: str,
        filters: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "limit": limit,
            "offset": offset,
        }
        if filters:
            params["filter"] = filters
        result = self._get_index().search(query, params)
        return dict(result)


def get_meili_client() -> MeiliSearchClient:
    global _client_instance
    if _client_instance is None:
        _client_instance = MeiliSearchClient()
    return _client_instance
