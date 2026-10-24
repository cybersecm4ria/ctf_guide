# FERRAMENTAS — instalação e links salva-vidas

---

## Instalar tudo de uma vez (Linux / Kali)

Se você estiver em Kali, quase tudo já vem instalado. Pra garantir, rode:

```bash
sudo apt update && sudo apt install -y \
  binwalk steghide exiftool foremost scalpel \
  gobuster ffuf john hashcat hashid sqlmap \
  wireshark tshark \
  gdb ltrace strace radare2 \
  zbar-tools audacity \
  stegseek outguess

# vêm por outros gerenciadores:
sudo gem install zsteg
pip install pwntools angr                 # pwn + resolver crackme automático
pip install pycryptodome                  # RSA/AES em Python

# ferramentas em git (clone se precisar):
#   RsaCtfTool, xortool, jwt_tool, pyinstxtractor, ROPgadget, Ghidra, Stegsolve

# wordlist rockyou (pra quebrar senhas) — descompacte se necessário:
sudo gunzip /usr/share/wordlists/rockyou.txt.gz 2>/dev/null
```

## Ferramentas avançadas por categoria (instalação rápida)

```bash
pip install ROPgadget                      # pwn: gadgets pra ROP
pip install uncompyle6 decompyle3          # reversing: decompila .pyc
# angr já instalado acima (reversing: execução simbólica)
# RsaCtfTool: git clone https://github.com/RsaCtfTool/RsaCtfTool
# xortool:    pip install xortool
# jwt_tool:   git clone https://github.com/ticarpi/jwt_tool
```

Testar se um comando existe:
```bash
which binwalk exiftool steghide wireshark   # mostra o caminho de cada um que existe
```

---

## SITES SALVA-VIDAS (quando houver internet)

| Pra quê | Site |
|---------|------|
| **Decodificar qualquer coisa** (base64, hex, cifras, em camadas) | https://gchq.github.io/CyberChef/ |
| **Identificar e quebrar cifras clássicas** | https://www.dcode.fr |
| **Esteganografia em imagem** (planos de bit, canais) | https://stegonline.georgeom.net |
| **Decodificar / inspecionar JWT** | https://jwt.io |
| **Quebrar hash** (procura em bancos vazados) | https://crackstation.net |
| **Busca reversa de imagem** (ótimo pra lugares) | https://yandex.com/images |
| **Decompilar binário online** | https://dogbolt.org |
| **Identificar tipo de hash** | https://hashes.com/en/tools/hash_identifier |

> Guarde esta tabela aberta numa aba. Metade dos desafios de cripto e estego cai aqui.

---

## A ÚNICA linha de comando que você precisa decorar

Em QUALQUER arquivo ou saída de texto, pra caçar a flag:

```bash
grep -rniE "flag\{|fiap\{|ctf\{" .
```
- `-r` entra em todas as subpastas
- `-n` mostra o número da linha
- `-i` ignora maiúscula/minúscula
- `-E` permite o padrão com `{`

---

## Se NÃO tiver internet e só o repositório Git

Tudo bem — os comandos de terminal deste repo (`file`, `strings`, `exiftool`, `binwalk`,
`zsteg`, `steghide`, `grep`, `xxd`, `base64`) funcionam 100% offline.
Os sites são atalhos; os comandos são a base. Você está coberta nos dois cenários.
