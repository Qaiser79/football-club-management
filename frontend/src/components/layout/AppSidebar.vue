<script setup>
defineProps({
    isOpen:{
        type: Boolean,
        default: false,
    }
})

const navigationItems = [
    { name: 'Dashboard', path: '/'},
    { name: 'Organizations', path: '/organizations'},
    { name: 'Clubs', path: '/clubs' },
    { name: 'Teams', path: '/teams' },
    { name: 'Players', path: '/players' },
    { name: 'Matches', path: '/matches' },
]
</script>

<template>
    <aside 
        :class="[
            'w-64 shrink-0 bg-gray-900 text-white',
            'lg:block',
            isOpen ? 'block' : 'hidden',
        ]"
    >
        <div class="p-6">
            <h2 class="text-lg font-semibold text-white">
                Football Club
            </h2>
        </div>

        <nav class="px-3">
            <RouterLink
                v-for="item in navigationItems"
                :key="item.path"
                :to="item.path"
                class="mb-1 block rounded-lg px-3 py-2 text-sm font-medium text-white transition-colors hover:bg-gray-800"
                active-class="bg-gray-700"
            >
                {{item.name}}
            </RouterLink>
        </nav>
    </aside>
</template>