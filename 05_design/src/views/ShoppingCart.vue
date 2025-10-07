<template>
  <div class="fixed bottom-4 left-4 z-50">
    <div class="bg-white rounded-lg shadow-lg border border-gray-200 w-80">
      <div class="p-4 border-b border-gray-200">
        <h2 class="text-lg font-semibold text-black flex items-center gap-2">
          <span>Shopping Cart</span>
          <span class="text-sm text-gray-500">({{ totalItems }} items)</span>
        </h2>
      </div>
      
      <div class="max-h-96 overflow-y-auto">
        <div v-if="cart.items.length === 0" class="p-4 text-gray-500 text-center">
          Your cart is empty
        </div>
        <div v-else class="divide-y divide-gray-200">
          <div v-for="item in cart.items" :key="item.id" class="p-4 flex items-start gap-3">
            <div class="flex-1">
              <h3 class="font-medium text-black">{{ item.product.name }}</h3>
              <div class="text-sm text-gray-500">
                Quantity: {{ item.quantity }}
              </div>
              <div class="text-sm font-medium text-black">
                ${{ (item.product.price * item.quantity).toFixed(2) }}
              </div>
            </div>
            <button 
              @click="async () => {
                await removeFromCart(item.id);
              }"
              class="text-red-600 hover:text-red-700 transition"
            >
              <img src="/src/assets/bin.svg" alt="Remove" class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
      
      <div v-if="cart.items.length > 0" class="p-4 border-t border-gray-200">
        <div class="flex justify-between items-center mb-4">
          <span class="font-semibold text-black">Total:</span>
          <span class="font-semibold text-black">${{ totalPrice.toFixed(2) }}</span>
        </div>
        <button class="w-full bg-[#030213] text-white px-4 py-2 rounded-md hover:bg-black transition">
          Checkout
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useCart } from '../composables/useCart';

const { cart, removeFromCart, initializeCart } = useCart();

const totalItems = computed(() => 
  cart.value?.items?.reduce((sum, item) => sum + (item?.quantity || 0), 0) || 0
);

const totalPrice = computed(() => 
  cart.value?.items?.reduce((sum, item) => 
    sum + ((item?.product?.price || 0) * (item?.quantity || 0)), 0) || 0
);

onMounted(async () => {
  await initializeCart();
});
</script>