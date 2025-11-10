// Função para salvar configurações
function salvarConfig() {
    const pasta = document.getElementById('pasta_salvamento').value;
    const workers = document.getElementById('workers').value;

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
            alert('✅ Configurações salvas com sucesso!');
            carregarEstatisticas();
        }
    })
    .catch(error => {
        alert('❌ Erro ao salvar configurações: ' + error);
    });
}

// Função para filtrar tribunais
function filtrarTribunais() {
    const termo = document.getElementById('busca_tribunal').value.toLowerCase();
    const items = document.querySelectorAll('.tribunal-item');
    const grupos = document.querySelectorAll('.uf-group');

    items.forEach(item => {
        const sigla = item.dataset.sigla.toLowerCase();
        const nome = item.dataset.nome.toLowerCase();

        if (sigla.includes(termo) || nome.includes(termo)) {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });

    // Esconde grupos vazios
    grupos.forEach(grupo => {
        const visibleItems = grupo.querySelectorAll('.tribunal-item[style="display: flex;"]');
        if (visibleItems.length === 0 && termo !== '') {
            grupo.style.display = 'none';
        } else {
            grupo.style.display = 'block';
        }
    });
}

// Função para selecionar todos os tribunais
function selecionarTodos() {
    const checkboxes = document.querySelectorAll('.tribunal-checkbox');
    checkboxes.forEach(cb => cb.checked = true);
}

// Função para desselecionar todos
function deselecionarTodos() {
    const checkboxes = document.querySelectorAll('.tribunal-checkbox');
    checkboxes.forEach(cb => cb.checked = false);
}

// Função para selecionar tribunais superiores
function selecionarSuperiores() {
    const superiores = ['STJ', 'STF', 'TST', 'TSE', 'STM', 'CNJ', 'CJF'];
    const checkboxes = document.querySelectorAll('.tribunal-checkbox');

    checkboxes.forEach(cb => {
        cb.checked = superiores.includes(cb.value);
    });
}

// Função para iniciar download
function iniciarDownload() {
    const checkboxes = document.querySelectorAll('.tribunal-checkbox:checked');
    const tribunais = Array.from(checkboxes).map(cb => cb.value);

    if (tribunais.length === 0) {
        alert('⚠️ Selecione pelo menos um tribunal!');
        return;
    }

    const dataInicio = document.getElementById('data_inicio').value;
    const dataFim = document.getElementById('data_fim').value;

    // Converte datas para formato DD/MM/YYYY
    const dataInicioFormatada = dataInicio ? formatarData(dataInicio) : null;
    const dataFimFormatada = dataFim ? formatarData(dataFim) : null;

    // Tipos selecionados
    const tiposCheckboxes = document.querySelectorAll('.checkbox-group input[type="checkbox"]:checked');
    const tipos = Array.from(tiposCheckboxes).map(cb => cb.value);

    if (tipos.length === 0) {
        alert('⚠️ Selecione pelo menos um tipo de caderno!');
        return;
    }

    const btn = document.getElementById('btn_download');
    btn.disabled = true;
    btn.textContent = '⏳ Iniciando...';

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
            btn.textContent = '🚀 Iniciar Download';
        }
    })
    .catch(error => {
        alert('❌ Erro ao iniciar download: ' + error);
        btn.disabled = false;
        btn.textContent = '🚀 Iniciar Download';
    });
}

// Função para verificar status do download
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
            btn.textContent = '⏳ Download em andamento...';
        } else {
            const statusBox = document.getElementById('download_status');
            if (statusBox && statusBox.style.display !== 'none') {
                // Download terminou
                const btn = document.getElementById('btn_download');
                btn.disabled = false;
                btn.textContent = '🚀 Iniciar Download';

                // Atualiza estatísticas
                setTimeout(carregarEstatisticas, 1000);
            }
        }
    })
    .catch(error => {
        console.error('Erro ao verificar status:', error);
    });
}

