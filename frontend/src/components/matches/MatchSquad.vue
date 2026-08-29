<script setup>
import { ref } from 'vue'

const props = defineProps({
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

const selectedPlayerIds = ref([])

const togglePlayer = (playerId) => {
    const index = selectedPlayerIds.value.indexOf(playerId)

    if (index !==-1) {
        selectedPlayerIds.value.splice(index, 1)
        emit('update:selected-player-idd',selectedPlayerIds.value)
        return
    }

    if (selectedPlayerIds.value.length >= 15) {
        return
    }

    selectedPlayerIds.value.push(playerId)
    emit('update:selected-player-idd',selectedPlayerIds.value)
}
</script>

<template>
    <div class="mt-6">
        <div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
            <h3 class="text-lg font-semibold text-gray-900">
                Match Squad
            </h3>
            <p class="mt-1 text-sm text-gray-500">
                Players available from {{ props.teamName }}
            </p>

            <div class="mt-3 flex items-center justify-between">
                <p class="text-sm font-medium text-gray-700">
                    Selected: {{ selectedPlayerIds.length }}/15
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
                    class="cursor-pointer rounded-lg border p-4 transition"
                    :class="
                        selectedPlayerIds.includes(player.id)
                            ? 'border-gray-900 bg-gray-50'
                            : 'border-gray-200 bg-white hover:bg-gray-50'
                    "
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

        </div>

    </div>
</template>