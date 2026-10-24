# 02 — OSINT & MISC AVANÇADO

---

## OSINT — técnicas que ganham desafio difícil

### Geolocalização de foto (quando não tem GPS no exif)
- **Yandex** reverse image > Google pra lugares. Teste também Bing Visual Search.
- Pistas: formato de placas de carro/rua (cada país tem o seu), postes, hidrantes,
  idioma, faixa de pedestre, lado da direção, tipo de vegetação/clima.
- **GeoGuessr-style:** procure por nomes de loja no Google Maps da região suspeita.
- Sombras indicam hemisfério e hora aproximada.

### Pessoa / username
```bash
sherlock usuario              # procura o user em centenas de sites
holehe email@alvo.com         # descobre em quais sites o email tem conta
```
- Email → busque em vazamentos (haveibeenpwned), Gravatar, GitHub commits
  (`git log` mostra emails de autores).
- Foto de perfil → busca reversa.

### Google Dorking pesado
```
site:alvo.com ext:sql | ext:log | ext:bak
intitle:"index of" "parent directory"
inurl:"/.git/config"
"flag{" site:pastebin.com
```
Combine com **Wayback Machine** (web.archive.org) pra ver versões antigas da página
(a flag pode ter sido apagada mas estar no histórico).

### Metadados em documento
```bash
exiftool arquivo.pdf           # autor, software, datas
exiftool -ee -G3 arquivo.*     # extrai metadados embutidos profundos
```

---

## MISC — reconhecer rápido

| Sinal | É provavelmente | Ação |
|-------|-----------------|------|
| `+++++[->++...` | Brainfuck | dcode.fr roda |
| imagem de QR/barras | código | `zbarimg img.png` ou celular |
| áudio | Morse/DTMF/espectrograma | Audacity → espectrograma |
| muitas interações rápidas via rede | precisa de script | pwntools (abaixo) |
| texto `()()()[]` gigante | JSFuck | cole no console do navegador |
| xadrez / PGN | esteganografia em jogo | ferramentas de chess stego |

### Script pra desafio de rede que pede respostas rápidas
```python
from pwn import *
p = remote('host', porta)
while True:
    linha = p.recvline().decode()
    print(linha)
    # ex: se pedir pra resolver "3 + 4 ="
    import re
    m = re.search(r'(\d+)\s*([+\-*])\s*(\d+)', linha)
    if m:
        a,op,b = int(m.group(1)), m.group(2), int(m.group(3))
        r = {'+':a+b,'-':a-b,'*':a*b}[op]
        p.sendline(str(r).encode())
```

### QR/Barras
```bash
zbarimg imagem.png             # lê qualquer QR ou código de barras
```

---

## CHECKLIST

- [ ] Foto: GPS no exif? busca reversa no Yandex? pistas visuais?
- [ ] Wayback Machine na URL do alvo?
- [ ] Username/email: sherlock, holehe, GitHub?
- [ ] Texto esquisito: identifiquei a linguagem (dcode.fr)?
- [ ] Desafio de velocidade: montei um loop com pwntools?
