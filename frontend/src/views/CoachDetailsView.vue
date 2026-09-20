<script setup>
import {ref, onMounted} from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCoach, updateCoach, uploadCoachImage } from '@/services/coachService'
import AppModal from '@/components/common/AppModal.vue'
import CoachForm from '@/components/coaches/CoachForm.vue'
import { formatDate } from '@/utils/date'

const route = useRoute()
const router = useRouter()

const coach= ref(null)
const loading = ref(true)
const error = ref(null)

const showEditCoach = ref(false)

const loadCoach = async () => {
    loading.value = true
    error.value = null

    try {
        coach.value = await getCoach(route.params.coachId)
    } catch(err) {
        console.error(err)
        error.value = 'Failed to load coach.'
    } finally {
        loading.value = false
    }
}

const goBack=()=> {
    router.push('/coaches')
}

const handleEditSave = async ({formData, imageFile}) => {
    try {
        await updateCoach(coach.value.id, formData)

        if (imageFile) {
            await uploadCoachImage(coach.value.id,imageFile)
        }

        showEditCoach.value = false
        await loadCoach()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to update coach.'
    }
}

onMounted(()=> {
    loadCoach()
})

</script>


<template>
    <div>
        <!-- Back -->
        <button
            type="button"
            class="text-sm font-medium text-gray-600 hover:text-gray-900"
            @click="goBack"
        >
            ← Back to Coaches
        </button>

        <!-- Loading -->
        <div
            v-if="loading"
            class="mt-6 text-sm text-gray-500"
        >
            Loading coach...
        </div>

        <!-- Error -->
        <div
            v-else-if="error"
            class="mt-6 rounded-lg bg-red-50 p-4 text-sm text-red-700"
        >
            {{ error }}
        </div>

        <!-- Coach Profile -->
        <div
            v-else-if="coach"
            class="mt-6 overflow-hidden rounded-2xl border border-gray-200 bg-white"
        >
            <div class="p-6 sm:p-8">
                <div class="flex flex-col gap-6 sm:flex-row sm:items-center">

                    <!-- Profile Image -->
                    <div class="shrink-0">
                        <div
                            class="flex h-28 w-28 items-center justify-center overflow-hidden rounded-2xl bg-gray-100 text-3xl font-bold text-gray-500"
                        >
                            <img
                                v-if="coach.profile_image"
                                :src="`http://127.0.0.1:8000${coach.profile_image}`"
                                :alt="coach.name"
                                class="h-full w-full object-cover"
                            />

                            <span v-else>
                                {{ coach.name?.charAt(0) }}
                            </span>
                        </div>
                    </div>

                    <!-- Coach Identity -->
                    <div class="min-w-0 flex-1">
                        <div class="flex flex-wrap items-center gap-3">
                            <h1 class="text-3xl font-bold text-gray-900">
                                {{ coach.name }}
                            </h1>

                            <span
                                class="inline-flex rounded-full px-3 py-1 text-xs font-medium"
                                :class="
                                    coach.status === 'Active'
                                        ? 'bg-green-100 text-green-700'
                                        : 'bg-orange-100 text-orange-700'
                                "
                            >
                                {{ coach.status }}
                            </span>
                        </div>

                        <div class="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-gray-600">
                            <span>
                                {{ coach.role }}
                            </span>

                            <span class="text-gray-300">•</span>

                            <span>
                                {{ coach.team?.name }}
                            </span>
                        </div>
                    </div>

                    <!-- Edit Coach -->
                    <button
                        type="button"
                        class="shrink-0 rounded-lg border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50"
                        @click="showEditCoach = true"
                    >
                        Edit Coach
                    </button>

                </div>
            </div>
        </div>

                <!-- Coach Information -->
        <div
            v-if="coach"
            class="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2"
        >
            <!-- Personal Information -->
            <div class="rounded-2xl border border-gray-200 bg-white p-6">
                <h2 class="text-lg font-semibold text-gray-900">
                    Personal Information
                </h2>

                <div class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-2">
                    <div>
                        <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                            Date of Birth
                        </div>

                        <div class="mt-1 text-sm font-medium text-gray-900">
                            {{ coach.date_of_birth || '—' }}
                        </div>
                    </div>

                    <div>
                        <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                            Nationality
                        </div>

                        <div class="mt-1 text-sm font-medium text-gray-900">
                            {{ coach.nationality || '—' }}
                        </div>
                    </div>
                </div>
            </div>

            <!-- Coaching Information -->
            <div class="rounded-2xl border border-gray-200 bg-white p-6">
                <h2 class="text-lg font-semibold text-gray-900">
                    Coaching Information
                </h2>

                <div class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-2">
                    <div>
                        <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                            Role
                        </div>

                        <div class="mt-1 text-sm font-medium text-gray-900">
                            {{ coach.role || '—' }}
                        </div>
                    </div>

                    <div>
                        <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                            Team
                        </div>

                        <div class="mt-1 text-sm font-medium text-gray-900">
                            {{ coach.team?.name || '—' }}
                        </div>
                    </div>
                </div>
            </div>
        </div>

                <!-- Contact & Club Information -->
        <div
            v-if="coach"
            class="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2"
        >
            <!-- Contact Information -->
            <div class="rounded-2xl border border-gray-200 bg-white p-6">
                <h2 class="text-lg font-semibold text-gray-900">
                    Contact Information
                </h2>

                <div class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-2">
                    <div>
                        <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                            Phone
                        </div>

                        <div class="mt-1 text-sm font-medium text-gray-900">
                            {{ coach.phone || '—' }}
                        </div>
                    </div>

                    <div>
                        <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                            Email
                        </div>

                        <div class="mt-1 break-all text-sm font-medium text-gray-900">
                            {{ coach.email || '—' }}
                        </div>
                    </div>
                </div>
            </div>

            <!-- Club Information -->
            <div class="rounded-2xl border border-gray-200 bg-white p-6">
                <h2 class="text-lg font-semibold text-gray-900">
                    Club Information
                </h2>

                <div class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-2">
                    <div>
                        <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                            Joined Date
                        </div>

                        <div class="mt-1 text-sm font-medium text-gray-900">
                            {{ coach.joined_date || '—' }}
                        </div>
                    </div>

                    <div>
                        <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                            Status
                        </div>

                        <div class="mt-1 text-sm font-medium text-gray-900">
                            {{ coach.status || '—' }}
                        </div>
                    </div>
                </div>
            </div>
        </div>

                <!-- Bio -->
        <div
            v-if="coach"
            class="mt-6 rounded-2xl border border-gray-200 bg-white p-6"
        >
            <h2 class="text-lg font-semibold text-gray-900">
                Bio
            </h2>

            <p class="mt-4 whitespace-pre-line text-sm leading-6 text-gray-600">
                {{ coach.bio || 'No biography has been added for this coach.' }}
            </p>
        </div>

                <!-- Edit Coach Modal -->
        <AppModal
            :open="showEditCoach"
            title="Edit Coach"
            @close="showEditCoach = false"
        >
            <CoachForm
                :coach="coach"
                @save="handleEditSave"
                @cancel="showEditCoach = false"
            />

            <template #footer>
                <button
                    type="button"
                    class="rounded-lg border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50"
                    @click="showEditCoach = false"
                >
                    Cancel
                </button>

                <button
                    type="submit"
                    form="coach-form"
                    class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-gray-800"
                >
                    Save Changes
                </button>
            </template>
        </AppModal>

    </div>
</template>