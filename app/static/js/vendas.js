let carrinhoProdutos = [];

document.addEventListener("DOMContentLoaded", function () {
    const btnAdicionar = document.getElementById("btn-adicionar-produto");
    
    if (btnAdicionar) {
        btnAdicionar.addEventListener("click", adicionarProdutoCarrinho);
    }

    const inputDescValor = document.getElementById("desconto_valor");
    const inputDescPorcentagem = document.getElementById("desconto_percentual");
    const inputParcelas = document.getElementById("quantidade_parcelas");
    const inputDate = document.getElementById("data_venda");
    
    // --- NOVO CAMPO: Captura o observador da Data Prevista de Pagamento ---
    const inputDatePrevista = document.getElementById("data_prevista_pagamento");

    if (inputDescValor) inputDescValor.addEventListener("input", recalcularTotaisVenda);
    if (inputDescPorcentagem) inputDescPorcentagem.addEventListener("input", recalcularTotaisVenda);
    if (inputParcelas) inputParcelas.addEventListener("input", recalcularTotaisVenda);
    if (inputDate) inputDate.addEventListener("input", recalcularTotaisVenda);
    
    // Anexa o gatilho de recalculo visual na data prevista também
    if (inputDatePrevista) inputDatePrevista.addEventListener("input", recalcularTotaisVenda);

    // Inicialização da Data de Venda com o dia de Hoje caso esteja vazio
    if (inputDate && !inputDate.value) {
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        inputDate.value = `${yyyy}-${mm}-${dd}`;
    }
});

function adicionarProdutoCarrinho() {
    const selectProduto = document.getElementById("select-produto");
    const inputQuantidade = document.getElementById("input-quantidade");

    if (!selectProduto.value || parseInt(inputQuantidade.value) <= 0) {
        alert("Selecione um produto válido e informe a quantidade.");
        return;
    }

    const option = selectProduto.options[selectProduto.selectedIndex];
    const produtoId = option.value;
    const nomeProduto = option.getAttribute("data-nome");
    const precoVenda = parseFloat(option.getAttribute("data-preco"));
    const estoqueAtual = parseInt(option.getAttribute("data-estoque"));
    const quantidade = parseInt(inputQuantidade.value);

    if (quantidade > estoqueAtual) {
        alert(`Estoque insuficiente. Quantidade disponível: ${estoqueAtual}`);
        return;
    }

    const itemExistente = carrinhoProdutos.find(item => item.produto_id === produtoId);

    if (itemExistente) {
        if ((itemExistente.quantidade + quantidade) > estoqueAtual) {
            alert(`A soma ultrapassa o estoque disponível (${estoqueAtual}).`);
            return;
        }
        itemExistente.quantidade += quantidade;
        itemExistente.valor_total = itemExistente.quantidade * precoVenda;
    } else {
        carrinhoProdutos.push({
            produto_id: produtoId,
            nome: nomeProduto,
            quantidade: quantidade,
            valor_unitario: precoVenda,
            valor_total: quantidade * precoVenda
        });
    }

    inputQuantidade.value = 1;
    renderizarTabelaCarrinho();
}

function removerProdutoCarrinho(produtoId) {
    carrinhoProdutos = carrinhoProdutos.filter(item => item.produto_id !== produtoId);
    renderizarTabelaCarrinho();
}

function renderizarTabelaCarrinho() {
    const tbody = document.getElementById("tbody-carrinho");
    
    if (!tbody) return;

    if (carrinhoProdutos.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-muted); padding: 30px;">Nenhum cosmético inserido no carrinho de compras até o momento.</td></tr>`;
        recalcularTotaisVenda();
        return;
    }

    tbody.innerHTML = "";

    carrinhoProdutos.forEach(item => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><strong>${item.nome}</strong></td>
            <td>${item.quantidade}</td>
            <td>${Utils.formatarMoeda(item.valor_unitario)}</td>
            <td><strong>${Utils.formatarMoeda(item.valor_total)}</strong></td>
            <td style="text-align: center;">
                <button type="button" class="btn btn-danger" style="padding: 6px 12px; font-size: 12px; font-weight:700; border-radius:6px;" onclick="removerProdutoCarrinho('${item.produto_id}')">Remover</button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    recalcularTotaisVenda();
}

