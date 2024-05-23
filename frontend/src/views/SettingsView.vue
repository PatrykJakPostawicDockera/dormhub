<template>
  <div class="flex flex-col gap-3">
    <h1 class="text-3xl">Settings</h1>
    <div class="flex justify-between rounded-xl bg-white px-5 py-3 dark:bg-[#50504D]">
      <p class="text-xl font-medium">Dark mode</p>
      <button
        class="flex w-12 items-center justify-start rounded-full bg-gray-300/60 transition-all focus:outline-none dark:bg-green-400/60"
        @click="handleThemeSwitch"
      >
        <span
          class="flex h-6 w-6 translate-x-0 transform items-center rounded-full bg-light px-2 py-1 opacity-100 shadow-md transition-transform dark:translate-x-full dark:bg-dark"
        >
        </span>
      </button>
    </div>
    <RouterLink
      to="/app/settings/edit-profile"
      class="flex items-center gap-3 rounded-xl bg-white px-5 py-3 transition-opacity transition-transform ease-in-out hover:scale-[101%] focus:bg-opacity-50 dark:bg-[#50504D]"
    >
      <Pencil />
      <p class="text-xl font-medium">Edit profile</p>
    </RouterLink>
    <div
      class="flex flex-col justify-between gap-3 rounded-xl bg-white px-5 py-3 dark:bg-[#50504D]"
    >
      <p class="text-xl font-medium">Visibility preferences</p>
      <p class="text-lg font-medium">Personal info</p>
      <MainSwitch
        switch-id="surname"
        switch-label="Show surname"
        @switch="handleSwitchCllick"
        :value="showSurname"
        :disabled="!surnameSettings"
      />
      <MainSwitch
        switch-id="age"
        switch-label="Show age"
        @switch="handleSwitchCllick"
        :value="showAge"
      />
      <MainSwitch
        switch-id="dates"
        switch-label="Show date of arrival/departure"
        @switch="handleSwitchCllick"
        :value="showDates"
      />
      <p class="text-lg">Contact info</p>
      <MainSwitch
        switch-id="email"
        switch-label="Show email address"
        @switch="handleSwitchCllick"
        :value="showEmail"
      />
      <MainSwitch
        switch-id="phone"
        switch-label="Show phone number"
        @switch="handleSwitchCllick"
        :value="showPhone"
      />
      <MainSwitch
        switch-id="social"
        switch-label="Show social media links"
        @switch="handleSwitchCllick"
        :value="showSocial"
      />
    </div>
    <div
      class="flex flex-col justify-between gap-3 rounded-xl bg-white px-5 py-3 dark:bg-[#50504D]"
    >
      <p class="text-xl font-medium">Suite preferences</p>
      <MainInput type="date" label="Departure date" name="departure" v-model:value="departure" />
      <MainInput label="Room number" name="room" v-model:value="room" />
      <MainButton buttonText="Save settings" @click="handleSuiteInfoUpdate" />
      <p class="text-lg font-medium"></p>
      <div class="flex flex-col justify-between gap-5 md:flex-row md:items-end">
        <MainInput label="Change suite code" name="suite" v-model:value="suite" />
        <MainButton class="w-full" buttonText="Change suite" />
        <MainButton class="w-full" color="alert" buttonText="Exit suite" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Pencil } from 'lucide-vue-next';
import { onMounted, ref } from 'vue';
import MainSwitch from '@/components/MainSwitch.vue';
import MainInput from '@/components/MainInput.vue';
import MainButton from '@/components/MainButton.vue';
import { apiInstance } from '@/helpers/api';
import type { UserDataModel } from '@/models/user.model';
import { useAuthStore } from '@/stores/auth';

const showSurname = ref(false);
const showAge = ref(false);
const showDates = ref(false);
const showEmail = ref(false);
const showPhone = ref(false);
const showSocial = ref(false);

const room = ref('');
const suite = ref('');
const departure = ref('');
const surnameSettings = ref(false);
const theme = ref(
  (() => {
    if (typeof localStorage !== 'undefined' && localStorage.getItem('theme')) {
      return localStorage.getItem('theme');
    }
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  })(),
);

onMounted(async () => {
  handleThemeCheckOnLoad();
  await apiInstance
    .get<{
      DepartureDate: string;
      RoomNumber: string;
      SurnameExists: boolean;
    }>('users/settings_info', true)
    .then((response) => {
      if (response) {
        departure.value = new Date(response.DepartureDate).toISOString().split('T')[0];
        room.value = response.RoomNumber;
        surnameSettings.value = response.SurnameExists;
        console.log(response);
      }
    });
  await apiInstance
    .get<UserDataModel[]>(`users/${useAuthStore().getTokenData.UserId}`, true)
    .then((response) => {
      if (response && response[0]) {
        console.log(response[0]);
        showSurname.value = intToBool(response[0].ShowSurname);
        showAge.value = intToBool(response[0].ShowAge);
        showDates.value = intToBool(response[0].ShowDate);
        showEmail.value = intToBool(response[0].ShowEmail);
        showPhone.value = intToBool(response[0].ShowPhone);
        showSocial.value = intToBool(response[0].ShowSocial);
      }
    });
});

const intToBool = (value: number) => value === 1;

const handleSuiteInfoUpdate = async () => {
  console.log({
    DepartureDate: departure.value,
    RoomNumber: room.value,
  });
  const response = await apiInstance.put<string>(
    'users/settings_info',
    {
      DepartureDate: departure.value,
      RoomNumber: room.value,
    },
    true,
  );
  if (response) {
    console.log(response);
  }
};

// theme handling
const handleThemeCheckOnLoad = () => {
  if (theme.value === 'light') {
    document.documentElement.classList.remove('dark');
  } else {
    document.documentElement.classList.add('dark');
  }

  window.localStorage.setItem('theme', theme.value as string);
};

const handleThemeSwitch = () => {
  const isDark = document.documentElement.classList.toggle('dark');
  theme.value = isDark ? 'dark' : 'light';
  localStorage.setItem('theme', theme.value as string);
};

const handleSwitchCllick = async (switchName: string, switched: boolean) => {
  const getTrueName = (name: string) => {
    switch (name) {
      case 'surname':
        return 'ShowSurname';
      case 'age':
        return 'ShowAge';
      case 'dates':
        return 'ShowDate';
      case 'email':
        return 'ShowEmail';
      case 'phone':
        return 'ShowPhone';
      case 'social':
        return 'ShowSocial';
      default:
        return '';
    }
  };
  await apiInstance.put<string>(
    `users/settings_info`,
    {
      [getTrueName(switchName)]: switched,
    },
    true,
  );
};
</script>
