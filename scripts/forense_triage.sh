#!/usr/bin/env bash
# TRIAGEM FORENSE CORINGA — joga TODA a bateria de análise num arquivo de uma vez.
# Pensado pra você olhar o relatório e já saber pra onde ir.
#
# Uso:
#   bash forense_triage.sh arquivo_suspeito.jpg
#
# Roda (o que estiver instalado): file, exiftool, strings+grep, binwalk,
# zsteg (png/bmp), steghide (senha vazia), e tenta extrair embutidos.

F="$1"
if [ -z "$F" ] || [ ! -f "$F" ]; then
  echo "Uso: bash forense_triage.sh <arquivo>"; exit 1
fi
PAD='flag\{|fiap\{|ctf\{|key\{|FLAG\{|FIAP\{'
have(){ command -v "$1" >/dev/null 2>&1; }

echo "############################################################"
echo "#  TRIAGEM FORENSE: $F"
echo "############################################################"

echo ""; echo "=== [1] TIPO REAL (file) ==="
file "$F"

echo ""; echo "=== [2] METADADOS (exiftool) ==="
if have exiftool; then exiftool "$F"; else echo "(exiftool não instalado)"; fi

echo ""; echo "=== [3] STRINGS + busca de flag ==="
strings -n 5 "$F" | grep -iEa "$PAD" && echo "  ^ olha isso!" || echo "  (sem flag crua nas strings)"
echo "  -- primeiras strings longas (pode ter pista): --"
strings -n 8 "$F" | head -15

echo ""; echo "=== [4] ARQUIVOS EMBUTIDOS (binwalk) ==="
if have binwalk; then
  binwalk "$F"
  echo "  -- tentando extrair embutidos --"
  binwalk --dd='.*' -C /tmp/triage_extract "$F" >/dev/null 2>&1 && \
    echo "  extraído em /tmp/triage_extract (rode flag_hunter.sh lá!)" || echo "  (nada a extrair)"
else echo "(binwalk não instalado)"; fi

echo ""; echo "=== [5] ESTEGANOGRAFIA ==="
EXT="${F##*.}"
if have zsteg && echo "$EXT" | grep -qiE 'png|bmp'; then
  echo "  -- zsteg (LSB em PNG/BMP) --"; zsteg -a "$F" 2>/dev/null | grep -iEa "$PAD|text|ascii" | head -10
fi
if have steghide && echo "$EXT" | grep -qiE 'jpg|jpeg|bmp|wav'; then
  echo "  -- steghide com senha VAZIA --"
  steghide extract -sf "$F" -p "" -xf /tmp/steghide_out 2>/dev/null && \
    echo "  EXTRAIU! veja /tmp/steghide_out" || echo "  (senha vazia não abriu; tente senha do enunciado)"
fi
if have stegseek && echo "$EXT" | grep -qiE 'jpg|jpeg'; then
  echo "  -- stegseek (quebra senha steghide com rockyou, RÁPIDO) --"
  stegseek "$F" /usr/share/wordlists/rockyou.txt 2>/dev/null | head -5
fi

echo ""; echo "############################################################"
echo "#  Fim. Próximos passos sugeridos:"
echo "#   - achou embutido? -> cd /tmp/triage_extract && flag_hunter.sh ."
echo "#   - é imagem e nada apareceu? -> abra no StegOnline/Stegsolve, mexa nos bits"
echo "#   - é .pcap? -> use o Wireshark (veja 04-forense/GUIA.md)"
echo "############################################################"
