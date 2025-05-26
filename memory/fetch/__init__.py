from typing import override
from uuid import UUID

from google.protobuf.timestamp_pb2 import Timestamp
from graphiti_core.search.search_filters import (ComparisonOperator,
                                                 DateFilter, SearchFilters)
from grpc import ServicerContext

from fetch.fetch import Fetcher
from fetch.v1.fetch_pb2 import SearchRequest, SearchResponse
from fetch.v1.fetch_pb2_grpc import FetchServiceServicer
from graph.v1.graph_pb2 import Edge


class FetchServicer(FetchServiceServicer):
    fetcher: Fetcher

    def __init__(self, fetcher: Fetcher):
        self.fetcher = fetcher

    @override
    async def Search(
        self,
        request: SearchRequest,
        context: ServicerContext | None = None,
    ) -> SearchResponse:
        """
        Search for entities in the graphiti.
        :param request: The search request.
        :param context: The gRPC context.
        :return: The search response.
        """
        results = await self.fetcher.search(
            group_ids=list(request.group_id) if request.group_id else None,
            query=request.query,
            central_node=(
                UUID(request.central_node, version=4) if request.central_node else None
            ),
            limit=request.limit,
            filters=SearchFilters(
                node_labels=(
                    list(request.filters.node_labels)
                    if request.filters.node_labels
                    else None
                ),
                valid_at=(
                    [
                        [
                            DateFilter(
                                date=date_filter.date.ToDatetime(),
                                comparison_operator=ComparisonOperator(
                                    date_filter.comparison_operator
                                ),
                            )
                            for date_filter in or_list.filters
                        ]
                        for or_list in request.filters.valid_at
                    ]
                    if request.filters.valid_at
                    else None
                ),
            ),
        )

        return SearchResponse(
            group_id=request.group_id[0] if request.group_id else "",
            results=[
                Edge(
                    name=edge.name,
                    fact=edge.fact,
                    valid_at=(
                        Timestamp().FromDatetime(edge.valid_at)
                        if edge.valid_at
                        else None
                    ),
                    episodes=edge.episodes,
                )
                for edge in results
            ],
        )
