<script setup>
import {ref, onMounted} from 'vue'
import { useRoute, useRouter } from 'vue-router';
import {getPlayer} from '@/services/playerService'


const route = useRoute()
const router = useRouter

const player = ref(null)
const loading = ref(null)
const error = ref(null)

const loadPlayer = async () => {
    loading.value = true
    error.value = null

    try {
        player.value = await getPlayer(route.params.playerId)
    } catch (err) {
        console.error(err)
        error.value = 'Failed to load player.'
    } finally {
        loading.value = false
    }
}

const goBack = () => {
    router.push('/players')
}

onMounted(()=> {
    loadPlayer()
})
</script>

<template>
    <div>
        <button
            type="button"
            class="text-sm font-medium text-gray-600 hover:text-gray-900"
            @click="goBack"
        >
            ← Back to Players
        </button>

        <div
            v-if="loading"
            class="mt-6 text-sm text-gray-500"
        >
            Loading player...
        </div>

        <div
            v-else-if="error"
            class="mt-6 rounded-lg bg-red-50 p-4 text-sm text-red-700"
        >
            {{ error }}
        </div>

        <div
            v-else-if="player"
            class="mt-6"
        >
            <h1 class="text-2xl font-bold text-gray-900">
                {{ player.name }}
            </h1>

            <p class="mt-2 text-gray-600">
                {{ player.position }} · {{ player.team?.name }}
            </p>
        </div>
    </div>
</template>