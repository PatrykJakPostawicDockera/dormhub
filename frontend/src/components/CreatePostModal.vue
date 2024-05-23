<template>
  <VueFinalModal
    class="flex items-center justify-center"
    content-class="flex flex-col gap-3 w-2/3 sm:w-1/2 justify-between rounded-xl bg-white p-7 dark:bg-[#50504D] text-textLight dark:text-textDark"
  >
    <div class="flex justify-between">
      <h1 class="text-3xl">Create post</h1>
      <button
        class="h-auto w-fit rounded-xl bg-primaryLight p-2 text-white transition-all duration-200 ease-in-out hover:scale-110 focus:bg-opacity-50 dark:bg-primaryDark dark:bg-opacity-50 hover:sm:scale-[110%]"
        @click="emit('confirm')"
      >
        <X />
      </button>
    </div>
    <div class="">
      <FileUpload
        class="basis-1/3"
        name="imageUpload"
        label="Dołącz pliki"
        :limit="6"
        :size-limit="5"
        :extensions="['jpeg', 'jpg', 'png', 'webp', 'heic']"
        @file-change="handleFileChange"
      />
    </div>
    <FormKit type="form" :actions="false" @submit="handlePostCreation">
      <div class="flex gap-5">
        <FormKit type="text" name="title" label="Title" placeholder="Title" />
        <FormKit type="select" name="type" label="Type" :options="postTypes" />
      </div>
      <FormKit outer-class="$reset !w-full" type="textarea" name="content" label="Content" />
      <MainButton class="mt-2" button-text="Create post" type="submit" />
    </FormKit>
  </VueFinalModal>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { VueFinalModal } from 'vue-final-modal';
import { X } from 'lucide-vue-next';
import FileUpload from '@/components/FileUpload.vue';
import MainButton from '@/components/MainButton.vue';
import type { PostTypes } from '@/models/post.model';
import { apiInstance } from '@/helpers/api';
import { fileToBase64 } from '@/helpers/imageToBase';

const emit = defineEmits<{
  (e: 'confirm'): void;
}>();

const postTypes = ref<Record<number, string>>({});
const images = ref<File[]>([]);

onMounted(async () => {
  await apiInstance.get<PostTypes[]>('posts/types', true).then((res) => {
    postTypes.value = res
      ? res.reduce(
          (acc, curr) => {
            acc[curr.TypeId] = curr.Name;
            return acc;
          },
          {} as Record<number, string>,
        )
      : {};
  });
});

const handleFileChange = (files: File[]) => {
  images.value = files;
};

interface PostForm {
  title: string;
  content: string;
  type: string;
}

const handlePostCreation = async (data: PostForm) => {
  let basedImages: string[] = [];
  for (const file of images.value) {
    await fileToBase64(file, 1920, 1080).then(async (res) => {
      basedImages.push(
        await apiInstance
          .post<{
            PhotoUrl: string;
          }>('inner/photos/upload', {
            PhotoData: res,
          })
          .then((response) => (response ? response.PhotoUrl : '')),
      );
    });
  }
  await apiInstance
    .post<string>(
      'posts/create',
      {
        PostTitle: data.title,
        PostContent: data.content,
        PostType: parseInt(data.type),
        Photos: basedImages,
      },
      true,
    )
    .then((res) => {
      console.log(res);
      emit('confirm');
    });
};
</script>