// Função para carregar estatísticas
function carregarEstatisticas() {
    fetch('/api/estatisticas')
    .then(response => response.json())
    .then(data => {
        const content = document.getElementById('estatisticas_content');
        if (!content) return;

        let html = '<div class="estatisticas-grid">';

        html += `
            <div class="estatistica-item">
                <span class="numero">${data.total_documentos}</span>
                <span class="label">Documentos Baixados</span>
            </div>
        `;

        html += `
            <div class="estatistica-item">
                <span class="numero">${data.tamanho_total_mb}</span>
                <span class="label">MB Armazenados</span>
            </div>
        `;

        html += `
            <div class="estatistica-item">
                <span class="numero">${Object.keys(data.por_tribunal).length}</span>
                <span class="label">Tribunais</span>
            </div>
        `;

        const totalEditais = data.por_tipo['E'] || 0;
        const totalDiarios = data.por_tipo['D'] || 0;

        html += `
            <div class="estatistica-item">
                <span class="numero">${totalEditais}</span>
                <span class="label">Editais</span>
            </div>
        `;

        html += `
            <div class="estatistica-item">
                <span class="numero">${totalDiarios}</span>
                <span class="label">Diários</span>
            </div>
        `;

        html += '</div>';

        // Top 5 tribunais
        if (Object.keys(data.por_tribunal).length > 0) {
            const topTribunais = Object.entries(data.por_tribunal)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 5);

            html += '<div class="info-grid" style="margin-top: 20px;">';
            topTribunais.forEach(([sigla, count]) => {
                html += `
                    <div class="info-item">
                        <strong>${sigla}</strong>
                        <span>${count} documentos</span>
                    </div>
                `;
            });
            html += '</div>';
        }

        content.innerHTML = html;
    })
    .catch(error => {
        console.error('Erro ao carregar estatísticas:', error);
    });
}

// Função para realizar busca
function realizarBusca() {
    const termo = document.getElementById('termo_busca').value.trim();

    if (!termo) {
        alert('⚠️ Digite um termo para buscar!');
        return;
    }

    const btn = document.getElementById('btn_buscar');
    btn.disabled = true;
    btn.textContent = '⏳ Buscando...';

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
        btn.textContent = 'Buscar';

        exibirResultados(data);
    })
    .catch(error => {
        alert('❌ Erro ao buscar: ' + error);
        document.getElementById('busca_status').style.display = 'none';
        btn.disabled = false;
        btn.textContent = 'Buscar';
    });
}

// Função para exibir resultados da busca
function exibirResultados(data) {
    const card = document.getElementById('resultados_card');
    const resumo = document.getElementById('resultados_resumo');
    const lista = document.getElementById('resultados_list');

    card.style.display = 'block';

    // Resumo
    let htmlResumo = `
        <h3>🎯 Termo: "${data.termo}"</h3>
        <p><strong>${data.documentos_encontrados}</strong> documentos encontrados de ${data.total_documentos_analisados} analisados</p>
        <p><strong>${data.total_ocorrencias}</strong> ocorrências encontradas no total</p>
    `;
    resumo.innerHTML = htmlResumo;

    // Lista de resultados
    if (data.resultados.length === 0) {
        lista.innerHTML = `
            <div class="alert alert-warning">
                Nenhum resultado encontrado para "${data.termo}".
                Tente outro termo ou baixe mais documentos.
            </div>
        `;
        return;
    }

    let htmlLista = '';
    data.resultados.forEach(resultado => {
        const tipoNome = resultado.tipo === 'E' ? 'Edital' : 'Diário';
        const tamanhoKb = (resultado.tamanho / 1024).toFixed(2);

        htmlLista += `
            <div class="resultado-item">
                <div class="resultado-header">
                    <span class="resultado-tribunal">${resultado.sigla} - ${tipoNome}</span>
                    <span class="resultado-ocorrencias">
                        ${resultado.ocorrencias} ocorrência${resultado.ocorrencias > 1 ? 's' : ''}
                    </span>
                </div>
                <div class="resultado-info">
                    <span>📅 ${formatarDataBR(resultado.data)}</span>
                    <span>📄 ${tamanhoKb} KB</span>
                </div>
                <div class="resultado-arquivo">
                    📁 ${resultado.arquivo}
                </div>
            </div>
        `;
    });

    lista.innerHTML = htmlLista;
}

// Função para formatar data (YYYY-MM-DD para DD/MM/YYYY)
function formatarData(dataISO) {
    const partes = dataISO.split('-');
    return `${partes[2]}/${partes[1]}/${partes[0]}`;
}

// Função para formatar data (DD-MM-YYYY para DD/MM/YYYY)
function formatarDataBR(data) {
    return data.replace(/-/g, '/');
}
