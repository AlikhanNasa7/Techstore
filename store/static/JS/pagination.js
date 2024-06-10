let currentPage = 1;
const itemsPerPage = 3;

function paginate(products, page, itemsPerPage) {
  const start = (page - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return products.slice(start, end);
}

function updatePaginationButtons(totalItems, itemsPerPage) {
  const totalPages = Math.ceil(totalItems / itemsPerPage);
  const paginationContainer = document.querySelector('.proc__links');
  paginationContainer.innerHTML = '';

  for (let i = 1; i <= totalPages; i++) {
    const pageButton = document.createElement('a');
    pageButton.href = '#';
    pageButton.innerHTML = `<div class="links__pagenmb">${i}</div>`;
    pageButton.addEventListener('click', (e) => {
      e.preventDefault();
      currentPage = i;
      loadBasketData(); // Обновите данные корзины при смене страницы
    });
    paginationContainer.appendChild(pageButton);
  }
}

export { paginate, updatePaginationButtons, itemsPerPage, currentPage };
