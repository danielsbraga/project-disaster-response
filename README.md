# Disaster Response App

Este repositório contém o código-fonte do **Disaster Response App**, uma aplicação web com backend em Flask e frontend em Next.js. Este guia refere-se à **branch de desenvolvimento**: `dev/monorepo-integration`.

---

## 🧪 Tecnologias

- Backend: Python + Flask
- Frontend: Next.js (React)
- Gerenciador de pacotes JS: pnpm

---

## 🚀 Como rodar o projeto localmente

### 1. Clone o repositório

```bash
git clone https://github.com/danielsbraga/project-disaster-response.git
cd project-disaster-response
git checkout dev/monorepo-integration
```

---

### 2. Inicie o backend (Flask)

Abra um terminal e execute:

```bash
cd MLmodel
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app/run.py
```

---

### 3. Configure o ambiente para o frontend

Se ainda não tiver o Node.js instalado, baixe e instale a versão LTS em:

🔗 https://nodejs.org

Depois, instale o `pnpm`:

```bash
npm install -g pnpm
```

---

### 4. Inicie o frontend (Next.js)

Abra outro terminal e execute:

```bash
cd nextjs-app
pnpm install
pnpm dev
```

---

## 📂 Estrutura do Monorepo

```
project-disaster-response/
│
├── MLmodel/         # Backend Flask app
│   └── app/
│
└── nextjs-app/      # Frontend Next.js app
```

---

## 📌 Observações

- Esta é a branch de desenvolvimento. Para ver o projeto em produção, acesse a branch `main`.
- Certifique-se de que o backend esteja rodando antes de iniciar o frontend.

---

## 🛠️ Em desenvolvimento

Esta versão está em progresso e pode conter alterações frequentes. Feedbacks e contribuições são bem-vindos!