<script setup>
defineProps({
    isOpen:{
        type: Boolean,
        default: false,
    }
})
defineEmits(['close-sidebar'])

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
            'fixed inset-y-0 left-0 z-50 w-64 bg-gray-900 text-white',
            'transform transition-transform duration-300',
            'lg:static lg:block lg:translate-x-0',
            isOpen ? 'translate-x-0' : '-translate-x-full',
        ]"
    >
        
    <div class="flex items-center justify-between p-6">
        <h2 class="text-lg font-semibold text-white">
            Football Club
        </h2>

        <button
            type="button"
            class="rounded-lg p-2 text-gray-300 hover:bg-gray-800 hover:text-white lg:hidden"
            aria-label="Close navigation menu"
            @click="$emit('close-sidebar')"
        >
            ✕
        </button>
    </div>


        <nav class="px-3">
            <RouterLink
                v-for="item in navigationItems"
                :key="item.path"
                :to="item.path"
                class="mb-1 block rounded-lg px-3 py-2 text-sm font-medium text-white transition-colors hover:bg-gray-800"
                active-class="bg-gray-700"
                @click="$emit('close-sidebar')"
                >
                {{item.name}}
            </RouterLink>
        </nav>
    </aside>
</template>