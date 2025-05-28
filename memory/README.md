# Memory Project

## Table of Contents

1. [Configuration](#configuration)
2. [Environment Variables](#environment-variables)
3. [Running in Tilt](#running-in-tilt)
4. [gRPC Services](#grpc-services)
   - [Fetch Service](#fetch-service)
   - [Graph Service](#graph-service)
   - [Ingest Service](#ingest-service)
   - [JSONSchema](#jsonschema)
5. [Entity-Based Ingestion](#entity-based-ingestion)
   - [Entities](#entities)
   - [Entities in the Knowledge Graph](#entities-in-the-knowledge-graph)

The `memory/` project is a robust service designed to manage entity-based ingestion and retrieval using gRPC. It leverages JSONSchema for data validation and integrates seamlessly with Tilt for local development.

## Configuration

To configure the `memory/` project, create a `.env` file with the following variables:

```
# Example .env file
OPENAI_API_KEY=<your_openai_api_key>
```

### Environment Variables

- **NEO4J_URI**: URI for the Neo4j database.
- **NEO4J_USER**: Username for Neo4j.
- **NEO4J_PASS**: Password for Neo4j.
- **OPENAI_API_KEY**: API key for OpenAI.
- **OPENAI_API_URL**: URL for OpenAI API.
- **GRPC_PORT**: Port for the gRPC server.
- **POSTGRES_URI**: PostgreSQL connection string.

## Running in Tilt

The `memory/` project is configured to run in Tilt for local development. To start the service in Tilt:

1.  Install Tilt: [Tilt Installation Guide](https://docs.tilt.dev/install.html)
2.  Run `tilt up` in the project directory.
3.  Access the Tilt dashboard at `http://localhost:10350`.

Tilt will automatically build and deploy the service, providing live updates as you make changes.

## gRPC Services

### Fetch Service

#### Methods:

- **Search**: Searches for entities based on filters and query.

#### Types:

- **SearchRequest**: Contains query parameters and filters.

  - _group_id_: List of group IDs to search within.
  - _query_: Search query string.
  - _central_node_: Central node for the search.
  - _limit_: Maximum number of results to return.
  - _filters_: Filters to apply to the search.

- **Filters**: Represents search filters.

  - _node_labels_: List of node labels to filter by.
  - _valid_at_: Date filters for validity.
  - _invalid_at_: Date filters for invalidity.
  - _created_at_: Date filters for creation time.
  - _expired_at_: Date filters for expiration time.

- **DateFilterGroups**: Groups of date filters.

  - _filters_: List of `DateFilter` objects.

- **DateFilter**: Represents a single date filter.

  - _date_: Date in ISO 8601 format.
  - _comparison_operator_: Comparison operator (e.g., '=', '<>', '>', '<', '>=', '<=').

- **SearchResponse**: Contains the search results.
  - _group_id_: Group ID associated with the response.
  - _results_: List of `Edge` objects representing the search results.

### Graph

#### Types:

- **Episode**: Represents a collection of nodes and edges.

  - _uuid_: Unique identifier for the episode.
  - _valid_at_: Timestamp indicating when the episode is valid.
  - _nodes_: List of `Node` objects.
  - _edges_: List of `Edge` objects.

- **Node**: Represents an individual node.

  - _uuid_: Unique identifier for the node.
  - _summary_: Summary of the node.

- \_Edge\*\*: Represents a connection between nodes.
  - _uuid_: Unique identifier for the edge.
  - _fact_: Fact associated with the edge.
  - _name_: Name of the edge.
  - _episodes_: List of episode identifiers.
  - _expired_at_: Timestamp indicating when the edge expires.
  - _invalid_at_: Timestamp indicating when the edge becomes invalid.
  - _valid_at_: Timestamp indicating when the edge is valid.

### Graph Service

#### Types:

- **Episode**: Represents a collection of nodes and edges.
- **Node**: Represents an individual node.
- **Edge**: Represents a connection between nodes.

### Ingest Service

#### Methods:

- **Ingest**: Ingests records into the system.
- **AddEntity**: Adds a new entity.
- **GetEntity**: Retrieves an entity by ID or schema ID.
- **UpdateEntity**: Updates an existing entity.
- **DeleteEntity**: Deletes an entity by ID or schema ID.

#### Types:

- **IngestRequest**: Contains records and group ID.

  - _records_: A list of `Record` objects.
  - _group_id_: A string representing the group ID.

- _Record_: Represents an individual record.

  - _uuid_: Unique identifier for the record.
  - _timestamp_: Timestamp of the record.
  - _data_: Data associated with the record.
  - _source_description_: Description of the source.
  - _community_update_: Boolean indicating if it's a community update.
  - _previous_: List of previous record identifiers.
  - _name_: Name of the record.
  - _source_type_: Type of the source (e.g., message, JSON, text).
  - _identity_: Identity information associated with the record.
  - _entities_: List of entity identifiers.

- **Identity**: Represents identity information.

  - _name_: Name of the identity.
  - _role_: Role of the identity (e.g., user, assistant, system).

- **IngestResponse**: Contains episodes created during ingestion.

  - _group_id_: Group ID associated with the response.
  - _episodes_: List of `Episode` objects.

- **Entity**: Represents an entity.

  - _id_: Unique identifier for the entity.
  - _name_: Name of the entity.
  - _description_: Description of the entity.
  - _tags_: List of tags associated with the entity.
  - _valid_at_: Timestamp indicating when the entity is valid.
  - _schema_: JSONSchema associated with the entity.

- **AddEntityRequest**: Contains the entity to add.

  - _group_id_: Group ID for the request.
  - _entity_: The `Entity` object to add.

- **AddEntityResponse**: Contains the ID of the added entity.

  - _id_: Unique identifier of the added entity.

- **GetEntityRequest**: Contains the group ID and entity ID or schema ID.

  - _group_id_: Group ID for the request.
  - _id_: Unique identifier of the entity.
  - _schema_id_: Schema ID of the entity.

- **GetEntityResponse**: Contains the retrieved entity.

  - _entity_: The `Entity` object retrieved.

- **UpdateEntityRequest**: Contains the entity to update.

  - _group_id_: Group ID for the request.
  - _entity_: The `Entity` object to update.

- **DeleteEntityRequest**: Contains the group ID and entity ID or schema ID.
  - _group_id_: Group ID for the request.
  - _id_: Unique identifier of the entity.
  - _schema_id_: Schema ID of the entity.

### JSONSchema

#### Types:

- **JSONSchema**: Represents a JSONSchema definition.

## Entity-Based Ingestion

The `memory/` project supports entity-based ingestion using JSONSchema. This approach ensures that all ingested entities conform to a predefined schema, enabling validation and consistency.

### How It Works:

1.  **Define JSONSchema**: Create a JSONSchema file for each entity type and place it in the directory specified by `SCHEMA_PATH`.
2.  **Ingest Entity**: Use the `AddEntity` gRPC method to ingest an entity. The service validates the entity against its JSONSchema before storing it.
3.  **Validate Entity**: Use the `GetEntity` gRPC method to validate an entity against its schema without storing it.

### Entities

Entities in the `memory/` project are structured data objects that conform to JSONSchema definitions. They are used to represent real-world objects or concepts within the system. Each entity has the following attributes:

- `id`: A unique identifier for the entity.
- `name`: A human-readable name for the entity.
- `description`: A textual description of the entity.
- `tags`: A list of tags associated with the entity for categorization.
- `valid_at`: A timestamp indicating when the entity is valid.
- `schema`: A JSONSchema definition that specifies the structure and constraints of the entity.

Entities are managed through the following operations:

1. **v1.Ingest/AddEntity**: Adds a new entity to the system. The entity's schema is validated before storage.
2. **v1.Ingest/GetEntity**: Retrieves an entity by its ID or schema ID.
3. **v1.Ingest/UpdateEntity**: Updates an existing entity. The updated schema is re-validated before storage.
4. **v1.Ingest/DeleteEntity**: Deletes an entity by its ID or schema ID.

These operations ensure that entities are consistently validated and stored, maintaining data integrity and enabling schema evolution.

### Entities in the Knowledge Graph

Entities play a crucial role in encoding information within the knowledge graph. They are used to:

1. **Define Nodes**: Entities provide the structure and metadata for nodes in the graph. Each node represents an instance of an entity, enriched with attributes like `id`, `name`, and `tags`.
2. **Establish Relationships**: Entities are linked through edges, which encode relationships between nodes. These edges can include facts, timestamps, and other metadata derived from entity attributes.
3. **Enable Queries**: The structured nature of entities allows for efficient querying and retrieval of information within the graph. Filters and search criteria can be applied based on entity attributes.

By integrating entities into the knowledge graph, the `memory/` project ensures that information is stored in a structured, interconnected, and queryable format.
