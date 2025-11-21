# 📥 Instagram Downloader

Coleta vídeos de qualquer perfil do Instagram e faz download com qualidade máxima.

---

## 🚀 Quick Start

```bash
# 1. Configurar credenciais
# Editar .env com suas credenciais do Instagram

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar
python scripts/main.py
```

---

## 📋 Menu Principal

```
1. Coletar URLs do Instagram    (coleta todos os posts do perfil)
2. Baixar vídeos                (faz download dos vídeos)
3. Ver status dos downloads     (mostra quantos foram baixados)
4. Workflow completo            (faz tudo em sequência)
5. Sair
```

---

## ⚙️ Configuração (`.env`)

Editar arquivo `.env`:

```env
# Suas credenciais Instagram
INSTA_USERNAME=seu_usuario
INSTA_PASSWORD=sua_senha

# Qual perfil fazer download
INSTA_TARGET_PROFILE=nicolasbyte

# Onde salvar os vídeos
OUTPUT_DIR=F:\IMAGENS\nicolasbyte

# Configurações avançadas
MAX_SCROLL_ATTEMPTS=50              # Mais scrolls = mais URLs
DELAY_BETWEEN_REQUESTS=3             # Delay entre requisições (segundos)
WAIT_TIMEOUT=15                     # Timeout para carregar (segundos)
HEADLESS_BROWSER=false              # true = sem interface gráfica
VIDEO_FORMAT=best                   # Qualidade (best, worst, ou específica)
VIDEO_RETRIES=3                     # Tentativas de download
VIDEO_TIMEOUT=300                   # Timeout do download (segundos)
LOG_LEVEL=INFO                      # DEBUG, INFO, WARNING, ERROR
```

---

## 📂 Estrutura de Saída

```
OUTPUT_DIR/
├── post_1/
│   └── video.mp4
├── post_2/
│   └── video.mp4
└── post_N/
    └── video.mp4
```

---

## 🛠️ Comandos Individuais

### Coletar URLs

```bash
python scripts/collect_urls.py
```

Salva em `post_urls.txt`

### Fazer Download

```bash
python scripts/download_videos.py
```

Começa do `post_1` por padrão

### Ver Status

```bash
python scripts/status.py
```

Mostra quantos já foram baixados

---

## 🔧 Troubleshooting

### Coletando poucas URLs?

Aumentar em `.env`:
```env
MAX_SCROLL_ATTEMPTS=100  # De 50 para 100
DELAY_BETWEEN_REQUESTS=5  # De 3 para 5
```

### Erro de timeout?

Aumentar em `.env`:
```env
WAIT_TIMEOUT=30  # De 15 para 30
```

### Instagram bloqueando?

Aumentar delay em `.env`:
```env
DELAY_BETWEEN_REQUESTS=10  # De 3 para 10
```

### ⚠️ Rate Limit do Instagram

Se receber erro **"rate-limit reached"** ou **"Too Many Requests"**:

1. **Parar downloads imediatamente** para evitar bloqueio permanente
2. **Aguardar 15-30 minutos** antes de tentar novamente
3. **Recomendação: Dividir em lotes de ~100 downloads**
   - Fazer 100 downloads
   - Aguardar 30 minutos
   - Retomar os próximos 100

**Configuração segura:**
```env
VIDEOS_TO_UPLOAD_PER_RUN=100     # Máximo 100 por vez
DELAY_BETWEEN_REQUESTS=5          # 5 segundos entre requisições
VIDEO_RETRIES=2                   # Menos tentativas = menos requisições
```

**Como retomar de um ponto específico:**
Editar `scripts/download_videos.py`:
```python
# Mudar linha:
stats = use_case.execute("post_urls.txt", start_from=151)  # começar do 151
```

### Vídeos com qualidade ruim?

Verificar em `.env`:
```env
VIDEO_FORMAT=best  # Manter assim
VIDEO_RETRIES=5    # Aumentar de 3 para 5
```

---

## 📊 Estructura de Clean Architecture

```
src/
├── domain/                              ← Entidades e regras
│   ├── entities/instagram.py
│   └── repositories/instagram_post_repository.py
│
├── application/                         ← Casos de uso
│   └── use_cases/instagram_use_cases.py
│
└── infrastructure/                      ← Serviços e APIs
    ├── external_services/
    │   ├── instagram/url_collector.py
    │   └── video_downloader/ytdlp_downloader.py
    └── file_system/file_service.py
```

---

## 📝 Arquivos Criados

Durante execução, são criados:

- `post_urls.txt` - URLs coletadas
- `downloads.log` - Log de execução
- Pastas `post_1/`, `post_2/`, etc. em `OUTPUT_DIR`

---

## 🎯 Casos de Uso Comuns

### Scenario 1: Fazer download de todos os vídeos

```bash
python scripts/main.py
# Escolher opção 4 (Workflow completo)
```

### Scenario 2: Apenas coletar URLs (sem fazer download)

```bash
python scripts/collect_urls.py
# Depois editar post_urls.txt se necessário
```

### Scenario 3: Retomar downloads de um post específico

Editar temporariamente `scripts/download_videos.py`:
```python
# Mudar linha:
stats = use_case.execute("post_urls.txt", start_from=151)  # começar do 151
```

### Scenario 4: Baixar de outro perfil

Editar `.env`:
```env
INSTA_TARGET_PROFILE=outro_perfil
OUTPUT_DIR=F:\IMAGENS\outro_perfil
```

---

## 🔒 Segurança

⚠️ **NÃO commitar** arquivo `.env` com senhas!

Está em `.gitignore` para proteção.

Para outras pessoas usarem:
1. Criar `.env` a partir de `.env.example`
2. Preencher com suas credenciais

---

## 📞 Suporte

Ver `README.md` na raiz do projeto para suporte geral.
