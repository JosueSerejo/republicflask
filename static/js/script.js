const loadMoreBtn = document.getElementById('loadMore');
const cards = document.querySelectorAll('.card');
const filtros = document.querySelectorAll('input');
const searchInput = document.getElementById('searchInput');

// Função de filtragem
function filtrar() {
    const valor = document.querySelector('input[name="valor"]:checked')?.value;
    const tipos = Array.from(document.querySelectorAll('input[name="tipo"]:checked')).map(e => e.value);
    const quartos = Array.from(document.querySelectorAll('input[name="quartos"]:checked')).map(e => e.value);
    const extras = Array.from(document.querySelectorAll('input[name="extras"]:checked')).map(e => e.value);
    const search = searchInput.value.toLowerCase();

    cards.forEach(card => {
        let show = true;

        const cardValor = parseInt(card.dataset.valor);
        const cardTipo = card.dataset.tipo;
        const cardQuartos = parseInt(card.dataset.quartos);
        const cardExtras = card.dataset.extras.split(',');
        const cardEndereco = card.dataset.endereco.toLowerCase();

        if (valor && valor !== 'todos') {
            if (valor === '500' && cardValor > 500) show = false;
            if (valor === '1000' && (cardValor <= 500 || cardValor > 1000)) show = false;
            if (valor === 'acima' && cardValor <= 1000) show = false;
        }

        if (tipos.length && !tipos.includes(cardTipo)) show = false;
        if (quartos.length && !quartos.includes(cardQuartos >= 3 ? '3' : String(cardQuartos))) show = false;
        if (extras.length && !extras.every(extra => cardExtras.includes(extra))) show = false;
        if (search && !cardEndereco.includes(search)) show = false;

        card.style.display = show ? 'block' : 'none';
    });
}

// Inicializa com 6 cards visíveis e esconde os outros
document.addEventListener('DOMContentLoaded', () => {
    // Esconde todos os cards além dos 6 primeiros
    cards.forEach((card, index) => {
        if (index >= 6) {
            card.classList.add('hidden');
        }
    });
    filtrar(); // Aplica o filtro inicial
});

// Ao clicar no botão "Carregar mais"
loadMoreBtn?.addEventListener('click', () => {
    document.querySelectorAll('.card.hidden').forEach(card => {
        card.classList.remove('hidden'); // Remove a classe hidden para exibir os cards
    });
    loadMoreBtn.style.display = 'none'; // Esconde o botão após carregar os cards
    filtrar(); // Reaplica o filtro após mostrar os cards
});

// Filtra sempre que os filtros ou a barra de pesquisa mudam
filtros.forEach(input => {
    input.addEventListener('input', filtrar);
});

searchInput.addEventListener('input', filtrar);
