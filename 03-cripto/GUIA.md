# 03 — CRIPTOGRAFIA & CODIFICAÇÃO

> O jogo aqui é RECONHECER o que você tem na frente, e descascar camada por camada.
> Iniciante raramente precisa de matemática pesada — precisa identificar a codificação.

---

## PASSO 0 — Jogue no CyberChef e use a varinha mágica

Se tiver internet, este é o atalho que resolve metade dos desafios:

1. Abra **https://gchq.github.io/CyberChef/**
2. Cole o texto estranho no campo "Input"
3. Arraste a operação **"Magic"** pra receita (ou procure "Magic" na busca)
4. Ele tenta detectar e decodificar automaticamente, em camadas.

Sem internet? Use os comandos abaixo.

---

## PASSO 1 — Identifique a codificação pelo visual

| O texto parece... | É provavelmente... | Como decodificar |
|-------------------|--------------------|--------------------|
| Termina com `=` ou `==`, letras+números+/ | **Base64** | `echo "texto" \| base64 -d` |
| Só 0-9 e a-f (ex: `666c6167`) | **Hexadecimal** | `echo "666c6167" \| xxd -r -p` |
| Só 0 e 1 | **Binário** | CyberChef "From Binary" |
| Letras embaralhadas, mesmo tamanho | **Cifra de César / ROT13** | ver abaixo |
| `%41%42` | **URL encoding** | CyberChef "URL Decode" |
| `.... . .-..` | **Código Morse** | CyberChef "From Morse Code" |

> 💡 O "666c6167" do exemplo começa com `666c6167` que é "flag" em hex. Sempre que o
> hex começar assim, você está no caminho. Decodifica e vê o resto.

---

## PASSO 2 — Decodificação em CAMADAS (o truque mais comum)

Desafios de cripto empilham codificações. Exemplo real:

```bash
# 1. Chega uma string base64:
echo "NjY2YzYxNjc3YjY4MzM3ODVmMzE2ZTVmNjIzNjM0N2Q=" | base64 -d
# resultado: 666c61677b68337...  (vira hexadecimal!)

# 2. Agora decodifica o hex:
echo "666c61677b68337835..." | xxd -r -p
# resultado: flag{...}  🎯
```

**A regra de ouro:** decodificou e ainda parece embaralhado? NÃO é o fim.
É outra camada. Continue decodificando até aparecer a flag legível.

---

## PASSO 3 — Cifras clássicas (quando as letras estão trocadas)

```bash
# ROT13 (cada letra anda 13 casas) — muito comum
echo "synt" | tr 'A-Za-z' 'N-ZA-Mn-za-m'

# César (anda N casas): se tiver internet, use
# https://www.dcode.fr/caesar-cipher  → ele testa todas as 25 rotações de uma vez
```

Para QUALQUER cifra clássica que você não reconhece, o site **dcode.fr** é salva-vidas:
cole o texto e ele tenta identificar automaticamente (César, Vigenère, Atbash, etc).

---

## PASSO 4 — Hashes (texto de tamanho fixo, parece aleatório)

```bash
# Identificar o tipo de hash
hashid "5f4dcc3b5aa765d61d8327deb882cf99"
hash-identifier

# Muitas vezes o hash já foi quebrado por alguém — cole em:
# https://crackstation.net   (se tiver internet)
```

---

## PASSO 5 — RSA (quando aparecem n, e, c)

Em CTF o RSA sempre tem um ERRO proposital (números pequenos, chave fraca).
Não tente quebrar na mão. Use a ferramenta que testa todos os ataques conhecidos:
```bash
# RsaCtfTool faz o trabalho pesado
python3 RsaCtfTool.py --publickey chave.pub --uncipherfile cifra.bin
```

---

## CHECKLIST (releia quando travar)

- [ ] Joguei no CyberChef com "Magic"?
- [ ] Identifiquei a codificação pela tabela (termina em `=`? só hex? só binário?)
- [ ] Decodifiquei e o resultado AINDA parece código? → é outra camada, continue!
- [ ] Se são letras trocadas: testei ROT13 e joguei no dcode.fr?
- [ ] Se é hash: identifiquei o tipo e tentei o crackstation?
- [ ] O enunciado dá o nome da cifra? Usa isso.
