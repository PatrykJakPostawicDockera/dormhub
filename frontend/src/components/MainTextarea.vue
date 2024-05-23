<template>
  <div class="flex flex-col gap-1">
    <p>{{ label }}</p>
    <textarea
      :id="name"
      :name="name"
      class="rounded-lg border border-gray-400 bg-transparent px-2 py-1 focus:border-0 focus:outline-none focus:outline-primaryLight disabled:bg-gray-300 disabled:text-gray-600 dark:focus:outline-primaryDark"
      @input="updateOnInput ? handleInput(($event.target as HTMLInputElement).value) : null"
      @change="
        updateOnInput ? null : emit('update:value', ($event.target as HTMLInputElement).value)
      "
      :class="fieldClass"
      :autocomplete="autocomplete"
      :required="required"
      :disabled="disabled"
      :maxlength="maxlength"
      :value="value"
    />
  </div>
</template>

<script setup lang="ts">
export interface Props {
  name: string;
  label: string;
  autocomplete?: string;
  required?: boolean;
  disabled?: boolean;
  maxlength?: number;
  errorMsg?: string;
  showError?: boolean;
  helperText?: string;
  value?: string | number;
  updateOnInput?: boolean;
  fieldClass?: string;
}

withDefaults(defineProps<Props>(), {
  autocomplete: 'off',
  required: true,
  disabled: false,
  showError: false,
  value: '',
  fieldClass: '',
});

const emit = defineEmits<{
  inputChange: [input: string];
  'update:value': [value: string];
}>();

const handleInput = (input: string) => {
  emit('update:value', input);
  emit('inputChange', input);
};
</script>
