import { ref } from 'vue';
import api from '../utils/api';

const cart = ref({ items: [] });
const isInitialized = ref(false);
const listeners = ref(new Set());

export function useCart() {
  const notifyListeners = () => {
    listeners.value.forEach(listener => listener());
  };
  // Initialize cart if not already done
  const initializeCart = async () => {
    if (!isInitialized.value) {
      await fetchCart();
      isInitialized.value = true;
    }
  };
  const addToCart = async (product) => {
    try {
      console.log('Adding to cart:', {
        productId: product.id,
        stock: product.stock,
        currentCart: cart.value
      });
      
      const response = await api.post('/cart/add', {
        product_id: product.id,
        quantity: 1
      });
      
      cart.value = response.data;
      notifyListeners();
      return response.data;
    } catch (error) {
      throw error; // Re-throw to handle in the component
    }
  };

  const removeFromCart = async (itemId) => {
    try {
      // Optimistically remove the item from the UI
      const itemIndex = cart.value.items.findIndex(item => item.id === itemId);
      if (itemIndex !== -1) {
        cart.value = {
          ...cart.value,
          items: cart.value.items.filter(item => item.id !== itemId)
        };
      }

      // Make the API call
      const response = await api.delete(`/cart/remove/${itemId}`);
      
      // Update with the server response to ensure consistency
      cart.value = response.data;
      notifyListeners();
    } catch (error) {
      // If there was an error, refresh the cart to ensure consistency
      await fetchCart();
      notifyListeners();
    }
  };

  const fetchCart = async () => {
    try {
      const response = await api.get('/cart');
      cart.value = response.data;
    } catch (error) {
    }
  };

  const onCartUpdate = (callback) => {
    listeners.value.add(callback);
    return () => {
      listeners.value.delete(callback);
    };
  };

  return {
    cart,
    addToCart,
    removeFromCart,
    fetchCart,
    initializeCart,
    onCartUpdate
  };
}