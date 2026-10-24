# 01 — WEB (exploração de aplicações web)

> Você já viu SSTI e SQLi em lab. Aqui você olha o site com olhos de atacante.
> A regra: o criador do desafio ESCONDEU a flag em algum lugar. Sempre tem pista.

---

## PASSO 0 — Os primeiros 60 segundos (faça SEMPRE)

Abriu o site? Antes de qualquer ataque, olhe:

1. **Código-fonte** (Ctrl+U no navegador)
   Procure comentários HTML (`<!-- ... -->`), inputs escondidos (`type="hidden"`),
   caminhos de admin esquecidos. Devs deixam flag em comentário o tempo todo.

2. **DevTools** (F12) → aba **Console** e aba **Sources**
   Às vezes a flag está num arquivo `.js` carregado pela página.

3. **DevTools → aba Application → Cookies**
   Olhe os cookies. Um cookie `admin=false` que vira `admin=true` abre portas.
   Cookie que parece embaralhado? Pode ser base64 ou JWT — decodifique (ver `03-cripto`).

4. **Arquivos "escondidos" que quase todo site tem:**
   Adicione na URL, um de cada vez:
   ```
   /robots.txt          ← lista caminhos que o dono não quer indexados (ouro)
   /.git/               ← código-fonte vazado
   /sitemap.xml
   /admin   /login   /backup   /flag   /flag.txt
   ```

---

## PASSO 1 — Teste as injeções clássicas

### SQL Injection (burlar login / extrair dados)
No campo de usuário ou senha, teste:
```
' OR 1=1 --
' OR '1'='1
admin' --
```
**Por quê:** se o login não valida a entrada, isso transforma a consulta em "sempre
verdadeiro" e te loga sem senha. O `--` comenta o resto da query.

### XSS (injeção de JavaScript)
Em campos de busca ou comentário, teste:
```
<script>alert(1)</script>
```
Se aparecer o alerta, o site é vulnerável. Em CTF costuma ser prova de conceito.

### SSTI (você já fez em lab!)
Em campos que refletem seu texto na página, teste:
```
{{7*7}}
${7*7}
```
**Por quê:** se a página mostrar `49`, o servidor está executando o que você digita
(template injection). Daí dá pra escalar pra ler arquivos / executar comando.

### Directory Traversal (ler arquivos do servidor)
Em parâmetros de URL tipo `?file=foto.png`, teste trocar por:
```
?file=../../../../etc/passwd
```
**Por quê:** os `../` sobem de pasta. Se o site não filtra, você lê arquivos do sistema.

---

## PASSO 2 — Ferramentas

```bash
# Descobrir páginas/pastas escondidas por força bruta
gobuster dir -u http://alvo.com -w /usr/share/wordlists/dirb/common.txt
ffuf -u http://alvo.com/FUZZ -w /usr/share/wordlists/dirb/common.txt

# Ver cabeçalhos e redirecionamentos de uma requisição
curl -i http://alvo.com

# Baixar a página pra inspecionar offline
curl http://alvo.com -o pagina.html
```

**Burp Suite** (se tiver instalado): intercepta e modifica requisições.
Serve pra mudar valores que o navegador não deixa (preço, id de usuário, flag `admin`).

---

## PASSO 3 — Se tiver internet, decodificadores online

- Decodificar cookie/token: cole no **CyberChef** (https://gchq.github.io/CyberChef/)
- Decodificar JWT: **https://jwt.io** — mostra o conteúdo do token

---

## CHECKLIST (releia quando travar)

- [ ] Olhei o código-fonte (Ctrl+U) atrás de comentários?
- [ ] Vi `/robots.txt` e tentei `/admin`, `/flag.txt`?
- [ ] Inspecionei os cookies? Algum parece base64/JWT?
- [ ] Testei `' OR 1=1 --` no login?
- [ ] Testei `{{7*7}}` em campos que refletem meu texto?
- [ ] Rodei o gobuster pra achar páginas escondidas?
- [ ] O enunciado cita alguma palavra (cookie, upload, admin)? É a dica.
