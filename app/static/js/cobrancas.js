document.addEventListener("DOMContentLoaded", function () {

    // Inicialização dos botões de cópia de mensagem
    // A lógica de captura de data-modelo múltiplo foi substituída pela mensagem única e inteligente
    const btnCopiarMensagem = document.querySelectorAll(".btn-copiar-mensagem");

    btnCopiarMensagem.forEach(btn => {
        btn.addEventListener("click", function () {
            const targetId = this.getAttribute("data-target");
            const textoMensagem = document.getElementById(targetId).value;
            const financeiroId = this.getAttribute("data-financeiro");
            
            // --- NOVA LÓGICA DE COBRANÇA UNIFICADA ---
            // Fixamos o modelo como "Padrao" para manter a assinatura com o backend
            // sem a necessidade de manter vários if/elses legados.
            const modelo = "Padrao";

            // Executa a cópia para a área de transferência do dispositivo
            Utils.copiarTexto(textoMensagem, this);

            // Grava na auditoria assincronamente
            registrarDisparoCobranca(financeiroId, modelo, textoMensagem);
        });
    });

    // Inicialização dos botões de disparo via WhatsApp
    const btnCopiarWhatsapp = document.querySelectorAll(".btn-copiar-whatsapp");

    btnCopiarWhatsapp.forEach(btn => {
        btn.addEventListener("click", function () {
            // Higieniza o número, mantendo apenas dígitos
            const numeroZap = this.getAttribute("data-whatsapp").replace(/\D/g, "");
            const targetId = this.getAttribute("data-target");
            
            // Captura o texto exato da nova mensagem inteligente
            const textoMensagemBruto = document.getElementById(targetId).value;
            const textoMensagem = encodeURIComponent(textoMensagemBruto);
            const financeiroId = this.getAttribute("data-financeiro");
            
            // --- NOVA LÓGICA DE COBRANÇA UNIFICADA ---
            const modelo = "Padrao";

            // Monta o link nativo do WhatsApp com a mensagem pré-preenchida
            const urlZap = `https://api.whatsapp.com/send?phone=55${numeroZap}&text=${textoMensagem}`;
            
            // Abre o WhatsApp Web ou o App do dispositivo
            window.open(urlZap, '_blank');

            // Grava a auditoria mantendo o registro da ação do revendedor
            registrarDisparoCobranca(financeiroId, modelo, textoMensagemBruto);
        });
    });
});

/**
 * Função responsável por enviar silenciosamente a auditoria do disparo.
 * Mantivemos o parâmetro modelo para retrocompatibilidade de parâmetros com a API.
 */
function registrarDisparoCobranca(financeiroId, modelo, mensagem) {
    fetch(`/cobrancas/registrar/${financeiroId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `modelo=${encodeURIComponent(modelo)}&mensagem=${encodeURIComponent(mensagem)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            console.log("Histórico de cobrança inteligente atualizado automaticamente no servidor.");
        }
    })
    .catch(error => console.error("Erro crítico ao auditar disparo de cobrança:", error));
}