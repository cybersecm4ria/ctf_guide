# MAPA MENTAL CTF — Guia de Campo

> Abra este arquivo primeiro. Ele te diz, para qualquer desafio, **por onde começar e qual pasta abrir**.
> Feito para a primeira vez num CTF. Calma: ninguém resolve tudo. Achar 2 ou 3 flags já é vitória.

---

## 1. Antes de qualquer coisa: leia o enunciado como detetive

O título e a descrição quase SEMPRE escondem a dica da técnica. Trocadilho é pista.

- "Cookie Monster" → é web, olhe os **cookies**.
- "Read between the lines" / "hidden" → **esteganografia**.
- "Can you decode this?" → **cripto / codificação**.
- "Where was this photo taken?" → **OSINT**.
- Deu um **arquivo** pra baixar → quase sempre **forense**.
- Deu um **link / site** → **web**.
- Deu um **programa / binário** (.exe, ELF, sem extensão) → **reversing** ou **pwn**.

---

## 2. A flag tem formato

Você está procurando algo como `FLAG{...}`, `FIAP{...}`, `CTF{...}`.
Isso te diz **quando você achou**. Quando bater o olho nesse formato, é ela.

Guarde este comando na cabeça — procura o padrão da flag em qualquer arquivo de texto ou saída:

```bash
grep -rniE "flag\{|fiap\{|ctf\{" .
```

---

## 3. Árvore de decisão (o mapa)

```
            O que o desafio me deu?
                      |
   ┌──────────┬───────┼────────┬───────────┬──────────┐
   |          |       |        |           |          |
 um SITE   um ARQUIVO  um    um PROGRAMA  uma FOTO   um TEXTO
 /link     (img, pcap, TEXTO  (binário)   /pessoa    estranho
           zip, doc)  cifrado                        /lugar
   |          |       |        |           |          |
 01-web   04-forense 03-cripto 05-reversing 02-osint  03-cripto
                               06-pwn       02-osint
```

Na dúvida de categoria? Rode primeiro os 4 comandos de forense (pasta `04-forense`)
em qualquer arquivo. Eles revelam a natureza do que você tem nas mãos.

---

## 4. As 6 categorias (ordem do mais fácil pro mais difícil PRA VOCÊ)

| # | Pasta | Categoria | Por que começar aqui |
|---|-------|-----------|----------------------|
| 1 | `04-forense` | **Forense & Estego** | É a SUA casa. SIEM, log, análise de arquivo. Comece por aqui. |
| 2 | `01-web` | **Web** | Você já viu SSTI/SQLi em lab. Primeiros 60s no DevTools resolvem muita coisa. |
| 3 | `02-osint-misc` | **OSINT & Misc** | Busca e metadados. Vitórias rápidas, dá confiança. |
| 4 | `03-cripto` | **Cripto** | Reconhecer a codificação é 90% do jogo. CyberChef faz quase sozinho. |
| 5 | `05-reversing` | **Reversing** | Mais difícil. Mas `strings` no binário às vezes entrega a flag de graça. |
| 6 | `06-pwn` | **Pwn** | A mais difícil. Deixe por último. Tente só se sobrar tempo. |

---

## 5. Estratégia de prova (combine com o grupo)

1. **Varra o painel inteiro primeiro.** Anote quais desafios são de quais categorias.
2. **Dividam por afinidade.** Você pega **Forense** e **Web**. Colega de cripto pega cripto.
3. **Comece pelos de menor pontuação** (= mais fáceis). Pontue cedo, ganhe moral.
4. **Regra dos 25 minutos:** travou? Marca, pula, volta depois. Não afunda num só.
5. **Leu o enunciado 2x?** A dica tá lá. Releia antes de desistir.
6. **Submeteu errado?** Confere o formato da flag (maiúscula/minúscula, chaves, espaços).

---

## 6. Pastas deste repositório

Cada categoria tem DOIS arquivos: `GUIA.md` (básico, por onde começar) e
`AVANCADO.md` (técnicas de nível de final de campeonato).

- `01-web/` — exploração web (SQLi, SSTI→RCE, LFI, SSRF, JWT, upload…)
- `02-osint-misc/` — busca, metadados, geolocalização, misc
- `03-cripto/` — decodificação em camadas, XOR, RSA, cifras
- `04-forense/` — arquivos, pcap, estego, memória, carving **(sua força)**
- `05-reversing/` — binários, Ghidra, angr, ltrace
- `06-pwn/` — exploração de memória (ret2win, ROP, format string)
- `ferramentas/` — cola de instalação e links salva-vidas
- `scripts/` — **SCRIPTS CORINGA** pra rodar na hora (veja abaixo)

## 7. Scripts coringa (pasta `scripts/`) — rode na hora

| Script | Pra quê | Como rodar |
|--------|---------|------------|
| `decoder.py` | descasca base64/hex/binário/césar/morse em camadas e acha a flag | `python3 scripts/decoder.py "TEXTO"` |
| `xor_brute.py` | quebra XOR de 1 byte e por known-plaintext | `python3 scripts/xor_brute.py <hex>` |
| `flag_hunter.py`→`.sh` | varre pasta inteira (texto, binário, base64) atrás da flag | `bash scripts/flag_hunter.sh .` |
| `forense_triage.sh` | roda file+exif+strings+binwalk+estego de uma vez num arquivo | `bash scripts/forense_triage.sh arq.jpg` |
| `web_recon.sh` | recon de alvo web (robots, comentários, caminhos, cookies) | `bash scripts/web_recon.sh http://alvo:porta` |
| `pwn_template.py` | esqueleto de exploit pwntools (ret2win) pra preencher | editar e `python3 scripts/pwn_template.py` |

> Fluxo rápido pra arquivo misterioso: `forense_triage.sh arq` → se achar embutidos,
> `flag_hunter.sh /tmp/triage_extract` → se achar texto cifrado, `decoder.py`.

---

> Maria, você sabe mais do que o medo deixa ver. Forense é literalmente o seu trabalho.
> Respira, lê o enunciado, abre a pasta certa, segue a lista. Você consegue.
