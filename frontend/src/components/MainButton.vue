<template>
  <button
    :type="buttonType"
    class="h-auto rounded-xl bg-primaryLight px-5 py-2 text-white transition-all duration-200 ease-in-out hover:scale-105 focus:bg-opacity-50 dark:bg-primaryDark dark:bg-opacity-50 hover:sm:scale-[101%]"
    :class="{
      'bg-red-600 dark:bg-red-700': color === 'alert',
      '!bg-transparent !text-primaryLight dark:!text-primaryDark': color === 'transparent',
      '!bg-transparent !text-red-600 dark:!text-red-600': color === 'transparent-alert',
    }"
  >
    <slot>
      {{ buttonText }}
    </slot>
  </button>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    buttonText?: string;
    buttonType?: 'button' | 'submit' | 'reset';
    color?: 'primary' | 'alert' | 'transparent' | 'transparent-alert';
  }>(),
  {
    buttonText: 'Button',
    buttonType: 'button',
    color: 'primary',
  },
);
</script>
