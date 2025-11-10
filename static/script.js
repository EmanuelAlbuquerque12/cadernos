// ========================================
// FUNÇÕES DE CONTROLE DA INTERFACE
// ========================================

// Toggle de etapas (expandir/recolher)
function toggleStep(stepId) {
    const content = document.getElementById('content-' + stepId);
    content.classList.toggle('active');
}

// Atualizar valor do slider de workers
function updateWorkers(value) {
    document.getElementById('workers-value').textContent = value;
}

// Selecionar modo de download (tudo ou específico)
function selectMode(mode) {
    const specificSection = document.getElementById('specific-selection');

    if (mode === 'specific') {
        specificSection.style.display = 'block';
    } else {
        specificSection.style.display = 'none';
    }
}

// ========================================
// CONFIGURAÇÕES
// ========================================

function abrirSeletorPasta() {
    // Chama API para abrir seletor de pasta nativo do Windows
    fetch('/api/selecionar_pasta')
        .then(response => response.json())
        .then(data => {
            if (data.sucesso && data.pasta) {
                document.getElementById('pasta_salvamento').value = data.pasta;
                alert('📁 Pasta selecionada: ' + data.pasta);
            } else if (data.mensagem) {
                // Usuário cancelou a seleção
                console.log(data.mensagem);
            }
        })
        .catch(error => {
            alert('❌ Erro ao abrir seletor de pasta: ' + error);
        });
}

function salvarConfig() {
    const pasta = document.getElementById('pasta_salvamento').value;
    const workers = document.getElementById('workers').value;

    if (!pasta.trim()) {
        alert('⚠️ Por favor, selecione uma pasta de salvamento!');
        return;
    }

    fetch('/api/config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            pasta_salvamento: pasta,
            workers: parseInt(workers)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            alert('✅ Configurações salvas com sucesso!\n\n📁 Pasta: ' + pasta + '\n⚡ Velocidade: ' + workers + ' downloads simultâneos');

            // Fecha o modal
            const modal = document.getElementById('config-modal');
            if (modal) {
                modal.classList.remove('show');
            }

            carregarEstatisticas();
        }
    })
    .catch(error => {
        alert('❌ Erro ao salvar configurações: ' + error);
    });
}

// ========================================
// SELEÇÃO DE TRIBUNAIS
// ========================================

function filtrarTribunais() {
    const termo = document.getElementById('busca_tribunal').value.toLowerCase();
    const items = document.querySelectorAll('.tribunal-chip');
    const grupos = document.querySelectorAll('.uf-group-compact');

    items.forEach(item => {
        const sigla = item.dataset.sigla.toLowerCase();
        const nome = item.dataset.nome.toLowerCase();

        if (sigla.includes(termo) || nome.includes(termo)) {
            item.style.display = 'inline-block';
        } else {
            item.style.display = 'none';
        }
    });

    // Esconde grupos vazios
    grupos.forEach(grupo => {
        const visibleItems = grupo.querySelectorAll('.tribunal-chip[style*="inline-block"]');
        if (visibleItems.length === 0 && termo !== '') {
            grupo.style.display = 'none';
        } else {
            grupo.style.display = 'block';
        }
    });
}

function selecionarTodos() {
    const checkboxes = document.querySelectorAll('.tribunal-checkbox');
    checkboxes.forEach(cb => cb.checked = true);
}

function deselecionarTodos() {
    const checkboxes = document.querySelectorAll('.tribunal-checkbox');
    checkboxes.forEach(cb => cb.checked = false);
}

function selecionarSuperiores() {
    const superiores = ['STJ', 'STF', 'TST', 'TSE', 'STM', 'CNJ', 'CJF'];
    const checkboxes = document.querySelectorAll('.tribunal-checkbox');

    checkboxes.forEach(cb => {
        cb.checked = superiores.includes(cb.value);
    });
}

// ========================================
// DOWNLOAD
// ========================================

