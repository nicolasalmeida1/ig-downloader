#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.application.use_cases.instagram_use_cases import GetDownloadStatusUseCase
from config.settings import config


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main():
    setup_logging()
    
    print("=" * 70)
    print("STATUS DOS DOWNLOADS")
    print("=" * 70)
    
    try:
        use_case = GetDownloadStatusUseCase()
        status = use_case.execute()
        
        print(f"Diretório: {config.output_dir}")
        print(f"Posts baixados: {status['total_posts']}")
        print(f"Tamanho total: {status['total_size_mb']} MB")
        print(f"Tamanho médio: {status['average_size_mb']} MB")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
