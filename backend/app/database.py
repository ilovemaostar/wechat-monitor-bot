from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "wechat-monitor-bot"
    env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False

    database_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/wechat"
    redis_url: str = "redis://redis:6379/0"

    wechat_corp_id: str = ""
    wechat_agent_id: str = ""
    wechat_secret: str = ""
    wechat_token: str = ""

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    admin_secret: str = "change-me"
    frontend_url: str = "http://localhost:5173"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
