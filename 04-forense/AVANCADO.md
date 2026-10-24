# 04 — FORENSE AVANÇADO

> Quando os 4 comandos básicos não bastam. Aqui mora o nível de final de campeonato.
> Coringa: `bash scripts/forense_triage.sh arquivo` roda metade disso sozinho.

---

## ESTEGANOGRAFIA — arsenal completo

```bash
# stegseek: quebra senha de steghide com wordlist em SEGUNDOS (o favorito dos pros)
stegseek arquivo.jpg /usr/share/wordlists/rockyou.txt

# zsteg agressivo (PNG/BMP) — testa TODOS os planos de bit e canais
zsteg -a arquivo.png
zsteg -E 'b1,rgb,lsb,xy' arquivo.png   # extrai um canal específico

# outguess (outro algoritmo de estego em JPG)
outguess -r arquivo.jpg saida.txt

# exiftool extraindo thumbnail embutida (às vezes a imagem original tem a flag)
exiftool -b -ThumbnailImage arquivo.jpg > thumb.jpg

# Stegsolve (Java, gráfico): abre e navega por planos de bit com as setas.
#   java -jar stegsolve.jar
```

**Imagem que não entrega nada?** Pistas por tipo:
- PNG: cheque se há dados DEPOIS do chunk IEND (`binwalk` mostra).
- JPG: cheque dados depois do marcador FFD9.
- GIF: pode ter frames escondidos — separe os frames.
- Dois arquivos quase iguais? Faça `cmp -l a.png b.png` pra ver a diferença.

---

## ÁUDIO (wav, mp3)

```bash
# Ver o espectrograma (texto escondido aparece desenhado no som!)
#   Abra no Audacity ou Sonic Visualiser -> modo espectrograma
# Morse/DTMF escondido? ouça devagar ou:
strings arquivo.wav | grep -iE "flag|fiap"
```

---

## CARVING — recuperar arquivos escondidos/deletados

```bash
foremost -i imagem.dd -o saida/       # recupera por assinatura (jpg, zip, pdf...)
scalpel arquivo.bin -o saida/
binwalk --dd='.*' arquivo             # extrai TUDO que reconhecer
```

---

## PCAP AVANÇADO (análise de rede)

```bash
# Extrair credenciais de um pcap automaticamente
tshark -r cap.pcap -Y "http.request" -T fields -e http.host -e http.request.uri
# Senhas/forms em POST:
tshark -r cap.pcap -Y "http.request.method==POST" -T fields -e http.file_data

# Exportar TODOS os arquivos transferidos via HTTP
tshark -r cap.pcap --export-objects http,saida_http/

# USB capturado? (teclado) — reconstruir o que foi digitado:
tshark -r cap.pcap -Y "usb.capdata" -T fields -e usb.capdata
#  -> cada linha é um código de tecla; há scripts prontos (usbkeyboard) que traduzem

# TLS/HTTPS com chave de sessão (se deram o arquivo keylog):
#  Wireshark -> Preferences -> TLS -> (Pre)-Master-Secret log filename
```

No Wireshark (gráfico), os filtros de ouro:
- `http contains "flag"` — acha a flag no tráfego direto
- `ftp` / `telnet` — protocolos sem criptografia, senha em texto puro
- Statistics → Conversations — vê quem falou com quem
- Statistics → Protocol Hierarchy — vê o que tem no arquivo

---

## FORENSE DE MEMÓRIA (Volatility 3) — seu futuro de perita

```bash
vol -f dump.raw windows.info              # identifica SO/versão
vol -f dump.raw windows.pslist            # processos
vol -f dump.raw windows.cmdline           # linha de comando de cada processo (ouro)
vol -f dump.raw windows.netscan           # conexões de rede
vol -f dump.raw windows.filescan          # arquivos na memória
vol -f dump.raw windows.dumpfiles --virtaddr <addr>   # extrai um arquivo
vol -f dump.raw windows.hashdump          # hashes de senha do Windows
vol -f dump.raw windows.malfind           # injeção de código / malware
```

---

## DISCO / SISTEMA DE ARQUIVOS (Sleuth Kit)

```bash
mmls imagem.dd                 # tabela de partições
fls -r imagem.dd               # lista arquivos (inclusive deletados, marcados com *)
icat imagem.dd <inode>         # extrai o conteúdo de um arquivo pelo inode
```

---

## PISTAS QUE GENTE NOVA ESQUECE

- **Repositório Git dado?** `git log --all`, `git stash list`, `git show <commit>`.
  Flag costuma estar num commit antigo ou revertido.
- **Documento Office (.docm/.xlsm)?** macro maliciosa: `olevba arquivo.docm`.
- **Vários arquivos iguais?** compare com `cmp` ou `diff`.
- **Nome do arquivo / timestamps** às vezes SÃO a pista (data vira chave, etc).
