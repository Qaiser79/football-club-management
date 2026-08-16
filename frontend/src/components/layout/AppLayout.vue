<script setup>
import { ref } from 'vue'
import AppHeader from './AppHeader.vue'
import AppSidebar from './AppSidebar.vue'

const isSidebarOpen=ref(false)
</script>

<template>
    <div class="min-h-screen bg-gray-100">
        <AppHeader @toggle-sidebar="isSidebarOpen= !isSidebarOpen"/>

        <div
            v-if="isSidebarOpen"
            class="fixed inset-0 z-40 bg-black/50 lg:hidden"
            @click="isSidebarOpen = false"
            ></div>

        <div class="flex">
            <AppSidebar 
                :is-open="isSidebarOpen"
                @close-sidebar="isSidebarOpen = false"
            />
            
            <main class="min-w-0 flex-1 p-6">
                <slot />
            </main>
        </div>
    </div>
</template>