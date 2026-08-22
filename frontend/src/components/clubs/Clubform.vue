<script setup>
import { ref,onMounted } from 'vue'
import { getOrganizations } from '@/services/organizationService'

const props = defineProps({
    club: {
        type: Object,
        default: null,
    },
})

const emit = defineEmits(['save'])

const organizations = ref([])
const loadingOrganizations = ref(false)

const form = ref({
    organization_id: '',
    name: '',
    short_name: '',
    country: '',
})

const loadOrganizations = async ()=> {
    loadingOrganizations.value=true
    try {
        const data = await getOrganizations()
        organizations.value=data.items
    } catch (err) {
        console.error(err)
    } finally {
        loadingOrganizations.value = false
    }
}

const handleSubmit = ()=>{
    emit('save', {
        organization_id: Number(form.value.organization_id),
        name: form.value.name,
        short_name: form.value.short_name || null,
        country: form.value.country || null,
    })
}

onMounted(async ()=> {
    await loadOrganizations()

    if (props.club) {
        form.value = {
            organization_id: props.club.organization_id,
            name: props.club.name,
            short_name: props.club.short_name || '',
            country: props.club.country || '',
        }
    }
})
</script>

<template>
    <form
        :id="$attrs.id"
        class="space-y-4"
        @submit.prevent="handleSubmit"
    >
        <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">
                Organization
            </label>

            <select
                v-model="form.organization_id"
                class="w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 outline-none focus:border-gray-500 focus:ring-2 focus:ring-gray-200"
                required
                :disabled="loadingOrganizations"
            >
                <option value="" disabled>
                    Select organization
                </option>

                <option
                    v-for="organization in organizations"
                    :key="organization.id"
                    :value="organization.id"
                >
                    {{ organization.name }}
                </option>
            </select>
        </div>

        <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">
                Club Name
            </label>

            <input
                v-model="form.name"
                type="text"
                required
                minlength="2"
                maxlength="100"
                class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-900 outline-none focus:border-gray-500 focus:ring-2 focus:ring-gray-200"
                placeholder="Enter club name"
            />
        </div>

        <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">
                Short Name
            </label>

            <input
                v-model="form.short_name"
                type="text"
                minlength="2"
                maxlength="20"
                class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-900 outline-none focus:border-gray-500 focus:ring-2 focus:ring-gray-200"
                placeholder="Enter short name"
            />
        </div>

        <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">
                Country
            </label>

            <input
                v-model="form.country"
                type="text"
                minlength="2"
                maxlength="100"
                class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-900 outline-none focus:border-gray-500 focus:ring-2 focus:ring-gray-200"
                placeholder="Enter country"
            />
        </div>
    </form>
</template>