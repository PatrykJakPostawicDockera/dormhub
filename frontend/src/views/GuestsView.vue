<template>
  <h1 class="mb-3 text-3xl">Guest list</h1>
  <div class="flex flex-col gap-5">
    <div class="flex flex-col gap-3" v-for="floor in floors" :key="floor.floor">
      <h2 class="text-2xl">
        Floor {{ floor.floor }}
        <span class="text-xl">{{ usersFloor == parseInt(floor.floor) ? '(your floor)' : '' }}</span>
      </h2>
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-3">
        <GuestCard v-for="guest in floor.guests" :key="guest.UserId" :guest="guest" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { apiInstance } from '@/helpers/api';
import type { UserDataModel } from '@/models/user.model';
import GuestCard from '@/components/GuestCard.vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

const floors = ref<
  {
    floor: string;
    guests: UserDataModel[];
  }[]
>([]);
const usersFloor = parseInt(authStore.getTokenData.RoomNumber[0]);

onMounted(async () => {
  const response = await apiInstance.get<UserDataModel[]>(
    `dorms/${authStore.getTokenData.DormId}/members`,
    true,
  );
  if (response) {
    const sortedUsers = response.sort((a, b) => {
      const floorA = parseInt(a.RoomNumber[0]);
      const floorB = parseInt(b.RoomNumber[0]);
      return floorA === usersFloor ? -1 : floorB === usersFloor ? 1 : floorA - floorB;
    });
    const floorsMap = new Map<string, UserDataModel[]>();
    sortedUsers.forEach((user) => {
      const floor = user.RoomNumber[0];
      if (!floorsMap.has(floor)) {
        floorsMap.set(floor, []);
      }
      floorsMap.get(floor)?.push(user);
    });
    floors.value = Array.from(floorsMap).map(([floor, guests]) => ({ floor, guests }));
  }
});
</script>
