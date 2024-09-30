from pydantic import BaseSettings

class Settings(BaseSettings):
    
    # Application settings
    PROJECT_NAME: str = "URL Shortener API"
    PROJECT_VERSION: str = "1.0.0"
    
    # Database URL
    DATABASE_URL: str
    
    # Other configurations (add more as needed)
    SHORT_URL_LENGTH: int = 6
    SECRET_KEY: str = "your-secret-key"  # Can be stored in an env variable for security

    class Config:
        env_file = ".env"  # Load variables from the .env file

# Instantiate the settings
settings = Settings()
