<script setup>
import { ref } from 'vue'
import AppHeader from './AppHeader.vue'
import AppSidebar from './AppSidebar.vue'

const isSidebarOpen=ref(false)
</script>

<template>
    <div class="min-h-screen bg-gray-100">
        <AppHeader @toggle-sidebar="isSidebarOpen= !isSidebarOpen"/>

        <div class="flex">
            <AppSidebar :is-open="isSidebarOpen"/>

            <main class="min-w-0 flex-1 p-6">
                <slot />
            </main>
        </div>
    </div>
</template>