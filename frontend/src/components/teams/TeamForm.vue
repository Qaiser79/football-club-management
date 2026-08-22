<script setup>
import { ref, onMounted } from 'vue'
import { getClubs } from '@/services/clubService'

const props = defineProps({
    team: {
        type: Object,
        default: null,
    },
})

const emit = defineEmits(['save'])

const name = ref(props.team?.name || '')
const teamType = ref(props.team?.team_type || '')
const clubId = ref(props.team?.club_id || '')

const clubs = ref([])
const loadingClubs = ref(false)

const loadClubs = async () => {
    loadingClubs.value = true

    try {
        const data = await getClubs({
            page: 1,
            limit: 100,
        })

        clubs.value = data.items
    } catch (err) {
        console.error(err)
    } finally {
        loadingClubs.value = false
    }
}

const handleSubmit = () => {
    emit('save', {
        name: name.value,
        team_type: teamType.value,
        club_id: Number(clubId.value),
    })
}

onMounted(() => {
    loadClubs()
})
</script>

<template>
    <form
        :id="$attrs.id"
        @submit.prevent="handleSubmit"
        class="space-y-4"
    >
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
                Club
            </label>

            <select
                v-model="clubId"
                required
                :disabled="loadingClubs"
                class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            >
                <option value="" disabled>
                    {{ loadingClubs ? 'Loading clubs...' : 'Select a club' }}
                </option>

                <option
                    v-for="club in clubs"
                    :key="club.id"
                    :value="club.id"
                >
                    {{ club.name }}
                </option>
            </select>
        </div>
    </form>
</template>