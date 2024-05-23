<template>
  <div class="flex flex-col gap-1">
    <p>{{ props.label }}</p>
    <div
      class="flex flex-col gap-2 rounded-lg border p-2 focus-within:border-0 focus-within:outline focus-within:outline-2 focus-within:outline-offset-2"
    >
      <div class="grid grid-cols-3 gap-2">
        <div
          v-for="obj in attachmentsUrls"
          :key="obj.name"
          class="relative flex items-center gap-2"
          @mouseover="obj.mouseover = true"
          @mouseleave="obj.mouseover = false"
        >
          <img v-if="obj.url" :src="obj.url" :alt="obj.name" />

          <p
            :class="{ '!opacity-100': obj.mouseover }"
            class="bg-basicDark/50 hover:bg-basicDark/70 absolute left-0 top-0 flex h-full w-full cursor-pointer items-center justify-center text-white opacity-0 transition-all hover:font-medium"
            @click="removeAttachment(obj.name)"
          >
            Usuń
          </p>
        </div>
      </div>
      <div class="flex items-center gap-2" v-if="attachmentsCount <= limit">
        <input
          type="file"
          @change="validateFile"
          class="hidden"
          ref="fileInput"
          multiple
          max="limit"
        />
        <MainButton @click="fileInput?.click()" button-text="Wybierz plik" />
      </div>
      <div class="flex flex-col">
        <p class="text-greyLight text-sm">
          Maks. {{ limit }} załączników, po {{ sizeLimit }}mb każdy
        </p>
        <p class="text-greyLight text-sm">Dozwolone rozszerzenia: {{ extensions.join(', ') }}</p>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import MainButton from '@/components/MainButton.vue';
import { useToast } from 'vue-toastification';

interface FileAttachment {
  name: string;
  mouseover: boolean;
  url?: string;
}

const toast = useToast();

const attachments = ref<File[]>([]);
const attachmentsCount = ref(0);
const attachmentsUrls = ref<FileAttachment[]>([]);
const fileInput = ref<HTMLInputElement | null>(null);

const props = defineProps<{
  name: string;
  label: string;
  limit: number;
  sizeLimit: number;
  extensions: string[];
}>();

const emit = defineEmits<{
  fileChange: [files: File[]];
}>();

const validateFile = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  const maxSize = props.limit * 1024 * 1024;
  const files = target.files;
  if (!files) return;
  const file = files[0];

  if (attachmentsCount.value >= props.limit) {
    toast.error(`Przekroczono limit załączników`);
    return;
  }

  if (file.size > maxSize) {
    toast.error(`Plik jest za duży`);
    return;
  }

  if (!props.extensions.includes(file.name.split('.').pop()!)) {
    toast.error(`Nieprawidłowe rozszerzenie pliku`);
    return;
  }

  attachments.value.push(file);
  attachmentsCount.value++;
  if (file.type.includes('image')) {
    const fileUrl = await parseFileToImage(file);
    attachmentsUrls.value.push({ name: file.name, mouseover: false, url: fileUrl });
  } else {
    attachmentsUrls.value.push({ name: file.name, mouseover: false });
  }
  emit('fileChange', attachments.value);
};

const removeAttachment = (name: string) => {
  const index = attachmentsUrls.value.findIndex((obj) => obj.name === name);
  if (index === -1) return;
  attachmentsUrls.value.splice(index, 1);
  attachments.value.splice(index, 1);
  attachmentsCount.value--;
  emit('fileChange', attachments.value);
};

const parseFileToImage = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      resolve(reader.result as string);
    };
    reader.onerror = (error) => reject(error);
  });
};
</script>
