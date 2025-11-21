import logging
from typing import List
from src.infrastructure.external_services.instagram.url_collector import InstagramURLCollector
from src.infrastructure.external_services.video_downloader.ytdlp_downloader import VideoDownloadService
from src.infrastructure.file_system.file_service import FileSystemService
from config.settings import config


logger = logging.getLogger(__name__)


class CollectInstagramURLsUseCase:
    
    def __init__(self):
        self.collector = InstagramURLCollector()
        self.file_service = FileSystemService()
    
    def execute(self, output_file: str = "post_urls.txt") -> List[str]:
        logger.info("Iniciando coleta de URLs do Instagram...")
        
        urls = self.collector.collect_urls()
        
        if urls:
            self.file_service.save_urls_to_file(urls, output_file)
            logger.info(f"Coleta concluída: {len(urls)} URLs")
        else:
            logger.warning("Nenhuma URL foi coletada")
        
        return urls


class DownloadInstagramVideosUseCase:
    
    def __init__(self):
        self.downloader = VideoDownloadService()
        self.file_service = FileSystemService()
    
    def execute(self, urls_file: str = "post_urls.txt", start_from: int = 1) -> dict:
        logger.info("Iniciando download de vídeos...")
        
        urls = self.file_service.load_urls_from_file(urls_file)
        
        if not urls:
            logger.error(f"Nenhuma URL encontrada em {urls_file}")
            return {
                'total': 0,
                'success': 0,
                'failed': 0,
            'files': []
        }
        
        urls_with_posts = [
            (url, idx) for idx, url in enumerate(urls, start=1)
            if idx >= start_from
        ]        logger.info(f"Iniciando download de {len(urls_with_posts)} vídeos a partir de post_{start_from}")
        
        stats = self.downloader.batch_download(urls_with_posts)
        
        success_rate = (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0
        logger.info(
            f"Download concluído:\n"
            f"  Total: {stats['total']}\n"
            f"  Sucessos: {stats['success']}\n"
            f"  Falhas: {stats['failed']}\n"
            f"  Taxa: {success_rate:.1f}%"
        )
        
        return stats


class GetDownloadStatusUseCase:
    
    def __init__(self):
        self.file_service = FileSystemService()
    
    def execute(self) -> dict:
        status = self.file_service.get_download_status(config.output_dir)
        logger.info(f"Status dos downloads: {status}")
        return status
