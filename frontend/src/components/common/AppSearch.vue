<script setup>

defineProps ({
    modelValue:{
        type: String,
        default: '',
    },
    placeholder: {
        type: String,
        default: "Search...",
    },

})

const emit = defineEmits(['update:modelValue'])

</script>

<template>
    <div class="relative">
        <span
            class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400"

        >
            🔍
        </span>

        <input
            :value="modelValue"
            type="text"
            :placeholder="placeholder"
            class="w-full rounded-lg border border-gray-300 bg-white py-2 pl-10 pr-4 text-sm text-gray-900 outline-none transition focus:border-gray-500 focus:ring-2 focus:ring-gray-200"
            @input="emit('update:modelValue', $event.target.value)"
        />
    </div>

</template>