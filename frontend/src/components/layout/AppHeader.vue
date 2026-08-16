<script setup>
defineEmits(['toggle-sidebar'])
</script>

<template>
    <header class="bg-white shadow-sm">
        <div class="flex items-center px-6 py-4">
            <button
                type="button"
                class="mr-4 rounded-lg p-2 text-gray-600 hover:bg-gray-100 lg:hidden"
                aria-label="Open navigation menu"
                @click="$emit('toggle-sidebar')"
            >
                ☰
        </button>
            <h1 class="text-xl font-semibold text-gray-900">
                Football Club Management
            </h1>
        </div>
    </header>
</template>