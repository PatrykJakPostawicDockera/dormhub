<template>
  <div class="min-h-screen w-screen p-20">
    <div class="flex flex-col items-center justify-center gap-5">
      <h1 class="text-4xl font-bold">Dorm Control</h1>
      <div class="flex flex-wrap gap-5 px-20 sm:px-40">
        <div v-for="dorm in dorms" :key="dorm.DormId">
          <div class="flex flex-col gap-2">
            <h2 class="text-2xl">{{ dorm.Name }}</h2>
            <MainButton button-text="Get QR" @click="getQr(dorm.DormId)" />
          </div>
        </div>
      </div>
      <FormKit type="form" :actions="false" @submit="handleQuickInsert">
        <FormKit
          input-class="!h-[30dvh]"
          type="textarea"
          name="dorm"
          label="Dorm JSON"
          :placeholder="placeholder"
          rows="100"
          cols="900"
        />
        <FormKit
          outer-class="$reset !w-[80dvw]"
          type="text"
          name="suiteCode"
          label="Suite code (auto generated)"
          :value="suiteCode"
          placeholder="Suite Code"
        />
        <MainButton class="mt-5" button-type="submit" button-text="Quick register" />
      </FormKit>
    </div>
  </div>
</template>
<script setup lang="ts">
import MainButton from '@/components/MainButton.vue';
import { onMounted, ref } from 'vue';
import { apiInstance } from '@/helpers/api';
import type Dorm from '@/models/dorm.model';

const suiteCode = Math.random().toString(36).substring(2, 8);

const placeholder =
  '{\n' +
  '      "Name": "Teścik",\n' +
  '      "Address": "1717 Pine Street",\n' +
  '      "ImageUrl": "https://....",\n' +
  '      "ApartmentAmount": 210,\n' +
  '      "DormVacancy": 70,\n' +
  '}';

const dorms = ref<Dorm[]>([]);

onMounted(async () => {
  await apiInstance.get<Dorm[]>('dorms', true).then((response) => {
    response ? (dorms.value = response) : console.log('No dorms found');
  });
});

interface QuickDormsFields {
  dorm: string;
  suiteCode: string;
}

const handleQuickInsert = async (fields: QuickDormsFields) => {
  const dormModel = {
    ...JSON.parse(fields.dorm),
    SuiteCode: fields.suiteCode,
  } as Dorm;
  await apiInstance.post<string>('dorms', dormModel, true).then((response) => {
    console.log(response);
  });
};

const getQr = async (dormId: string) => {
  await apiInstance.get<Blob>(`dorms/${dormId}/qr`, true).then((response) => {
    if (!response) return;
    const url = window.URL.createObjectURL(new Blob([response]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'qr.png');
    link.click();
  });
};
</script>
