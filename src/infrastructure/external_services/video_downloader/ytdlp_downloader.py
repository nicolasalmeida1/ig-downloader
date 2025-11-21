import logging
import os
import subprocess
import time
from typing import Optional, Tuple
from config.settings import config


logger = logging.getLogger(__name__)


class VideoDownloadService:
    
    def __init__(self):
        self.format = config.video_format
        self.retries = config.video_retries
        self.timeout = config.video_timeout
    
    def download_video(self, url: str, output_path: str, filename: str = "video") -> Tuple[bool, Optional[str]]:
        os.makedirs(output_path, exist_ok=True)
        
        output_template = os.path.join(output_path, f"{filename}.%(ext)s")
        
        for attempt in range(self.retries):
            try:
                logger.info(f"Tentando download {attempt + 1}/{self.retries}: {url}")
                
                cmd = [
                    "yt-dlp",
                    "-q",
                    "-f", self.format,
                    "-o", output_template,
                    "--no-warnings",
                    url
                ]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout
                )
                
                if result.returncode == 0:
                    
                    files = os.listdir(output_path)
                    if files:
                        file_path = os.path.join(output_path, files[0])
                        logger.info(f"Download bem-sucedido: {file_path}")
                        return True, file_path
                else:
                    logger.warning(f"yt-dlp falhou na tentativa {attempt + 1}")
                    if result.stderr:
                        logger.error(f"Erro: {result.stderr[:200]}")
                    
                    if attempt < self.retries - 1:
                        time.sleep(5)
                        
            except subprocess.TimeoutExpired:
                logger.error(f"Timeout no download (tentativa {attempt + 1}/{self.retries})")
                if attempt < self.retries - 1:
                    time.sleep(5)
            except Exception as e:
                logger.error(f"Erro durante download: {str(e)[:100]}")
                if attempt < self.retries - 1:
                    time.sleep(5)
        
        logger.error(f"Falha total ao baixar vídeo após {self.retries} tentativas")
        return False, None
    
    def batch_download(self, urls_with_posts: list) -> dict:
        stats = {
            'total': len(urls_with_posts),
            'success': 0,
            'failed': 0,
            'files': []
        }
        
        for idx, (url, post_num) in enumerate(urls_with_posts, 1):
            try:
                post_dir = os.path.join(config.output_dir, f"post_{post_num}")
                os.makedirs(post_dir, exist_ok=True)
                
                success, file_path = self.download_video(url, post_dir, "video")
                
                if success:
                    stats['success'] += 1
                    stats['files'].append(file_path)
                    logger.info(f"[{idx}/{len(urls_with_posts)}] post_{post_num}... OK")
                else:
                    stats['failed'] += 1
                    logger.warning(f"[{idx}/{len(urls_with_posts)}] post_{post_num}... ERRO")
                    try:
                        os.rmdir(post_dir)
                    except:
                        pass
                
                if idx < len(urls_with_posts):
                    time.sleep(self.delay_between_downloads)
                    
            except Exception as e:
                logger.error(f"Erro ao processar post_{post_num}: {str(e)[:100]}")
                stats['failed'] += 1
        
        return stats
    
    @property
    def delay_between_downloads(self) -> int:
        return 2 if self.retries < 3 else 1
