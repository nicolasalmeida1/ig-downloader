import json
import logging
import os
from typing import List, Dict, Optional
from datetime import datetime


logger = logging.getLogger(__name__)


class FileSystemService:
    
    def __init__(self):
        pass
    
    @staticmethod
    def save_urls_to_file(urls: List[str], file_path: str) -> bool:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for url in urls:
                    f.write(url + '\n')
            
            logger.info(f"Salvos {len(urls)} URLs em {file_path}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar URLs: {str(e)}")
            return False
    
    @staticmethod
    def load_urls_from_file(file_path: str) -> List[str]:
        urls = []
        try:
            if not os.path.exists(file_path):
                logger.warning(f"Arquivo não encontrado: {file_path}")
                return urls
            
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
            
            logger.info(f"Carregadas {len(urls)} URLs de {file_path}")
            return urls
        except Exception as e:
            logger.error(f"Erro ao carregar URLs: {str(e)}")
            return urls
    
    @staticmethod
    def save_json(data: dict, file_path: str) -> bool:
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"JSON salvo em {file_path}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar JSON: {str(e)}")
            return False
    
    @staticmethod
    def load_json(file_path: str) -> Optional[dict]:
        try:
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar JSON: {str(e)}")
            return None
    
    @staticmethod
    def get_downloaded_count(output_dir: str) -> int:
        try:
            count = 0
            for item in os.listdir(output_dir):
                if item.startswith('post_') and os.path.isdir(os.path.join(output_dir, item)):
                    count += 1
            return count
        except Exception as e:
            logger.error(f"Erro ao contar downloads: {str(e)}")
            return 0
    
    @staticmethod
    def get_download_status(output_dir: str) -> Dict[str, int]:
        try:
            total_posts = 0
            total_size = 0
            
            for item in os.listdir(output_dir):
                post_path = os.path.join(output_dir, item)
                if item.startswith('post_') and os.path.isdir(post_path):
                    total_posts += 1
                    for file in os.listdir(post_path):
                        file_path = os.path.join(post_path, file)
                        if os.path.isfile(file_path):
                            total_size += os.path.getsize(file_path)
            
            return {
                'total_posts': total_posts,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'average_size_mb': round((total_size / total_posts / (1024 * 1024)), 2) if total_posts > 0 else 0
            }
        except Exception as e:
            logger.error(f"Erro ao obter status: {str(e)}")
            return {'total_posts': 0, 'total_size_mb': 0}
