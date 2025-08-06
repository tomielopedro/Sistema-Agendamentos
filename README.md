# Sistema de Agendamento para Salão de Beleza

Um sistema completo de gerenciamento de agendamentos para salões de beleza, desenvolvido em Flask com interface web moderna e responsiva.

## 🚀 Funcionalidades

### Dashboard Administrativo
- Visão geral das estatísticas do salão
- Agendamentos do dia e próximos agendamentos
- Métricas de receita e performance

### Gerenciamento de Clientes
- Cadastro completo de clientes
- Edição e exclusão de registros
- Histórico de agendamentos por cliente

### Gerenciamento de Serviços
- Cadastro de serviços oferecidos
- Controle de preços e duração
- Ativação/desativação de serviços

### Sistema de Agendamentos
- Criação de novos agendamentos
- Verificação de disponibilidade de horários
- Controle de status (agendado, concluído, cancelado)
- Filtros por data e status
- Prevenção de conflitos de horário

### Relatórios e Analytics
- Estatísticas de agendamentos
- Receita por período
- Serviços mais populares
- Clientes mais frequentes

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Banco de Dados**: SQLite com SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Design**: CSS Grid, Flexbox, Gradientes
- **Ícones**: Font Awesome
- **Responsividade**: Mobile-first design

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. **Clone ou extraia o projeto**
   ```bash
   cd salao_agendamento
   ```

2. **Ative o ambiente virtual**
   ```bash
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o sistema**
   ```bash
   python src/main.py
   ```

5. **Acesse o sistema**
   Abra seu navegador e acesse: `http://localhost:5000`

## 📁 Estrutura do Projeto

```
salao_agendamento/
├── src/
│   ├── models/           # Modelos de dados
│   │   ├── user.py       # Configuração do banco
│   │   ├── cliente.py    # Modelo Cliente
│   │   ├── servico.py    # Modelo Serviço
│   │   └── agendamento.py # Modelo Agendamento
│   ├── routes/           # Rotas da API
│   │   ├── cliente.py    # Endpoints de clientes
│   │   ├── servico.py    # Endpoints de serviços
│   │   ├── agendamento.py # Endpoints de agendamentos
│   │   └── dashboard.py  # Endpoints do dashboard
│   ├── static/           # Arquivos estáticos
│   │   ├── index.html    # Interface principal
│   │   ├── styles.css    # Estilos CSS
│   │   └── script.js     # JavaScript
│   ├── database/         # Banco de dados
│   │   └── app.db        # SQLite database
│   └── main.py           # Arquivo principal
├── venv/                 # Ambiente virtual
├── requirements.txt      # Dependências
└── README.md            # Documentação
```

## 🎯 Como Usar

### 1. Cadastrar Serviços
- Acesse a seção "Serviços"
- Clique em "Novo Serviço"
- Preencha nome, descrição, preço e duração
- Salve o serviço

### 2. Cadastrar Clientes
- Acesse a seção "Clientes"
- Clique em "Novo Cliente"
- Preencha nome, telefone e email (opcional)
- Salve o cliente

### 3. Criar Agendamentos
- Acesse a seção "Agendamentos"
- Clique em "Novo Agendamento"
- Selecione cliente e serviço
- Escolha data e horário
- Adicione observações se necessário
- Salve o agendamento

### 4. Gerenciar Agendamentos
- Visualize todos os agendamentos na tabela
- Use filtros por data e status
- Marque como concluído ou cancele conforme necessário
- Edite informações quando necessário

## 🔌 API Endpoints

### Clientes
- `GET /api/clientes` - Listar todos os clientes
- `POST /api/clientes` - Criar novo cliente
- `GET /api/clientes/{id}` - Obter cliente específico
- `PUT /api/clientes/{id}` - Atualizar cliente
- `DELETE /api/clientes/{id}` - Deletar cliente

### Serviços
- `GET /api/servicos` - Listar todos os serviços
- `POST /api/servicos` - Criar novo serviço
- `GET /api/servicos/{id}` - Obter serviço específico
- `PUT /api/servicos/{id}` - Atualizar serviço
- `DELETE /api/servicos/{id}` - Deletar serviço
- `PATCH /api/servicos/{id}/toggle` - Ativar/desativar serviço

### Agendamentos
- `GET /api/agendamentos` - Listar agendamentos (com filtros)
- `POST /api/agendamentos` - Criar novo agendamento
- `GET /api/agendamentos/{id}` - Obter agendamento específico
- `PUT /api/agendamentos/{id}` - Atualizar agendamento
- `DELETE /api/agendamentos/{id}` - Deletar agendamento
- `PATCH /api/agendamentos/{id}/status` - Atualizar status
- `GET /api/agendamentos/disponibilidade` - Verificar disponibilidade

### Dashboard
- `GET /api/dashboard/estatisticas` - Estatísticas gerais
- `GET /api/dashboard/agendamentos-hoje` - Agendamentos de hoje
- `GET /api/dashboard/proximos-agendamentos` - Próximos agendamentos
- `GET /api/dashboard/servicos-populares` - Serviços mais populares
- `GET /api/dashboard/receita-diaria` - Receita diária
- `GET /api/dashboard/clientes-frequentes` - Clientes frequentes

## 🎨 Características da Interface

- **Design Moderno**: Interface limpa com gradientes e sombras
- **Responsivo**: Funciona perfeitamente em desktop, tablet e mobile
- **Navegação Intuitiva**: Menu lateral com ícones e transições suaves
- **Feedback Visual**: Notificações de sucesso e erro
- **Modais Elegantes**: Formulários em modais com animações
- **Tabelas Interativas**: Hover effects e ações rápidas
- **Dashboard Informativo**: Cards de estatísticas coloridos

## 🔒 Segurança

- Validação de dados no frontend e backend
- Prevenção de conflitos de agendamento
- Tratamento de erros robusto
- Sanitização de inputs

## 📱 Responsividade

O sistema é totalmente responsivo e se adapta a diferentes tamanhos de tela:
- **Desktop**: Layout completo com sidebar
- **Tablet**: Layout adaptado com menu colapsável
- **Mobile**: Interface otimizada para toque

## 🚀 Deploy

Para deploy em produção, recomenda-se:

1. Usar um servidor WSGI como Gunicorn
2. Configurar um proxy reverso (Nginx)
3. Usar um banco de dados mais robusto (PostgreSQL)
4. Configurar HTTPS
5. Implementar backup automático

## 🤝 Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

Para suporte ou dúvidas sobre o sistema, entre em contato através dos issues do repositório.

---

**Desenvolvido com ❤️ para salões de beleza modernos**

