# 02 — OSINT & MISC (busca e desafios diversos)

> OSINT é investigação com fontes públicas. Não exige ferramenta especial, só
> curiosidade e método. Ótima categoria pra pontuar rápido e ganhar confiança.
> (Você já faz isso no projeto de sock puppet!)

---

## OSINT — achar informação sobre pessoa, lugar ou organização

### Se deram uma FOTO e pedem o local
1. **Olhe os metadados primeiro** (pode ter GPS de graça):
   ```bash
   exiftool foto.jpg | grep -i gps
   ```
2. **Busca reversa de imagem** (se tiver internet):
   - Google Images (ícone da câmera)
   - https://images.google.com
   - https://yandex.com/images  ← o Yandex costuma ser MELHOR pra lugares
3. **Pistas visuais:** placas, idioma das lojas, arquitetura, tipo de vegetação,
   lado da rua que os carros andam. Cruze com o Google Street View.

### Se deram um NOME ou USUÁRIO
```bash
# Procurar o mesmo username em centenas de sites
sherlock nome_de_usuario
```
Sem a ferramenta? Busque manualmente no Google, LinkedIn, GitHub, Instagram.

### Google Dorking (busca avançada — decore estes operadores)
```
site:fiap.com.br          → só resultados desse site
filetype:pdf senha        → só arquivos PDF contendo "senha"
inurl:admin               → URLs que contêm "admin"
intitle:"index of"        → listagens de diretório abertas
```

---

## MISC — desafios diversos (lógica, scripting, "pega-ratão")

Não tem categoria fixa. Leia o enunciado e pense fora da caixa:

- **Pede pra resolver rápido / muitas vezes?** → é scripting. Escreva um loop em Python.
- **QR code / código de barras?** → leia com o celular ou:
  ```bash
  zbarimg imagem.png     # lê QR codes e códigos de barras
  ```
- **Áudio estranho?** → pode ser Morse, DTMF (tons de telefone) ou um espectrograma.
  Abra no **Audacity** → veja o espectrograma (texto escondido aparece na imagem do som).
- **Arquivo gigante de texto / "ache a agulha"?** → use `grep`:
  ```bash
  grep -iE "flag|fiap|ctf" arquivo_gigante.txt
  ```

### Exemplo de script rápido (quando pede pra responder 1000 continhas)
```python
# Se o desafio manda você resolver operações matemáticas em sequência via rede
# (pwntools ajuda, mas pra matemática simples um loop resolve)
import re
# ... conecta, lê a conta, calcula, responde, repete
```

---

## CHECKLIST

- [ ] Se foto: chequei GPS no exiftool?
- [ ] Se foto: fiz busca reversa (Yandex pra lugares)?
- [ ] Se foto: olhei placas, idioma, arquitetura?
- [ ] Se nome/user: busquei em Google, GitHub, LinkedIn, redes?
- [ ] Usei os Google Dorks (site:, filetype:, inurl:)?
- [ ] Se QR/barras: li com zbarimg ou celular?
- [ ] Se áudio: olhei o espectrograma no Audacity?
- [ ] Reli o enunciado? Misc é onde a dica mais importa.
