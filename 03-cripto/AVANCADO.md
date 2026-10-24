# 03 — CRIPTO AVANÇADO

> Quando o CyberChef "Magic" e o decoder.py não resolvem sozinhos.
> Coringas: `scripts/decoder.py` (camadas) e `scripts/xor_brute.py` (XOR).

---

## XOR (muito comum em nível intermediário)

```bash
# Chave de 1 byte ou known-plaintext: use o coringa
python3 scripts/xor_brute.py <hex_da_cifra>
python3 scripts/xor_brute.py -f cifra.bin
```
XOR de chave repetida (multi-byte)? A ferramenta **xortool** acha o tamanho da chave:
```bash
xortool -c 20 cifra.bin        # -c = caractere mais comum (espaço=0x20 em texto)
```

---

## CIFRAS CLÁSSICAS — como quebrar cada uma

| Cifra | Como reconhecer | Como quebrar |
|-------|-----------------|--------------|
| César / ROT-N | letras deslocadas | decoder.py mostra as 25; ou dcode.fr |
| Vigenère | letras trocadas, com "chave" | dcode.fr (auto) ou https://www.guballa.de/vigenere-solver |
| Substituição | cada letra vira outra fixa | https://quipqiup.com (resolve sozinho) |
| Atbash | A↔Z, B↔Y | decoder.py |
| Base85/Base58 | parece base64 mas "errado" | CyberChef |
| Bacon | só A e B (ou dois símbolos) | dcode.fr "Bacon" |
| Railfence / transposição | letras certas, ordem errada | dcode.fr "Rail Fence" |

> Regra: **não reconheceu a cifra? Jogue no dcode.fr** — ele identifica
> automaticamente a maioria e já resolve.

---

## RSA — o catálogo de ataques

Em CTF, o RSA SEMPRE tem um erro de propósito. Identifique o cenário:

```bash
# Ferramenta coringa que testa TODOS os ataques conhecidos de uma vez:
python3 RsaCtfTool.py --publickey key.pub --uncipherfile flag.enc
python3 RsaCtfTool.py -n <N> -e <e> --uncipher <c> --attack all
```

Cenários clássicos (pra você entender o que ele faz):
- **e pequeno (e=3) e mensagem curta** → raiz cúbica de c. (`--attack cube_root`)
- **n pequeno** → fatore n em https://factordb.com (já vem fatorado) e calcule d.
- **p e q muito próximos** → ataque de Fermat. (`--attack fermat`)
- **d pequeno** → ataque de Wiener. (`--attack wiener`)
- **mesmo n, dois e diferentes** → common modulus.

Fatorar n manualmente (quando é pequeno):
```python
# cole N em factordb.com; com p e q:
from Crypto.Util.number import inverse, long_to_bytes
phi = (p-1)*(q-1)
d = inverse(e, phi)
m = pow(c, d, n)
print(long_to_bytes(m))
```

---

## HASHES

```bash
# Identificar
hashid '<hash>'
# Quebrar offline com GPU/CPU
hashcat -m 0 hash.txt /usr/share/wordlists/rockyou.txt      # -m 0 = MD5
john --format=raw-md5 hash.txt --wordlist=rockyou.txt
# Online (rápido pra hashes comuns): crackstation.net, hashes.com
```
Tipos de `-m` no hashcat: 0=MD5, 100=SHA1, 1400=SHA256, 1800=sha512crypt, 3200=bcrypt.

---

## AES

- **ECB** (blocos repetidos viram cifra repetida): ataque byte-a-byte quando você
  controla parte da entrada. Reconhece por blocos de 16 bytes idênticos na cifra.
- **CBC padding oracle**: se o servidor diz "padding inválido", dá pra decifrar tudo.
  Ferramenta: `padbuster`.

---

## QUANDO NADA FUNCIONA

- É esotérico? Brainfuck (`+++...`), Ook!, Malbolge → dcode.fr identifica e roda.
- Parece coordenadas / números estranhos → pode ser índice de livro, ASCII, ou
  posição no teclado. Pense lateral.
- Cole SEMPRE no CyberChef com "Magic" e aumente a profundidade (depth).
