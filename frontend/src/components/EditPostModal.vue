<template>
  <VueFinalModal
    class="flex items-center justify-center"
    content-class="flex flex-col gap-3 w-2/3 sm:w-1/2 justify-between rounded-xl bg-white p-7 dark:bg-[#50504D] text-textLight dark:text-textDark"
  >
    <div class="flex justify-between">
      <h1 class="text-3xl">Edit post</h1>
      <button
        class="h-auto w-fit rounded-xl bg-primaryLight p-2 text-white transition-all duration-200 ease-in-out hover:scale-110 focus:bg-opacity-50 dark:bg-primaryDark dark:bg-opacity-50 hover:sm:scale-[110%]"
        @click="emit('confirm')"
      >
        <X />
      </button>
    </div>
    <div class="">
      <p>Current images:</p>
      <div class="flex gap-3">
        <div v-for="image in newPost.Photos" :key="image" class="relative flex gap-3">
          <img :src="image" class="h-32 w-32 rounded-xl" alt="post image" />
          <div
            class="absolute right-0 top-0 cursor-pointer rounded-bl-xl rounded-tr-xl bg-primaryLight p-1 text-white"
            @click="removeImage(image)"
          >
            <Trash2 />
          </div>
        </div>
      </div>
      <FileUpload
        class="basis-1/3"
        name="imageUpload"
        label=""
        :limit="6"
        :size-limit="5"
        :extensions="['jpeg', 'jpg', 'png', 'webp', 'heic']"
        @file-change="handleFileChange"
      />
    </div>
    <FormKit type="form" :actions="false" @submit="handlePostCreation">
      <div class="flex gap-5">
        <FormKit
          type="text"
          name="title"
          label="Title"
          placeholder="Title"
          :value="post.PostTitle"
        />
        <FormKit
          type="select"
          name="type"
          label="Type"
          :options="postTypes"
          :value="post.PostType"
        />
      </div>
      <FormKit
        outer-class="$reset !w-full"
        type="textarea"
        name="content"
        label="Content"
        :value="post.PostContent"
      />
      <MainButton class="mt-2" button-text="Create post" type="submit" />
    </FormKit>
  </VueFinalModal>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { VueFinalModal } from 'vue-final-modal';
import { Trash2, X } from 'lucide-vue-next';
import FileUpload from '@/components/FileUpload.vue';
import MainButton from '@/components/MainButton.vue';
import type { PostTypes } from '@/models/post.model';
import type PostModel from '@/models/post.model';
import { apiInstance } from '@/helpers/api';
import { fileToBase64 } from '@/helpers/imageToBase';

const props = defineProps<{
  post: PostModel;
}>();

const emit = defineEmits<{
  (e: 'confirm'): void;
}>();

const newPost = ref<PostModel>(props.post);

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
    .put<string>(
      `posts/${newPost.value.PostId}`,
      {
        PostTitle: data.title,
        PostContent: data.content,
        PostType: parseInt(data.type),
        Photos: [...newPost.value.Photos, ...basedImages],
      },
      true,
    )
    .then((res) => {
      console.log(res);
      emit('confirm');
    });
};

const removeImage = (image: string) => {
  newPost.value.Photos = newPost.value.Photos.filter((img) => img !== image);
};
</script>
