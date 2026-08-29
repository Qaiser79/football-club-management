<script setup>
import { ref, onMounted, computed } from 'vue'
import { getMatchSquad, updateMatchSquad } from '@/services/matchService'

const props = defineProps({
    matchId: {
        type: Number,
        required: true,
    },
    matchStatus: {
        type: String,
        default: 'scheduled',
    },
    players: {
        type: Array,
        default: ()=>[],
    },
    teamName: {
        type: String,
        default: '',
    },
    loading: {
        type: Boolean,
        default: false,
    },
    error: {
        type: String,
        default: null,
    }
})

const selectedPlayerIds = ref([])
const saving = ref(false)
const saveError = ref(null)
const saveSuccess = ref(false)
const squadLoading = ref(false)
const squadError = ref(null)
const squadExists = ref(false)

const squadEditable = computed(()=> {
    return props.matchStatus?.toLowerCase() === 'scheduled'
})

const loadSquad = async () => {
    squadLoading.value = true
    squadError.value = null

    try {
        const data = await getMatchSquad(props.matchId)

        selectedPlayerIds.value = data.player_ids
        squadExists.value = data.player_ids.length > 0
    } catch (err) {
        console.error(err)
        squadError.value = 'Failed to load match squad'
    } finally {
        squadLoading.value = false
    }
}

const togglePlayer = (playerId) => {

    if (!squadEditable.value){
        return
    }

    const index = selectedPlayerIds.value.indexOf(playerId)

    if (index !==-1) {
        selectedPlayerIds.value.splice(index, 1)
        return
    }

    if (selectedPlayerIds.value.length >= 15) {
        return
    }

    selectedPlayerIds.value.push(playerId)
}

const saveSquad = async () => {
    saving.value = true
    saveError.value = null
    saveSuccess.value = false

    try {
        await updateMatchSquad(
            props.matchId,
            selectedPlayerIds.value
        )
        squadExists.value = selectedPlayerIds.value.length > 0
        saveSuccess.value = true
    } catch (err) {
        console.error(err)
        saveError.value = 'Failed to save match squad'
    } finally {
         saving.value = false
    }
}

onMounted(()=>{
    loadSquad()
})

</script>

<template>
    <div class="mt-6">
        <div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
            <h3 class="text-lg font-semibold text-gray-900">
                Match Squad
            </h3>
            <p class="mt-1 text-sm text-gray-500">
                {{ squadEditable
                    ? `Players available from ${props.teamName}`
                    : `Match squad for ${props.teamName}`
                }}
            </p>

            <p
                v-if="!squadEditable"
                class="mt-2 text-sm text-gray-500"
            >
                Squad is locked because this match is {{ props.matchStatus.toLowerCase() }}.
            </p>

            <div class="mt-3 flex items-center justify-between">
                <p class="text-sm font-medium text-gray-700">
                    Squad: {{ selectedPlayerIds.length }}/15
                </p>

                <p
                    v-if="squadEditable && selectedPlayerIds.length < 11"
                    class="text-sm text-gray-500"
                >
                    Select at least 11 players
                </p>

                <p
                    v-else-if="squadEditable"
                    class="text-sm text-green-600"
                >
                    Minimum squad requirement met
                </p>
            </div>

            <div
                v-if="props.loading"
                class="mt-4 text-sm text-gray-500"
            >
                Loading players
            </div>

            <div
                v-else-if="props.error"
                class="mt-4 rounded-lg bg-red-50 p-4 text-sm text-red-700"
            >
                {{ props.error }}
            </div>

            <div
                v-else-if="props.players.length === 0"
                class="mt-4 text-sm text-gray-500"
            >
                No players available for this team.
            </div>

            <div
                v-else
                class="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3"
            >
                <div
                    v-for="player in props.players"
                    :key="player.id"
                    class="rounded-lg border p-4 transition"
                    :class="[
                        selectedPlayerIds.includes(player.id)
                            ? 'border-gray-900 bg-gray-50'
                            : 'border-gray-200 bg-white hover:bg-gray-50',
                        squadEditable
                            ? 'cursor-pointer hover:bg-gray-50'
                            : 'cursor-default opacity-75'
                        ]"
                    @click = "togglePlayer(player.id)"
                    >
                    <p class="font-medium text-gray-900">
                        {{ player.name }}
                    </p>

                    <p class="mt-1 text-sm text-gray-500">
                        {{ player.position || 'No position' }}
                    </p>
                </div>
            </div>

            <div
                v-if="props.players.length > 0"
                class="mt-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"
            >
                <div class="text-sm text-gray-500">
                    {{ selectedPlayerIds.length }} of 15 players selected
                </div>

                <button
                    type="button"
                    class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
                    :disabled="saving || selectedPlayerIds.length < 11"
                    @click="saveSquad"
                >
                    {{ saving ? 'Saving...' : squadExists ? 'Update Squad' : 'Save Squad' }}
                </button>
            </div>

            <p
                v-if="saveSuccess"
                class="mt-3 text-sm text-green-600"
            >
                Squad saved successfully.
            </p>

            <p
                v-if="saveError"
                class="mt-3 text-sm text-red-600"
            >
                {{ saveError }}
            </p>

        </div>

    </div>
</template>