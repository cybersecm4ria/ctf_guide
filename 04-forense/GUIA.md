# 04 — FORENSE & ESTEGANOGRAFIA (a sua casa)

> Você investiga um arquivo pra achar o que alguém escondeu. É o mesmo olhar que você usa
> no SOC analisando log: metódico, camada por camada. Confie no seu instinto aqui.

---

## PASSO 0 — Sempre comece por estes 4 comandos

Não importa o que te deram (imagem, pdf, áudio, arquivo sem extensão). Rode nesta ordem:

```bash
file arquivo.jpg
```
**Por quê:** mostra o TIPO REAL do arquivo, ignorando a extensão. Um `.jpg` que o `file`
diz ser um ZIP é a pista inteira do desafio. Extensão mente; o `file` não.

```bash
exiftool arquivo.jpg
```
**Por quê:** lê os metadados. Autor, comentário, GPS, software. Flags vivem no campo
"Comment" ou "Artist" com uma frequência que assusta. Olhe linha por linha.

```bash
strings -n 6 arquivo.jpg
```
**Por quê:** extrai todo texto legível de dentro do binário. `-n 6` = só sequências de 6+
caracteres (corta lixo). Muitas flags estão aqui, cruas. Combine com a busca:

```bash
strings arquivo.jpg | grep -iE "flag|fiap|ctf"
```

```bash
binwalk arquivo.jpg
```
**Por quê:** detecta se há **outro arquivo escondido dentro** (um ZIP dentro de um PNG,
por exemplo). Se achar algo, extraia com:

```bash
binwalk -e arquivo.jpg      # extrai pra uma pasta _arquivo.jpg.extracted/
```

> ⚠️ Se esses 4 comandos não acharam nada, NÃO desista — você só subiu as escadas.
> Continue pros passos específicos abaixo.

---

## SE FOR IMAGEM (png, jpg, bmp, gif)

```bash
# 1. Esteganografia clássica em PNG/BMP (bits escondidos nos pixels)
zsteg arquivo.png              # só PNG/BMP — testa todos os canais de bits de uma vez
zsteg -a arquivo.png           # modo agressivo, testa tudo

# 2. Estego com senha (JPG/BMP/WAV). Senha costuma estar no enunciado ou ser vazia
steghide extract -sf arquivo.jpg          # pede senha; tenta ENTER (vazia) primeiro
steghide info arquivo.jpg                 # mostra se há algo embutido

# 3. Olhar a imagem com outros olhos (online, se tiver internet)
#    Abra em: https://stegonline.georgeom.net  — mexe em planos de bits, canais RGB
```

**Ideia-chave:** abra a imagem num editor e aumente o brilho/contraste no máximo.
Texto branco em fundo branco aparece. Simples e funciona.

---

## SE FOR CAPTURA DE REDE (.pcap, .pcapng)

Isso é PURO SOC. Você já faz análise de tráfego.

```bash
# Abrir no Wireshark (interface gráfica — melhor jeito)
wireshark captura.pcap
```

Dentro do Wireshark, os reflexos:
1. **Botão direito num pacote → "Follow" → "TCP Stream"** — reconstrói a conversa inteira.
   A flag costuma estar numa requisição HTTP ou numa resposta.
2. Barra de filtro, digite `http` — vê só o tráfego web.
3. Filtro `http.request.method == "POST"` — dados enviados (login, upload).
4. **File → Export Objects → HTTP** — extrai arquivos que foram transferidos na rede.

Sem interface gráfica? Linha de comando:
```bash
tshark -r captura.pcap -Y "http"                    # filtra HTTP
strings captura.pcap | grep -iE "flag|fiap|ctf"     # força bruta rápida
```

---

## SE FOR ARQUIVO COMPACTADO (.zip, .rar) COM SENHA

```bash
# Quebrar senha de ZIP com wordlist (a rockyou é a clássica)
zip2john arquivo.zip > hash.txt
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
john hash.txt --show        # mostra a senha achada
```

---

## SE FOR DUMP DE MEMÓRIA (.raw, .mem, .vmem)

Avançado, mas é forense de verdade (seu futuro como perita!):
```bash
volatility3 -f dump.raw windows.info          # identifica o SO
volatility3 -f dump.raw windows.pslist        # processos que rodavam
volatility3 -f dump.raw windows.netscan       # conexões de rede
```

---

## SE FOR PDF ou DOCUMENTO

```bash
exiftool documento.pdf                 # metadados
strings documento.pdf | grep -i flag   # texto embutido
pdftotext documento.pdf saida.txt      # extrai todo o texto pra ler
```
Dica: texto escondido em PDF às vezes é só texto branco. Selecione tudo (Ctrl+A) no
leitor e cole num bloco de notas.

---

## CHECKLIST RÁPIDO (quando travar, releia)

- [ ] Rodei `file`, `exiftool`, `strings`, `binwalk`?
- [ ] A extensão bate com o tipo real?
- [ ] Olhei TODOS os campos de metadado?
- [ ] Se imagem: tentei `zsteg` e `steghide` (senha vazia)?
- [ ] Se imagem: aumentei brilho/contraste?
- [ ] Se pcap: segui o TCP stream e exportei objetos?
- [ ] Busquei o padrão da flag com `grep -iE "flag|fiap|ctf"`?
