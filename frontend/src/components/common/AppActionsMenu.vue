<script setup>
import { ref } from 'vue'

const props = defineProps({
    rowIndex: {
        type: Number,
        required: true,
    },
    totalRows: {
        type: Number,
        required: true,
    },
})

const emit = defineEmits(['view','edit', 'delete'])

const open = ref(false)

const handleView = () => {
    open.value = false
    emit('view')
}

const handleEdit = () => {
    open.value = false
    emit('edit')
}

const handleDelete = () => {
    open.value = false
    emit('delete')
}
</script>

<template>
    <div class="relative flex justify-end">
        <button
            type="button"
            class="rounded-lg p-2 text-gray-500 transition-colors hover:bg-gray-100 hover:text-gray-900"
            aria-label="Actions"
            @click="open = !open"
        >
            ⋮
        </button>

        <div
            v-if="open"
            class="absolute right-0 z-50 w-32 rounded-lg border border-gray-200 bg-white py-1 shadow-lg"
            :class="
                rowIndex === totalRows - 1
                    ? 'bottom-10'
                    : 'top-10'
            "
        >

            <button
                type="button"
                class="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50"
                @click="handleView"
            >
                View
            </button>

            <button
                type="button"
                class="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50"
                @click="handleEdit"
            >
                Edit
            </button>

            <button
                type="button"
                class="block w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50"
                @click="handleDelete"
            >
                Delete
            </button>
        </div>
    </div>
</template>