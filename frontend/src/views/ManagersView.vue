<script setup>
import { ref, reactive, onMounted, watch, onUnmounted } from 'vue'
import AppTable from '@/components/common/AppTable.vue'
import AppPagination from '@/components/common/AppPagination.vue'
import {
    getManagers,
    getManager,
    deleteManager,
    createManager,
    updateManager,
    uploadManagerImage,
} from '@/services/managerService'
import AppSearch from '@/components/common/AppSearch.vue'
import AppModal from '@/components/common/AppModal.vue'
import ManagerForm from '@/components/managers/ManagerForm.vue'
import AppActionsMenu from '@/components/common/AppActionsMenu.vue'
import { useRouter } from 'vue-router'
import AppSelect from '@/components/common/AppSelect.vue'
import { getTeams } from '@/services/teamService'

const columns = [
    { key: 'name', label: 'Manager' },
    { key: 'team', label: 'Team' },
    { key: 'status', label: 'Status' },
]

const managers = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const totalPages = ref(1)
const loading = ref(false)
const error = ref(null)
const search = ref('')
const sort = ref('')
const teamId = ref(null)
const status = ref('')

const router = useRouter()
const showAddManager = ref(false)
const showEditManager = ref(false)
const selectedManager = ref(null)

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

const loadManagers = async () => {
    loading.value = true
    error.value = null

    try {
        const data = await getManagers({
            page: currentPage.value,
            limit: pageSize.value,
            name: search.value,
            sort: sort.value,
            status: status.value,
            teamId: teamId.value,
        })

        managers.value = data.items
        totalPages.value = data.pages
    } catch (err) {
        console.error(err)
        error.value = 'Failed to load managers.'
    } finally {
        loading.value = false
    }
}

const handlePageChange = (page) => {
    currentPage.value = page
    loadManagers()
}

const openManager = (manager) => {
    router.push(`/managers/${manager.id}`)
}

const handleEdit = async (manager) => {
    console.log('EDIT CLICKED:', manager)

    try {
        selectedManager.value = await getManager(manager.id)

        console.log('MANAGER LOADED:', selectedManager.value)

        showEditManager.value = true

        console.log('MODAL STATE:', showEditManager.value)
    } catch (err) {
        console.error(err)
        error.value = 'Failed to load manager.'
    }
}

const handleDelete = async (manager) => {
    const confirmed = window.confirm(
        `Are you sure you want to delete ${manager.name}?`
    )

    if (!confirmed) return

    try {
        await deleteManager(manager.id)
        await loadManagers()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to delete manager.'
    }
}

const addManager = async ({ formData, imageFile }) => {
    try {
        const manager = await createManager(formData)

        if (imageFile) {
            await uploadManagerImage(manager.id, imageFile)
        }

        showAddManager.value = false
        currentPage.value = 1

        await loadManagers()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to create manager.'
    }
}

const saveManager = async ({ formData, imageFile }) => {
    try {
        const manager = await updateManager(
            selectedManager.value.id,
            formData
        )

        if (imageFile) {
            await uploadManagerImage(manager.id, imageFile)
        }

        showEditManager.value = false
        selectedManager.value = null

        await loadManagers()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to update manager.'
    }
}

let searchTimeout = null

watch([search, sort, teamId, status], () => {
    currentPage.value = 1

    clearTimeout(searchTimeout)

    searchTimeout = setTimeout(() => {
        loadManagers()
    }, 500)
})

onMounted(() => {
    loadTeams()
    loadManagers()
})

onUnmounted(() => {
    clearTimeout(searchTimeout)
})
</script>

<template>
    <div>
        <div class="flex items-start justify-between gap-4">
            <div>
                <h2 class="text-2xl font-bold text-gray-900">
                    Managers
                </h2>

                <p class="mt-2 text-gray-600">
                    Manage your football managers.
                </p>
            </div>

            <button
                type="button"
                @click="showAddManager = true"
                class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
            >
                Add Manager
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
                <AppSearch
                    v-model="search"
                    placeholder="Search managers..."
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
                    v-model="status"
                    :options="[
                        { value: '', label: 'All Statuses' },
                        { value: 'Active', label: 'Active' },
                        { value: 'Inactive', label: 'Inactive' },
                    ]"
                    placeholder="Filter by status"
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
                    placeholder="Sort managers"
                />
            </div>
        </div>

        <div class="relative mt-6">
            <AppTable
                :columns="columns"
                :rows="managers"
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
                                Manager #{{ row.id }}
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
                        :total-rows="managers.length"
                        @view="openManager(row)"
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
            :open="showAddManager"
            title="Add Manager"
            description="Add a new football manager."
            @close="showAddManager = false"
        >
            <ManagerForm
                id="add-manager-form"
                :manager="null"
                @save="addManager"
            />

            <template #footer>
                <button
                    type="button"
                    class="rounded-lg border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                    @click="showAddManager = false"
                >
                    Cancel
                </button>

                <button
                    type="submit"
                    form="add-manager-form"
                    class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
                >
                    Add Manager
                </button>
            </template>
        </AppModal>

        <AppModal
            :open="showEditManager"
            title="Edit Manager"
            description="Update manager information."
            @close="showEditManager = false"
        >
            <ManagerForm
                id="edit-manager-form"
                :manager="selectedManager"
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

        <AppPagination
            :current-page="currentPage"
            :total-pages="totalPages"
            @update:current-page="handlePageChange"
        />
    </div>
</template>