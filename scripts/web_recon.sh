#!/usr/bin/env bash
# WEB RECON CORINGA — reconhecimento rápido de um alvo web de CTF.
# Use SOMENTE contra o alvo oficial da competição (autorizado).
#
# Uso:
#   bash web_recon.sh http://alvo.com:1234
#
# Faz: baixa a página, extrai comentários HTML, vê robots.txt e caminhos comuns,
# inspeciona cabeçalhos e cookies.

U="$1"
if [ -z "$U" ]; then echo "Uso: bash web_recon.sh http://alvo:porta"; exit 1; fi
U="${U%/}"   # tira barra final
PAD='flag\{|fiap\{|ctf\{|FLAG\{'

echo "=== [1] Cabeçalhos e cookies ==="
curl -s -I "$U"
curl -s -i "$U" | grep -iE "set-cookie|x-|server" | head

echo ""; echo "=== [2] Comentários HTML na página (dev esquece flag aqui) ==="
curl -s "$U" | grep -oE '<!--.*-->' | head -20
curl -s "$U" | grep -iEa "$PAD" && echo "  ^ FLAG no fonte!"

echo ""; echo "=== [3] Arquivos e caminhos clássicos ==="
for p in robots.txt sitemap.xml .git/HEAD .env flag flag.txt admin login \
         backup backup.zip index.php.bak .htaccess config.php; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$U/$p")
  if [ "$code" = "200" ] || [ "$code" = "301" ] || [ "$code" = "302" ]; then
    echo "  [$code] $U/$p   <-- existe, investigue!"
  fi
done

echo ""; echo "=== [4] Conteúdo do robots.txt (se houver) ==="
curl -s "$U/robots.txt" | head -20

echo ""; echo "=== Próximo: se achou /admin ou login, tente SQLi (' OR 1=1 -- )"
echo "    se há campo que reflete seu texto, tente SSTI ({{7*7}})"
echo "    pra achar MAIS caminhos: gobuster dir -u $U -w <wordlist>"