function recalcularTotaisVenda() {
    let totalBruto = 0;
    carrinhoProdutos.forEach(item => { 
        totalBruto += item.valor_total; 
    });

    const inputDescValor = document.getElementById("desconto_valor");
    const inputDescPorcentagem = document.getElementById("desconto_percentual");
    const inputParcelas = document.getElementById("quantidade_parcelas");

    let descValor = inputDescValor ? parseFloat(inputDescValor.value) || 0 : 0;
    let descPorcentagem = inputDescPorcentagem ? parseFloat(inputDescPorcentagem.value) || 0 : 0;
    let qtdParcelas = inputParcelas ? parseInt(inputParcelas.value) || 1 : 1;

    let totalLiquido = totalBruto;

    if (descPorcentagem > 0) {
        totalLiquido = totalBruto - (totalBruto * (descPorcentagem / 100));
    } else {
        totalLiquido = totalBruto - descValor;
    }

    if (totalLiquido < 0) totalLiquido = 0;

    const elTotalBruto = document.getElementById("render-total-bruto");
    const elTotalLiquido = document.getElementById("render-total-liquido");
    const hiddenProdutosJson = document.getElementById("produtos_json");

    if (elTotalBruto) elTotalBruto.innerText = Utils.formatarMoeda(totalBruto);
    if (elTotalLiquido) elTotalLiquido.innerText = Utils.formatarMoeda(totalLiquido);
    if (hiddenProdutosJson) hiddenProdutosJson.value = JSON.stringify(carrinhoProdutos);

    renderizarPrevisaoParcelas(totalLiquido, qtdParcelas);
}

function renderizarPrevisaoParcelas(totalLiquido, qtdParcelas) {
    const container = document.getElementById("render-preview-parcelas");
    const inputDate = document.getElementById("data_venda");
    const inputDatePrevista = document.getElementById("data_prevista_pagamento");
    
    if (!container) return;

    if (totalLiquido <= 0 || qtdParcelas <= 1 || !inputDate || !inputDate.value) {
        container.innerHTML = "";
        container.style.display = "none";
        return;
    }

    container.style.display = "block";
    let html = '<div style="font-weight: 700; margin-bottom: 10px; color: var(--primary-color);">Cronograma de Recebimento Previsto:</div><ul style="list-style: none; padding: 0; margin: 0; display:flex; flex-direction:column; gap:6px;">';
    
    let valorParcela = totalLiquido / qtdParcelas;
    
    // --- NOVA LÓGICA DE CÁLCULO BASEADA NA DATA PREVISTA DE PAGAMENTO ---
    // Se existir uma data prevista explícita informada, utilizamos ela como o gatilho da primeira parcela.
    let dataReferenciaStr = (inputDatePrevista && inputDatePrevista.value) ? inputDatePrevista.value : inputDate.value;
    let dataBase = new Date(dataReferenciaStr + 'T12:00:00');

    for (let i = 1; i <= qtdParcelas; i++) {
        let dataVencimento = new Date(dataBase.getTime());
        
        // Se a Data Prevista está preenchida, o primeiro pagamento é no próprio dia previsto.
        if (inputDatePrevista && inputDatePrevista.value) {
            dataVencimento.setDate(dataBase.getDate() + (30 * (i - 1)));
        } else {
            // Comportamento original: A primeira parcela é para daqui a 30 dias após a venda
            dataVencimento.setDate(dataBase.getDate() + (30 * i));
        }
        
        let dia = String(dataVencimento.getDate()).padStart(2, '0');
        let mes = String(dataVencimento.getMonth() + 1).padStart(2, '0');
        let ano = dataVencimento.getFullYear();
        
        html += `<li style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #eef2f5;">
            <span style="color: var(--text-muted);">Parcela ${i}/${qtdParcelas} (Venc: <strong>${dia}/${mes}/${ano}</strong>)</span>
            <strong style="color: var(--text-main);">${Utils.formatarMoeda(valorParcela)}</strong>
        </li>`;
    }
    
    html += '</ul>';
    container.innerHTML = html;
}