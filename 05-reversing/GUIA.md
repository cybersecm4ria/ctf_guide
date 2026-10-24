# 05 — REVERSING (engenharia reversa)

> Deram um programa compilado (sem código-fonte) e você precisa entender o que ele faz:
> achar uma senha que ele verifica, burlar uma checagem. Categoria mais difícil — mas
> tem um atalho que resolve MUITO desafio fácil.

---

## PASSO 0 — O atalho que você faz ANTES de abrir qualquer ferramenta pesada

```bash
file programa          # é ELF (Linux)? PE (Windows)? 32 ou 64 bits?
strings programa | grep -iE "flag|fiap|ctf|senha|password"
```

**Por quê:** uma quantidade enorme de desafios fáceis deixa a flag ou a senha
**em texto puro dentro do binário**. O `strings` acha de graça. Tente SEMPRE isso primeiro,
antes de perder 1 hora decompilando.

---

## PASSO 1 — Rode o programa (com cuidado) pra ver o que ele pede

```bash
chmod +x programa      # dá permissão de execução
./programa             # roda e vê o comportamento
```
Ele pede uma senha? Mostra um menu? Entenda o que ele quer antes de atacar.

---

## PASSO 2 — Análise estática (ler o código sem rodar)

**Ghidra** (gratuito, da NSA) é a ferramenta principal. Ele pega o código de máquina e
transforma de volta em pseudocódigo parecido com C, que dá pra ler.

Fluxo no Ghidra:
1. New Project → importe o binário → deixe analisar (yes pra tudo).
2. Procure a função `main`.
3. Leia o pseudocódigo. Procure:
   - comparações de string (`strcmp`) → a senha que ele espera costuma estar ali do lado
   - uma string montada letra por letra → pode ser a flag sendo construída
   - um `if` que decide entre "Correto!" e "Errado!" → a condição é a resposta

Alternativa mais leve e online (se tiver internet): **https://dogbolt.org**
(cola o binário e vários decompiladores rodam de uma vez).

---

## PASSO 3 — Análise dinâmica (rodar observando a memória)

Quando a senha é verificada em tempo de execução:
```bash
gdb ./programa                 # debugger (com a extensão pwndbg fica melhor)
# dentro do gdb: coloca breakpoint na comparação e lê o valor esperado na memória
ltrace ./programa              # mostra chamadas de biblioteca (ex: o strcmp e o que compara)
```
**Dica de ouro:** `ltrace` às vezes mostra a senha correta sendo comparada com a sua,
na tela, sem você precisar entender assembly nenhum.

---

## CHECKLIST

- [ ] Rodei `strings | grep flag` ANTES de tudo?
- [ ] Rodei `file` pra saber o tipo?
- [ ] Executei o programa pra ver o que ele pede?
- [ ] Abri no Ghidra e li a função `main`?
- [ ] Procurei comparações de string (strcmp) e os `if` de certo/errado?
- [ ] Tentei `ltrace` pra ver a senha sendo comparada?

> Honestidade: reversing frustra no começo, é normal. Se travar e houver desafios de
> forense/web no painel, prefira aqueles. Volte aqui se sobrar tempo.
