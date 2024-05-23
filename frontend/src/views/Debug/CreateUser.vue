<template>
  <div class="flex h-screen w-screen flex-col items-center justify-center">
    <FormKit type="form" :actions="false" @submit="handleQuickInsert">
      <FormKit
        outer-class="$reset !w-[80dvw]"
        input-class="!h-[30dvh]"
        type="textarea"
        name="users"
        label="User(s) JSON"
        placeholder="User"
        rows="100"
        cols="900"
      />
      <FormKit
        outer-class="$reset !w-[80dvw]"
        type="file"
        name="avatars"
        label="Avatar(s)"
        placeholder="Avatar"
        multiple
      />
      <MainButton class="mt-5" button-type="submit" button-text="Quick register" />
    </FormKit>
  </div>
</template>

<script setup lang="ts">
import MainButton from '@/components/MainButton.vue';
import type { UserRegisterModel } from '@/models/user.model';
import { apiInstance } from '@/helpers/api';
import { fileToBase64 } from '@/helpers/imageToBase';
import { useToast } from 'vue-toastification';

interface QuickRegisterFields {
  users: string;
  avatars: {
    name: string;
    file: File;
  }[];
}
const handleQuickInsert = async (fields: QuickRegisterFields) => {
  let users = JSON.parse(fields.users) as UserRegisterModel[];
  for (let user of users) {
    console.log(user);
    if (user.AvatarUrl) {
      const file = fields.avatars.find((avatar) => avatar.name === user.Name);
      if (file) {
        user.AvatarUrl = await apiInstance
          .post<{
            PhotoUrl: string;
          }>('inner/photos/upload', {
            PhotoData: await fileToBase64(file.file),
          })
          .then((response) => {
            return response ? response.PhotoUrl : '';
          });
      }
    }
    await apiInstance.post<string>('users/register', user).then((response) => {
      useToast().success('User registered: ' + response);
    });
  }
  console.log(users);
};
</script>
