<script setup>
const props = defineProps({
    currentPage: {
        type: Number,
        default: 1,
    },

    totalPages: {
        type: Number,
        default: 1,
    },

})

const emit =defineEmits(['update:currentPage'])

const goToPage = (page) => {
    if (page < 1|| page > props.totalPages) {
        return
    }

    emit('update:currentPage', page)
}
</script>

<template>

    <div
        v-if="props.totalPages > 1"
        class="flex items-center justify-between border-t border-gray-200 px-4 py-3"

    >
        <button
           type="button"
           class="rounded-lg border bordr-gray300 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
           :disabled="props.currentPage === 1" 
            @click="goToPage(props.currentPage - 1)"
           >
            Previous
        </button>

        <div>
            <button
                v-for="page in props.totalPages"
                :key="page"
                type="button"
                class="min-w-9 rounded-lg px-3 py-2 text-sm"
                :class="
                    page === props.currentPage
                        ? 'bg-gray-900 text-white'
                        : 'text-gray-700 hover:bg-gray-100'
                "
                @click="goToPage(page)"
            >
                {{ page }}
            </button>
        </div>

        <button
            type="button"
            class="rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
            :disabled="props.currentPage === props.totalPages"
            @click="goToPage(props.currentPage + 1)"
        >
            Next
        </button>
    </div>
</template>