<script setup>
import {ref,onMounted, watch, onUnmounted} from 'vue'
import AppTable from '@/components/common/AppTable.vue'
import AppPagination from '@/components/common/AppPagination.vue'
import { getCoaches, deleteCoach, createCoach, uploadCoachImage } from '@/services/coachService'
import AppSearch from '@/components/common/AppSearch.vue';
import AppModal from '@/components/common/AppModal.vue'
import CoachForm from '@/components/coaches/CoachForm.vue'
import AppActionsMenu from '@/components/common/AppActionsMenu.vue'
import { useRouter } from 'vue-router'


const columns = [
    {key: 'name', label: 'Coach'},
    {key: 'team', label: 'Team'},
    {key: 'role', label: 'Role'},
    {key: 'status', label: 'Status' },
]

const coaches = ref ([])
const currentPage = ref(1)
const pageSize = ref(10)
const totalPages = ref(1)
const loading = ref(false)
const error = ref(null)
const search = ref('')
const router = useRouter()
const showAddCoach = ref(false)


const loadCoaches = async () => {
    loading.value=true
    error.value=null

    try {
        const data = await getCoaches({
            page: currentPage.value,
            limit: pageSize.value,
            name: search.value,
        })

        coaches.value = data.items
        totalPages.value = data.pages
    } catch(err) {
        console.error(err)
        error.value = 'Failed to load coaches.'
    } finally {
        loading.value = false
    }
}

const handlePageChange = (page) => {
    currentPage.value = page
    loadCoaches()
}

const openCoach = (coach) => {
    router.push(`/coaches/${coach.id}`)
}

const handleEdit = (coach)=> {
    console.log('Edit coach:', coach)
}

const handleDelete = async (coach) => {
    const confirmed = window.confirm(
        `Are you sure you want to delete ${coach.name}?`
    )
    if (!confirmed) return

    try {
        await deleteCoach(coach.id)
        await loadCoaches()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to delete coach.'
    }
}

const addCoach = async ({ formData, imageFile}) => {
    try {
        const coach = await createCoach(formData)

        if (imageFile) {
            await uploadCoachImage(coach.id, imageFile)
        }

        showAddCoach.value=false
        currentPage.value=1
        await loadCoaches()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to create coach.'
    }

}


let searchTimeout = null

watch(search, () =>{
    currentPage.value=1
    clearTimeout(searchTimeout)

    searchTimeout = setTimeout(()=>{
        loadCoaches()
    }, 500)
})

onMounted(()=>{
    loadCoaches()
})

onUnmounted(()=>{
    clearTimeout(searchTimeout)
})

</script>


<template>
    <div>
        <div class="flex items-start justify-between gap-4">
            <div>
                <h2 class="text-2xl font-bold text-gray-900">
                    Coaches
                </h2>

                <p class="mt-2 text-gray-600">
                    Manage your football coaches.
                </p>
            </div>

            <button
                type="button"
                @click="showAddCoach=true"
                class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
            >
                Add Coach
            </button>
        </div>

        <div
            v-if="error"
            class="mt-6 rounded-lg bg-red-50 p-4 text-sm text-red-700"
        >
            {{ error }}
        </div>

        <div class="mt-6 max-w-sm">
            <AppSearch
                v-model="search"
                placeholder="Search coaches..."
            />
        </div>

        <div class="relative mt-6">
            <AppTable
                :columns="columns"
                :rows="coaches"
                :actions="true"
            >
                <template #cell-name="{ row }">
                    <div class="flex items-center gap-3">
                        <div
                            class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-gray-900 text-sm font-semibold text-white"
                        >
                            {{ row.name?.charAt(0) }}
                        </div>

                        <div>
                            <div class="font-medium text-gray-900">
                                {{ row.name }}
                            </div>

                            <div class="text-xs text-gray-500">
                                Coach #{{ row.id }}
                            </div>
                        </div>
                    </div>
                </template>

                <template #cell-team="{ row }">
                    {{ row.team?.name }}
                </template>

                <template #cell-status="{ value }">
                    <span
                        class="inline-flex rounded-full px-2.5 py-1 text-xs font-medium"
                        :class="
                            value === 'Active'
                                ? 'bg-green-100 text-green-700'
                                : 'bg-orange-100 text-orange-700'
                        "
                    >
                        {{ value }}
                    </span>
                </template>

                <template #actions="{ row, rowIndex }">
                    <AppActionsMenu
                        :row-index="rowIndex"
                        :total-rows="coaches.length"
                        @view="openCoach(row)"
                        @edit="handleEdit(row)"
                        @delete="handleDelete(row)"
                    />
                </template>

            </AppTable>



            <div
                v-if="loading"
                class="absolute inset-0 flex items-center justify-center bg-white/60"
            >
                <span class="text-sm text-gray-500">
                    Searching...
                </span>
            </div>
        </div>

        <AppModal
            :open="showAddCoach"
            title="Add Coach"
            description="Add a new football coach."
            @close="showAddCoach = false"
        >
            <CoachForm
                id="add-coach-form"
                :coach="null"
                @save="addCoach"
            />

            <template #footer>
                <button
                    type="button"
                    class="rounded-lg border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                    @click="showAddCoach = false"
                >
                    Cancel
                </button>

                <button
                    type="submit"
                    form="add-coach-form"
                    class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
                >
                    Add Coach
                </button>
            </template>
        </AppModal>

        <AppPagination
            :current-page="currentPage"
            :total-pages="totalPages"
            @update:current-page="handlePageChange"
        />
    </div>
</template>