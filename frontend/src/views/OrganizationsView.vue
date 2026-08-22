<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import AppTable from '@/components/common/AppTable.vue'
import AppPagination from '@/components/common/AppPagination.vue'
import AppSearch from '@/components/common/AppSearch.vue'
import AppModal from '@/components/common/AppModal.vue'
import OrganizationForm from '@/components/organizations/OrganizationForm.vue'
import AppActionsMenu from '@/components/common/AppActionsMenu.vue'
import {
    getOrganizations,
    createOrganization,
    updateOrganization,
    deleteOrganization,
} from '@/services/organizationService'

const columns = [
    { key: 'name', label: 'Organization' },
]

const organizations = ref([])
const search = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const totalPages = ref(1)
const loading = ref(false)
const error = ref(null)
const showAddOrganization = ref(false)
const editingOrganization = ref(null)

const loadOrganizations = async () => {
    loading.value = true
    error.value = null

    try {
        const data = await getOrganizations({
            page: currentPage.value,
            limit: pageSize.value,
            name: search.value,
        })

        organizations.value = data.items
        totalPages.value = data.pages
    } catch (err) {
        console.error(err)
        error.value = 'Failed to load organizations'
    } finally {
        loading.value = false
    }
}

const addOrganization = async (formData) => {
    try {
        await createOrganization(formData)

        showAddOrganization.value = false
        currentPage.value = 1

        await loadOrganizations()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to create organization'
    }
}

const handlePageChange = (page) => {
    currentPage.value = page
    loadOrganizations()
}


const handleEdit = (organization) => {
    editingOrganization.value = { ...organization }
}

const saveOrganization = async (formData) => {
    try {
        await updateOrganization(
            editingOrganization.value.id,
            formData
        )

        editingOrganization.value = null

        await loadOrganizations()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to update organization'
    }
}

const handleDelete = async (organization) => {
    const confirmed = window.confirm(
        `Are you sure you want to delete ${organization.name}?`
    )

    if (!confirmed) {
        return
    }

    try {
        await deleteOrganization(organization.id)
        await loadOrganizations()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to delete organization'
    }
}


let searchTimeout = null

watch(search, () => {
    currentPage.value = 1

    clearTimeout(searchTimeout)

    searchTimeout = setTimeout(() => {
        loadOrganizations()
    }, 500)
})

onMounted(() => {
    loadOrganizations()
})

onUnmounted(() => {
    clearTimeout(searchTimeout)
})
</script>

<template>
    <div>
        <div class="flex items-center justify-between">
            <h2 class="text-2xl font-bold text-gray-900">
                Organizations
            </h2>

            <button
                type="button"
                class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
                @click="showAddOrganization = true"
            >
                Add Organization
            </button>
        </div>

        <p class="mt-2 text-gray-600">
            Manage organizations.
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
            Loading organizations...
        </div>

        <div class="mt-6 max-w-sm">
            <AppSearch
                v-model="search"
                placeholder="Search organizations..."
            />
        </div>

        <div class="mt-6">
            <AppTable
            :columns="columns"
            :rows="organizations"
            :actions="true"
        >
            <template #actions="{ row, rowIndex }">
                <AppActionsMenu
                    :row-index="rowIndex"
                    :total-rows="organizations.length"
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
        :open="showAddOrganization"
        title="Add Organization"
        description="Add a new organization."
        @close="showAddOrganization = false"
    >
        <OrganizationForm
            id="add-organization-form"
            @save="addOrganization"
        />

        <template #footer>
            <button
                type="button"
                class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
                @click="showAddOrganization = false"
            >
                Cancel
            </button>

            <button
                type="submit"
                form="add-organization-form"
                class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white"
            >
                Add Organization
            </button>
        </template>
    </AppModal>

    <AppModal
        :open="!!editingOrganization"
        title="Edit Organization"
        description="Update organization information."
        @close="editingOrganization = null"
    >
        <OrganizationForm
            id="edit-organization-form"
            :organization="editingOrganization"
            @save="saveOrganization"
        />

        <template #footer>
            <button
                type="button"
                class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
                @click="editingOrganization = null"
            >
                Cancel
            </button>

            <button
                type="submit"
                form="edit-organization-form"
                class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white"
            >
                Save
            </button>
        </template>
    </AppModal>

</template>