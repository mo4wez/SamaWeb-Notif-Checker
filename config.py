import os
import json
from pathlib import Path
from dotenv import load_dotenv
from exceptions import InvalidJsonConfigFileException


class SamaWebNotifCheckerConfig:
    def __init__(self):
        try:
            self.tg_notif, self.login_url, self.refresh_rate = self._read_config()
            self.username, self.password, self.token, self.api_id, self.api_hash, self.proxy_ip, self.proxy_ip, self.proxy_scheme= self._read_env_config()
        except InvalidJsonConfigFileException:
            exit(2)

    def _read_env_config(self):
        
        load_dotenv(verbose=False)
        env_path = Path('./env') / '.env'
        load_dotenv(dotenv_path=str(env_path))

        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        api_id = os.getenv("API_ID")
        api_hash = os.getenv("API_HASH")
        token = os.getenv("TOKEN")
        proxy_ip = os.getenv("PROXY_IP")
        proxy_port = os.getenv("PROXY_PORT")
        proxy_scheme = os.getenv("PROXY_SCHEME")

        return username, password, token, api_hash, api_id, proxy_ip, proxy_ip, proxy_scheme

    def _read_config(self):
        with open('config.json') as f:
            data = json.load(f)

        if 'tele_notif' not in data:
            raise InvalidJsonConfigFileException('tele_notif')
        if 'samaweb_login_url' not in data:
            raise InvalidJsonConfigFileException('samaweb_login_url')
        if 'refresh_rate' not in data:
            raise InvalidJsonConfigFileException('refresh_rate')

        return data['tele_notif'], data['samaweb_login_url'], data['refresh_rate']
