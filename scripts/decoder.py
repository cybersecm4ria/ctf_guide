#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DECODER CORINGA — descasca codificações em camadas automaticamente.

Uso:
    python3 decoder.py "TEXTO_ESTRANHO_AQUI"
    echo "TEXTO" | python3 decoder.py
    python3 decoder.py -f arquivo.txt

O que ele tenta, recursivamente (até 12 camadas):
    base64, base32, hex, binário, URL-encode, ROT13, ROT-N (todas),
    Atbash, texto invertido, Morse, decimal-ASCII.
Sempre que o resultado contém algo tipo flag{...}/fiap{...}/ctf{...},
ele PARA e te mostra o caminho inteiro de como chegou lá.

Só usa biblioteca padrão do Python — roda em qualquer lugar, offline.
"""
import sys, base64, binascii, codecs, re, urllib.parse

FLAG_RE = re.compile(r'(flag|fiap|ctf|key|secret)\{[^}]{1,80}\}', re.IGNORECASE)

MORSE = {
    '.-':'A','-...':'B','-.-.':'C','-..':'D','.':'E','..-.':'F','--.':'G',
    '....':'H','..':'I','.---':'J','-.-':'K','.-..':'L','--':'M','-.':'N',
    '---':'O','.--.':'P','--.-':'Q','.-.':'R','...':'S','-':'T','..-':'U',
    '...-':'V','.--':'W','-..-':'X','-.--':'Y','--..':'Z','-----':'0',
    '.----':'1','..---':'2','...--':'3','....-':'4','.....':'5','-....':'6',
    '--...':'7','---..':'8','----.':'9'
}

def printable_ratio(s):
    if not s: return 0
    ok = sum(1 for c in s if 32 <= ord(c) < 127 or c in '\n\t')
    return ok/len(s)

def try_base64(s):
    s2 = s.strip()
    if len(s2) < 4 or len(s2) % 4 != 0: return None
    if not re.fullmatch(r'[A-Za-z0-9+/=]+', s2): return None
    try:
        out = base64.b64decode(s2, validate=True).decode('utf-8','replace')
        return out if printable_ratio(out) > 0.85 and out != s2 else None
    except Exception: return None

def try_base32(s):
    s2 = s.strip().upper()
    if not re.fullmatch(r'[A-Z2-7=]+', s2) or len(s2) < 8: return None
    try:
        out = base64.b32decode(s2).decode('utf-8','replace')
        return out if printable_ratio(out) > 0.85 else None
    except Exception: return None

def try_hex(s):
    s2 = re.sub(r'\s+','',s.strip())
    if not re.fullmatch(r'[0-9a-fA-F]+', s2) or len(s2) < 4 or len(s2)%2: return None
    try:
        out = binascii.unhexlify(s2).decode('utf-8','replace')
        return out if printable_ratio(out) > 0.85 else None
    except Exception: return None

def try_binary(s):
    bits = re.sub(r'[^01]','',s)
    if len(bits) < 8 or len(bits)%8: return None
    try:
        out = ''.join(chr(int(bits[i:i+8],2)) for i in range(0,len(bits),8))
        return out if printable_ratio(out) > 0.85 else None
    except Exception: return None

def try_url(s):
    if '%' not in s: return None
    out = urllib.parse.unquote(s)
    return out if out != s else None

def try_rot13(s):
    out = codecs.encode(s,'rot_13')
    return out if out != s else None

def try_atbash(s):
    def f(c):
        if 'a'<=c<='z': return chr(ord('z')-(ord(c)-ord('a')))
        if 'A'<=c<='Z': return chr(ord('Z')-(ord(c)-ord('A')))
        return c
    out = ''.join(f(c) for c in s)
    return out if out != s else None

def try_reverse(s):
    return s[::-1]

def try_decimal(s):
    nums = re.findall(r'\d{1,3}', s)
    if len(nums) < 3: return None
    try:
        vals = [int(n) for n in nums]
        if all(0 <= v < 256 for v in vals):
            out = ''.join(chr(v) for v in vals)
            return out if printable_ratio(out) > 0.85 else None
    except Exception: return None
    return None

def try_morse(s):
    if not re.fullmatch(r'[.\-/\s]+', s.strip()): return None
    words = s.strip().split('/')
    try:
        out = ' '.join(''.join(MORSE.get(c,'?') for c in w.split()) for w in words)
        return out if '?' not in out and out.strip() else None
    except Exception: return None

def all_caesar(s):
    """Retorna lista de (deslocamento, texto) pra TODAS as 25 rotações."""
    res = []
    for shift in range(1,26):
        out = []
        for c in s:
            if 'a'<=c<='z': out.append(chr((ord(c)-ord('a')+shift)%26+ord('a')))
            elif 'A'<=c<='Z': out.append(chr((ord(c)-ord('A')+shift)%26+ord('A')))
            else: out.append(c)
        res.append((shift, ''.join(out)))
    return res

CODECS = [
    ('base64', try_base64), ('base32', try_base32), ('hex', try_hex),
    ('binario', try_binary), ('url', try_url), ('rot13', try_rot13),
    ('atbash', try_atbash), ('decimal', try_decimal), ('morse', try_morse),
    ('reverso', try_reverse),
]

def search(text, path=None, depth=0, seen=None):
    if path is None: path = []
    if seen is None: seen = set()
    if depth > 12 or text in seen: return
    seen.add(text)

    m = FLAG_RE.search(text)
    if m:
        print("\n" + "="*60)
        print("  >>> POSSÍVEL FLAG ENCONTRADA <<<")
        print("  Flag:", m.group(0))
        print("  Caminho:", " -> ".join(path) if path else "(texto original)")
        print("  Texto completo:", text[:200])
        print("="*60)
        return

    for name, fn in CODECS:
        try:
            out = fn(text)
        except Exception:
            out = None
        if out and out not in seen:
            search(out, path+[name], depth+1, seen)

    # César é tratado à parte (gera 25 saídas)
    if depth < 3:
        for shift, out in all_caesar(text):
            if FLAG_RE.search(out):
                print(f"\n[CESAR shift={shift}] {out[:200]}")
            if out not in seen and depth < 2:
                # só aprofunda nas rotações que viram texto plausível
                pass

def main():
    if len(sys.argv) >= 3 and sys.argv[1] == '-f':
        data = open(sys.argv[2], 'r', errors='replace').read().strip()
    elif len(sys.argv) >= 2:
        data = sys.argv[1]
    else:
        data = sys.stdin.read().strip()

    print(f"[*] Entrada ({len(data)} chars): {data[:80]}...")
    print("[*] Testando codificações em camadas...\n")

    # mostra as 25 rotações de César logo de cara (muito comum)
    print("--- Todas as rotações de César (procure a legível) ---")
    for shift, out in all_caesar(data):
        marca = "  <-- FLAG!" if FLAG_RE.search(out) else ""
        print(f"  [{shift:2d}] {out[:70]}{marca}")
    print()

    search(data)
    print("\n[*] Fim. Se nada apareceu como FLAG, o texto pode precisar de uma")
    print("    ferramenta específica (XOR, Vigenère, RSA). Veja 03-cripto/AVANCADO.md")

if __name__ == '__main__':
    main()
