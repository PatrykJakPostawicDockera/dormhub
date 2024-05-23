<template>
  <nav class="absolute left-0 top-0 flex w-full justify-between px-7 py-5">
    <div class="flex items-center gap-2">
      <RouterLink to="/app" class="!scale-100 !text-3xl font-medium">
        Dorm<span class="!font-bold text-primaryLight dark:text-primaryDark">Hub</span>
      </RouterLink>
      <div class="flex flex-col lg:flex-row lg:gap-2" v-if="authStore.isAuthenticated">
        <p class="font-bold">{{ authStore.getTokenData.Name }}</p>
        <p>{{ authStore.getTokenData.Address }}</p>
      </div>
    </div>
    <div class="hidden items-center gap-5 lg:flex">
      <RouterLink
        to="/app/posts"
        class="flex gap-1 transition-all duration-200 ease-in-out hover:scale-105"
      >
        <MessageSquare />
        <p class="text-lg">Posts</p>
      </RouterLink>
      <RouterLink
        to="/app/todos"
        class="flex gap-1 transition-all duration-200 ease-in-out hover:scale-105"
      >
        <SquareCheckBig />
        <p class="text-lg">Todos</p>
      </RouterLink>
      <RouterLink
        to="/app/guests"
        class="flex gap-1 transition-all duration-200 ease-in-out hover:scale-105"
      >
        <Users />
        <p class="text-lg">Guests</p>
      </RouterLink>
      <RouterLink
        to="/app/settings"
        class="flex gap-1 transition-all duration-200 ease-in-out hover:scale-105"
      >
        <Settings2 />
        <p class="text-lg">Settings</p>
      </RouterLink>
      <MainButton
        v-if="authStore.isAuthenticated"
        button-text="Logout"
        @click="authStore.logout()"
      />
    </div>
  </nav>
  <div
    class="fixed bottom-0 z-50 flex w-screen justify-center bg-gradient-to-t from-dark/10 to-light/0 backdrop-blur-[1px] dark:from-light/10 dark:to-dark/0 lg:hidden"
  >
    <nav class="my-10 flex gap-5 rounded-3xl bg-light px-2 py-1 dark:bg-dark">
      <RouterLink
        to="/app/todos"
        class="flex items-center justify-center gap-1 p-2 transition-all duration-200 ease-in-out"
      >
        <SquareCheckBig />
      </RouterLink>
      <RouterLink
        to="/app/posts"
        class="flex items-center justify-center gap-1 p-2 transition-all duration-200 ease-in-out"
      >
        <MessageSquare class="h-7 w-7" />
      </RouterLink>
      <RouterLink
        to="/app"
        class="flex scale-125 items-center justify-center gap-1 rounded-full bg-primaryLight p-2 text-white transition-all duration-200 ease-in-out dark:bg-primaryDark"
      >
        <LayoutDashboard
          :class="{
            '!scale-100': $route.path === '/app',
          }"
          class="h-7 w-7 scale-90 transition-all duration-200 ease-in-out"
        />
      </RouterLink>
      <RouterLink
        to="/app/guests"
        class="flex items-center justify-center gap-1 p-2 transition-all duration-200 ease-in-out"
      >
        <Users class="h-7 w-7" />
      </RouterLink>
      <RouterLink
        to="/app/settings"
        class="flex items-center justify-center gap-1 p-2 transition-all duration-200 ease-in-out"
      >
        <Settings2 class="h-7 w-7" />
      </RouterLink>
    </nav>
  </div>
</template>

<script setup lang="ts">
import {
  HandCoins,
  MessageSquare,
  SquareCheckBig,
  Users,
  Settings2,
  LayoutDashboard,
} from 'lucide-vue-next';
import MainButton from '@/components/MainButton.vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
</script>

<style scoped>
.router-link-exact-active {
  @apply scale-125 text-xl sm:scale-105;
}
</style>
