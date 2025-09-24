<template>
  <div class="flex justify-center items-center min-h-[60vh] py-10">
    <div class="bg-white rounded-xl border border-gray-200 shadow-lg p-8 w-full max-w-md">
      <h2 class="text-2xl font-semibold text-black mb-6">{{ isEdit ? 'Edit Product' : 'Add New Product' }}</h2>
      <form @submit.prevent="handleSubmit" class="space-y-5">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Product Name</label>
          <input v-model="form.name" required class="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#030213]" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea v-model="form.description" class="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#030213]" rows="3"></textarea>
        </div>
          <div class="flex gap-4">
            <div class="w-1/2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Price ($)</label>
              <input v-model.number="form.price" type="number" required class="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#030213]" />
            </div>
            <div class="w-1/2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Stock</label>
              <input v-model.number="form.stock" type="number" min="0" required class="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#030213]" />
            </div>
          </div>
        <div class="flex gap-3 mt-6">
          <button type="submit" class="inline-flex items-center justify-center bg-[#030213] text-white px-6 py-2 rounded-md font-medium hover:bg-black transition">{{ isEdit ? 'Update Product' : 'Add Product' }}</button>
          <router-link to="/" class="inline-flex items-center justify-center border border-gray-300 text-gray-700 px-6 py-2 rounded-md font-medium hover:bg-gray-100 transition">Cancel</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const isEdit = ref(!!route.params.id);
const form = ref({ name: '', price: 0, description: '', stock: 0 });

const fetchProduct = async () => {
  if (isEdit.value) {
    const res = await axios.get(`http://localhost:8000/products/${route.params.id}`);
    form.value = res.data;
  }
};

const handleSubmit = async () => {
  if (isEdit.value) {
    await axios.put(`http://localhost:8000/products/${route.params.id}`, form.value);
  } else {
    await axios.post('http://localhost:8000/products', form.value);
  }
  router.push('/');
};

onMounted(fetchProduct);
</script>
