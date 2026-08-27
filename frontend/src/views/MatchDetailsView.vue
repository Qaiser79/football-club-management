<script setup>
import {ref,onMounted} from 'vue'
import { useRoute } from 'vue-router';
import { getMatch } from '@/services/matchService';

const route = useRoute()

const match = ref(null)
const loading = ref(false)
const error = ref(null)

const loadMatch = async ()=> {
    loading.value=true
    error.value=null

    try {
        match.value = await getMatch(route.params.matchId)
    } catch (err) {
        console.error(err)
        error.value = 'Failed to load match'
    } finally {
        loading.value = false
    }
}
onMounted(()=> {
    loadMatch()
})
</script>

<template>
     <div>
        <div
            v-if="loading"
            class="text-sm text-gray-500"
        >
            Loading match...
        </div>

        <div
            v-else-if="error"
            class="rounded-lg bg-red-50 p-4 text-sm text-red-700"
        >
            {{ error }}
        </div>

        <div v-else-if="match">
            <h2 class="text-2xl font-bold text-gray-900">
                {{ match.team.name }} vs {{ match.opponent_name }}
            </h2>

            <p class="mt-2 text-gray-600">
                {{ match.competition }}
            </p>
        </div>
    </div>
</template>