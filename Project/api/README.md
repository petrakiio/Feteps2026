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
