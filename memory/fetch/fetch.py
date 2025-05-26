import logging
from typing import List, Optional
from uuid import UUID

from graphiti_core.edges import EntityEdge
from graphiti_core.graphiti import Graphiti
from graphiti_core.search.search_config import DEFAULT_SEARCH_LIMIT
from graphiti_core.search.search_filters import SearchFilters


class Fetcher:
    __graphiti: Graphiti

    def __init__(self, graphiti: Graphiti):
        self.graphiti = graphiti

    async def search(
        self,
        query: str,
        limit: int = DEFAULT_SEARCH_LIMIT,
        group_ids: Optional[List[str]] = None,
        central_node: Optional[UUID] = None,
        filters: Optional[SearchFilters] = None,
    ) -> list[EntityEdge]:
        """
        Search for entities in the graphiti.
        :return: None
        """
        if limit <= 0:
            limit = DEFAULT_SEARCH_LIMIT

        logging.debug(
            f"Searching for entities with query: {query}, group_ids: {group_ids}, "
            f"central_node: {central_node}, limit: {limit}, filters: {filters}"
        )
        return await self.graphiti.search(
            query,
            group_ids=group_ids,
            center_node_uuid=central_node.__str__() if central_node else None,
            num_results=limit,
            search_filter=filters,
        )
