<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
    <div class="bg-white rounded-xl border border-gray-200 shadow-lg w-full max-w-md p-6 relative">
      <h3 class="text-lg font-semibold text-black mb-2">Delete Product</h3>
      <p class="text-sm text-gray-400 mb-6">Are you sure you want to delete "{{ productName }}"? This action cannot be undone.</p>
      <div class="flex justify-end gap-3">
        <button @click="$emit('cancel')" class="inline-flex items-center justify-center border border-gray-300 text-gray-700 px-6 py-2 rounded-md font-medium hover:bg-gray-100 transition">Cancel</button>
        <button @click="$emit('confirm')" class="inline-flex items-center justify-center bg-red-600 text-white px-6 py-2 rounded-md font-medium hover:bg-red-700 transition">Delete Product</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: Boolean,
  productName: String
});
</script>
