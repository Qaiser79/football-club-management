<script setup>
import { reactive, watch, onMounted, ref } from 'vue'
import AppInput from '@/components/common/AppInput.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import { getTeams } from '@/services/teamService'

const props = defineProps({
    manager: {
        type: Object,
        default: null,
    },
    id: {
        type: String,
        default: 'manager-form',
    },
})

const emit = defineEmits(['save'])

const selectedImage = ref(null)
const imagePreview = ref('')

const statusOptions = [
    { value: 'Active', label: 'Active' },
    { value: 'Inactive', label: 'Inactive' },
]

const form = reactive({
    name: '',
    team_id: null,
    date_of_birth: null,
    nationality: '',
    phone: '',
    email: '',
    bio: '',
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

    if (!file) return

    selectedImage.value = file
    imagePreview.value = URL.createObjectURL(file)
}

const removeImage = () => {
    selectedImage.value = null
    imagePreview.value = ''
}

onMounted(() => {
    loadTeams()
})

watch(
    () => props.manager,
    (manager) => {
        form.name = manager?.name ?? ''
        form.team_id = manager?.team_id ?? null
        form.date_of_birth = manager?.date_of_birth ?? null
        form.nationality = manager?.nationality ?? ''
        form.phone = manager?.phone ?? ''
        form.email = manager?.email ?? ''
        form.bio = manager?.bio ?? ''
        form.joined_date = manager?.joined_date ?? null
        form.profile_image = manager?.profile_image ?? ''
        form.status = manager?.status ?? 'Active'

        selectedImage.value = null

        if (manager?.profile_image) {
            imagePreview.value =
                `http://127.0.0.1:8000${manager.profile_image}`
        } else {
            imagePreview.value = ''
        }
    },
    {
        immediate: true,
    }
)

const save = () => {
    emit('save', {
        formData: { ...form },
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
            <h3 class="mb-4 text-lg font-semibold text-gray-900">
                Personal Information
            </h3>

            <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
                <AppInput
                    v-model="form.name"
                    label="Full Name"
                    placeholder="Enter manager name"
                    required
                />

                <AppInput
                    v-model="form.date_of_birth"
                    label="Date of Birth"
                    type="date"
                />

                <AppInput
                    v-model="form.nationality"
                    label="Nationality"
                    placeholder="Enter nationality"
                />

                <AppInput
                    v-model="form.phone"
                    label="Phone"
                    placeholder="Enter phone number"
                />

                <AppInput
                    v-model="form.email"
                    label="Email"
                    type="email"
                    placeholder="Enter email address"
                />
            </div>
        </section>

        <!-- Management Information -->
        <section>
            <h3 class="mb-4 text-lg font-semibold text-gray-900">
                Management Information
            </h3>

            <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
                <AppSelect
                    v-model="form.team_id"
                    :options="teamOptions"
                    placeholder="Select team"
                />

                <AppSelect
                    v-model="form.status"
                    :options="statusOptions"
                    placeholder="Select status"
                />
            </div>
        </section>

        <!-- Club Information -->
        <section>
            <h3 class="mb-4 text-lg font-semibold text-gray-900">
                Club Information
            </h3>

            <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
                <AppInput
                    v-model="form.joined_date"
                    label="Joined Date"
                    type="date"
                />
            </div>
        </section>

        <!-- About -->
        <section>
            <h3 class="mb-4 text-lg font-semibold text-gray-900">
                About
            </h3>

            <textarea
                v-model="form.bio"
                rows="5"
                placeholder="Enter manager biography"
                class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
            ></textarea>
        </section>

        <!-- Profile Photo -->
        <section>
            <h3 class="mb-4 text-lg font-semibold text-gray-900">
                Profile Photo
            </h3>

            <div class="flex flex-col gap-4">
                <div
                    v-if="imagePreview"
                    class="relative h-32 w-32 overflow-hidden rounded-xl border border-gray-200"
                >
                    <img
                        :src="imagePreview"
                        alt="Manager preview"
                        class="h-full w-full object-cover"
                    />

                    <button
                        type="button"
                        class="absolute right-1 top-1 rounded-full bg-white px-2 py-1 text-xs text-gray-700 shadow"
                        @click="removeImage"
                    >
                        Remove
                    </button>
                </div>

                <input
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    class="block w-full text-sm text-gray-600"
                    @change="handleImageSelect"
                />
            </div>
        </section>

        <button
            type="submit"
            class="hidden"
        >
            Save
        </button>
    </form>
</template>