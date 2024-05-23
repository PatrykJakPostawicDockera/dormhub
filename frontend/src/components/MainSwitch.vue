<template>
  <div class="flex justify-between">
    <p class="text-lg opacity-70">{{ switchLabel }}</p>
    <button
      :disabled="disabled"
      @click="switched = !switched"
      class="flex w-12 items-center justify-start rounded-full bg-gray-300 bg-opacity-60 transition-all focus:outline-none disabled:cursor-not-allowed disabled:bg-opacity-20"
      :class="{
        'bg-green-400': switched,
      }"
    >
      <span
        class="flex h-6 w-6 translate-x-0 transform items-center rounded-full bg-light px-2 py-1 opacity-100 shadow-md transition-transform dark:bg-dark"
        :class="{
          'translate-x-full': switched,
        }"
      />
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

const props = withDefaults(
  defineProps<{
    switchId: string;
    switchLabel: string;
    disabled?: boolean;
    value?: boolean;
  }>(),
  {
    disabled: false,
    value: false,
  },
);

const emit = defineEmits<{
  switch: [switchId: string, switched: boolean];
}>();

const switched = ref(props.value);

watch(switched, (newValue) => {
  emit('switch', props.switchId, newValue);
});

watch(props, (newValue) => {
  switched.value = newValue.value;
});
</script>
