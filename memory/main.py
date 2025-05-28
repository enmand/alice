import asyncio
import logging

import graphiti_core
import grpc.aio
import sqlalchemy

from config import Config
from fetch import FetchServicer
from fetch.fetch import Fetcher
from fetch.v1 import fetch_pb2_grpc
from ingest import IngestServicer
from ingest.ingest import Ingester
from ingest.v1 import ingest_pb2_grpc


async def main():
    config = Config()

    graphiti = graphiti_core.Graphiti(
        config.neo4j.uri,
        config.neo4j.username,
        config.neo4j.password,
    )
    await graphiti.build_indices_and_constraints()

    db = sqlalchemy.create_engine(config.postgres.uri)

    server = grpc.aio.server()
    ingest_pb2_grpc.add_IngestServiceServicer_to_server(
        IngestServicer(Ingester(graphiti, db)),
        server,
    )
    fetch_pb2_grpc.add_FetchServiceServicer_to_server(
        FetchServicer(Fetcher(graphiti)),
        server,
    )

    logging.info(f"Starting gRPC server on port {config.grpc.port}")
    server.add_insecure_port(f"[::]:{config.grpc.port}")

    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    logging.getLogger("neo4j").setLevel(logging.INFO)
    asyncio.get_event_loop().run_until_complete(main())
