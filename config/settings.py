import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    
    def __init__(self):
        env_path = Path(__file__).parent.parent.parent / '.env'
        load_dotenv(dotenv_path=env_path)
    
    @property
    def insta_username(self) -> str:
        return os.getenv('INSTA_USERNAME', '')
    
    @property
    def insta_password(self) -> str:
        return os.getenv('INSTA_PASSWORD', '')
    
    # Target Settings
    @property
    def insta_target_profile(self) -> str:
        return os.getenv('INSTA_TARGET_PROFILE', 'nicolasbyte')
    
    @property
    def output_dir(self) -> str:
        return os.getenv('OUTPUT_DIR', r'F:\IMAGENS\nicolasbyte')
    
    @property
    def max_scroll_attempts(self) -> int:
        return int(os.getenv('MAX_SCROLL_ATTEMPTS', '50'))
    
    @property
    def delay_between_requests(self) -> int:
        return int(os.getenv('DELAY_BETWEEN_REQUESTS', '3'))
    
    @property
    def wait_timeout(self) -> int:
        return int(os.getenv('WAIT_TIMEOUT', '15'))
    
    @property
    def headless_browser(self) -> bool:
        return os.getenv('HEADLESS_BROWSER', 'false').lower() == 'true'
    
    @property
    def video_format(self) -> str:
        return os.getenv('VIDEO_FORMAT', 'best')
    
    @property
    def video_retries(self) -> int:
        return int(os.getenv('VIDEO_RETRIES', '3'))
    
    @property
    def video_timeout(self) -> int:
        return int(os.getenv('VIDEO_TIMEOUT', '300'))
    
    @property
    def log_level(self) -> str:
        return os.getenv('LOG_LEVEL', 'INFO')
    
    @property
    def log_file(self) -> str:
        return os.getenv('LOG_FILE', 'downloads.log')
    
    @property
    def proxy_url(self) -> str:
        return os.getenv('PROXY_URL', '')


config = Config()
