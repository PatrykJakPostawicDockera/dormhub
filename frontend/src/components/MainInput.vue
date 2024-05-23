<template>
  <div class="flex flex-col gap-1">
    <p>{{ label }}</p>
    <input
      :type="type"
      :id="name"
      :name="name"
      class="h-10 rounded-lg border border-gray-400 bg-transparent px-2 py-1 focus:border-0 focus:outline-none focus:outline-primaryLight disabled:bg-gray-300 disabled:text-gray-600 dark:focus:outline-primaryDark"
      @input="updateOnInput ? handleInput(($event.target as HTMLInputElement).value) : null"
      @change="
        updateOnInput ? null : emit('update:value', ($event.target as HTMLInputElement).value)
      "
      :autocomplete="autocomplete"
      :required="required"
      :disabled="disabled"
      :min="min"
      :max="max"
      :maxlength="maxlength"
      :value="value"
    />
  </div>
</template>

<script setup lang="ts">
export interface Props {
  name: string;
  label: string;
  type?: string;
  autocomplete?: string;
  required?: boolean;
  disabled?: boolean;
  min?: number;
  max?: number;
  maxlength?: number;
  errorMsg?: string;
  showError?: boolean;
  helperText?: string;
  value?: string | number;
  updateOnInput?: boolean;
}

withDefaults(defineProps<Props>(), {
  type: 'text',
  autocomplete: 'off',
  required: true,
  disabled: false,
  showError: false,
  value: '',
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
