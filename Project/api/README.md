# API - Gerenciador de Horarios de Remedio

API em Django para cadastrar usuarios e verificar, minuto a minuto, quem precisa tomar remedio.

## Requisitos

- Python 3.10+
- Django instalado

## Estrutura principal

- `model/login/user.py`: model `User` (paciente/idoso)
- `model/login/doctor.py`: model `Doctor` (token automatico de 250 digitos)
- `model/login/cuidador.py`: model `Cuidador`
- `model/management/commands/verificar_horarios.py`: comando que faz a checagem
- `routes/alert_route.py`: rota de comunicacao com dispositivo (placeholder)

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

## Relacionamentos entre tabelas

- `Doctor` -> `User`: um medico possui varios pacientes. O vinculo real e o campo `User.id_doctor` apontando para `Doctor.id` (N:1).
- `Doctor` -> `Instituicao`: a instituicao usa `id_doctor` como PK e FK, entao o relacionamento e 1:1.
- `Cuidador` -> `User`: o cuidador aponta para um idoso pelo campo `Cuidador.id_idoso` (1:1).
- `Doctor.paciente_ids`: e uma lista simples de IDs, nao e relacionamento relacional (serve apenas para referencia manual).

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
    <input id="cadEmail" placeholder="Email" type="email" />
    <input id="cadPassword" placeholder="Senha" type="password" />
    <input id="cadRemedio" placeholder="Remedio" />
    <input id="cadHorario" type="time" />
    <button onclick="cadastro()">Cadastrar</button>
  </div>

  <div class="card">
    <h2>Login</h2>
    <input id="logEmail" placeholder="Email" type="email" />
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
          email: document.getElementById("cadEmail").value,
          password: document.getElementById("cadPassword").value,
          cpf: "00000000000",
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
          email: document.getElementById("logEmail").value,
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

## Teste rapido no Postman

Base URL local:

- `http://127.0.0.1:8000`

Resumo de endpoints:

| Metodo | Endpoint | Uso |
|---|---|---|
| `POST` | `/api/cadastro/` | Criar usuario (paciente) |
| `POST` | `/api/idosos/cadastro/` | Criar idoso (usuario sem doutor) |
| `POST` | `/api/login/` | Autenticar usuario |
| `GET` | `/api/usuarios/?codigo=admin123` | Usuarios sem doutor |
| `GET` | `/api/usuarios/?codigo=TOKEN_MEDICO` | Pacientes do medico |
| `POST` | `/api/doctors/cadastro/` | Criar medico (token automatico) |
| `GET` | `/api/doctors/` | Listar medicos |
| `GET` | `/api/doctors/<id>/` | Detalhar medico |
| `POST` | `/api/instituicoes/cadastro/` | Criar instituicao |
| `GET` | `/api/instituicoes/` | Listar instituicoes |
| `GET` | `/api/instituicoes/<id_doctor>/` | Detalhar instituicao |
| `POST` | `/api/cuidadores/cadastro/` | Criar cuidador |
| `GET` | `/api/cuidadores/` | Listar cuidadores |
| `GET` | `/api/cuidadores/<id>/` | Detalhar cuidador |
| `GET` | `/api/cuidadores/<id>/idoso/` | Cuidador + idoso |

Formato de `data_criacao` nos retornos: `YYYY-MM-DD HH:MM:SS` (sem microssegundos).

### 1. Cadastro de usuario (paciente)

- Metodo: `POST`
- URL: `http://127.0.0.1:8000/api/cadastro/`
- Headers: `Content-Type: application/json`
- Body (raw JSON):

```json
{
  "nome": "Ana",
  "email": "ana@email.com",
  "password": "123456",
  "cpf": "12345678901",
  "remedio": "Dipirona",
  "horario": "08:30:00",
  "remedios": ["Dipirona", "Omeprazol"],
  "horarios": ["08:30:00", "20:30:00"],
  "id_doctor": 1
}
```

