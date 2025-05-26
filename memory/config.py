from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Neo4j(BaseModel):
    uri: str = Field(default="bolt://localhost:7687")
    username: str = Field(default="neo4j", alias="user")
    password: str


class OpenAIAPI(BaseModel):
    key: str = Field(default="sk-")
    url: str = Field(default="https://api.openai.com/v1/chat/completions")


class OpenAI(BaseModel):
    api: OpenAIAPI


class GRPC(BaseModel):
    port: int = Field(default=50051)


class Postgres(BaseModel):
    uri: str = Field(default="postgresql://postgres:nopostgres@localhost:5432/memory")


class Config(BaseSettings):
    grpc: GRPC = GRPC()
    neo4j: Neo4j
    openai: OpenAI
    postgres: Postgres

    model_config = SettingsConfigDict(
        env_nested_delimiter="_",
    )
