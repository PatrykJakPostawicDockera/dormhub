<template>
  <div
    class="flex flex-col items-center justify-center gap-5 bg-white p-5 shadow dark:bg-[#50504D] sm:rounded-lg"
  >
    <img :src="guest.AvatarUrl" alt="Guest avatar" class="h-20 w-20 rounded-full" />
    <div class="flex flex-col items-center gap-1">
      <p>Room {{ guest.RoomNumber }}</p>
      <h1 class="text-2xl">
        {{ `${guest.Name}${guest.Surname ? ` ${guest.Surname}` : ''}`
        }}{{ guest.Age ? `, ${guest.Age}` : '' }}
      </h1>
      <p>From: {{ nationality.Nationality }}</p>
    </div>
    <p class="text-center text-sm text-gray-500 dark:text-neutral-200">{{ guest.AboutMe }}</p>
    <p class="mt-auto">
      {{ guest.ArrivalDate ? `${new Date(guest.ArrivalDate).toLocaleDateString()} -` : '' }}
      {{ guest.DepartureDate ? new Date(guest.DepartureDate).toLocaleDateString() : '' }}
    </p>
    <div v-if="guest.FacebookLink" class="flex gap-5">
      <a
        v-if="guest.FacebookLink"
        :href="guest.FacebookLink"
        target="_blank"
        class="text-blue-500 hover:underline"
        >Facebook</a
      >
      <a
        v-if="guest.InstagramLink"
        :href="guest.InstagramLink"
        target="_blank"
        class="text-pink-500 hover:underline"
        >Instagram</a
      >
    </div>
  </div>
</template>

<script setup lang="ts">
import type { UserDataModel } from '@/models/user.model';
import { onMounted, ref } from 'vue';
import { apiInstance } from '@/helpers/api';

const props = defineProps<{
  guest: UserDataModel;
}>();

interface Nationality {
  Nationality: string;
  NationalityCode: string;
}

const nationality = ref<Nationality>({} as Nationality);

onMounted(async () => {
  await apiInstance
    .get<Nationality>(`nationalities/${props.guest.Nationality}`)
    .then((response) => {
      nationality.value = response ? response : ({} as Nationality);
    });
});
</script>
