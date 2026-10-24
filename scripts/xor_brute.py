#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XOR BRUTE CORINGA — quebra XOR de chave única (1 byte) e tenta chaves curtas.

XOR é pão-de-cada-dia em cripto de CTF. Se o enunciado fala "XOR", ou se o
decoder.py não achou nada e o dado parece lixo binário/hex, tente este.

Uso:
    python3 xor_brute.py 1b2e3f...              # dado em HEX
    python3 xor_brute.py -f arquivo.bin         # dado de um arquivo binário
    python3 xor_brute.py -s "texto cru"         # dado como string crua

Faz:
    1) Brute force de TODAS as 256 chaves de 1 byte, mostra as que viram texto legível.
    2) Se você souber parte da flag (ex: "flag{"), recupera a chave por known-plaintext.
"""
import sys, re, binascii

FLAG_RE = re.compile(rb'(flag|fiap|ctf|key)\{', re.IGNORECASE)

def load():
    if len(sys.argv) >= 3 and sys.argv[1] == '-f':
        return open(sys.argv[2],'rb').read()
    if len(sys.argv) >= 3 and sys.argv[1] == '-s':
        return sys.argv[2].encode()
    if len(sys.argv) >= 2:
        h = re.sub(r'\s+','',sys.argv[1])
        return binascii.unhexlify(h)
    return sys.stdin.buffer.read()

def printable_ratio(b):
    if not b: return 0
    return sum(1 for c in b if 32<=c<127 or c in (9,10,13))/len(b)

def single_byte(data):
    print("=== Brute force de chave de 1 byte (0x00 a 0xFF) ===")
    hits = []
    for k in range(256):
        out = bytes(c ^ k for c in data)
        if FLAG_RE.search(out):
            print(f"  [chave 0x{k:02x} = {k}]  *** FLAG ***  {out[:80]}")
            hits.append(k)
        elif printable_ratio(out) > 0.9:
            print(f"  [chave 0x{k:02x} = {k}]  {out[:80]}")
    if not hits:
        print("  (nenhuma chave de 1 byte deu flag — tente chave maior abaixo)")

def known_plaintext(data, crib=b'flag{'):
    print(f"\n=== Recuperar chave sabendo que começa com {crib!r} ===")
    if len(data) < len(crib):
        print("  dado muito curto"); return
    key = bytes(data[i] ^ crib[i] for i in range(len(crib)))
    print(f"  Início da chave (hex): {key.hex()}")
    try: print(f"  Início da chave (txt): {key.decode('latin1')}")
    except Exception: pass
    # se a chave se repete, aplica ela inteira
    full = bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))
    print(f"  Texto com chave repetida: {full[:120]}")

def main():
    data = load()
    print(f"[*] {len(data)} bytes carregados.\n")
    single_byte(data)
    for crib in (b'flag{', b'fiap{', b'ctf{', b'FLAG{'):
        known_plaintext(data, crib)

if __name__ == '__main__':
    main()
