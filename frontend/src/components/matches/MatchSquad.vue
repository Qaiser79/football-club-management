<script setup>
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
                    class="rounded-lg border border-gray-200 p-4"
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