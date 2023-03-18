const totalPriceElement = document.querySelector('.total-price');
const cart = document.querySelector('.cart');
const filterForm = document.querySelector('#filterForm');

const cartItemsCount = {
    cartItemsCountElement: document.querySelector('.cart_items-count'),
    add: function () {
        const itemsCount = parseInt(this.cartItemsCountElement.textContent);
        this.cartItemsCountElement.textContent =  itemsCount + 1;
    },
    reduce: function() {
        const itemsCount = parseInt(this.cartItemsCountElement.textContent);
        this.cartItemsCountElement.textContent =  itemsCount - 1;
    }
}

function generatePlaceholder() {
    const row = document.createElement('div');
    row.classList.add('row');

    const col = document.createElement('div');
    col.classList.add('col','my-5', 'text-center');

    const title = document.createElement('div');
    title.classList.add('h2');
    title.textContent = 'Your cart is empty.';

    const linkWrapper = document.createElement('div');
    linkWrapper.classList.add('fs-5');

    const link = document.createElement('a');
    link.classList.add('text-decoration-none');
    link.href = window.location.origin;
    link.textContent = 'Show categories';

    linkWrapper.append(link)
    col.append(title, linkWrapper);
    row.append(col);

    return row;
};

function sendPersonalSettings(value) {
    const queryParams = new URLSearchParams({
        filter_form: value
    })
    const options = {
        method: 'GET',
        mode: 'same-origin'
    };

    fetch(window.location.origin + '/personal/?' + queryParams, options)
        .then(response => {
            if (!response.ok) {
                alert('Server error: Personal settings doesn\'t saved.')
            }
        });
}

function createForm(target) {
    const product_code_query = 'input[name=product_code]';
    const category_query = 'input[name=category]';
    const procut_code = target.querySelector(product_code_query);
    const category = target.querySelector(category_query);
    const form = new FormData();
    form.append('category', category.value);
    form.append('product_code', procut_code.value);

    return form;
};

function addToCart(event) {
    const target = event.target;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const options = {
        method: 'POST',
        body: createForm(target.parentElement),
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin'
    };

    fetch(window.location.origin + '/cart/add/', options)
        .then(response => {
            if (response.status === 200) {
                target.textContent = 'Remove from Cart';
                target.classList.replace('btn-primary', 'btn-success');
                target.removeEventListener('click', addToCart);
                target.addEventListener('click', removeFromCart);
                cartItemsCount.add()
            }
        });
};

function removeFromCart(event) {
    const target = event.target;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const options = {
        method: 'POST',
        body: createForm(target.parentElement),
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin'
    };

    fetch(window.location.origin + '/cart/remove/', options)
        .then(response => {
            if (response.status === 200) {
                target.textContent = 'Add to Cart';
                target.classList.replace('btn-success' ,'btn-primary');
                target.removeEventListener('click', removeFromCart);
                target.addEventListener('click', addToCart);
                cartItemsCount.reduce()
            }
        });
};

function deleteFromCart(event, el, totalPriceElement) {
    const target = event.target;
    const productPriceElement = el.querySelector('.product-price');
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const options = {
        method: 'POST',
        body: createForm(el),
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin'
    };

    fetch(window.location.origin + '/cart/remove/', options)
        .then(response => {
            if (response.status === 200) {
                return response.text();
            }
        })
        .then(product_code => {
            const productPrice = parseFloat(productPriceElement.textContent);
            const totalPrice = parseFloat(totalPriceElement.textContent);
            totalPriceElement.textContent = totalPrice - productPrice;
            el.remove();
            cartItemsCount.reduce()

            if (cart.children.length === 1) {
                cart.innerHTML = '';
                cart.append(generatePlaceholder());
            }
        });
};

function addProductCount(event, el, reduceProductCountBtn, totalPriceElement) {
    const target = event.target;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const productCountElement = el.querySelector('.product-count');
    const productPriceElement = el.querySelector('.product-price');
    const itemPriceElement = el.querySelector('input[name=price]');
    const itemPrice = parseFloat(itemPriceElement.value);
    const options = {
        method: 'POST',
        body: createForm(el),
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin'
    };
    fetch(window.location.origin + '/cart/add/', options)
        .then(response => {
            if (response.status === 200) {
                const productCount = parseInt(productCountElement.textContent);
                const productPrice = parseFloat(productPriceElement.textContent);
                const updatedProductCount = productCount + 1;
                productCountElement.textContent = updatedProductCount;
                productPriceElement.textContent = (productPrice + itemPrice).toFixed(1);
                totalPrice =  parseFloat(totalPriceElement.textContent);
                totalPriceElement.textContent = (totalPrice + itemPrice).toFixed(1);
                if (updatedProductCount >= 1) {
                    reduceProductCountBtn.disabled = false;
                }
            }
        });
};

function reduceProductCount(event, el, totalPriceElement) {
    const target = event.target;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const productCountElement = el.querySelector('.product-count');
    const productPriceElement = el.querySelector('.product-price');
    const itemPriceElement = el.querySelector('input[name=price]');
    const itemPrice = parseFloat(itemPriceElement.value);
    const options = {
        method: 'POST',
        body: createForm(el),
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin'
    };
    fetch(window.location.origin + '/cart/reduce/', options)
        .then(response => {
            if (response.status === 200) {
                const productCount = parseInt(productCountElement.textContent);
                const productPrice = parseFloat(productPriceElement.textContent);
                const updatedProductCount = productCount - 1;
                productCountElement.textContent = updatedProductCount;
                productPriceElement.textContent = (productPrice - itemPrice).toFixed(1);
                totalPrice =  parseFloat(totalPriceElement.textContent);
                totalPriceElement.textContent = (totalPrice - itemPrice).toFixed(1);
                if (updatedProductCount <= 1) {
                    target.disabled = true;
                }
            }
        });
};

document.querySelectorAll('.cart-product')
    .forEach(el => {
        const removeFromCartBtn = el.querySelector('.remove-from-cart_btn');
        const deleteFromCartBtn = el.querySelector('.delete-from-cart_btn');
        const addProductCountBtn = el.querySelector('.add-product-count_btn');
        const reduceProductCountBtn = el.querySelector('.reduce-product-count_btn');

        addProductCountBtn.addEventListener('click',(event) => {
            addProductCount(event, el, reduceProductCountBtn, totalPriceElement);
        });

        reduceProductCountBtn.addEventListener('click', (event) => {
            reduceProductCount(event, el, totalPriceElement);
        });

        deleteFromCartBtn.addEventListener('click', (event) => {
            deleteFromCart(event, el, totalPriceElement);
        });
    });

document.querySelectorAll('.add-to-cart_btn').forEach((el) => {
    el.addEventListener('click', addToCart);
});

document.querySelectorAll('.remove-from-cart_btn').forEach((el) => {
    el.addEventListener('click', removeFromCart);
});

if (filterForm) {
    filterForm.addEventListener('hidden.bs.collapse', event => {
        sendPersonalSettings('collapsed')
    });

    filterForm.addEventListener('shown.bs.collapse', event => {
        sendPersonalSettings('expanded')
    }); 
};
