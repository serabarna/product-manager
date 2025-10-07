<template>
  <div class="min-h-screen bg-gray-50">
    <router-view />
    <ShoppingCart />
  </div>
</template>

<script setup>
import ShoppingCart from './views/ShoppingCart.vue';
</script>

<style>
body {
  margin: 0;
  padding: 0;
}
</style>
