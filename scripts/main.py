#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.application.use_cases.instagram_use_cases import (
    CollectInstagramURLsUseCase,
    DownloadInstagramVideosUseCase,
    GetDownloadStatusUseCase
)


def menu():
    print("\n" + "=" * 70)
    print("INSTAGRAM DOWNLOADER - MENU PRINCIPAL")
    print("=" * 70)
    print("1. Coletar URLs do Instagram")
    print("2. Baixar vídeos")
    print("3. Ver status dos downloads")
    print("4. Workflow completo (Coletar + Baixar)")
    print("5. Sair")
    print("=" * 70)
    choice = input("Escolha uma opção (1-5): ").strip()
    return choice


def main():
    while True:
        choice = menu()
        
        try:
            if choice == "1":
                print("\n>>> Coletando URLs...")
                use_case = CollectInstagramURLsUseCase()
                urls = use_case.execute()
                print(f"✓ {len(urls)} URLs coletadas!")
                
            elif choice == "2":
                print("\n>>> Baixando vídeos...")
                use_case = DownloadInstagramVideosUseCase()
                stats = use_case.execute()
                print(f"✓ Download concluído: {stats['success']} sucessos, {stats['failed']} falhas")
                
            elif choice == "3":
                print("\n>>> Status dos downloads...")
                use_case = GetDownloadStatusUseCase()
                status = use_case.execute()
                print(f"✓ Posts: {status['total_posts']} | Tamanho: {status['total_size_mb']} MB")
                
            elif choice == "4":
                print("\n>>> Workflow completo...")
                print("\n[1/2] Coletando URLs...")
                collect_use_case = CollectInstagramURLsUseCase()
                urls = collect_use_case.execute()
                print(f"✓ {len(urls)} URLs coletadas!")
                
                print("\n[2/2] Baixando vídeos...")
                download_use_case = DownloadInstagramVideosUseCase()
                stats = download_use_case.execute()
                print(f"✓ Download concluído: {stats['success']} sucessos, {stats['failed']} falhas")
                
            elif choice == "5":
                print("Saindo...")
                break
                
            else:
                print("✗ Opção inválida!")
                
        except Exception as e:
            print(f"✗ Erro: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
