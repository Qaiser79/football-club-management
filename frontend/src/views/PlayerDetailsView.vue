<script setup>
import {ref, onMounted} from 'vue'
import { useRoute, useRouter } from 'vue-router';
import {getPlayer} from '@/services/playerService'


const route = useRoute()
const router = useRouter()

const player = ref(null)
const loading = ref(true)
const error = ref(null)

const loadPlayer = async () => {
    loading.value = true
    error.value = null

    try {
        player.value = await getPlayer(route.params.playerId)
    } catch (err) {
        console.error(err)
        error.value = 'Failed to load player.'
    } finally {
        loading.value = false
    }
}

const goBack = () => {
    router.push('/players')
}

onMounted(()=> {
    loadPlayer()
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
            ← Back to Players
        </button>

        <!-- Loading -->
        <div
            v-if="loading"
            class="mt-6 text-sm text-gray-500"
        >
            Loading player...
        </div>

        <!-- Error -->
        <div
            v-else-if="error"
            class="mt-6 rounded-lg bg-red-50 p-4 text-sm text-red-700"
        >
            {{ error }}
        </div>

        <!-- Player Profile -->
        <div
            v-else-if="player"
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
                                v-if="player.profile_image"
                                :src="`http://127.0.0.1:8000${player.profile_image}`"
                                :alt="player.name"
                                class="h-full w-full object-cover"
                            />

                            <span v-else>
                                {{ player.name?.charAt(0) }}
                            </span>
                        </div>
                    </div>

                    <!-- Player Identity -->
                    <div class="min-w-0 flex-1">
                        <div class="flex flex-wrap items-center gap-3">
                            <h1 class="text-3xl font-bold text-gray-900">
                                {{ player.name }}
                            </h1>

                            <span
                                class="inline-flex rounded-full px-3 py-1 text-xs font-medium"
                                :class="
                                    player.status === 'Active'
                                        ? 'bg-green-100 text-green-700'
                                        : 'bg-orange-100 text-orange-700'
                                "
                            >
                                {{ player.status }}
                            </span>
                        </div>

                        <div class="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-gray-600">
                            <span>
                                {{ player.position }}
                            </span>

                            <span class="text-gray-300">•</span>

                            <span>
                                {{ player.team?.name }}
                            </span>
                        </div>
                    </div>

                    <!-- Shirt Number -->
                    <div
                        v-if="player.shirt_number"
                        class="shrink-0 text-left sm:text-right"
                    >
                        <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                            Shirt Number
                        </div>

                        <div class="mt-1 text-4xl font-bold text-gray-900">
                            #{{ player.shirt_number }}
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <div
            v-if="player"
            class="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2"
        >   
            <div class="rounded-2xl border border-gray-200 bg-white p-6">
            <h2 class="text-lg font-semibold text-gray-900">
                Personal Information
            </h2>

            <div class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-3">
                <div>
                    <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                        Date of Birth
                    </div>

                    <div class="mt-1 text-sm font-medium text-gray-900">
                        {{ player.date_of_birth || '—' }}
                    </div>
                </div>

                <div>
                    <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                        Nationality
                    </div>

                    <div class="mt-1 text-sm font-medium text-gray-900">
                        {{ player.nationality || '—' }}
                    </div>
                </div>

                <div>
                    <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                        Preferred Foot
                    </div>

                    <div class="mt-1 text-sm font-medium text-gray-900">
                        {{ player.preferred_foot || '—' }}
                    </div>
                </div>
            </div>
            </div>

            <div
                class="rounded-2xl border border-gray-200 bg-white p-6"
            >
                <h2 class="text-lg font-semibold text-gray-900">
                    Physical Information
                </h2>

                <div class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-2">
                    <div>
                        <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                            Height
                        </div>

                        <div class="mt-1 text-sm font-medium text-gray-900">
                            {{ player.height ? `${player.height} cm` : '—' }}
                        </div>
                    </div>

                    <div>
                        <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                            Weight
                        </div>

                        <div class="mt-1 text-sm font-medium text-gray-900">
                            {{ player.weight ? `${player.weight} kg` : '—' }}
                        </div>
                    </div>
                </div>
            </div>

            <div
                class="rounded-2xl border border-gray-200 bg-white p-6"
            >
                <h2 class="text-lg font-semibold text-gray-900">
                    Contact Information
                </h2>

                <div class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-2">
                    <div>
                        <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                            Phone
                        </div>

                        <div class="mt-1 text-sm font-medium text-gray-900">
                            {{ player.phone || '—' }}
                        </div>
                    </div>

                    <div>
                        <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                            Email
                        </div>

                        <div class="mt-1 break-all text-sm font-medium text-gray-900">
                            {{ player.email || '—' }}
                        </div>
                    </div>
                </div>
            </div>

            <div
                v-if="player"
                class="rounded-2xl border border-gray-200 bg-white p-6"
            >
                <h2 class="text-lg font-semibold text-gray-900">
                    Club Information
                </h2>

                <div class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-3">
                    <div>
                        <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                            Team
                        </div>

                        <div class="mt-1 text-sm font-medium text-gray-900">
                            {{ player.team?.name || '—' }}
                        </div>
                    </div>

                    <div>
                        <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                            Joined Date
                        </div>

                        <div class="mt-1 text-sm font-medium text-gray-900">
                            {{ player.joined_date || '—' }}
                        </div>
                    </div>

                    <div>
                        <div class="text-xs font-medium uppercase tracking-wide text-gray-500">
                            Status
                        </div>

                        <div class="mt-1 text-sm font-medium text-gray-900">
                            {{ player.status || '—' }}
                        </div>
                    </div>
                </div>
            </div>

        </div>



       

        

        <div
            v-if="player"
            class="mt-6 rounded-2xl border border-gray-200 bg-white p-6"
        >
            <h2 class="text-lg font-semibold text-gray-900">
                Bio
            </h2>

            <p class="mt-4 whitespace-pre-line text-sm leading-6 text-gray-600">
                {{ player.bio || 'No biography has been added for this player.' }}
            </p>
        </div>

    </div>
</template>