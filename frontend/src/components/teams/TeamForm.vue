<script setup>
import { ref } from 'vue'

const props = defineProps({
    team: {
        type: Object,
        default: null,
    },
})

const emit = defineEmits(['save'])

const name = ref(props.team?.name || '')
const teamType = ref(props.team?.team_type.club_id || '')
const clubId = ref(props.team?.club_id || '')

const handleSubmit = () => {
    emit('save', {
        name: name.value,
        team_type: teamType.value,
        club_id: Number(clubId.value),
    })
}

</script>

<template>
    <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
            <label class="block text-sm font-medium text-gray-700">
                Team Name
            </label>

            <input
                v-model="name"
                type="text"
                required
                class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            />
        </div>

        <div>
            <label class="block text-sm font-medium text-gray-700">
                Team Type
            </label>

            <input
                v-model="teamType"
                type="text"
                placeholder="e.g. Senior, U21, U18"
                required
                class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            />
        </div>

        <div>
            <label class="block text-sm font-medium text-gray-700">
                Club ID
            </label>

            <input
                v-model="clubId"
                type="number"
                required
                class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            />
        </div>
    </form>
</template>