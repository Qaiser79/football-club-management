<script setup>
import { reactive, watch, onMounted, ref } from 'vue'
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
const selectedImage = ref(null)
const imagePreview = ref('')

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

const handleImageSelect = (event) => {
    const file = event.target.files?.[0]

    if (!file) {
        return
    }

    selectedImage.value = file
    imagePreview.value = URL.createObjectURL(file)
}

const removeImage = () => {
    selectedImage.value=null
    imagePreview.value = ''
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
        selectedImage.value = null
        if(player?.profile_image) {
            imagePreview.value = `http://127.0.0.1:8000${player.profile_image}`
        } else {
            imagePreview.value = ''
        }
        form.status = player?.status ?? 'Active'
    },
    {immediate: true}
)

const save = () => {
    emit('save', {
        formData: {
            ...form
        },
        imageFile: selectedImage.value,
    })
}

</script>

<template>
    <form
        :id="props.id"
        class="space-y-8"
        @submit.prevent="save"
    >

        <!-- Personal Information -->
        <section>
            <div class="mb-4">
                <h4 class="text-sm font-semibold text-gray-900">
                    Personal Information
                </h4>
                <p class="mt-1 text-xs text-gray-500">
                    Basic information about the player.
                </p>
            </div>

            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">

                <!-- Name -->
                <div class="sm:col-span-2">
                    <label class="text-sm font-medium text-gray-700">
                        Name
                    </label>

                    <AppInput
                        v-model="form.name"
                        placeholder="Player name"
                    />
                </div>

                <!-- Date of Birth -->
                <div>
                    <label class="text-sm font-medium text-gray-700">
                        Date of Birth
                    </label>

                    <AppInput
                        v-model="form.date_of_birth"
                        type="date"
                    />
                </div>

                <!-- Nationality -->
                <div>
                    <label class="text-sm font-medium text-gray-700">
                        Nationality
                    </label>

                    <AppInput
                        v-model="form.nationality"
                        placeholder="Nationality"
                    />
                </div>

                <!-- Phone -->
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

                <!-- Email -->
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

            </div>
        </section>


        <!-- Football Information -->
        <section class="border-t border-gray-100 pt-6">
            <div class="mb-4">
                <h4 class="text-sm font-semibold text-gray-900">
                    Football Information
                </h4>
                <p class="mt-1 text-xs text-gray-500">
                    Player's role and football-specific information.
                </p>
            </div>

            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">

                <!-- Team -->
                <div class="sm:col-span-2">
                    <label class="text-sm font-medium text-gray-700">
                        Team
                    </label>

                    <AppSelect
                        v-model="form.team_id"
                        :options="teamOptions"
                        placeholder="Select Team"
                    />
                </div>

                <!-- Position -->
                <div>
                    <label class="text-sm font-medium text-gray-700">
                        Position
                    </label>

                    <AppInput
                        v-model="form.position"
                        placeholder="Position"
                    />
                </div>

                <!-- Preferred Foot -->
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

                <!-- Shirt Number -->
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

                <!-- Status -->
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

            </div>
        </section>


        <!-- Physical Information -->
        <section class="border-t border-gray-100 pt-6">
            <div class="mb-4">
                <h4 class="text-sm font-semibold text-gray-900">
                    Physical Information
                </h4>
                <p class="mt-1 text-xs text-gray-500">
                    Optional physical details.
                </p>
            </div>

            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">

                <!-- Height -->
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

                <!-- Weight -->
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

            </div>
        </section>

        <!-- Club Information -->
        <section class="border-t border-gray-100 pt-6">
            <div class="mb-4">
                <h4 class="text-sm font-semibold text-gray-900">
                    Club Information
                </h4>
                <p class="mt-1 text-xs text-gray-500">
                    Information about the player's time at the club.
                </p>
            </div>

            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">

                <!-- Joined Date -->
                <div>
                    <label class="text-sm font-medium text-gray-700">
                        Joined Date
                    </label>

                    <AppInput
                        v-model="form.joined_date"
                        type="date"
                    />
                </div>

            </div>
        </section>

        <!-- About -->
        <section class="border-t border-gray-100 pt-6">
            <div class="mb-4">
                <h4 class="text-sm font-semibold text-gray-900">
                    About
                </h4>
                <p class="mt-1 text-xs text-gray-500">
                    Add a short description about the player.
                </p>
            </div>

            <div>
                <label class="text-sm font-medium text-gray-700">
                    Bio
                </label>

                <textarea
                    v-model="form.bio"
                    rows="4"
                    placeholder="Write a short player bio..."
                    class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-gray-500 focus:ring-2 focus:ring-gray-100"
                ></textarea>
            </div>
        </section>

        <!-- Profile -->
        <section class="border-t border-gray-100 pt-6">
            <div class="mb-4">
                <h4 class="text-sm font-semibold text-gray-900">
                    Profile Photo
                </h4>
                <p class="mt-1 text-xs text-gray-500">
                    Add a profile photo for the player.
                </p>
            </div>

            <div class="flex flex-col items-start gap-4 sm:flex-row sm:items-center">

                <!-- Preview -->
                <div
                    class="flex h-24 w-24 shrink-0 items-center justify-center overflow-hidden rounded-full bg-gray-100 ring-1 ring-gray-200"
                >
                    <img
                        v-if="imagePreview"
                        :src="imagePreview"
                        alt="Player profile"
                        class="h-full w-full object-cover"
                    />

                    <span
                        v-else
                        class="text-2xl font-semibold text-gray-400"
                    >
                        {{ form.name?.charAt(0)?.toUpperCase() || '?' }}
                    </span>
                </div>

                <!-- Controls -->
                <div class="space-y-2">
                    <label
                        class="inline-flex cursor-pointer items-center rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm transition hover:bg-gray-50"
                    >
                        {{ imagePreview ? 'Change photo' : 'Choose photo' }}

                        <input
                            type="file"
                            accept="image/jpeg,image/png,image/webp"
                            class="hidden"
                            @change="handleImageSelect"
                        />
                    </label>

                    <button
                        v-if="imagePreview"
                        type="button"
                        class="ml-2 text-sm text-gray-500 hover:text-red-600"
                        @click="removeImage"
                    >
                        Remove
                    </button>

                    <p class="text-xs text-gray-400">
                        JPG, PNG or WebP
                    </p>
                </div>

            </div>
        </section>


        <!-- Save -->
        <button
            type="submit"
            class="hidden"
        >
            Save
        </button>

    </form>
</template>
