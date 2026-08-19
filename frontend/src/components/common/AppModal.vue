<script setup>
const emit = defineEmits(['close'])
const props= defineProps({
    open: {
        type: Boolean,
        default: false,
    },
    title: {
        type: String,
        default: '',
    },
    description: {
        type: String,
        default: '',
    },

})
</script>

<template>
    <div
        v-if="props.open"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4"
    >
        <div class="w-full max-w-md rounded-xl bg-white shadow-xl">
            <!-- Header -->
            <div class="flex items-start justify-between border-b border-gray-100 px-6 py-4">
                <div>
                    <h3 class="text-lg font-semibold text-gray-900">
                        {{ props.title }}
                    </h3>

                    <p
                        v-if="props.description"
                        class="mt-1 text-sm text-gray-500"
                    >
                        {{ props.description }}
                    </p>
                </div>

                <button
                    type="button"
                    class="rounded-lg p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-700"
                    aria-label="Close"
                    @click="emit('close')"
                >
                    ×
                </button>
            </div>

            <!-- Body -->
            <div class="px-6 py-5">
                <slot />
            </div>

            <!-- Footer -->
            <div class="flex justify-end gap-3 border-t border-gray-100 px-6 py-4">
                <slot name="footer" />
            </div>
        </div>
    </div>
</template>