function iniciarDownload() {
    const mode = document.querySelector('input[name="download_mode"]:checked').value;

    let tribunais = [];

    if (mode === 'all') {
        // Baixar de todos os tribunais
        const allCheckboxes = document.querySelectorAll('.tribunal-checkbox');
        allCheckboxes.forEach(cb => {
            tribunais.push(cb.value);
        });
    } else {
        // Baixar apenas selecionados
        const checkboxes = document.querySelectorAll('.tribunal-checkbox:checked');
        tribunais = Array.from(checkboxes).map(cb => cb.value);
    }

    if (tribunais.length === 0 && mode === 'specific') {
        alert('⚠️ Selecione pelo menos um tribunal!');
        return;
    }

    const dataInicio = document.getElementById('data_inicio').value;
    const dataFim = document.getElementById('data_fim').value;

    if (!dataInicio || !dataFim) {
        alert('⚠️ Selecione as datas!');
        return;
    }

    // Converte datas para formato DD/MM/YYYY
    const dataInicioFormatada = formatarData(dataInicio);
    const dataFimFormatada = formatarData(dataFim);

    // Tipos selecionados
    const tiposCheckboxes = document.querySelectorAll('.checkbox-group-inline input[type="checkbox"]:checked');
    const tipos = Array.from(tiposCheckboxes).map(cb => cb.value);

    if (tipos.length === 0) {
        alert('⚠️ Selecione pelo menos um tipo de caderno!');
        return;
    }

    const btn = document.getElementById('btn_download');
    btn.disabled = true;
    btn.innerHTML = '<span class="btn-icon">⏳</span> Iniciando...';

    fetch('/api/baixar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            tribunais: tribunais,
            data_inicio: dataInicioFormatada,
            data_fim: dataFimFormatada,
            tipos: tipos
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            document.getElementById('download_status').style.display = 'block';
            document.getElementById('status_mensagem').textContent = data.mensagem;
        } else {
            alert('❌ Erro: ' + data.erro);
            btn.disabled = false;
            btn.innerHTML = '<span class="btn-icon">🚀</span> Iniciar Download';
        }
    })
    .catch(error => {
        alert('❌ Erro ao iniciar download: ' + error);
        btn.disabled = false;
        btn.innerHTML = '<span class="btn-icon">🚀</span> Iniciar Download';
    });
}

function verificarStatus() {
    fetch('/api/status')
    .then(response => response.json())
    .then(data => {
        if (data.em_andamento) {
            document.getElementById('download_status').style.display = 'block';

            const progresso = data.total > 0 ? (data.progresso / data.total * 100) : 0;
            document.getElementById('progress_fill').style.width = progresso + '%';
            document.getElementById('status_mensagem').textContent = data.mensagem;
            document.getElementById('status_progresso').textContent =
                `${data.progresso} de ${data.total} documentos`;

            const btn = document.getElementById('btn_download');
            btn.disabled = true;
            btn.innerHTML = '<span class="btn-icon">⏳</span> Download em andamento...';

            // Atualiza badge
            document.getElementById('status-step2').innerHTML =
                '<span class="badge badge-info">Baixando...</span>';
        } else {
            const statusBox = document.getElementById('download_status');
            if (statusBox && statusBox.style.display !== 'none') {
                // Download terminou
                const btn = document.getElementById('btn_download');
                btn.disabled = false;
                btn.innerHTML = '<span class="btn-icon">🚀</span> Iniciar Download';

                document.getElementById('status-step2').innerHTML =
                    '<span class="badge badge-success">✓ Concluído</span>';

                // Atualiza estatísticas e habilita busca
                setTimeout(() => {
                    carregarEstatisticas();
                    verificarBuscaDisponivel();
                }, 1000);
            }
        }
    })
    .catch(error => {
        console.error('Erro ao verificar status:', error);
    });
}

// ========================================
// BUSCA
// ========================================

function verificarBuscaDisponivel() {
    fetch('/api/estatisticas')
    .then(response => response.json())
    .then(data => {
        const totalDocs = data.total_documentos;

        if (totalDocs > 0) {
            // Habilita busca
            document.getElementById('busca-disabled-msg').style.display = 'none';
            document.getElementById('busca-enabled').style.display = 'block';
            document.getElementById('badge-busca').className = 'badge badge-success';
            document.getElementById('badge-busca').textContent = `${totalDocs} docs`;
        } else {
            // Desabilita busca
            document.getElementById('busca-disabled-msg').style.display = 'block';
            document.getElementById('busca-enabled').style.display = 'none';
            document.getElementById('badge-busca').className = 'badge badge-disabled';
            document.getElementById('badge-busca').textContent = 'Desabilitado';
        }
    });
}