Resposta esperada (sucesso):

```json
{
  "id": 1,
  "message": "Usuario cadastrado"
}
```

### 2. Login

- Metodo: `POST`
- URL: `http://127.0.0.1:8000/api/login/`
- Headers: `Content-Type: application/json`
- Body (raw JSON):

```json
{
  "email": "ana@email.com",
  "password": "123456"
}
```

Resposta esperada (sucesso):

```json
{
  "message": "Login realizado",
  "user": {
    "id": 1,
    "nome": "Ana",
      "email": "ana@email.com"
  }
}
```

### 3. Consulta de usuarios (protegida por codigo)

- Metodo: `GET`
- URL com codigo correto:
  `http://127.0.0.1:8000/api/usuarios/?codigo=admin123`
- URL sem codigo (ou errado):
  `http://127.0.0.1:8000/api/usuarios/`

Com `admin123` retorna usuarios sem medico associado.
Com token de medico retorna pacientes daquele medico.

### 4. Cadastro de idoso (usuario sem doutor)

- Metodo: `POST`
- URL: `http://127.0.0.1:8000/api/idosos/cadastro/`
- Body (raw JSON):

```json
{
  "nome": "Maria",
  "email": "maria@email.com",
  "password": "123456",
  "cpf": "12345678901",
  "remedio": "Dipirona",
  "horario": "08:00:00",
  "remedios": ["Dipirona"],
  "horarios": ["08:00:00"]
}
```

### 5. Cadastro de doctor

- Metodo: `POST`
- URL: `http://127.0.0.1:8000/api/doctors/cadastro/`
- Body (raw JSON):

```json
{
  "nome": "Dr Carlos",
  "idade": 45,
  "cpf": "12345678901",
  "password": "senha123",
  "paciente_ids": [1, 2, 3]
}
```

Resposta inclui `token` de 250 digitos.

### 6. Cadastro de instituicao

- Metodo: `POST`
- URL: `http://127.0.0.1:8000/api/instituicoes/cadastro/`
- Body (raw JSON):

```json
{
  "id_doctor": 1,
  "nome": "Clinica Alfa",
  "cnpj": "12345678901234",
  "bairro": "Centro",
  "rua": "Rua A",
  "cep": "12345678"
}
```

### 7. Cadastro de cuidador

- Metodo: `POST`
- URL: `http://127.0.0.1:8000/api/cuidadores/cadastro/`
- Body (raw JSON):

```json
{
  "nome": "Ana",
  "email": "ana@email.com",
  "password": "123456",
  "cpf": "99999999999",
  "id_idoso": 1
}
```

### 8. Cuidador + idoso

- Metodo: `GET`
- URL: `http://127.0.0.1:8000/api/cuidadores/1/idoso/`

## JSONs prontos para teste

### Cadastro (valido)

```json
{
  "nome": "Joao Silva",
  "email": "joao.silva@email.com",
  "password": "senha123",
  "cpf": "12345678901",
  "remedio": "Paracetamol",
  "horario": "07:30:00",
  "remedios": ["Paracetamol"],
  "horarios": ["07:30:00"],
  "id_doctor": 1
}
```

### Cadastro (faltando campo - deve retornar erro 400)

```json
{
  "nome": "Maria Souza",
  "email": "maria@email.com",
  "password": "123456",
  "cpf": "12345678901",
  "horario": "10:00:00"
}
```

### Login (valido)

```json
{
  "email": "joao.silva@email.com",
  "password": "senha123"
}
```

### Login (senha errada - deve retornar 401)

```json
{
  "email": "joao.silva@email.com",
  "password": "senha-errada"
}
```

### Consulta de usuarios (GET)

Nao usa body JSON. Use a query string:

- Admin: `http://127.0.0.1:8000/api/usuarios/?codigo=admin123`
- Medico: `http://127.0.0.1:8000/api/usuarios/?codigo=TOKEN_MEDICO`
