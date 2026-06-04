let carrinhoProdutos = [];

document.addEventListener("DOMContentLoaded", function () {
    const btnAdicionar = document.getElementById("btn-adicionar-produto");
    if (btnAdicionar) {
        btnAdicionar.addEventListener("click", adicionarProdutoCarrinho);
    }

    const inputDescValor = document.getElementById("desconto_valor");
    const inputDescPorcentagem = document.getElementById("desconto_percentual");

    if (inputDescValor) inputDescValor.addEventListener("input", recalcularTotaisVenda);
    if (inputDescPorcentagem) inputDescPorcentagem.addEventListener("input", recalcularTotaisVenda);
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

    tbody.innerHTML = "";

    carrinhoProdutos.forEach(item => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${item.nome}</td>
            <td>${item.quantidade}</td>
            <td>${Utils.formatarMoeda(item.valor_unitario)}</td>
            <td>${Utils.formatarMoeda(item.valor_total)}</td>
            <td>
                <button type="button" class="btn btn-danger" style="padding: 5px 10px;" onclick="removerProdutoCarrinho('${item.produto_id}')">Remover</button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    recalcularTotaisVenda();
}

function recalcularTotaisVenda() {
    let totalBruto = 0;
    carrinhoProdutos.forEach(item => { totalBruto += item.valor_total; });

    const inputDescValor = document.getElementById("desconto_valor");
    const inputDescPorcentagem = document.getElementById("desconto_percentual");

    let descValor = inputDescValor ? parseFloat(inputDescValor.value) || 0 : 0;
    let descPorcentagem = inputDescPorcentagem ? parseFloat(inputDescPorcentagem.value) || 0 : 0;

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
}