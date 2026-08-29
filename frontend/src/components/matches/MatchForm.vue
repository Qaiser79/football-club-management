<script setup>

import { ref, onMounted } from 'vue'
import { getTeams } from '@/services/teamService'

const props =defineProps({
    match: {
        type: Object,
        default: null,
    },
})

const emit = defineEmits(['save'])

const teams = ref([])
const loadingTeams = ref(false)

const teamId = ref(props.match?.team_id || '')
const opponentName= ref(props.match?.opponent_name || '')

const matchDate= ref(
    props.match?.match_date
        ? props.match.match_date.slice(0, 16)
        : ''
)

const competition = ref(props.match?.competition || '')
const venue = ref(props.match?.venue || '')
const isHome = ref(
    props.match?.is_home ?? true
)
const ourScore = ref(props.match?.our_score ?? 0)
const opponentScore = ref(
    props.match?.opponent_score ?? 0
)
const status = ref(
    props.match?.status || 'scheduled'
)

const loadTeams = async ()=>{
    loadingTeams.value = true

    try {
        const data = await getTeams({
            page: 1,
            limit: 100,
        })
        teams.value = data.items
    } catch (err) {
        console.error(err)
    } finally {
        loadingTeams.value = false
    }
}

const handleSubmit = () => {
    emit('save', {
        team_id: Number(teamId.value),
        opponent_name: opponentName.value,
        match_date: matchDate.value,
        competition: competition.value,
        venue: venue.value || null,
        is_home: isHome.value,
        our_score: Number(ourScore.value),
        opponent_score: Number(opponentScore.value),
        status: status.value,
    })
}

onMounted(()=>{
    loadTeams()
})


</script>

<template>
    <form
        @submit.prevent="handleSubmit"
        class="space-y-4"
    >
        <div>
            <label class="block text-sm font-medium text-gray-700">
                Our Team
            </label>

            <select
                v-model="teamId"
                required
                class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            >
                <option value="" disabled>
                    Select team
                </option>

                <option
                    v-for="team in teams"
                    :key="team.id"
                    :value="team.id"
                >
                    {{ team.name }} ({{ team.team_type }})
                </option>
            </select>

            <p
                v-if="loadingTeams"
                class="mt-1 text-xs text-gray-500"
            >
                Loading teams...
            </p>
        </div>

        <div>
            <label class="block text-sm font-medium text-gray-700">
                Opponent
            </label>

            <input
                v-model="opponentName"
                type="text"
                required
                placeholder="e.g. Rawalpindi FC"
                class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            />
        </div>

        <div>
            <label class="block text-sm font-medium text-gray-700">
                Match Date
            </label>

            <input
                v-model="matchDate"
                type="datetime-local"
                required
                class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            />
        </div>

        <div>
            <label class="block text-sm font-medium text-gray-700">
                Competition
            </label>

            <input
                v-model="competition"
                type="text"
                required
                placeholder="e.g. Premier League"
                class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            />
        </div>

        <div>
            <label class="block text-sm font-medium text-gray-700">
                Venue
            </label>

            <input
                v-model="venue"
                type="text"
                placeholder="e.g. Rawalpindi Stadium"
                class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            />
        </div>

        <div>
            <label class="block text-sm font-medium text-gray-700">
                Location
            </label>

            <select
                v-model="isHome"
                class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            >
                <option :value="true">
                    Home
                </option>

                <option :value="false">
                    Away
                </option>
            </select>
        </div>

        <div>
            <label class="block text-sm font-medium text-gray-700">
                Status
            </label>

            <select
                v-model="status"
                class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            >
                <option value="scheduled">
                    Scheduled
                </option>

                <option value="live">
                    Live
                </option>

                <option value="completed">
                    Completed
                </option>

                <option value="cancelled">
                    Cancelled
                </option>
            </select>
        </div>

        <div class="grid grid-cols-2 gap-4">
            <div>
                <label class="block text-sm font-medium text-gray-700">
                    Our Score
                </label>

                <input
                    v-model="ourScore"
                    type="number"
                    min="0"
                    required
                    class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
                />
            </div>

            <div>
                <label class="block text-sm font-medium text-gray-700">
                    Opponent Score
                </label>

                <input
                    v-model="opponentScore"
                    type="number"
                    min="0"
                    required
                    class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
                />
            </div>
        </div>
    </form>
</template>