<script setup>
defineProps({
    variant: {
        type: String,
        default: 'primary',
        validator: (value)=> {
            return ['primary','secondary','danger'].includes(value)
        },

    },
    type: {
        type: String,
        default: 'button',
    },
    disabled: {
        type: Boolean,
        default: false,
    },
})
</script>

<template>
    <button
        :type="type"
        :disabled="disabled"
        :class="[
            'rounded-lg px-4 py-2 text-sm font-medium transition-colors',
            {
                'bg-blue-600 text-white hover:bg-blue-700':
                variant === 'primary',

                'bg-gray-200 text-gray-800 hover:bg-gray-300':
                variant === 'secondary',

                'bg-red-600 text-white hover:bg-red-700':
                variant === 'danger',
            },
            disabled && 'cursor-not-allowed opacity-50'
        ]"
    >
        <slot />
    </button>
</template>