<template>
  <DeleteProductDialog :show="showDelete" :productName="deleteName" @cancel="showDelete = false" @confirm="confirmDelete" />
  <div class="max-w-7xl mx-auto py-10 px-4">
    <div class="mb-2">
      <h1 class="text-2xl font-semibold text-black mb-4">Product Management</h1>
      <div class="flex flex-col sm:flex-row sm:items-center gap-3">
        <div class="flex-1 relative">
          <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
            <img src="/src/assets/search.svg" alt="Search" class="w-5 h-5" />
          </span>
          <input v-model="search" type="text" placeholder="Search products..." class="w-full sm:w-72 border border-gray-300 rounded-md pl-10 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#030213]" />
        </div>
        <router-link to="/add" class="inline-flex items-center bg-[#030213] text-white px-6 py-2 rounded-md hover:bg-black transition whitespace-nowrap ml-auto">Add Product</router-link>
      </div>
    </div>
    <div v-if="products.length === 0" class="text-gray-400 text-center">No products found.</div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="product in filteredProducts" :key="product.id" class="bg-white rounded-xl border border-gray-200 shadow p-6 flex flex-col gap-2">
        <div class="flex justify-between items-center mb-2">
          <span class="font-semibold text-lg text-black">{{ product.name }}</span>
          <span class="text-xs text-gray-400">ID: {{ product.id }}</span>
        </div>
        <div class="text-[#030213] font-bold text-xl mb-1">${{ product.price }}</div>
        <div class="text-gray-500 text-sm mb-2">{{ product.description }}</div>
        <div class="text-xs text-gray-500 mb-4">Stock: <span class="font-medium text-black">{{ product.stock }}</span></div>
        <div class="flex gap-2 mt-auto">
          <router-link :to="`/product/${product.id}`" class="px-2 py-1 rounded bg-gray-100 text-[#030213] text-xs font-medium hover:bg-gray-200 transition flex items-center gap-1">
            <img src="/src/assets/eye.svg" alt="View" class="w-4 h-4" />
            View
          </router-link>
          <router-link :to="`/edit/${product.id}`" class="px-2 py-1 rounded bg-white border border-gray-300 text-[#030213] text-xs font-medium hover:bg-gray-100 transition flex items-center gap-1">
            <img src="/src/assets/edit.svg" alt="Edit" class="w-4 h-4" />
            Edit
          </router-link>
          <button @click="askDelete(product.id, product.name)" class="px-2 py-1 rounded bg-red-600 text-white text-xs font-medium hover:bg-red-700 transition flex items-center gap-1">
            <img src="/src/assets/bin.svg" alt="Delete" class="w-4 h-4 filter invert" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import DeleteProductDialog from './DeleteProductDialog.vue';

const products = ref([]);
const showDelete = ref(false);
const deleteId = ref(null);
const deleteName = ref('');
const search = ref('');

const fetchProducts = async () => {
  const res = await axios.get('http://localhost:8000/products');
  products.value = res.data;
};

const askDelete = (id, name) => {
  deleteId.value = id;
  deleteName.value = name;
  showDelete.value = true;
};

const confirmDelete = async () => {
  await axios.delete(`http://localhost:8000/products/${deleteId.value}`);
  showDelete.value = false;
  fetchProducts();
};

const filteredProducts = computed(() => {
  if (!search.value) return products.value;
  return products.value.filter(p =>
    p.name.toLowerCase().includes(search.value.toLowerCase()) ||
    (p.description && p.description.toLowerCase().includes(search.value.toLowerCase()))
  );
});

onMounted(fetchProducts);
</script>
