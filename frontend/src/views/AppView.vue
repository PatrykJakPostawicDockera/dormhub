<template>
  <MainNavbar />
  <div class="min-h-screen px-5 pt-20 sm:pb-32 md:px-48 lg:pb-10">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import MainNavbar from '@/components/MainNavbar.vue';
</script>
