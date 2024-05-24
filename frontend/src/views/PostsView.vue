<template>
  <div class="flex justify-between pb-5">
    <h1 class="text-3xl">Posts</h1>
    <MainButton class="w-fit" button-text="Create post" @click="show = !show" />
  </div>
  <div class="flex flex-col gap-12">
    <PostCard v-for="post in posts" :key="post.PostId" :post="post" @post-update="fetchPosts" />
  </div>
  <CreatePostModal v-model="show" @confirm="handleModalClose" />
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { apiInstance } from '@/helpers/api';
import type PostModel from '@/models/post.model';
import PostCard from '@/components/PostCard.vue';
import MainButton from '@/components/MainButton.vue';
import CreatePostModal from '@/components/CreatePostModal.vue';
import { useAuthStore } from '@/stores/auth';

const posts = ref<PostModel[]>([]);
const show = ref(false);

onMounted(async () => {
  await fetchPosts();
});

const fetchPosts = async () => {
  await apiInstance.get<PostModel[]>(`posts`, true).then((response) => {
    posts.value = response ? response : [];
  });
};

const handleModalClose = async () => {
  show.value = false;
  await fetchPosts();
};
</script>
