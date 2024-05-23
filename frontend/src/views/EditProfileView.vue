<template>
  <div class="flex flex-col gap-3">
    <FormKit type="form" :actions="false" @submit="handleUpdateData">
      <div class="flex justify-between py-3">
        <h1 class="text-3xl">Edit profile information</h1>
        <MainButton class="w-fit" button-text="Save changes" type="submit" />
      </div>
      <div class="flex items-center gap-3 rounded-xl bg-white p-7 dark:bg-[#50504D]">
        <img id="preview" :src="userData.AvatarUrl" alt="Avatar" class="h-32 w-32 rounded-xl" />
        <FormKit
          outer-class="$reset w-full"
          name="profilePhoto"
          type="file"
          label="Avatar"
          placeholder="Avatar"
          validation-visibility="dirty"
          v-model="files"
        />
      </div>
      <div class="mt-5 flex flex-col gap-3 rounded-xl bg-white p-7 dark:bg-[#50504D]">
        <p class="text-xl font-medium">Change password</p>
        <div class="flex gap-5">
          <MainInput
            class="w-full"
            label="New password"
            name="password"
            type="password"
            v-model:value="password"
            :required="false"
          />
          <MainInput
            class="w-full"
            label="Confirm new password"
            name="password_confirm"
            type="password"
            v-model:value="passwordConfirm"
            :required="false"
          />
        </div>
        <MainButton class="w-full" @click="handlePasswordUpdate" button-text="Change password" />
      </div>
      <div class="mt-5 flex flex-col gap-3 rounded-xl bg-white p-7 dark:bg-[#50504D]">
        <p class="text-xl font-medium">Personal info</p>
        <div class="flex gap-5">
          <FormKit
            outer-class="$reset w-full"
            name="name"
            type="text"
            label="Name"
            placeholder="Name"
            validation="required"
            validation-visibility="blur"
            v-model="userData.Name"
          />
          <FormKit
            outer-class="$reset w-full"
            name="surname"
            type="text"
            label="Surname"
            placeholder="Surname"
            v-model="userData.Surname"
          />
        </div>
        <div class="flex gap-5">
          <FormKit
            outer-class="$reset w-full"
            name="nickname"
            type="text"
            label="Nickname"
            placeholder="Nickname"
            v-model="userData.Nickname"
          />
          <FormKit
            outer-class="$reset w-full"
            name="gender"
            type="select"
            label="Gender"
            :options="['Male', 'Female', 'Other', 'Prefer not to say']"
            validation="required"
            validation-visibility="dirty"
            v-model="userData.Gender"
          />
        </div>
        <FormKit
          outer-class="$reset"
          name="nationality"
          type="select"
          label="Nationality"
          :options="nationalities"
          validation="required"
          validation-visibility="dirty"
          v-model="userData.Nationality"
        />
        <FormKit
          outer-class="$reset w-full"
          name="birthday"
          type="date"
          label="Date of birth"
          placeholder="Date of birth"
          validation="required"
          validation-visibility="dirty"
          v-model="birthday"
        />
        <FormKit
          outer-class="$reset w-full"
          name="aboutMe"
          type="textarea"
          label="About me"
          v-model="userData.AboutMe"
        />
      </div>
      <div class="mt-5 flex flex-col gap-3 rounded-xl bg-white p-7 dark:bg-[#50504D]">
        <p class="text-xl font-medium">Contact info</p>
        <div class="flex gap-5">
          <FormKit
            outer-class="$reset w-full"
            name="email"
            type="email"
            label="Email"
            placeholder="Email"
            validation="email"
            v-model="userData.Email"
          />
          <FormKit
            outer-class="$reset w-full"
            name="phoneNumber"
            type="text"
            label="Phone number"
            placeholder="Phone number"
            validation-visibility="dirty"
            v-model="userData.PhoneNumber"
          />
        </div>
        <div class="flex gap-5">
          <FormKit
            outer-class="$reset w-full"
            name="facebookLink"
            type="text"
            label="Facebook"
            placeholder="Link to Facebook profile"
            validation="url"
            validation-visibility="dirty"
            v-model="userData.FacebookLink"
          />
          <FormKit
            outer-class="$reset w-full"
            name="instagramLink"
            type="text"
            label="Instagram"
            placeholder="Link to Instagram profile"
            validation="url"
            validation-visibility="dirty"
            v-model="userData.InstagramLink"
          />
        </div>
      </div>
    </FormKit>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { apiInstance } from '@/helpers/api';
