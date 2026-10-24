# 06 — PWN (exploração binária) — AVANÇADO

> A categoria mais difícil. Você explora erros de memória num programa pra assumir o
> controle da execução. Exige C, assembly e noção de pilha/memória.
> **Estratégia honesta pra amanhã: deixe por último. Só encare se sobrar tempo.**

---

## Mas antes de ignorar: tente o atalho (igual reversing)

Às vezes o que o painel chama de "pwn fácil" é só:
```bash
file programa
strings programa | grep -iE "flag|fiap|ctf"
./programa              # e vê se dá pra "quebrar" só digitando muito texto
```
Se digitar um monte de letra (`AAAAAAAAAAAAA...`) faz o programa se comportar estranho
ou vazar algo, você já achou o ponto fraco (buffer overflow).

---

## O conceito central (pra você reconhecer, não dominar hoje)

**Buffer overflow:** o programa reserva um espaço pequeno pra sua entrada. Se você digita
mais do que cabe, o excesso "vaza" e sobrescreve o que vem depois na memória — inclusive
o endereço pra onde o programa volta. Controlando isso, você redireciona a execução
(muitas vezes pra uma função escondida que imprime a flag, chamada "ret2win").

---

## Ferramenta padrão (se for mesmo tentar)

```bash
# pwntools: a biblioteca que automatiza a comunicação com o programa
pip install pwntools

# esqueleto mínimo de um script de exploração:
python3 -c "
from pwn import *
p = process('./programa')      # ou remote('ip', porta) pra alvo na rede
p.sendline(b'A' * 100)         # envia 100 A's pra testar overflow
print(p.recvall())
"
```

Encontrar quantos bytes até estourar:
```bash
cyclic 200                     # gera padrão único; veja onde quebrou e calcule o offset
```

---

## CHECKLIST (versão realista pra primeira vez)

- [ ] Tentei o atalho `strings | grep flag`?
- [ ] Rodei e testei jogar MUITO texto (`AAAA...`) pra ver se quebra?
- [ ] Há desafio de forense/web/osint ainda aberto no painel? → faça aquele primeiro.
- [ ] Sobrou tempo E tenho colega que manja de C? → tentem o overflow juntos.

> Sem culpa nenhuma de pular pwn na estreia. Até gente experiente deixa por último.
> Seus pontos virão de forense, web, cripto e osint. Foque sua energia lá.
