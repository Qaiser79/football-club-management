<script setup>
import {ref,onMounted, computed} from 'vue'
import { useRoute } from 'vue-router';
import { getMatch, getMatchSquad,getMatchEvents } from '@/services/matchService';
import { getPlayers } from '@/services/playerService'
import { formatDate } from '@/utils/date';
import { getMatchResult, matchResultLabels } from '@/utils/match'
import MatchSquad from '@/components/matches/MatchSquad.vue';
import MatchEvents from '@/components/matches/MatchEvents.vue'
import {
    Radio,
    CalendarDays,
    Trophy,
    Clock3,
    CircleX,
} from '@lucide/vue'


const route = useRoute()

const activeSection = ref('overview')

const match = ref(null)
const loading = ref(false)
const error = ref(null)

const players = ref([])
const playersLoading = ref(false)
const playersError = ref(null)

const selectedPlayerIds = ref([])
const matchEvents = ref([])

const eventIcons = {
    goal: '⚽',
    yellow_card: '🟨',
    red_card: '🟥',
    substitution: '🔄',
}

const importantEvents = computed(() => {
    return matchEvents.value.filter(event =>
        ['goal', 'yellow_card', 'red_card', 'substitution'].includes(
            event.event_type
        )
    )
})

const statusClasses = {
    scheduled: 'bg-blue-50 text-blue-700',
    completed: 'bg-green-50 text-green-700',
    cancelled: 'bg-red-50 text-red-700',
    postponed: 'bg-yellow-50 text-yellow-700',
}

const resultClasses = {
    win: 'bg-green-50 text-green-700',
    draw: 'bg-yellow-50 text-yellow-700',
    loss: 'bg-red-50 text-red-700',
}

