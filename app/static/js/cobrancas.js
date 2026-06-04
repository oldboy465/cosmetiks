document.addEventListener("DOMContentLoaded", function () {
    const btnCopiarMensagem = document.querySelectorAll(".btn-copiar-mensagem");
    btnCopiarMensagem.forEach(btn => {
        btn.addEventListener("click", function () {
            const targetId = this.getAttribute("data-target");
            const textoMensagem = document.getElementById(targetId).value;
            const financeiroId = this.getAttribute("data-financeiro");
            const modelo = this.getAttribute("data-modelo");

            Utils.copiarTexto(textoMensagem, this);
            registrarDisparoCobranca(financeiroId, modelo, textoMensagem);
        });
    });

    const btnCopiarWhatsapp = document.querySelectorAll(".btn-copiar-whatsapp");
    btnCopiarWhatsapp.forEach(btn => {
        btn.addEventListener("click", function () {
            const numeroZap = this.getAttribute("data-whatsapp").replace(/\D/g, "");
            const targetId = this.getAttribute("data-target");
            const textoMensagem = encodeURIComponent(document.getElementById(targetId).value);
            const financeiroId = this.getAttribute("data-financeiro");
            const modelo = this.getAttribute("data-modelo");

            const urlZap = `https://api.whatsapp.com/send?phone=55${numeroZap}&text=${textoMensagem}`;
            window.open(urlZap, '_blank');

            registrarDisparoCobranca(financeiroId, modelo, document.getElementById(targetId).value);
        });
    });
});

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
            console.log("Histórico de cobrança atualizado automaticamente.");
        }
    })
    .catch(error => console.error("Erro ao auditar disparo de cobranca:", error));
}