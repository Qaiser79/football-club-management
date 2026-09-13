<script setup>
import { reactive, watch, onMounted } from 'vue'
import AppInput from '@/components/common/AppInput.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import {getTeams} from '@/services/teamService'

const props = defineProps({
    player: {
        type: Object,
        default: null,
    },

    id: {
        type: String,
        default: 'player-form'
    },
})

const emit = defineEmits(['save'])

const statusOptions = [
    { value: 'Active', label: 'Active' },
    { value: 'Injured', label: 'Injured' },
]

const form = reactive({
    name: '',
    team_id: null,
    position: '',
    preferred_foot: '',
    shirt_number: null,
    date_of_birth: null,
    nationality: '',
    phone: '',
    email: '',
    bio: '',
    height: null,
    weight: null,
    joined_date: null,
    profile_image: '',
    status: 'Active',
})

const teamOptions = reactive([])
const loadTeams = async () => {
    try {
        const data = await getTeams()

        teamOptions.splice(
            0,
            teamOptions.length,
            ...data.items.map(team => ({
                value: team.id,
                label: team.name,
            }))
        )
    } catch (err) {
        console.error(err)
    }
}

onMounted(()=>{
    loadTeams()
})

watch(
    () => props.player,
    (player) => {
        form.name = player?.name ?? ''
        form.team_id = player?.team_id ?? null
        form.position = player?.position ?? ''
        form.preferred_foot = player?.preferred_foot ?? ''
        form.shirt_number = player?.shirt_number ?? null
        form.date_of_birth = player?.date_of_birth ?? null
        form.nationality = player?.nationality ?? ''
        form.phone = player?.phone ?? ''
        form.email = player?.email ?? ''
        form.bio = player?.bio ?? ''
        form.height = player?.height ?? null
        form.weight = player?.weight ?? null
        form.joined_date = player?.joined_date ?? null
        form.profile_image = player?.profile_image ?? ''
        form.status = player?.status ?? 'Active'
    },
    {immediate: true}
)

const save = () => {
    emit('save', {
        ...form
    })
}

</script>

<template>
    <form
        :id="props.id"
        class="space-y-4"
        @submit.prevent="save"
    >
            <div>
                <label class="text-sm font-medium text-gray-700">
                    Name
                </label>

                <AppInput
                    v-model="form.name"
                    placeholder="Player name"
                />
            </div>

            <div>
                <label class="text-sm font-medium text-gray-700">
                    Team
                </label>

                <AppSelect
                    v-model="form.team_id"
                    :options="teamOptions"
                    placeholder="Select Team"
                />
            </div>

            <div>
                <label class="text-sm font-medium text-gray-700">
                    Position
                </label>

                <AppInput
                    v-model="form.position"
                    placeholder="Position"
                />
            </div>

            <div>
                <label class="text-sm font-medium text-gray-700">
                    Preferred Foot
                </label>

                <AppSelect
                    v-model="form.preferred_foot"
                    :options="[
                        { value: 'Right', label: 'Right' },
                        { value: 'Left', label: 'Left' },
                        { value: 'Both', label: 'Both' },
                    ]"
                    placeholder="Select preferred foot"
                />
            </div>

            <div>
                <label class="text-sm font-medium text-gray-700">
                    Shirt Number
                </label>

                <AppInput
                    v-model="form.shirt_number"
                    type="number"
                    placeholder="Shirt number"
                />
            </div>

            <div>
                <label class="text-sm font-medium text-gray-700">
                    Date of Birth
                </label>

                <AppInput
                    v-model="form.date_of_birth"
                    type="date"
                />
            </div>

            <div>
                <label class="text-sm font-medium text-gray-700">
                    Nationality
                </label>

                <AppInput
                    v-model="form.nationality"
                    placeholder="Nationality"
                />
            </div>

            <div>
                <label class="text-sm font-medium text-gray-700">
                    Phone
                </label>

                <AppInput
                    v-model="form.phone"
                    type="tel"
                    placeholder="Phone number"
                />
            </div>

            <div>
                <label class="text-sm font-medium text-gray-700">
                    Email
                </label>

                <AppInput
                    v-model="form.email"
                    type="email"
                    placeholder="Email address"
                />
            </div>

            <div>
                <label class="text-sm font-medium text-gray-700">
                    Height (cm)
                </label>

                <AppInput
                    v-model="form.height"
                    type="number"
                    placeholder="Height in cm"
                />
            </div>

            <div>
                <label class="text-sm font-medium text-gray-700">
                    Weight (kg)
                </label>

                <AppInput
                    v-model="form.weight"
                    type="number"
                    placeholder="Weight in kg"
                />
            </div>

            <div>
                <label class="text-sm font-medium text-gray-700">
                    Status
                </label>
                <AppSelect
                v-model="form.status"
                :options="statusOptions"
                placeholder="Select status"
                />
            </div>
            <button
                type="submit"
                class="hidden"
            >
                Save
            </button>
        </form>
</template>
