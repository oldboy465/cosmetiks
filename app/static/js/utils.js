const Utils = {
    formatarMoeda: function (valor) {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);
    },

    mascararCPF: function (input) {
        let v = input.value.replace(/\D/g, "");
        if (v.length > 11) v = v.slice(0, 11);
        v = v.replace(/(\D* text )/g, "");
        v = v.replace(/(\d{3})(\d)/, "$1.$2");
        v = v.replace(/(\d{3})(\d)/, "$1.$2");
        v = v.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
        input.value = v;
    },

    mascararTelefone: function (input) {
        let v = input.value.replace(/\D/g, "");
        if (v.length > 11) v = v.slice(0, 11);
        v = v.replace(/^(\d{2})(\d)/g, "($1) $2");
        v = v.replace(/(\d{5})(\d)/, "$1-$2");
        input.value = v;
    },

    mascararCEP: function (input) {
        let v = input.value.replace(/\D/g, "");
        if (v.length > 8) v = v.slice(0, 8);
        v = v.replace(/^(\d{5})(\d)/, "$1-$2");
        input.value = v;
    },

    copiarTexto: function (texto, botaoEl) {
        navigator.clipboard.writeText(texto).then(() => {
            const textoOriginal = botaoEl.innerHTML;
            botaoEl.innerHTML = "Copiado!";
            botaoEl.style.backgroundColor = "#00b074";
            setTimeout(() => {
                botaoEl.innerHTML = textoOriginal;
                botaoEl.style.backgroundColor = "";
            }, 2000);
        }).catch(err => {
            console.error("Erro ao copiar: ", err);
        });
    }
};