from pydantic import BaseSettings


class Settings(BaseSettings):
    key: int = 0
    grid_width: int = 32
    grid_height: int = 16
    hole_ratio: float = 0.25


cfg = Settings()
