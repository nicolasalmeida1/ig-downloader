#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.application.use_cases.instagram_use_cases import DownloadInstagramVideosUseCase
from config.settings import config


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(config.log_file)
        ]
    )


def main():
    setup_logging()
    
    print("=" * 70)
    print("DOWNLOAD DE VÍDEOS - Instagram")
    print("=" * 70)
    print(f"Perfil alvo: @{config.insta_target_profile}")
    print(f"Diretório de saída: {config.output_dir}")
    print("=" * 70)
    
    try:
        # Verificar se arquivo de URLs existe
        if not Path("post_urls.txt").exists():
            print("\n✗ Arquivo 'post_urls.txt' não encontrado!")
            print("Execute primeiro: python scripts/collect_urls.py")
            sys.exit(1)
        
        use_case = DownloadInstagramVideosUseCase()
        stats = use_case.execute("post_urls.txt", start_from=1)
        
        print("\n" + "=" * 70)
        print("RESUMO DO DOWNLOAD")
        print("=" * 70)
        print(f"Total:    {stats['total']}")
        print(f"Sucessos: {stats['success']}")
        print(f"Falhas:   {stats['failed']}")
        if stats['total'] > 0:
            print(f"Taxa:     {(stats['success']/stats['total']*100):.1f}%")
        print(f"Destino:  {config.output_dir}")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Erro durante download: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
