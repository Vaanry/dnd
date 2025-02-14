from pydantic_settings import BaseSettings
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError


class Settings(BaseSettings):
    app_title: str
    database_url: str
    secret_key: str
    algorithm: str
    mongo: str
    cookie_samesite: str

    class Config:
        env_file = ".env"


settings = Settings()



class CsrfSettings(BaseSettings):
  secret_key: str = "asecrettoeverybody"
  #cookie_samesite: str = "none"


@CsrfProtect.load_config
def get_csrf_config():
  return CsrfSettings()
