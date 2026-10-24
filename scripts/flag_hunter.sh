#!/usr/bin/env bash
# FLAG HUNTER CORINGA — varre uma pasta inteira atrás do padrão de flag,
# inclusive dentro de binários (via strings) e arquivos escondidos.
#
# Uso:
#   bash flag_hunter.sh                 # varre a pasta atual
#   bash flag_hunter.sh /caminho/pasta  # varre a pasta indicada
#   bash flag_hunter.sh arquivo.bin     # varre um arquivo só
#
# Dica: rode isso DEPOIS de extrair tudo (binwalk -e, unzip, etc).

ALVO="${1:-.}"
# ajuste aqui o formato da flag do SEU ctf se souber (ex: só FIAP):
PADRAO='flag\{|fiap\{|ctf\{|key\{|secret\{|FLAG\{|FIAP\{'

echo "========================================================"
echo "  Caçando flags em: $ALVO"
echo "  Padrão: $PADRAO"
echo "========================================================"

echo ""
echo "--- 1) Busca direta em texto (recursiva) ---"
grep -rniEa "$PADRAO" "$ALVO" 2>/dev/null | head -50

echo ""
echo "--- 2) Busca dentro de binários (via strings) ---"
if [ -d "$ALVO" ]; then
  find "$ALVO" -type f 2>/dev/null | while read -r f; do
    strings -n 5 "$f" 2>/dev/null | grep -iEa "$PADRAO" | sed "s|^|[$f] |"
  done | head -50
else
  strings -n 5 "$ALVO" 2>/dev/null | grep -iEa "$PADRAO" | head -50
fi

echo ""
echo "--- 3) Busca em base64 escondido (decodifica trechos e procura) ---"
if [ -d "$ALVO" ]; then SRC=$(find "$ALVO" -type f 2>/dev/null); else SRC="$ALVO"; fi
for f in $SRC; do
  grep -oEa '[A-Za-z0-9+/]{16,}={0,2}' "$f" 2>/dev/null | while read -r b; do
    dec=$(echo "$b" | base64 -d 2>/dev/null)
    echo "$dec" | grep -iEaq "$PADRAO" && echo "[$f] base64->  $dec"
  done
done | head -20

echo ""
echo "========================================================"
echo "  Fim da caçada. Nada? O dado está codificado/cifrado:"
echo "  passe o arquivo pelo decoder.py ou xor_brute.py."
echo "========================================================"
