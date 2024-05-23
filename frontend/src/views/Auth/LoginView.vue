<template>
  <Navbar />
  <div class="flex h-screen w-screen flex-col items-center justify-center">
    <FormKit type="form" :actions="false" @submit="handleLogin">
      <FormKit type="text" name="username" label="Username" placeholder="Username" />
      <FormKit type="password" name="password" label="Password" placeholder="Password" />
      <MainButton class="w-full" button-type="submit" button-text="Login" />
    </FormKit>
    <RouterLink to="/register" class="mt-2 text-blue-500">
      Don't have an account? Register here
    </RouterLink>
  </div>
</template>

<script setup lang="ts">
import Navbar from '@/components/MainNavbar.vue';
import { useAuthStore } from '@/stores/auth';
import MainButton from '@/components/MainButton.vue';

const auth = useAuthStore();

interface LoginForm {
  username: string;
  password: string;
}

const handleLogin = async (fields: LoginForm) => {
  await auth.login(fields.username, fields.password);
};
</script>
