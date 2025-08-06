// Configuração da API
const API_BASE = '/api';

// Estado da aplicação
let currentPage = 'dashboard';
let editingItem = null;
let clientes = [];
let servicos = [];
let agendamentos = [];

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupEventListeners();
    loadDashboard();
    loadClientes();
    loadServicos();
    loadAgendamentos();
}

// Event Listeners
function setupEventListeners() {
    // Menu de navegação
    document.querySelectorAll('.menu-item').forEach(item => {
        item.addEventListener('click', function() {
            const page = this.dataset.page;
            navigateToPage(page);
        });
    });

    // Toggle do menu mobile
    document.querySelector('.menu-toggle').addEventListener('click', function() {
        document.querySelector('.sidebar').classList.toggle('active');
    });

    // Formulários
    document.getElementById('form-cliente').addEventListener('submit', handleClienteSubmit);
    document.getElementById('form-servico').addEventListener('submit', handleServicoSubmit);
    document.getElementById('form-agendamento').addEventListener('submit', handleAgendamentoSubmit);

    // Fechar modais clicando fora
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                fecharModal(this.id);
            }
        });
    });
}

// Navegação
function navigateToPage(page) {
    // Atualizar menu ativo
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
    });
    document.querySelector(`[data-page="${page}"]`).classList.add('active');

    // Mostrar página
    document.querySelectorAll('.page').forEach(p => {
        p.classList.remove('active');
    });
    document.getElementById(`${page}-page`).classList.add('active');

    // Atualizar título
    const titles = {
        dashboard: 'Dashboard',
        agendamentos: 'Agendamentos',
        clientes: 'Clientes',
        servicos: 'Serviços'
    };
    document.getElementById('page-title').textContent = titles[page];

    currentPage = page;

    // Carregar dados específicos da página
    if (page === 'dashboard') {
        loadDashboard();
    } else if (page === 'agendamentos') {
        loadAgendamentos();
    } else if (page === 'clientes') {
        loadClientes();
    } else if (page === 'servicos') {
        loadServicos();
    }
}

// Utilitários
function showLoading() {
    document.getElementById('loading').classList.add('active');
}

function hideLoading() {
    document.getElementById('loading').classList.remove('active');
}

function showNotification(message, type = 'success') {
    // Criar notificação simples
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? '#28a745' : '#dc3545'};
        color: white;
        border-radius: 8px;
        z-index: 4000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR');
}

function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// API Calls
async function apiCall(endpoint, options = {}) {
    try {
        showLoading();
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.erro || 'Erro na requisição');
        }
        
        return data;
    } catch (error) {
        showNotification(error.message, 'error');
        throw error;
    } finally {
        hideLoading();
    }
}

// Dashboard
async function loadDashboard() {
    try {
        const stats = await apiCall('/dashboard/estatisticas');
        
        document.getElementById('total-clientes').textContent = stats.total_clientes;
        document.getElementById('agendamentos-hoje').textContent = stats.agendamentos_hoje;
        document.getElementById('total-servicos').textContent = stats.total_servicos;
        document.getElementById('receita-mes').textContent = formatCurrency(stats.receita_mes);

        // Carregar agendamentos de hoje
        const agendamentosHoje = await apiCall('/dashboard/agendamentos-hoje');
        renderAgendamentosHoje(agendamentosHoje);

        // Carregar próximos agendamentos
        const proximosAgendamentos = await apiCall('/dashboard/proximos-agendamentos');
        renderProximosAgendamentos(proximosAgendamentos);
        
    } catch (error) {
        console.error('Erro ao carregar dashboard:', error);
    }
}

function renderAgendamentosHoje(agendamentos) {
    const container = document.getElementById('agendamentos-hoje-lista');
    
    if (agendamentos.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #666; padding: 20px;">Nenhum agendamento para hoje</p>';
        return;
    }

    container.innerHTML = agendamentos.map(agendamento => `
        <div class="agendamento-item">
            <div class="agendamento-info">
                <h4>${agendamento.cliente_nome}</h4>
                <p>${agendamento.servico_nome}</p>
                <p>${formatCurrency(agendamento.servico_preco)}</p>
            </div>
            <div class="agendamento-time">
                ${new Date(agendamento.data_agendamento).toLocaleTimeString('pt-BR', {hour: '2-digit', minute: '2-digit'})}
            </div>
        </div>
    `).join('');
}

