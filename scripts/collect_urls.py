#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.application.use_cases.instagram_use_cases import CollectInstagramURLsUseCase


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('downloads.log')
        ]
    )


def main():
    setup_logging()
    
    print("=" * 70)
    print("COLETA OTIMIZADA DE URLs - Instagram")
    print("=" * 70)
    
    try:
        use_case = CollectInstagramURLsUseCase()
        urls = use_case.execute("post_urls.txt")
        
        print("\n" + "=" * 70)
        print(f"✓ Coleta concluída com sucesso!")
        print(f"Total de URLs coletadas: {len(urls)}")
        print(f"Arquivo salvo em: post_urls.txt")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Erro durante coleta: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
