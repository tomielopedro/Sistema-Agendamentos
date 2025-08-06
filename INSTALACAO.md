# Guia de Instalação - Sistema de Agendamento

## 📋 Requisitos do Sistema

### Requisitos Mínimos
- **Sistema Operacional**: Windows 10, macOS 10.14, ou Linux (Ubuntu 18.04+)
- **Python**: Versão 3.8 ou superior
- **RAM**: 2GB mínimo (4GB recomendado)
- **Espaço em Disco**: 500MB livres
- **Navegador**: Chrome, Firefox, Safari ou Edge (versões recentes)

### Verificando o Python
```bash
python --version
# ou
python3 --version
```

Se o Python não estiver instalado, baixe em: https://python.org/downloads/

## 🚀 Instalação Passo a Passo

### 1. Preparação do Ambiente

#### No Windows:
```cmd
# Abra o Prompt de Comando como Administrador
cd C:\
mkdir projetos
cd projetos
```

#### No macOS/Linux:
```bash
# Abra o Terminal
cd ~
mkdir projetos
cd projetos
```

### 2. Extrair o Sistema
- Extraia o arquivo `salao_agendamento.zip` na pasta `projetos`
- Navegue até a pasta do sistema:

```bash
cd salao_agendamento
```

### 3. Ativar o Ambiente Virtual

#### No Windows:
```cmd
venv\Scripts\activate
```

#### No macOS/Linux:
```bash
source venv/bin/activate
```

**Nota**: Você verá `(venv)` no início da linha de comando, indicando que o ambiente virtual está ativo.

### 4. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 5. Inicializar o Banco de Dados
O banco de dados será criado automaticamente na primeira execução.

### 6. Executar o Sistema
```bash
python src/main.py
```

Você verá uma mensagem similar a:
```
* Running on http://127.0.0.1:5000
* Running on http://0.0.0.0:5000
```

### 7. Acessar o Sistema
- Abra seu navegador
- Acesse: `http://localhost:5000`
- O sistema estará pronto para uso!

## 🔧 Configuração Inicial

### Primeiro Acesso
1. **Cadastre Serviços**: Comece cadastrando os serviços oferecidos pelo salão
2. **Cadastre Clientes**: Adicione os clientes existentes
3. **Crie Agendamentos**: Comece a agendar serviços

### Dados de Exemplo
Para testar o sistema, você pode criar:

**Serviços Exemplo:**
- Corte Feminino - R$ 45,00 - 60 min
- Corte Masculino - R$ 25,00 - 30 min
- Escova - R$ 35,00 - 45 min
- Manicure - R$ 20,00 - 40 min
- Pedicure - R$ 25,00 - 50 min

**Clientes Exemplo:**
- Maria Silva - (11) 99999-1111 - maria@email.com
- João Santos - (11) 99999-2222 - joao@email.com

## 🛠️ Solução de Problemas

### Erro: "Python não encontrado"
**Solução**: Instale o Python em python.org ou use o Microsoft Store (Windows)

### Erro: "pip não encontrado"
**Solução**: 
```bash
python -m ensurepip --upgrade
```

### Erro: "Porta 5000 em uso"
**Solução**: 
1. Feche outros programas que possam estar usando a porta
2. Ou edite `src/main.py` e mude `port=5000` para `port=5001`

### Erro: "Módulo não encontrado"
**Solução**: 
1. Certifique-se de que o ambiente virtual está ativo
2. Execute novamente: `pip install -r requirements.txt`

### Erro: "Permissão negada"
**Solução**: 
- **Windows**: Execute o Prompt como Administrador
- **macOS/Linux**: Use `sudo` se necessário

### Sistema não carrega no navegador
**Verificações**:
1. Confirme que o servidor está rodando (mensagem no terminal)
2. Teste com `http://127.0.0.1:5000` em vez de `localhost`
3. Desative temporariamente firewall/antivírus
4. Teste em outro navegador

## 🔄 Atualizações

### Para atualizar o sistema:
1. Pare o servidor (Ctrl+C)
2. Faça backup do banco de dados (`src/database/app.db`)
3. Substitua os arquivos do sistema
4. Execute novamente: `python src/main.py`

## 🗄️ Backup dos Dados

### Backup Manual:
```bash
# Copie o arquivo do banco de dados
cp src/database/app.db backup_$(date +%Y%m%d).db
```

### Backup Automático:
Recomenda-se configurar backup automático do arquivo `src/database/app.db`

## 🌐 Acesso Remoto

### Para acessar de outros dispositivos na rede:
1. Descubra o IP do computador:
   - **Windows**: `ipconfig`
   - **macOS/Linux**: `ifconfig` ou `ip addr`

2. Acesse de outros dispositivos: `http://[IP_DO_COMPUTADOR]:5000`

**Exemplo**: `http://192.168.1.100:5000`

## 📱 Uso Mobile

O sistema é totalmente responsivo e funciona perfeitamente em:
- Smartphones (iOS/Android)
- Tablets
- Notebooks
- Desktops

## 🔒 Segurança

### Recomendações:
- Use apenas em redes confiáveis
- Faça backup regular dos dados
- Mantenha o sistema atualizado
- Para uso em produção, configure HTTPS

## 📞 Suporte

### Em caso de problemas:
1. Verifique este guia de solução de problemas
2. Consulte o arquivo README.md
3. Verifique se todos os requisitos foram atendidos
4. Entre em contato com o suporte técnico

---

**Sistema pronto para uso! 🎉**