function renderProximosAgendamentos(agendamentos) {
    const container = document.getElementById('proximos-agendamentos');
    
    if (agendamentos.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #666; padding: 20px;">Nenhum agendamento próximo</p>';
        return;
    }

    container.innerHTML = agendamentos.map(agendamento => `
        <div class="agendamento-item">
            <div class="agendamento-info">
                <h4>${agendamento.cliente_nome}</h4>
                <p>${agendamento.servico_nome}</p>
                <p>${formatDate(agendamento.data_agendamento)}</p>
            </div>
            <div class="agendamento-time">
                ${new Date(agendamento.data_agendamento).toLocaleTimeString('pt-BR', {hour: '2-digit', minute: '2-digit'})}
            </div>
        </div>
    `).join('');
}

// Clientes
async function loadClientes() {
    try {
        clientes = await apiCall('/clientes');
        renderClientes();
    } catch (error) {
        console.error('Erro ao carregar clientes:', error);
    }
}

function renderClientes() {
    const tbody = document.querySelector('#tabela-clientes tbody');
    
    if (clientes.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 20px;">Nenhum cliente cadastrado</td></tr>';
        return;
    }

    tbody.innerHTML = clientes.map(cliente => `
        <tr>
            <td>${cliente.nome}</td>
            <td>${cliente.telefone}</td>
            <td>${cliente.email || '-'}</td>
            <td>${formatDate(cliente.data_cadastro)}</td>
            <td>
                <button class="btn btn-sm btn-warning" onclick="editarCliente(${cliente.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deletarCliente(${cliente.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

function abrirModalCliente(clienteId = null) {
    editingItem = clienteId;
    const modal = document.getElementById('modal-cliente');
    const titulo = document.getElementById('modal-cliente-titulo');
    const form = document.getElementById('form-cliente');
    
    if (clienteId) {
        const cliente = clientes.find(c => c.id === clienteId);
        titulo.textContent = 'Editar Cliente';
        document.getElementById('cliente-nome').value = cliente.nome;
        document.getElementById('cliente-telefone').value = cliente.telefone;
        document.getElementById('cliente-email').value = cliente.email || '';
    } else {
        titulo.textContent = 'Novo Cliente';
        form.reset();
    }
    
    modal.classList.add('active');
}

function editarCliente(id) {
    abrirModalCliente(id);
}

async function deletarCliente(id) {
    if (!confirm('Tem certeza que deseja deletar este cliente?')) {
        return;
    }

    try {
        await apiCall(`/clientes/${id}`, { method: 'DELETE' });
        showNotification('Cliente deletado com sucesso!');
        loadClientes();
    } catch (error) {
        console.error('Erro ao deletar cliente:', error);
    }
}

async function handleClienteSubmit(e) {
    e.preventDefault();
    
    const formData = {
        nome: document.getElementById('cliente-nome').value,
        telefone: document.getElementById('cliente-telefone').value,
        email: document.getElementById('cliente-email').value || null
    };

    try {
        if (editingItem) {
            await apiCall(`/clientes/${editingItem}`, {
                method: 'PUT',
                body: JSON.stringify(formData)
            });
            showNotification('Cliente atualizado com sucesso!');
        } else {
            await apiCall('/clientes', {
                method: 'POST',
                body: JSON.stringify(formData)
            });
            showNotification('Cliente criado com sucesso!');
        }
        
        fecharModal('modal-cliente');
        loadClientes();
    } catch (error) {
        console.error('Erro ao salvar cliente:', error);
    }
}

// Serviços
async function loadServicos() {
    try {
        servicos = await apiCall('/servicos?apenas_ativos=false');
        renderServicos();
        updateServicoSelects();
    } catch (error) {
        console.error('Erro ao carregar serviços:', error);
    }
}

function renderServicos() {
    const tbody = document.querySelector('#tabela-servicos tbody');
    
    if (servicos.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 20px;">Nenhum serviço cadastrado</td></tr>';
        return;
    }

    tbody.innerHTML = servicos.map(servico => `
        <tr>
            <td>${servico.nome}</td>
            <td>${servico.descricao || '-'}</td>
            <td>${formatCurrency(servico.preco)}</td>
            <td>${servico.duracao_minutos} min</td>
            <td>
                <span class="status-badge ${servico.ativo ? 'status-concluido' : 'status-cancelado'}">
                    ${servico.ativo ? 'Ativo' : 'Inativo'}
                </span>
            </td>
            <td>
                <button class="btn btn-sm btn-warning" onclick="editarServico(${servico.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm ${servico.ativo ? 'btn-secondary' : 'btn-success'}" onclick="toggleServico(${servico.id})">
                    <i class="fas fa-${servico.ativo ? 'pause' : 'play'}"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deletarServico(${servico.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

function updateServicoSelects() {
    const select = document.getElementById('agendamento-servico');
    select.innerHTML = '<option value="">Selecione um serviço</option>';
    
    servicos.filter(s => s.ativo).forEach(servico => {
        const option = document.createElement('option');
        option.value = servico.id;
        option.textContent = `${servico.nome} - ${formatCurrency(servico.preco)} (${servico.duracao_minutos}min)`;
        select.appendChild(option);
    });
}

function abrirModalServico(servicoId = null) {
    editingItem = servicoId;
    const modal = document.getElementById('modal-servico');
    const titulo = document.getElementById('modal-servico-titulo');
    const form = document.getElementById('form-servico');
    
    if (servicoId) {
        const servico = servicos.find(s => s.id === servicoId);
        titulo.textContent = 'Editar Serviço';
        document.getElementById('servico-nome').value = servico.nome;
        document.getElementById('servico-descricao').value = servico.descricao || '';
        document.getElementById('servico-preco').value = servico.preco;
        document.getElementById('servico-duracao').value = servico.duracao_minutos;
    } else {
        titulo.textContent = 'Novo Serviço';
        form.reset();
    }
    
    modal.classList.add('active');
}

function editarServico(id) {
    abrirModalServico(id);
}

async function toggleServico(id) {
    try {
        await apiCall(`/servicos/${id}/toggle`, { method: 'PATCH' });
        showNotification('Status do serviço atualizado!');
        loadServicos();
    } catch (error) {
        console.error('Erro ao alterar status do serviço:', error);
    }
}

async function deletarServico(id) {
    if (!confirm('Tem certeza que deseja deletar este serviço?')) {
        return;
    }

    try {
        await apiCall(`/servicos/${id}`, { method: 'DELETE' });
        showNotification('Serviço deletado com sucesso!');
        loadServicos();
    } catch (error) {
        console.error('Erro ao deletar serviço:', error);
    }
}

async function handleServicoSubmit(e) {
    e.preventDefault();
    
    const formData = {
        nome: document.getElementById('servico-nome').value,
        descricao: document.getElementById('servico-descricao').value || '',
        preco: parseFloat(document.getElementById('servico-preco').value),
        duracao_minutos: parseInt(document.getElementById('servico-duracao').value)
    };

    try {
        if (editingItem) {
            await apiCall(`/servicos/${editingItem}`, {
                method: 'PUT',
                body: JSON.stringify(formData)
            });
            showNotification('Serviço atualizado com sucesso!');
        } else {
            await apiCall('/servicos', {
                method: 'POST',
                body: JSON.stringify(formData)
            });
            showNotification('Serviço criado com sucesso!');
        }
        
        fecharModal('modal-servico');
        loadServicos();
    } catch (error) {
        console.error('Erro ao salvar serviço:', error);
    }
}

// Agendamentos
async function loadAgendamentos() {
    try {
        agendamentos = await apiCall('/agendamentos');
        renderAgendamentos();
        updateClienteSelects();
    } catch (error) {
        console.error('Erro ao carregar agendamentos:', error);
    }
}

function renderAgendamentos() {
    const tbody = document.querySelector('#tabela-agendamentos tbody');
    
    if (agendamentos.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 20px;">Nenhum agendamento encontrado</td></tr>';
        return;
    }

    tbody.innerHTML = agendamentos.map(agendamento => `
        <tr>
            <td>${formatDateTime(agendamento.data_agendamento)}</td>
            <td>${agendamento.cliente_nome}</td>
            <td>${agendamento.servico_nome}</td>
            <td>${formatCurrency(agendamento.servico_preco)}</td>
            <td>
                <span class="status-badge status-${agendamento.status}">
                    ${agendamento.status.charAt(0).toUpperCase() + agendamento.status.slice(1)}
                </span>
            </td>
            <td>
                <button class="btn btn-sm btn-warning" onclick="editarAgendamento(${agendamento.id})">
                    <i class="fas fa-edit"></i>
                </button>
                ${agendamento.status === 'agendado' ? `
                    <button class="btn btn-sm btn-success" onclick="concluirAgendamento(${agendamento.id})">
                        <i class="fas fa-check"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="cancelarAgendamento(${agendamento.id})">
                        <i class="fas fa-times"></i>
                    </button>
                ` : ''}
                <button class="btn btn-sm btn-danger" onclick="deletarAgendamento(${agendamento.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

function updateClienteSelects() {
    const select = document.getElementById('agendamento-cliente');
    select.innerHTML = '<option value="">Selecione um cliente</option>';
    
    clientes.forEach(cliente => {
        const option = document.createElement('option');
        option.value = cliente.id;
        option.textContent = `${cliente.nome} - ${cliente.telefone}`;
        select.appendChild(option);
    });
}

function abrirModalAgendamento(agendamentoId = null) {
    editingItem = agendamentoId;
    const modal = document.getElementById('modal-agendamento');
    const titulo = document.getElementById('modal-agendamento-titulo');
    const form = document.getElementById('form-agendamento');
    
    if (agendamentoId) {
        const agendamento = agendamentos.find(a => a.id === agendamentoId);
        titulo.textContent = 'Editar Agendamento';
        
        const dataAgendamento = new Date(agendamento.data_agendamento);
        document.getElementById('agendamento-cliente').value = agendamento.cliente_id;
        document.getElementById('agendamento-servico').value = agendamento.servico_id;
        document.getElementById('agendamento-data').value = dataAgendamento.toISOString().split('T')[0];
        document.getElementById('agendamento-hora').value = dataAgendamento.toTimeString().slice(0, 5);
        document.getElementById('agendamento-observacoes').value = agendamento.observacoes || '';
    } else {
        titulo.textContent = 'Novo Agendamento';
        form.reset();
        // Definir data mínima como hoje
        const hoje = new Date().toISOString().split('T')[0];
        document.getElementById('agendamento-data').min = hoje;
    }
    
    modal.classList.add('active');
}

function editarAgendamento(id) {
    abrirModalAgendamento(id);
}

async function concluirAgendamento(id) {
    try {
        await apiCall(`/agendamentos/${id}/status`, {
            method: 'PATCH',
            body: JSON.stringify({ status: 'concluido' })
        });
        showNotification('Agendamento concluído!');
        loadAgendamentos();
        if (currentPage === 'dashboard') {
            loadDashboard();
        }
    } catch (error) {
        console.error('Erro ao concluir agendamento:', error);
    }
}

async function cancelarAgendamento(id) {
    if (!confirm('Tem certeza que deseja cancelar este agendamento?')) {
        return;
    }

    try {
        await apiCall(`/agendamentos/${id}/status`, {
            method: 'PATCH',
            body: JSON.stringify({ status: 'cancelado' })
        });
        showNotification('Agendamento cancelado!');
        loadAgendamentos();
        if (currentPage === 'dashboard') {
            loadDashboard();
        }
    } catch (error) {
        console.error('Erro ao cancelar agendamento:', error);
    }
}

async function deletarAgendamento(id) {
    if (!confirm('Tem certeza que deseja deletar este agendamento?')) {
        return;
    }

    try {
        await apiCall(`/agendamentos/${id}`, { method: 'DELETE' });
        showNotification('Agendamento deletado com sucesso!');
        loadAgendamentos();
        if (currentPage === 'dashboard') {
            loadDashboard();
        }
    } catch (error) {
        console.error('Erro ao deletar agendamento:', error);
    }
}

async function handleAgendamentoSubmit(e) {
    e.preventDefault();
    
    const data = document.getElementById('agendamento-data').value;
    const hora = document.getElementById('agendamento-hora').value;
    const dataAgendamento = new Date(`${data}T${hora}`);
    
    const formData = {
        cliente_id: parseInt(document.getElementById('agendamento-cliente').value),
        servico_id: parseInt(document.getElementById('agendamento-servico').value),
        data_agendamento: dataAgendamento.toISOString(),
        observacoes: document.getElementById('agendamento-observacoes').value || ''
    };

    try {
        if (editingItem) {
            await apiCall(`/agendamentos/${editingItem}`, {
                method: 'PUT',
                body: JSON.stringify(formData)
            });
            showNotification('Agendamento atualizado com sucesso!');
        } else {
            await apiCall('/agendamentos', {
                method: 'POST',
                body: JSON.stringify(formData)
            });
            showNotification('Agendamento criado com sucesso!');
        }
        
        fecharModal('modal-agendamento');
        loadAgendamentos();
        if (currentPage === 'dashboard') {
            loadDashboard();
        }
    } catch (error) {
        console.error('Erro ao salvar agendamento:', error);
    }
}

// Filtros
async function aplicarFiltros() {
    const data = document.getElementById('filtro-data').value;
    const status = document.getElementById('filtro-status').value;
    
    let url = '/agendamentos?';
    const params = [];
    
    if (data) {
        params.push(`data_inicio=${data}T00:00:00`);
        params.push(`data_fim=${data}T23:59:59`);
    }
    
    if (status) {
        params.push(`status=${status}`);
    }
    
    url += params.join('&');
    
    try {
        agendamentos = await apiCall(url);
        renderAgendamentos();
    } catch (error) {
        console.error('Erro ao aplicar filtros:', error);
    }
}

// Modais
function fecharModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
    editingItem = null;
}

