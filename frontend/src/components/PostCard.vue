<template>
  <EditPostModal :post="post" @confirm="handleEdit" v-model="editMode" />
  <div class="flex w-full flex-col gap-5 lg:flex-row">
    <div
      class="h-full basis-1/2 overflow-hidden bg-white shadow dark:bg-[#50504D] sm:rounded-lg"
      ref="postCard"
      :class="{
        'border-2 border-primaryLight dark:border-primaryDark':
          post.UserId === useAuthStore().getTokenData.UserId && !editMode,
      }"
    >
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white">{{ post.PostTitle }}</h3>
        <p class="mt-1 text-wrap text-sm text-gray-500 dark:text-white/70">
          {{ post.PostContent }}
        </p>
      </div>
      <div
        class="grid gap-1"
        :style="{
          gridTemplateColumns: `repeat(${post.Photos.length}, minmax(0, 1fr))`,
        }"
      >
        <img
          v-for="photo in post.Photos"
          :src="photo"
          :key="photo"
          alt="Post image"
          class="h-48 w-full object-cover"
        />
      </div>
      <div class="flex justify-between bg-gray-50 px-4 py-4 dark:bg-black sm:px-6">
        <div class="text-sm text-gray-500">
          <p>
            Created by <span class="font-medium">{{ post.Nickname }}</span>
          </p>
          <p>
            on <span class="font-medium">{{ post.Date }}</span>
          </p>
        </div>
        <div
          v-if="post.UserId === useAuthStore().getTokenData.UserId && !editMode"
          class="flex gap-2"
        >
          <MainButton @click="editMode = !editMode" buttonText="Edit" color="transparent">
            <Pencil class="transition-all duration-150 ease-in hover:scale-105" />
          </MainButton>
          <MainButton @click="deletePost" color="alert" buttonText="Delete" />
        </div>
      </div>
    </div>
    <div
      class="flex h-96 basis-1/2 flex-col gap-3"
      :style="{
        'max-height': `${height}px`,
      }"
    >
      <div class="ml-1 flex items-center gap-3">
        <MainInput
          class="w-full"
          v-model:value="comment"
          name="comment"
          label=""
          type="text"
          autocomplete="off"
          required
        />
        <MainButton @click="addComment">
          <SendHorizontal />
        </MainButton>
      </div>
      <div class="flex flex-col gap-3 overflow-y-auto">
        <PostComment
          :comment="com"
          v-for="com in comments"
          :key="com.CommentId"
          @comment-update="fetchComments"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type PostModel from '@/models/post.model';
import PostComment from '@/components/PostComment.vue';
import type CommentModel from '@/models/comment.model';
import { onMounted, ref } from 'vue';
import { apiInstance } from '@/helpers/api';
import MainInput from '@/components/MainInput.vue';
import MainButton from '@/components/MainButton.vue';
import { useAuthStore } from '@/stores/auth';
import { Pencil, SendHorizontal } from 'lucide-vue-next';
import EditPostModal from '@/components/EditPostModal.vue';

const props = defineProps<{
  post: PostModel;
}>();

const emit = defineEmits<{
  postUpdate: [];
}>();

const authStore = useAuthStore();

const postCard = ref<HTMLDivElement | null>(null);
const height = ref<number>(0);
const comments = ref<CommentModel[]>([]);

const comment = ref<string>('');
const editMode = ref<boolean>(false);

const addComment = async () => {
  if (comment.value === '') return;
  await apiInstance.post<CommentModel>(
    `posts/${props.post.PostId}/comments/create`,
    {
      CommentContent: comment.value,
    },
    true,
  );
  await fetchComments();
  comment.value = '';
};

const fetchComments = async () => {
  const response = await apiInstance.get<CommentModel[]>(
    `posts/${props.post.PostId}/comments`,
    true,
  );
  comments.value = response ? response : [];
};

onMounted(async () => {
  await fetchComments();
  height.value = postCard.value?.clientHeight || 0;
  window.addEventListener('resize', () => {
    height.value = postCard.value?.clientHeight || 0;
  });
});

const deletePost = async () => {
  await apiInstance.delete(`posts/${props.post.PostId}`, true);
  emit('postUpdate');
};

const handleEdit = async () => {
  editMode.value = false;
  emit('postUpdate');
};
</script>
