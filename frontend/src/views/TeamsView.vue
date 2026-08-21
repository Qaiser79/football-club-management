<script setup>
import { ref,onMounted, watch, onUnmounted } from 'vue'
import AppTable from '@/components/common/AppTable.vue'
import { getTeams, createTeam } from '@/services/teamService'
import AppPagination from '@/components/common/AppPagination.vue'
import AppSearch from '@/components/common/AppSearch.vue'
import TeamForm from '@/components/teams/TeamForm.vue'
import AppModal from '@/components/common/AppModal.vue'

const columns = [
    {key: 'name', label: 'Team'},
    {key: 'club', label: 'Club'},
    {key: 'team_type', label: 'Type'},
]

const teams = ref([])
const search = ref('')
const loading = ref(false)
const error = ref(null)
const currentPage = ref(1)
const pageSize = ref(1)
const totalPages = ref(1)
const showAddTeam = ref(false)

const loadTeams = async () => {
    loading.value = true
    error.value = null

    try {
        const data = await getTeams({
            page: currentPage.value,
            limit: pageSize.value,
            name: search.value,
        })

        teams.value = data.items
        totalPages.value = data.pages
    } catch (err) {
        console.error(err)
        error.value = 'Failed to load teams'
    } finally {
        loading.value = false
    }
}

const addTeam = async (formData) => {
    try {
        await createTeam(formData)

        showAddTeam.value=false
        currentPage.value = 1

        await loadTeams()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to create team'
    }
}


let searchTimeout = null

watch(search, ()=>{
    currentPage.value = 1

    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(()=>{
        loadTeams()
    }, 500)
})

const handlePageChange = (page) => {
    currentPage.value = page
    loadTeams()
}

onMounted(()=> {
    loadTeams()
})

onUnmounted(()=>{
    clearTimeout(searchTimeout)
})

</script>

<template>
    <div>
        <h2 class="text-2xl font-bold text-gray-900">
            Teams
        </h2>

        <p class="mt-2 text-gray-600">
            Manage teams.
        </p>

        <div
            v-if="error"
            class="mt-6 rounded-lg bg-red-50 p-4 text-sm text-red-700"
        >
            {{ error }}
        </div>

        <button
            type="button"
            class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
            @click="showAddTeam = true"
        >
            Add Team
        </button>

        <div
            v-if="loading"
            class="mt-6 text-sm text-gray-500"
        >
            Loading teams...
        </div>

        <div class="mt-6 max-w-sm">
            <AppSearch
                v-model="search"
                placeholder="Search teams..."
            />
        </div>

        <div
            class="mt-6"
        >

            <AppTable
                :columns="columns"
                :rows="teams"
            >
                <template #cell-club="{ row }">
                    {{ row.club?.name }}
                </template>
            </AppTable>

            <AppPagination
                :current-page="currentPage"
                :total-pages="totalPages"
                @update:current-page="handlePageChange"
            >
            </AppPagination>

        </div>

        <AppModal
            :open="showAddTeam"
            title="Add Team"
            description="Add a new team."
            @close="showAddTeam = false"
        >
            <TeamForm
                id="add-team-form"
                @save="addTeam"
            />

            <template #footer>
                <button
                    type="button"
                    class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
                    @click="showAddTeam = false"
                >
                    Cancel
                </button>

                <button
                    type="submit"
                    form="add-team-form"
                    class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white"
                >
                    Add Team
                </button>
            </template>
        </AppModal>


    </div>
</template>