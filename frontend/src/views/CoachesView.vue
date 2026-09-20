<script setup>
import {ref,reactive,onMounted, watch, onUnmounted} from 'vue'
import AppTable from '@/components/common/AppTable.vue'
import AppPagination from '@/components/common/AppPagination.vue'
import { getCoaches, getCoach, deleteCoach, createCoach,updateCoach, uploadCoachImage } from '@/services/coachService'
import AppSearch from '@/components/common/AppSearch.vue';
import AppModal from '@/components/common/AppModal.vue'
import CoachForm from '@/components/coaches/CoachForm.vue'
import AppActionsMenu from '@/components/common/AppActionsMenu.vue'
import { useRouter } from 'vue-router'
import AppSelect from '@/components/common/AppSelect.vue'
import { getTeams } from '@/services/teamService'

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
const role = ref('')
const sort = ref('')
const teamId = ref(null)

const router = useRouter()
const showAddCoach = ref(false)
const showEditCoach = ref(false)
const selectedCoach = ref(null)


const teamOptions = reactive([])

const loadTeams = async () => {
    try {
        const data=await getTeams()

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

const loadCoaches = async () => {
    loading.value=true
    error.value=null

    try {
        const data = await getCoaches({
            page: currentPage.value,
            limit: pageSize.value,
            name: search.value,
            role: role.value,
            sort: sort.value,
            teamId: teamId.value,

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

const handleEdit = async (coach)=> {
    console.log('EDIT CLICKED:', coach)
    try {
        selectedCoach.value = await getCoach(coach.id)
        console.log('COACH LOADED:', selectedCoach.value)

        showEditCoach.value = true
        console.log('MODAL STATE:', showEditCoach.value)
    } catch (err) {
        console.error(err)
        error.value = 'Failed to load coach.'
    }
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

const saveCoach = async ({formData, imageFile}) => {
    try {
        const coach = await updateCoach(selectedCoach.value.id, formData)

        if (imageFile) {
            await uploadCoachImage(coach.id, imageFile)
        }

        showEditCoach.value = false 
        selectedCoach.value = null

        await loadCoaches()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to update coach.'
    }
}



let searchTimeout = null

watch([search,role, sort,teamId], () =>{
    currentPage.value=1
    clearTimeout(searchTimeout)

    searchTimeout = setTimeout(()=>{
        loadCoaches()
    }, 500)
})

onMounted(()=>{
    loadTeams()
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

        <div class="mt-6 flex flex-col gap-3 sm:flex-row">
            <div class="max-w-sm flex-1">
                <AppSearch v-model="search" placeholder="Search coaches..." />
            </div>

            <div class="w-full sm:w-56">
                <AppSelect
                    v-model="role"
                    :options="[
                        { value: '', label: 'All Roles' },
                        { value: 'Head Coach', label: 'Head Coach' },
                        { value: 'Assistant Coach', label: 'Assistant Coach' },
                        { value: 'Coach', label: 'Coach' },
                    ]"
                    placeholder="Filter by role"
                />
            </div>

            <div class="w-full sm:w-56">
                <AppSelect
                    v-model="teamId"
                    :options="[
                        { value: '', label: 'All Teams' },
                        ...teamOptions,
                    ]"
                    placeholder="Filter by team"
                />
            </div>

            <div class="w-full sm:w-56">
                <AppSelect
                    v-model="sort"
                    :options="[
                        { value: '', label: 'Default Order' },
                        { value: 'name', label: 'Name: A–Z' },
                        { value: '-name', label: 'Name: Z–A' },
                        { value: 'created_at', label: 'Oldest First' },
                        { value: '-created_at', label: 'Newest First' },
                    ]"
                    placeholder="Sort coaches"
                />
            </div>
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

        <AppModal
            :open="showEditCoach"
            title="Edit Coach"
            description="Update coach information."
            @close="showEditCoach = false"
        >
            <CoachForm
                id="edit-coach-form"
                :coach="selectedCoach"
                @save="saveCoach"
            />

            <template #footer>
                <button
                    type="button"
                    class="rounded-lg border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                    @click="showEditCoach = false"
                >
                    Cancel
                </button>

                <button
                    type="submit"
                    form="edit-coach-form"
                    class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
                >
                    Save Changes
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