import type { BaseUserModel, UserDataModel } from '@/models/user.model';
import MainButton from '@/components/MainButton.vue';
import type NationalityModel from '@/models/nationality.model';
import MainInput from '@/components/MainInput.vue';
import { useToast } from 'vue-toastification';
import { fileToBase64 } from '@/helpers/imageToBase';
import router from '@/router';

const toast = useToast();

const authStore = useAuthStore();
const userData = ref<UserDataModel>({} as UserDataModel);
const birthday = ref('');
const nationalities = ref<Record<number, string>>({});

const password = ref('');
const passwordConfirm = ref('');

const files = ref<
  {
    name: string;
    file: File;
  }[]
>([]);

onMounted(async () => {
  await apiInstance
    .get<UserDataModel[]>(`users/${authStore.getTokenData.UserId}`, true)
    .then((response) => {
      userData.value = response ? response[0] : ({} as UserDataModel);
      birthday.value = new Date(userData.value.Birthday).toISOString().split('T')[0];
    });
  await apiInstance.get<NationalityModel[]>('nationalities', true).then((response) => {
    nationalities.value = response
      ? response.reduce(
          (acc, curr) => {
            acc[curr.NationalityId] = curr.Nationality;
            return acc;
          },
          {} as Record<number, string>,
        )
      : {};
  });
});

watch(files, (newFiles) => {
  const file = newFiles[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      const target = e.target as FileReader;
      const img = document.getElementById('preview') as HTMLImageElement;
      if (img) {
        img.src = target.result as string;
      }
    };
    reader.readAsDataURL(file.file);
  }
});

interface EditForm {
  aboutMe: string;
  birthday: string;
  email: string;
  facebookLink: string;
  gender: string;
  instagramLink: string;
  name: string;
  nickname: string;
  phoneNumber: string;
  profilePhoto: {
    name: string;
    file: File;
  }[];
  surname: string;
  nationality: number;
}

const handleUpdateData = async (data: EditForm) => {
  const avatarUrl =
    data.profilePhoto.length > 0
      ? await apiInstance
          .post<{
            PhotoUrl: string;
          }>('inner/photos/upload', {
            PhotoData: await fileToBase64(data.profilePhoto[0].file),
          })
          .then((response) => {
            return response ? response.PhotoUrl : userData.value.AvatarUrl;
          })
      : userData.value.AvatarUrl;

  const dataField: BaseUserModel = {
    Name: data.name,
    Surname: data.surname || '',
    Nickname: data.nickname || '',
    Nationality: data.nationality,
    Email: data.email,
    PhoneNumber: data.phoneNumber || '',
    Birthday: data.birthday,
    Gender: data.gender,
    AvatarUrl: avatarUrl,
    AboutMe: data.aboutMe || '',
    FacebookLink: data.facebookLink || '',
    InstagramLink: data.instagramLink || '',
  };

  await apiInstance.put<string>('users/settings_info', dataField, true).then(async (response) => {
    if (response) {
      toast.info('Profile updated successfully');
      await router.push({ name: 'Settings' });
    }
  });
};

const handlePasswordUpdate = async () => {
  if (password.value !== passwordConfirm.value) {
    toast.error('Passwords do not match');
    return;
  }

  console.log({ Password: password.value });
  await apiInstance
    .put<string>('users/settings_info', { Password: password.value }, true)
    .then(async (response) => {
      if (response) {
        toast.info('Password updated successfully');
        await router.push({ name: 'Settings' });
      }
    });
};
</script>
