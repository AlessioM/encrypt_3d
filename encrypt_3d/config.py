from pydantic import BaseSettings


class Settings(BaseSettings):
    key: int = 0
    grid_width: int = 8
    grid_height: int = 8
    hole_ratio: float = 0.2


cfg = Settings()
