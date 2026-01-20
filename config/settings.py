"""Configuration settings for API tests."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    """Application settings."""

    # API Configuration
    BASE_URL: str = os.getenv('BASE_URL', 'https://jsonplaceholder.typicode.com')
    API_TIMEOUT: int = int(os.getenv('API_TIMEOUT', '30'))

    # Test Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')

    # Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    LOGS_DIR: Path = PROJECT_ROOT / 'logs'
    ALLURE_RESULTS_DIR: Path = PROJECT_ROOT / 'allure-results'
    DATA_DIR: Path = PROJECT_ROOT / 'data'

    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.LOGS_DIR.mkdir(exist_ok=True)
        cls.ALLURE_RESULTS_DIR.mkdir(exist_ok=True)
        cls.DATA_DIR.mkdir(exist_ok=True)


# Create settings instance
settings = Settings()
settings.create_directories()
