<script setup>
import {ref, onMounted, watch, onUnmounted} from 'vue'
import AppTable from '@/components/common/AppTable.vue'
import AppPagination from '@/components/common/AppPagination.vue'
import { getClubs,createClub,updateClub,deleteClub } from '@/services/clubService'
import AppSearch from '@/components/common/AppSearch.vue'
import ClubForm from '@/components/clubs/ClubForm.vue'
import AppModal from '@/components/common/AppModal.vue'
import AppActionsMenu from '@/components/common/AppActionsMenu.vue'

const columns = [
    {key: 'name', label: 'Club'},
    {key: 'short_name', label: 'Short Name'},
    {key: 'country', label: 'Country'},
]

const clubs = ref([])
const search = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const totalPages = ref(1)
const loading = ref(false)
const error = ref(null)
const showAddClub = ref(false)
const editingClub = ref(null)

const loadClubs = async () => {
    loading.value = true
    error.value = null

    try {
        const data = await getClubs({
            page: currentPage.value,
            limit: pageSize.value,
            name: search.value,
        })

        clubs.value=data.items
        totalPages.value=data.pages
    } catch(err){
        console.error(err)
        error.value = 'Failed to load clubs'
    } finally {
        loading.value = false
    }
}

const handlePageChange = (page) => {
    currentPage.value = page
    loadClubs()
}


const addClub = async (formData)=> {
    try {
        await createClub(formData)

        showAddClub.value=false
        currentPage.value = 1

        await loadClubs()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to create club'
    }
}

const handleEdit = (club) => {
    editingClub.value = {...club}
}

const saveClub = async (formData) => {
    try {
        await updateClub(
            editingClub.value.id,
            formData
        )

        editingClub.value = null

        await loadClubs()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to update club'
    }
}

const handleDelete = async (club) => {
    const confirmed = window.confirm(
        `Are you sure you want to delete ${club.name}?`
    )

    if (!confirmed) {
        return
    }

    try {
        await deleteClub(club.id)
        await loadClubs()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to delete club'
    }
}

let searchTimeout = null
watch(search, ()=>{
    currentPage.value = 1
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(()=>{
        loadClubs()
    }, 500)
})

onMounted(() => {
    loadClubs()
})

onUnmounted(()=>{
    clearTimeout(searchTimeout)
})
</script>

<template>
    <div>
        <div class="flex items-center justify-between">
            <h2 class="text-2xl font-bold text-gray-900">
                Clubs
            </h2>

            <button
                type="button"
                class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
                @click="showAddClub = true"
            >
                Add Club
            </button>
        </div>

        <p class="mt-2 text-gray-600">
            Manage clubs.
        </p>

        <div
            v-if="error"
            class="mt-6 rounded-lg bg-red-50 p-4 text-sm text-red-700"
        >
            {{ error }}
        </div>

        <div
            v-if="loading"
            class="mt-6 text-sm text-gray-500"
        >
            Loading clubs...
        </div>
        <div class="mt-6 max-w-sm">
            <AppSearch
                v-model="search"
                placeholder="Search clubs..."
            />
        </div>

        <div class="mt-6">
            <AppTable
                :columns="columns"
                :rows="clubs"
                :actions="true"
            >
                <template #actions="{ row, rowIndex }">
                    <AppActionsMenu
                        :row-index="rowIndex"
                        :total-rows="clubs.length"
                        @edit="handleEdit(row)"
                        @delete="handleDelete(row)"
                    />
                </template>
            </AppTable>
        </div>

        <AppPagination
            :current-page="currentPage"
            :total-pages="totalPages"
            @update:current-page="handlePageChange"
        />
    </div>

    <AppModal
        :open="showAddClub"
        title="Add Club"
        description="Add a new club."
        @close="showAddClub = false"
    >
        <ClubForm
            id="add-club-form"
            @save="addClub"
        />

        <template #footer>
            <button
                type="button"
                class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
                @click="showAddClub = false"
            >
                Cancel
            </button>

            <button
                type="submit"
                form="add-club-form"
                class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white"
            >
                Add Club
            </button>
        </template>
    </AppModal>

        <AppModal
        :open="!!editingClub"
        title="Edit Club"
        description="Update club information."
        @close="editingClub = null"
    >
        <ClubForm
            id="edit-club-form"
            :club="editingClub"
            @save="saveClub"
        />

        <template #footer>
            <button
                type="button"
                class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
                @click="editingClub = null"
            >
                Cancel
            </button>

            <button
                type="submit"
                form="edit-club-form"
                class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white"
            >
                Save
            </button>
        </template>
    </AppModal>

</template>