from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Neo4j(BaseModel):
    uri: str = Field(
        default="bolt://neo4j.db.svc.cluster.local:7687"
    )  # Default to Tilt for development
    username: str = Field(default="neo4j", alias="user")
    password: str = Field(default="notneo4j", alias="pass")


class OpenAIAPI(BaseModel):
    key: str = Field()
    url: str = Field(default="https://api.openai.com/v1/chat/completions")


class OpenAI(BaseModel):
    api: OpenAIAPI


class GRPC(BaseModel):
    port: int = Field(default=50051)


class Postgres(BaseModel):
    uri: str = Field(
        default="postgresql://postgres:notpostgres@postgresql.db.svc.cluster.local:5432/memory"
    )  # Default to Tilt for development


class Config(BaseSettings):
    grpc: GRPC = GRPC()
    neo4j: Neo4j = Neo4j()
    openai: OpenAI = OpenAI(api=OpenAIAPI(key=""))
    postgres: Postgres = Postgres()

    model_config = SettingsConfigDict(
        env_nested_delimiter="_",
        validate_default=False,
        env_file=".env",
    )
