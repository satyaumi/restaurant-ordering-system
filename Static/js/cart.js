// document.addEventListener("DOMContentLoaded", function () {

//   document.querySelectorAll(".add-to-cart").forEach(button => {
//     button.addEventListener("click", function () {

//       fetch("/add-to-cart/", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//           "X-CSRFToken": getCookie("csrftoken"),
//         },
//         body: JSON.stringify({
//           item_id: this.dataset.itemId,
//           discount: this.dataset.discount || 0
//         })
//       })
//       .then(res => res.json())
//       .then(data => {
//         if (data.error) {
//           alert(data.error);
//         } else {
//           alert("Added to cart");
//         }
//       });

//     });
//   });

// });

// // ADD TO CART (OFFER ITEMS)
//   document.querySelectorAll(".order-offer").forEach(btn => {
//     btn.addEventListener("click", function (e) {
//       e.preventDefault();

//       fetch("/add-to-cart/", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//           "X-CSRFToken": getCookie("csrftoken"),
//         },
//         body: JSON.stringify({
//           item_id: this.dataset.itemId,
//           discount: this.dataset.discount
//         })
//       })
//       .then(res => res.json())
//       .then(() => {
//         loadCartItems();
//         $("#cart-modal").modal("show");
//       });
//     });
//   });

// // CART POPUP LOADER
// function loadCartItems() {
//   fetch("/cart/items/")
//     .then(res => res.json())
//     .then(data => {
//       const list = document.getElementById("cart-items-list");
//       if (!list) return;

//       list.innerHTML = "";

//       data.items.forEach(item => {
//         list.innerHTML += `
//           <li>
//             <strong>${item.name}</strong><br>
//             ₹${item.price} × ${item.quantity}<br>
//             Total: ₹${item.total}
//           </li><hr>
//         `;
//       });
//     })
//     .catch(err => {
//       console.warn("Cart popup load failed", err);
//     });
// }


// // CSRF HELPER
// function getCookie(name) {
//   let cookieValue = null;
//   if (document.cookie && document.cookie !== "") {
//     document.cookie.split(";").forEach(cookie => {
//       cookie = cookie.trim();
//       if (cookie.startsWith(name + "=")) {
//         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//       }
//     });
//   }
//   return cookieValue;
// }




document.addEventListener("DOMContentLoaded", function () {

  // NORMAL ADD TO CART
  document.querySelectorAll(".add-to-cart").forEach(button => {
    button.addEventListener("click", function () {
      addToCart(this.dataset.itemId, this.dataset.discount || 0);
    });

 
  });
  
   
  // OFFER ADD TO CART
  document.querySelectorAll(".order-offer").forEach(button => {
  button.addEventListener("click", function (e) {
    e.preventDefault();
    console.log("Offer clicked:", this.dataset.itemId); // 👈 DEBUG
    addToCart(this.dataset.itemId, this.dataset.discount);
  });
});


});

function addToCart(itemId, discount) {
   console.log("Offer clicked:", itemId, discount);
  fetch("/add-to-cart/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      item_id: itemId,
      discount: discount
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.error) {
      alert(data.error);
      return;
    }

    if (data.success) {
      loadCartItems();
      $("#cart-modal").modal("show");
    } else {
      alert("Failed to add item to cart");
    }
  })
  .catch(err => {
    console.error(err);
    alert("Something went wrong");
  });
}


// LOAD CART ITEMS INTO POPUP
function loadCartItems() {
  fetch("/cart/items/")
    .then(res => res.json())
    .then(data => {
      const list = document.getElementById("cart-items-list");
      if (!list) return;

      list.innerHTML = "";

      if (data.items.length === 0) {
        list.innerHTML = "<li>Your cart is empty</li>";
        return;
      }

   
        data.items.forEach(item => {
  list.innerHTML += `
    <li>
      <strong>${item.name}</strong><br>
      ₹${item.price} × ${item.quantity}<br>
      <strong>Total: ₹${item.total}</strong><br>

      <button class="btn btn-sm btn-danger mt-2"
              onclick="removeFromCart(${item.id})">
        Remove
      </button>
    </li>
    <hr>
  `;
});

}).catch(err => {
      console.warn("Popup loaded but items failed", err);
    });
}
// remove cart
function removeFromCart(itemId) {
  fetch("/cart/remove/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      item_id: itemId
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      loadCartItems(); // refresh popup
    } else {
      alert(data.error || "Failed to remove item");
    }
  })
  .catch(err => {
    console.error(err);
  });
}

// CSRF HELPER
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    document.cookie.split(";").forEach(cookie => {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
      }
    });
  }
  return cookieValue;
}




