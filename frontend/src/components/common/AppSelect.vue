<script setup>
const props = defineProps({
    modelValue: {
        type: [String, Number],
        default: '',
    },

    options: {
        type: Array,
        default: () => [],
    },

    placeholder: {
        type: String,
        default: 'Select an option',
    },

    disabled: {
        type: Boolean,
        default: false,
    },

    id: {
        type: String,
        default: '',
    },
})

const emit = defineEmits(['update:modelValue'])
</script>

<template>
    <select
        :id="props.id"
        :value="props.modelValue"
        :disabled="props.disabled"
        class="w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200 disabled:cursor-not-allowed disabled:bg-gray-100"
        @change="emit('update:modelValue', $event.target.value)"
    >
        <option 
            v-if="props.placeholder"
            value="" 
            disabled
        >
            {{props.placeholder}}
        </option>

        <option
            v-for="option in props.options"
            :key="option.value"
            :value="option.value"
        >
            {{option.label}}
        </option>
    </select>
</template>