<template>
  <div class="flex justify-center items-center min-h-[60vh] py-10">
    <div v-if="product" class="bg-white rounded-xl border border-gray-200 shadow-lg w-full max-w-md p-8 relative">
      <router-link to="/" class="absolute top-4 right-4 text-gray-400 hover:text-black text-xl font-bold">&times;</router-link>
  <h2 class="text-lg font-bold text-black mb-2">Product Details</h2>
  <div class="text-xl font-semibold text-black mb-2">{{ product.name }}</div>
      <div class="h-px bg-gray-200 my-4"></div>
      <div class="flex justify-between items-center mb-2">
        <span class="text-gray-400 text-sm">Product ID:</span>
        <span class="text-black text-sm">{{ product.id }}</span>
      </div>
      <div class="flex justify-between items-center mb-2">
        <span class="text-gray-400 text-sm">Stock:</span>
        <span class="text-black text-sm">{{ product.stock }} units</span>
      </div>
      <div class="flex justify-between items-center mb-2">
        <span class="text-gray-400 text-sm">Price:</span>
        <span class="text-[#030213] font-bold text-base">${{ product.price }}</span>
      </div>
      <div class="text-gray-500 text-base mt-4 mb-2">{{ product.description }}</div>
    </div>
    <div v-else class="text-gray-500">Loading...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const product = ref(null);

const fetchProduct = async () => {
  const res = await axios.get(`http://localhost:8000/products/${route.params.id}`);
  product.value = res.data;
};

onMounted(fetchProduct);
</script>