function realizarBusca() {
    const termo = document.getElementById('termo_busca').value.trim();

    if (!termo) {
        alert('⚠️ Digite um termo para buscar!');
        return;
    }

    const btn = document.getElementById('btn_buscar');
    btn.disabled = true;
    btn.innerHTML = '<span class="btn-icon">⏳</span> Buscando...';

    document.getElementById('busca_status').style.display = 'block';
    document.getElementById('resultados_card').style.display = 'none';

    fetch('/api/buscar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ termo: termo })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('busca_status').style.display = 'none';
        btn.disabled = false;
        btn.innerHTML = '<span class="btn-icon">🔎</span> Buscar';

        exibirResultados(data);
    })
    .catch(error => {
        alert('❌ Erro ao buscar: ' + error);
        document.getElementById('busca_status').style.display = 'none';
        btn.disabled = false;
        btn.innerHTML = '<span class="btn-icon">🔎</span> Buscar';
    });
}

function exibirResultados(data) {
    const card = document.getElementById('resultados_card');
    const resumo = document.getElementById('resultados_resumo');
    const lista = document.getElementById('resultados_list');

    card.style.display = 'block';

    // Resumo
    let htmlResumo = `
        <span class="badge badge-info">${data.documentos_encontrados} documentos</span>
        <span class="badge badge-success">${data.total_ocorrencias} ocorrências</span>
    `;
    resumo.innerHTML = htmlResumo;

    // Lista de resultados
    if (data.resultados.length === 0) {
        lista.innerHTML = `
            <div class="info-box info-warning">
                <div class="info-icon">😕</div>
                <div>
                    <strong>Nenhum resultado encontrado</strong>
                    <p>Termo "${data.termo}" não foi encontrado nos documentos baixados.</p>
                </div>
            </div>
        `;
        return;
    }

    let htmlLista = '';
    data.resultados.forEach(resultado => {
        const tipoNome = resultado.tipo === 'E' ? 'Edital' : 'Diário';
        const tamanhoKb = (resultado.tamanho / 1024).toFixed(2);

        htmlLista += `
            <div class="resultado-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                    <div>
                        <h4 style="color: var(--primary); margin-bottom: 5px;">
                            ${resultado.sigla} - ${tipoNome}
                        </h4>
                        <p style="color: var(--text-light); font-size: 0.9em;">
                            📅 ${formatarDataBR(resultado.data)} • 📄 ${tamanhoKb} KB
                        </p>
                    </div>
                    <span class="badge badge-success" style="font-size: 1.1em;">
                        ${resultado.ocorrencias} ocorrência${resultado.ocorrencias > 1 ? 's' : ''}
                    </span>
                </div>
                <div style="background: var(--bg-light); padding: 10px; border-radius: 8px; font-size: 0.85em; color: var(--text-light); word-break: break-all;">
                    📁 ${resultado.arquivo}
                </div>
            </div>
        `;
    });

    lista.innerHTML = htmlLista;
}

// ========================================
// ESTATÍSTICAS
// ========================================

function carregarEstatisticas() {
    fetch('/api/estatisticas')
    .then(response => response.json())
    .then(data => {
        document.getElementById('stat-documentos').textContent = data.total_documentos;
        document.getElementById('stat-tamanho').textContent = data.tamanho_total_mb + ' MB';
        document.getElementById('stat-tribunais').textContent = Object.keys(data.por_tribunal).length;
    })
    .catch(error => {
        console.error('Erro ao carregar estatísticas:', error);
    });
}

// ========================================
// UTILITÁRIOS
// ========================================

function formatarData(dataISO) {
    const partes = dataISO.split('-');
    return `${partes[2]}/${partes[1]}/${partes[0]}`;
}

function formatarDataBR(data) {
    return data.replace(/-/g, '/');
}
