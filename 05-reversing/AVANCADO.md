# 05 — REVERSING AVANÇADO

> Além do `strings`. Coringa: muitas vezes o **angr** resolve o crackme sozinho.

---

## FLUXO COMPLETO

```bash
file programa              # tipo, arquitetura, se está "stripped" (sem nomes)
checksec --file=programa   # proteções
./programa                 # comportamento
ltrace ./programa          # chamadas de biblioteca (strcmp mostra a senha!)
strace ./programa          # chamadas de sistema (arquivos que ele abre)
```

**O truque do ltrace:** se o programa compara sua senha com a correta usando `strcmp`,
o `ltrace` imprime as DUAS strings sendo comparadas. A senha certa aparece de graça.

---

## GHIDRA (análise estática séria)

1. Import → analisa tudo → abra `main` na janela "Decompile".
2. Procure:
   - `strcmp`/`memcmp` → o segundo argumento costuma ser a senha esperada.
   - laços que montam uma string caractere por caractere → a flag sendo construída.
   - `if` que separa "Correct"/"Wrong" → a condição É a solução.
3. Renomeie variáveis (tecla L) pra ir entendendo. Mude tipos (tecla T).

Online e rápido: **https://dogbolt.org** roda Ghidra+IDA+outros de uma vez no binário.

---

## ANGR — resolver crackme AUTOMATICAMENTE (o grande coringa de RE)

angr faz execução simbólica: você diz "quero chegar no 'Correct'" e ele CALCULA a
entrada que leva lá. Resolve muitos crackmes sem você ler assembly.

```python
import angr, claripy
proj = angr.Project('./programa', auto_load_libs=False)

# endereços: veja no Ghidra o endereço do print "Correct" (good) e do "Wrong" (bad)
GOOD = 0x401234   # <<< endereço do caminho de sucesso
BAD  = 0x401250   # <<< endereço do caminho de falha

simgr = proj.factory.simgr(proj.factory.full_init_state())
simgr.explore(find=GOOD, avoid=BAD)
if simgr.found:
    print(simgr.found[0].posix.dumps(0))   # a entrada que resolve (a flag!)
```

---

## PYTHON COMPILADO (.exe feito com PyInstaller, ou .pyc)

```bash
# Extrair um .exe PyInstaller de volta pros .pyc:
python3 pyinstxtractor.py programa.exe
# Decompilar .pyc pra código Python legível:
pip install decompyle3 ;  decompyle3 arquivo.pyc
# (alternativa) uncompyle6 arquivo.pyc
```

---

## .NET (C#) — se o `file` disser "Mono/.Net assembly"

Use **dnSpy** (Windows) ou **ilspycmd**: ele mostra o código C# praticamente original.
Muitas vezes a flag está escrita ali, legível.

---

## RADARE2 / rizin (alternativa ao Ghidra no terminal)

```bash
r2 -A programa      # analisa
> afl               # lista funções
> pdf @ main        # desassembla a main
> iz                # strings
```

---

## CHECKLIST AVANÇADO

- [ ] `ltrace` mostrou a senha num strcmp?
- [ ] Ghidra: achei o strcmp / o if de certo-errado?
- [ ] É crackme com "Correct/Wrong"? → tentei angr (resolve sozinho)?
- [ ] É Python empacotado? → extraí e decompilei?
- [ ] É .NET? → abri no dnSpy?
