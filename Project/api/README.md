# API - Gerenciador de Horarios de Remedio

API em Django para cadastrar usuarios e verificar, minuto a minuto, quem precisa tomar remedio.

## Requisitos

- Python 3.10+
- Django instalado

## Estrutura principal

- `model/user.py`: model `User` com campo `horario` (`TimeField`)
- `model/management/commands/verificar_horarios.py`: comando que faz a checagem
- `routes/alert.py`: envia notificacao para o dispositivo via Wi-Fi (HTTP)

## Setup rapido

No diretorio `Project/api`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install django
```

## Banco de dados

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

## Rodar servidor Django

```bash
python3 manage.py runserver
```

## Verificacao de horarios

Rodar uma vez:

```bash
python3 manage.py verificar_horarios
```

Rodar continuamente (a cada 60 segundos):

```bash
python3 manage.py verificar_horarios --loop --interval 60
```

## Notificacao via Wi-Fi (dispositivo)

A API usa variaveis de ambiente para chamar o dispositivo:

- `ARDUINO_URL` (default: `http://192.168.0.50/girar`)
- `ARDUINO_TOKEN` (default vazio)
- `ARDUINO_TIMEOUT` (default: `3`)

Exemplo:

```bash
export ARDUINO_URL=http://192.168.1.120/girar
export ARDUINO_TOKEN=troque-este-token
export ARDUINO_TIMEOUT=3
python3 manage.py verificar_horarios --loop --interval 60
```

## Observacoes

- A checagem so encontra usuarios se existir registro na tabela `model_user`.
- O dispositivo precisa estar na mesma rede e responder no endpoint `/girar`.

## Integracao com HTML/CSS (frontend separado)

Quando o frontend nao fica dentro do Django, use `fetch` para chamar a API:

- `POST /api/cadastro/`
- `POST /api/login/`

Exemplo simples de pagina (`index.html`) com cadastro e login:

```html
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Auth</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f4f6f8;
      margin: 0;
      padding: 24px;
    }
    .card {
      max-width: 420px;
      margin: 0 auto 16px;
      background: #fff;
      border: 1px solid #ddd;
      border-radius: 8px;
      padding: 16px;
    }
    h2 { margin-top: 0; }
    input, button {
      width: 100%;
      margin: 6px 0;
      padding: 10px;
      box-sizing: border-box;
    }
    button {
      border: 0;
      background: #0d6efd;
      color: #fff;
      cursor: pointer;
    }
    .log {
      max-width: 420px;
      margin: 0 auto;
      white-space: pre-wrap;
      font-size: 14px;
    }
  </style>
</head>
<body>
  <div class="card">
    <h2>Cadastro</h2>
    <input id="cadNome" placeholder="Nome" />
    <input id="cadGmail" placeholder="Gmail" type="email" />
    <input id="cadPassword" placeholder="Senha" type="password" />
    <input id="cadRemedio" placeholder="Remedio" />
    <input id="cadHorario" type="time" />
    <button onclick="cadastro()">Cadastrar</button>
  </div>

  <div class="card">
    <h2>Login</h2>
    <input id="logGmail" placeholder="Gmail" type="email" />
    <input id="logPassword" placeholder="Senha" type="password" />
    <button onclick="login()">Entrar</button>
  </div>

  <div class="log" id="saida"></div>

  <script>
    const API = "http://127.0.0.1:8000";
    const saida = document.getElementById("saida");

    function mostrar(data) {
      saida.textContent = JSON.stringify(data, null, 2);
    }

    async function cadastro() {
      const resp = await fetch(`${API}/api/cadastro/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nome: document.getElementById("cadNome").value,
          gmail: document.getElementById("cadGmail").value,
          password: document.getElementById("cadPassword").value,
          remedio: document.getElementById("cadRemedio").value,
          horario: document.getElementById("cadHorario").value + ":00"
        })
      });
      mostrar(await resp.json());
    }

    async function login() {
      const resp = await fetch(`${API}/api/login/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          gmail: document.getElementById("logGmail").value,
          password: document.getElementById("logPassword").value
        })
      });
      mostrar(await resp.json());
    }
  </script>
</body>
</html>
```

Se frontend e API estiverem em portas diferentes, configure CORS no Django:

```bash
pip install django-cors-headers
```

No `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    # ...
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5173",
]
```
