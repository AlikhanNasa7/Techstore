// Функция для добавления товара в корзину
function addToBasket(product) {
  let basket = JSON.parse(localStorage.getItem('basket')) || [];
  
  // Проверяем, есть ли уже такой товар в корзине
  const existingProduct = basket.find(p => p.article === product.article);
  if (existingProduct) {
    existingProduct.quantity += 1;
  } else {
    product.quantity = 1;
    basket.push(product);
  }

  localStorage.setItem('basket', JSON.stringify(basket));
  updateTotalPrice();
}

// Функция для обновления общей стоимости
function updateTotalPrice() {
  const basket = JSON.parse(localStorage.getItem('basket')) || [];
  let totalPrice = 0;
  basket.forEach(product => {
    totalPrice += product.quantity * parseInt(product.price.replace(/\D/g, ''));
  });
  document.querySelector('.purchase__exodus').innerText = `${totalPrice.toLocaleString()} ₸`;
}

// Функция для создания элемента избранного товара
function createFavoriteElement(product) {
  const favoriteElement = document.createElement('div');
  favoriteElement.className = 'goods__el';
  favoriteElement.innerHTML = `
    <div class="goods__white">
      <a href="goods.html">
        <div class="goods__img"><img src="${product.image}" alt="proc"></div>
        <div class="goods__descr">
          <div class="goods__name">${product.name}</div>
          <div class="goods__wrapper">
            <div class="goods__param">
              <div class="param__type">
                <div class="param__cell">Тип процессора</div>                                      
              </div>
              <div class="param__socket">
                <div class="param__cell">Сокет</div>                                        
              </div>
              <div class="param__core">
                <div class="param__cell">Общее количество ядер</div>                                       
              </div>
              <div class="param__stream">
                <div class="param__cell">Количество потоков</div>                                        
              </div>
              <div class="param__frequency">
                <div class="param__cell">Тактовая частота, ГГц</div>                                      
              </div>
              <div class="param__micro">
                <div class="param__cell">Микроархитектура</div>
              </div>
            </div>
            <div class="goods__data">
              <div class="data__data">${product.type}</div>
              <div class="data__data">${product.socket}</div>
              <div class="data__data">${product.cores}</div>
              <div class="data__data">${product.threads}</div>
              <div class="data__data">${product.frequency}</div>
              <div class="data__data">${product.microarchitecture}</div>
            </div>
          </div>
        </div>
      </a>
    </div>
    <div class="goods__blue">
      <div class="blue__chosen">
        <button><img src="icons/chosen/Vector_3.svg" alt="like"></button>
      </div>
      <div class="blue__avail">
        ${product.availability}
      </div>
      <div class="blue__selfdel">
        <img src="icons/proc/purchase-cash-register-svgrepo-com 1.svg" alt="purch" class="blue__img">
        <div class="blue__text">${product.selfPickup}</div>
      </div>
      <div class="blue__del">
        <img src="icons/proc/delivery-shipping-and-delivery-svgrepo-com 2.svg" alt="del" class="blue__img">
        <div class="blue__text">${product.delivery}</div>
      </div>
      <div class="blue__buy">
        <div class="blue__price">${product.price} ₸</div>
        <div class="blue__buttons">
          <button class="blue__oneclick">
            <img src="icons/proc/basket-commerce-and-shopping-svgrepo-com 1.svg" alt="one">
            <div class="button_text">В один клик</div>
          </button> 
          <button class="blue__basket">
            <img src="icons/proc/cart-commerce-and-shopping-svgrepo-com 1 (1).svg" alt="cart">
            <div class="button__text">В корзину</div>
          </button>
        </div>
      </div>
    </div>
  `;

  // Добавляем обработчик события для кнопки "В корзину"
  favoriteElement.querySelector('.blue__basket').addEventListener('click', () => addToBasket(product));

  return favoriteElement;
}

// Функция для добавления элементов в контейнер избранных товаров
function populateFavorites(container, products) {
  products.forEach(product => {
    const favoriteElement = createFavoriteElement(product);
    container.appendChild(favoriteElement);
  });
}

// Функция для загрузки данных из JSON для избранных товаров
async function loadFavoriteData() {
  try {
    const response = await fetch('chosen.json');
    const data = await response.json();
    const products = data.products;

    const favoritesContainer = document.getElementById('favorites-container');
    populateFavorites(favoritesContainer, products);
  } catch (error) {
    console.error('Error loading favorite data:', error);
  }
}

// Инициализация избранных товаров при загрузке страницы
document.addEventListener('DOMContentLoaded', loadFavoriteData);
