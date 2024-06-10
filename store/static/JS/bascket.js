import { paginate, updatePaginationButtons, itemsPerPage, currentPage } from './pagination.js';

// Функция для создания элемента корзины
function createBasketElement(product) {
  const basketElement = document.createElement('div');
  basketElement.className = 'basket__el';
  basketElement.innerHTML = `
    <div class="el__delete">
      <button><img src="icons/basket/basket-commerce-and-shopping-svgrepo-com 2.svg" alt="delete"></button>
    </div>
    <a href="goods.html">
      <div class="el__img"><img src="img/main/image 1.png" alt="img"></div>
      <div class="el__descr">
        <div class="el__name">${product.name}</div>
        <div class="el__arc">Артикул: ${product.article}</div>
      </div>
    </a>
    <div class="el__plus">
      <button class="el_minus">-</button>
      <div class="el_value">${product.quantity}</div>
      <button class="el_plus">+</button>
    </div>
    <div class="el__price">${product.price} ₸</div>
  `;
  // Добавляем обработчики событий для кнопок увеличения и уменьшения количества
  basketElement.querySelector('.el_minus').addEventListener('click', () => updateQuantity(basketElement, product, -1));
  basketElement.querySelector('.el_plus').addEventListener('click', () => updateQuantity(basketElement, product, 1));
  
  return basketElement;
}

// Функция для обновления количества товаров
function updateQuantity(basketElement, product, change) {
  product.quantity += change;
  
  // Если количество товара стало 0, удаляем его из корзины
  if (product.quantity < 1) {
    basketElement.remove();
    // Обновляем список продуктов в localStorage, удаляя товар с количеством 0
    let products = JSON.parse(localStorage.getItem('products')) || [];
    products = products.filter(p => p.article !== product.article);
    localStorage.setItem('products', JSON.stringify(products));
  } else {
    // Обновляем отображаемое количество
    basketElement.querySelector('.el_value').innerText = product.quantity;
    // Обновляем список продуктов в localStorage
    let products = JSON.parse(localStorage.getItem('products')) || [];
    const index = products.findIndex(p => p.article === product.article);
    if (index !== -1) {
      products[index].quantity = product.quantity;
      localStorage.setItem('products', JSON.stringify(products));
    }
  }
  
  updateTotalPrice();
}

// Функция для обновления общей стоимости
function updateTotalPrice() {
  const products = JSON.parse(localStorage.getItem('products')) || [];
  let totalPrice = 0;
  products.forEach(product => {
    totalPrice += product.quantity * parseInt(product.price.replace(/\D/g, ''));
  });
  document.querySelector('.purchase__exodus').innerText = `${totalPrice.toLocaleString()} ₸`;
}

// Функция для добавления элементов в контейнер корзины
function populateBasket(container, products) {
  container.innerHTML = ''; // Очистить контейнер перед добавлением новых элементов
  products.forEach(product => {
    const basketElement = createBasketElement(product);
    container.appendChild(basketElement);
  });
}

// Функция для загрузки данных из JSON
async function loadBasketData() {
  try {
    const response = await fetch('products.json');
    const data = await response.json();
    const products = data.products;

    // Сохраняем продукты в localStorage для дальнейшего использования
    localStorage.setItem('products', JSON.stringify(products));

    const paginatedProducts = paginate(products, currentPage, itemsPerPage);
    const basketContainer = document.getElementById('basket-container');
    populateBasket(basketContainer, paginatedProducts);

    // Обновляем кнопки пагинации
    updatePaginationButtons(products.length, itemsPerPage);

    // Обновляем общую стоимость
    updateTotalPrice();
  } catch (error) {
    console.error('Error loading basket data:', error);
  }
}

// Инициализация корзины при загрузке страницы
document.addEventListener('DOMContentLoaded', loadBasketData);
