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

    selectedPlayerIds: {
        type: Array,
        default: () => [],
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

const emit = defineEmits(['update:selected-player-ids'])

const selectedPlayers = ref([])
const saving = ref(false)
const saveError = ref(null)
const saveSuccess = ref(false)
const squadLoading = ref(false)
const squadError = ref(null)
const squadExists = ref(false)

const starterCount = computed(() =>
    selectedPlayers.value.filter(
        player => player.is_starter
    ).length
)

const substituteCount = computed(() =>
    selectedPlayers.value.length - starterCount.value
)

const toggleStarter = (playerId) => {
    if (!squadEditable.value) {
        return
    }

    const player = selectedPlayers.value.find(
        item => item.player_id === playerId
    )

    if (!player) {
        return
    }

    if (!player.is_starter && starterCount.value >= 11) {
        return
    }

    player.is_starter = !player.is_starter
}

const squadEditable = computed(()=> {
    return props.matchStatus?.toLowerCase() === 'scheduled'
})

const loadSquad = async () => {
    squadLoading.value = true
    squadError.value = null

    try {
        const data = await getMatchSquad(props.matchId)

        selectedPlayers.value = data.players
        emit(
            'update:selected-player-ids',
            selectedPlayers.value.map(player => player.player_id)
        )
        squadExists.value = data.players.length > 0
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

    const index = selectedPlayers.value.findIndex(
        player => player.player_id === playerId
    )

    if (index !==-1) {
        selectedPlayers.value.splice(index, 1)
        emit(
            'update:selected-player-ids',
            selectedPlayers.value.map(player => player.player_id)
        )
        return
    }

    if (selectedPlayers.value.length >= 15) {
        return
    }

    selectedPlayers.value.push({
        player_id: playerId,
        is_starter: false,
    })
    emit(
        'update:selected-player-ids',
        selectedPlayers.value.map(player => player.player_id)
    )
}

const saveSquad = async () => {
    saving.value = true
    saveError.value = null
    saveSuccess.value = false

    try {
        await updateMatchSquad(
            props.matchId,
            {
                players: selectedPlayers.value,
            }
        )
        squadExists.value = selectedPlayers.value.length > 0
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
                    Squad: {{ selectedPlayers.length }}/15
                </p>

                <p
                    v-if="squadEditable && selectedPlayers.length < 11"
                    class="text-sm text-gray-500"
                >
                    Select at least 11 players
                </p>

                <p
                    v-else-if="squadEditable && starterCount < 11"
                    class="text-sm text-gray-500"
                >
                    Select 11 starters
                </p>

                <p
                    v-else-if="squadEditable"
                    class="text-sm text-green-600"
                >
                    Starting XI selected
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
                    selectedPlayers.some(
                        selected => selected.player_id === player.id
                    )
                        ? 'border-gray-900 bg-gray-50'
                        : 'border-gray-200 bg-white hover:bg-gray-50',
                    squadEditable
                        ? 'cursor-pointer hover:bg-gray-50'
                        : 'cursor-default opacity-75'
                ]"
                @click="togglePlayer(player.id)"
            >
                <p class="font-medium text-gray-900">
                    {{ player.name }}
                </p>

                <p class="mt-1 text-sm text-gray-500">
                    {{ player.position || 'No position' }}
                </p>

                <div
                    v-if="selectedPlayers.some(
                        selected => selected.player_id === player.id
                    )"
                    class="mt-3"
                >
                    <button
                        type="button"
                        class="rounded-lg border px-3 py-1 text-xs font-medium"
                        :class="
                            selectedPlayers.find(
                                selected => selected.player_id === player.id
                            )?.is_starter
                                ? 'border-gray-900 bg-gray-900 text-white'
                                : 'border-gray-300 bg-white text-gray-700'
                        "
                        @click.stop="toggleStarter(player.id)"
                    >
                        {{
                            selectedPlayers.find(
                                selected => selected.player_id === player.id
                            )?.is_starter
                                ? '✓ Starter'
                                : 'Substitute'
                        }}
                    </button>
                </div>
            </div>
            </div>

            <div
                v-if="props.players.length > 0"
                class="mt-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"
            >
                <div class="text-sm text-gray-500">
                    {{ selectedPlayers.length }} of 15 players selected
                </div>

                <button
                    type="button"
                    class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
                    :disabled="
                        saving ||
                        selectedPlayers.length < 11 ||
                        starterCount < 11
                    "
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