const statusIcons = {
    scheduled: CalendarDays,
    live: Radio,
    completed: Trophy,
    postponed: Clock3,
    cancelled: CircleX,
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

const loadPlayers = async () => {
    if (!match.value?.team_id) {
        return
    }

    playersLoading.value = true
    playersError.value = null

    try {
        const data = await getPlayers({
            teamId: match.value.team_id,
            limit: 100,
        })
        console.log('PLAYERS:',data)
        players.value=data.items
    } catch (err) {
        console.error(err)
        playersError.value = 'Failed to load'
    } finally {
        playersLoading.value = false
    }
}

const loadMatchSquad = async () => {
    if (!match.value?.id) {
        return
    }

    try {
        const data = await getMatchSquad(match.value.id)

        console.log('MATCH SQUAD PLAYERS:', data.players)

        selectedPlayerIds.value = data.players.map(
            player => player.player_id
        )

        console.log('SELECTED PLAYER IDS:', selectedPlayerIds.value)
    } catch (err) {
        console.error(err)
    }
}

onMounted(async()=> {
    await loadMatch()
    await loadPlayers()
    await loadMatchSquad()
    matchEvents.value = await getMatchEvents(match.value.id)
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

                <div class="mt-2 flex flex-wrap items-center gap-2">
                    <p class="text-gray-600">
                        {{ match.competition }}
                    </p>

                    <span class="text-gray-300">•</span>

                    <span class="inline-flex rounded-full bg-gray-100 px-2.5 py-1 text-xs font-medium text-gray-700">
                        {{ match.is_home ? 'Home' : 'Away' }}
                    </span>
                </div>
            </div>

            <button
                type="button"
                class="rounded-lg border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                @click="$router.push('/matches')"
            >
                Back to Matches
            </button>
        </div>

        <div
            class="mt-6 overflow-hidden rounded-2xl border border-gray-800 bg-gradient-to-br from-gray-950 via-gray-900 to-gray-800 px-4 py-8 text-white shadow-lg min-[375px]:px-6"
        >
            <div class="text-center">

                <p class="text-sm font-medium text-gray-400">
                    {{ formatDate(match.match_date) }}
                </p>

                <div
                    class="mt-3 inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wide"
                    :class="statusClasses[match.status?.toLowerCase()]"
                >
                    <component
                        :is="statusIcons[match.status?.toLowerCase()]"
                        class="h-3.5 w-3.5"
                    />

                    {{ match.status }}
                </div>

                <div class="mt-5 flex flex-col items-center justify-center gap-4 min-[375px]:flex-row min-[375px]:gap-8">

                    <div class="min-w-0 flex-1 text-center min-[375px]:text-right">
                        <p class="truncate text-lg font-semibold">
                            {{ match.team.name }}
                        </p>
                    </div>

                    <div class="shrink-0 text-center">
                        <div class="whitespace-nowrap text-3xl font-bold tracking-tight">
                            {{ match.our_score }}
                            <span class="mx-1 text-gray-500">-</span>
                            {{ match.opponent_score }}
                        </div>

                        <span
                            v-if="getMatchResult(match)"
                            class="mt-2 inline-flex rounded-full px-3 py-1 text-xs font-semibold"
                            :class="resultClasses[getMatchResult(match)]"
                        >
                            {{ matchResultLabels[getMatchResult(match)] }}
                        </span>
                    </div>

                    <div class="min-w-0 flex-1 text-center min-[375px]:text-left">
                        <p class="truncate text-lg font-semibold">
                            {{ match.opponent_name }}
                        </p>
                    </div>

                </div>

                <p class="mt-5 text-xs font-medium uppercase tracking-wider text-gray-500">
                    {{ match.competition }}
                </p>

            </div>
        </div>
        
    </div>

    <div v-if="match" class="mt-6 border-b border-gray-200">
        <nav class="flex gap-6 overflow-x-auto">
            <button
                type="button"
                class="whitespace-nowrap border-b-2 px-1 pb-3 text-sm font-medium"
                :class="
                    activeSection === 'overview'
                        ? 'border-gray-900 text-gray-900'
                        : 'border-transparent text-gray-500 hover:text-gray-700'
                "
                @click="activeSection = 'overview'"
            >
                Overview
            </button>

            <button
                type="button"
                class="whitespace-nowrap border-b-2 px-1 pb-3 text-sm font-medium"
                :class="
                    activeSection === 'squad'
                        ? 'border-gray-900 text-gray-900'
                        : 'border-transparent text-gray-500 hover:text-gray-700'
                "
                @click="activeSection = 'squad'"
            >
                Squad
            </button>

            <button
                type="button"
                class="whitespace-nowrap border-b-2 px-1 pb-3 text-sm font-medium"
                :class="
                    activeSection === 'events'
                        ? 'border-gray-900 text-gray-900'
                        : 'border-transparent text-gray-500 hover:text-gray-700'
                "
                @click="activeSection = 'events'"
            >
                Events
            </button>
        </nav>
    </div>

    <MatchSquad
        v-if="match && activeSection === 'squad'"
        :match-id="match.id"
        :players="players"
        :team-name="match.team.name"
        :match-status="match.status"
        :loading="playersLoading"
        :error="playersError"
        @update:selected-player-ids="selectedPlayerIds = $event"
    />
    <MatchEvents
        v-if="match && activeSection === 'events'"
        :match-id="match.id"
        :match="match"
        :players="players"
        :squad-player-ids="selectedPlayerIds"
        :match-status="match.status"
        @event-created="loadMatch"
        @match-status-changed="loadMatch"
    />


    <div
        v-if="match && activeSection === 'overview' && importantEvents.length"
        class="mt-6 rounded-xl border border-gray-200 bg-white p-6 shadow-sm"
    >
        <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold text-gray-900">
                Key Events
            </h3>

            <button
                type="button"
                class="text-sm font-medium text-gray-600 hover:text-gray-900"
                @click="activeSection = 'events'"
            >
                View all
            </button>
        </div>

        <div class="mt-4 space-y-3">
            <div
                v-for="event in importantEvents"
                :key="event.id"
                class="flex items-center gap-3 rounded-lg bg-gray-50 px-3 py-2"
            >
                <span class="w-10 text-sm font-semibold text-gray-500">
                    {{ event.minute ? `${event.minute}'` : '-' }}
                </span>

                <span class="text-sm font-medium text-gray-900">
                    {{ event.player.name }}
                </span>

                <span class="text-base">
                    {{ eventIcons[event.event_type] }}
                </span>

                <span
                    v-if="event.event_type === 'substitution' && event.related_player"
                    class="text-sm text-gray-500"
                >
                    → {{ event.related_player.name }}
                </span>
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