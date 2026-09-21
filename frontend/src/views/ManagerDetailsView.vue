<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
    getManager,
    updateManager,
    uploadManagerImage,
} from '@/services/managerService'
import AppModal from '@/components/common/AppModal.vue'
import ManagerForm from '@/components/managers/ManagerForm.vue'

const route = useRoute()
const router = useRouter()

const manager = ref(null)
const loading = ref(true)
const error = ref(null)
const showEditManager = ref(false)

const loadManager = async () => {
    loading.value = true
    error.value = null

    try {
        manager.value = await getManager(route.params.managerId)
    } catch (err) {
        console.error(err)
        error.value = 'Failed to load manager.'
    } finally {
        loading.value = false
    }
}

const goBack = () => {
    router.push('/managers')
}

const openEditManager = () => {
    showEditManager.value = true
}

const saveManager = async ({ formData, imageFile }) => {
    try {
        const updatedManager = await updateManager(
            manager.value.id,
            formData
        )

        if (imageFile) {
            await uploadManagerImage(
                updatedManager.id,
                imageFile
            )
        }

        showEditManager.value = false

        await loadManager()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to update manager.'
    }
}

onMounted(() => {
    loadManager()
})
</script>

<template>
    <div>
        <div
            v-if="loading"
            class="py-12 text-center text-sm text-gray-500"
        >
            Loading manager...
        </div>

        <div
            v-else-if="error"
            class="rounded-lg bg-red-50 p-4 text-sm text-red-700"
        >
            {{ error }}
        </div>

        <div v-else-if="manager">
            <button
                type="button"
                class="mb-6 text-sm font-medium text-gray-600 hover:text-gray-900"
                @click="goBack"
            >
                ← Back to Managers
            </button>

            <div
                class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm"
            >
                <div
                    class="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between"
                >
                    <div class="flex items-center gap-6">
                        <div
                            class="flex h-24 w-24 shrink-0 items-center justify-center overflow-hidden rounded-full bg-gray-900 text-3xl font-semibold text-white"
                        >
                            <img
                                v-if="manager.profile_image"
                                :src="`http://127.0.0.1:8000${manager.profile_image}`"
                                alt="Manager profile"
                                class="h-full w-full object-cover"
                            />

                            <span v-else>
                                {{ manager.name?.charAt(0) }}
                            </span>
                        </div>

                        <div>
                            <h2 class="text-2xl font-bold text-gray-900">
                                {{ manager.name }}
                            </h2>

                            <p class="mt-1 text-sm text-gray-500">
                                Manager #{{ manager.id }}
                            </p>

                            <div class="mt-3 flex flex-wrap gap-2">
                                <span
                                    class="rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-700"
                                >
                                    {{ manager.team?.name }}
                                </span>

                                <span
                                    class="rounded-full px-3 py-1 text-xs font-medium"
                                    :class="
                                        manager.status === 'Active'
                                            ? 'bg-green-100 text-green-700'
                                            : 'bg-orange-100 text-orange-700'
                                    "
                                >
                                    {{ manager.status }}
                                </span>
                            </div>
                        </div>
                    </div>

                    <button
                        type="button"
                        class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
                        @click="openEditManager"
                    >
                        Edit Manager
                    </button>
                </div>
            </div>

            <div class="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
                <section
                    class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm"
                >
                    <h3 class="text-lg font-semibold text-gray-900">
                        Personal Information
                    </h3>

                    <div class="mt-4 space-y-4">
                        <div>
                            <p class="text-xs text-gray-500">
                                Date of Birth
                            </p>
                            <p class="mt-1 text-sm text-gray-900">
                                {{ manager.date_of_birth || '—' }}
                            </p>
                        </div>

                        <div>
                            <p class="text-xs text-gray-500">
                                Nationality
                            </p>
                            <p class="mt-1 text-sm text-gray-900">
                                {{ manager.nationality || '—' }}
                            </p>
                        </div>
                    </div>
                </section>

                <section
                    class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm"
                >
                    <h3 class="text-lg font-semibold text-gray-900">
                        Management Information
                    </h3>

                    <div class="mt-4 space-y-4">
                        <div>
                            <p class="text-xs text-gray-500">
                                Team
                            </p>
                            <p class="mt-1 text-sm text-gray-900">
                                {{ manager.team?.name || '—' }}
                            </p>
                        </div>

                        <div>
                            <p class="text-xs text-gray-500">
                                Team Type
                            </p>
                            <p class="mt-1 text-sm text-gray-900">
                                {{ manager.team?.team_type || '—' }}
                            </p>
                        </div>

                        <div>
                            <p class="text-xs text-gray-500">
                                Status
                            </p>
                            <p class="mt-1 text-sm text-gray-900">
                                {{ manager.status }}
                            </p>
                        </div>
                    </div>
                </section>

                <section
                    class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm"
                >
                    <h3 class="text-lg font-semibold text-gray-900">
                        Contact Information
                    </h3>

                    <div class="mt-4 space-y-4">
                        <div>
                            <p class="text-xs text-gray-500">
                                Phone
                            </p>
                            <p class="mt-1 text-sm text-gray-900">
                                {{ manager.phone || '—' }}
                            </p>
                        </div>

                        <div>
                            <p class="text-xs text-gray-500">
                                Email
                            </p>
                            <p class="mt-1 text-sm text-gray-900">
                                {{ manager.email || '—' }}
                            </p>
                        </div>
                    </div>
                </section>

                <section
                    class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm"
                >
                    <h3 class="text-lg font-semibold text-gray-900">
                        Club Information
                    </h3>

                    <div class="mt-4 space-y-4">
                        <div>
                            <p class="text-xs text-gray-500">
                                Joined Date
                            </p>
                            <p class="mt-1 text-sm text-gray-900">
                                {{ manager.joined_date || '—' }}
                            </p>
                        </div>
                    </div>
                </section>
            </div>

            <section
                class="mt-6 rounded-xl border border-gray-200 bg-white p-6 shadow-sm"
            >
                <h3 class="text-lg font-semibold text-gray-900">
                    About
                </h3>

                <p
                    class="mt-4 whitespace-pre-line text-sm leading-6 text-gray-600"
                >
                    {{ manager.bio || 'No biography available.' }}
                </p>
            </section>

            <AppModal
                :open="showEditManager"
                title="Edit Manager"
                description="Update manager information."
                @close="showEditManager = false"
            >
                <ManagerForm
                    id="edit-manager-form"
                    :manager="manager"
                    @save="saveManager"
                />

                <template #footer>
                    <button
                        type="button"
                        class="rounded-lg border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                        @click="showEditManager = false"
                    >
                        Cancel
                    </button>

                    <button
                        type="submit"
                        form="edit-manager-form"
                        class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
                    >
                        Save Changes
                    </button>
                </template>
            </AppModal>
        </div>
    </div>
</template>