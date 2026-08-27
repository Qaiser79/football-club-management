<script setup>
import {ref,onMounted} from 'vue'
import { useRoute } from 'vue-router';
import { getMatch } from '@/services/matchService';
import { formatDate } from '@/utils/date';

const route = useRoute()

const match = ref(null)
const loading = ref(false)
const error = ref(null)

const statusClasses = {
    scheduled: 'bg-blue-50 text-blue-700',
    completed: 'bg-green-50 text-green-700',
    cancelled: 'bg-red-50 text-red-700',
    postponed: 'bg-yellow-50 text-yellow-700',
}

const formatStatus = (status) => {
    if (!status) {
        return '-'
    }

    return status.charAt(0).toUpperCase() + status.slice(1)
}

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

    <div v-if="loading" class="mt-6 text-sm text-gray-500">
        Loading match...
    </div>

    <div
        v-else-if="error"
        class="mt-6 rounded-lg bg-red-50 p-4 text-sm text-red-700"
    >
        {{ error }}
    </div>

    <div v-if="match">

        <div class="flex flex-col gap-4 min-[375px]:flex-row min-[375px]:items-center min-[375px]:justify-between">
            <div>
                <h2 class="text-2xl font-bold text-gray-900">
                    Match Details
                </h2>

                <p class="mt-2 text-gray-600">
                    {{ match.competition }}
                </p>
            </div>

            <button
                type="button"
                class="rounded-lg border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                @click="$router.push('/matches')"
            >
                Back to Matches
            </button>
        </div>

        <div class="mt-6 rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
            <div class="text-center">

                <p class="text-sm font-medium text-gray-500">
                    {{ formatDate(match.match_date) }}
                </p>

            <div class="mt-4 flex flex-col items-center justify-center gap-2 min-[375px]:flex-row min-[375px]:gap-8">
                <div>
                    <p class="text-center text-lg font-semibold text-gray-900">
                        {{ match.team.name }}
                    </p>
                </div>

                <div class="text-2xl font-bold text-gray-900">
                    {{ match.our_score }} - {{ match.opponent_score }}
                </div>

                <div>
                    <p class="text-center text-lg font-semibold text-gray-900">
                        {{ match.opponent_name }}
                    </p>
                </div>
            </div>

            </div>
        </div>

    </div>

    <div v-if="match">
        <div class="mt-6 rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
            <h3 class="text-lg font-semibold text-gray-900">
                Match Information
            </h3>

            <div class="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <div>
                    <p class="text-sm text-gray-500">
                        Competition
                    </p>

                    <p class="mt-1 text-sm font-medium text-gray-900">
                        {{ match.competition || '-' }}
                    </p>
                </div>

                <div>
                    <p class="text-sm text-gray-500">
                        Venue
                    </p>

                    <p class="mt-1 text-sm font-medium text-gray-900">
                        {{ match.venue || '-' }}
                    </p>
                </div>

                <div>
                    <p class="text-sm text-gray-500">
                        Location
                    </p>

                    <p class="mt-1 text-sm font-medium text-gray-900">
                        {{ match.is_home ? 'Home' : 'Away' }}
                    </p>
                </div>

                <div>
                    <p class="text-sm text-gray-500">
                        Status
                    </p>

                    <span
                        class="mt-1 inline-flex rounded-full px-2.5 py-1 text-xs font-medium"
                        :class="statusClasses[match.status] || 'bg-gray-100 text-gray-700'"
                    >
                        {{ formatStatus(match.status) }}
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>