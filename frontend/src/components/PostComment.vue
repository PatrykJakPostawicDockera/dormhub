<template>
  <div
    class="flex w-full flex-col bg-white shadow transition-all duration-200 ease-in-out dark:bg-[#50504D] sm:rounded-lg"
    :class="{
      'border-2 border-primaryLight dark:border-primaryDark':
        comment.UserId === useAuthStore().getTokenData.UserId && !editMode,
    }"
  >
    <div class="flex flex-col gap-1 p-3 sm:rounded-lg">
      <p
        class="text-sm font-medium"
        :class="{
          'font-semibold text-primaryLight dark:text-primaryDark':
            comment.UserId === useAuthStore().getTokenData.UserId,
        }"
      >
        {{ comment.Nickname || comment.UserId }}
      </p>
      <p v-if="!editMode" class="text-sm">{{ comment.CommentContent }}</p>
      <MainInput v-else label="" name="newComment" v-model:value="newComment" />
    </div>
    <div
      class="flex items-center justify-between rounded-b-lg bg-gray-50 px-4 py-4 dark:bg-black sm:px-6"
      :class="{
        '!py-2': comment.UserId === useAuthStore().getTokenData.UserId,
      }"
    >
      <p class="text-sm font-medium text-gray-500">
        {{ new Date(comment.Date).toLocaleDateString() }}
      </p>
      <div
        v-if="comment.UserId === useAuthStore().getTokenData.UserId && !editMode"
        class="flex gap-2"
      >
        <MainButton @click="editMode = !editMode" buttonText="Edit" color="transparent">
          <Pencil class="transition-all duration-150 ease-in hover:scale-105" />
        </MainButton>
        <MainButton @click="deleteComment" color="alert" buttonText="Delete" />
      </div>
      <div v-if="editMode" class="flex gap-2">
        <MainButton buttonText="Save" @click="updateEditedComment" />
        <MainButton @click="updateEditedComment" color="alert">
          <X />
        </MainButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type CommentModel from '@/models/comment.model';
import { useAuthStore } from '@/stores/auth';
import { apiInstance } from '@/helpers/api';
import { ref } from 'vue';
import MainInput from '@/components/MainInput.vue';
import MainButton from '@/components/MainButton.vue';
import { X, Pencil } from 'lucide-vue-next';

const props = defineProps<{
  comment: CommentModel;
}>();

const emit = defineEmits<{
  commentUpdate: [];
}>();

const editMode = ref(false);
const newComment = ref(props.comment.CommentContent);

const deleteComment = async () => {
  await apiInstance.delete(`comments/${props.comment.CommentId}`, true);
  emit('commentUpdate');
};

const updateEditedComment = async () => {
  await apiInstance
    .put(
      `comments/${props.comment.CommentId}`,
      {
        CommentContent: newComment.value,
      },
      true,
    )
    .then(() => {
      editMode.value = false;
      emit('commentUpdate');
    });
};
</script>
