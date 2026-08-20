<script setup>
import { ref, onMounted,watch, onUnmounted } from 'vue'
import AppTable from '@/components/common/AppTable.vue'
import AppPagination from '@/components/common/AppPagination.vue'
import { getPlayers,deletePlayer,updatePlayer,createPlayer } from '@/services/playerService'
import AppModal from '@/components/common/AppModal.vue'
import PlayerForm from '@/components/players/PlayerForm.vue'
import AppActionsMenu from '@/components/common/AppActionsMenu.vue'
import AppSearch from '@/components/common/AppSearch.vue'

const columns = [
    { key: 'name', label: 'Player' },
    { key: 'team', label: 'Team' },
    { key: 'position', label: 'Position' },
    { key: 'status', label: 'Status' },
]

const players = ref([])
const currentPage = ref(1)
const pageSize = ref(2)
const totalPages = ref(1)
const loading = ref(false)
const error = ref(null)
const editingPlayer = ref(null)
const showAddPlayer = ref(false)
const search = ref('')

const loadPlayers = async () => {
    loading.value = true
    error.value = null

    try {
        const data = await getPlayers({
            page: currentPage.value,
            limit: pageSize.value,
            name: search.value
        })

        players.value = data.items
        totalPages.value = data.pages
    } catch (err) {
        console.error(err)
        error.value = 'Failed to load players.'
    } finally {
        loading.value = false
    }
}

const handlePageChange = (page) => {
    currentPage.value = page
    loadPlayers()
}

const handleDelete = async (player) => {
    const confirmed = window.confirm(
        `Are you sure you want to delete ${player.name}?`
    )
    if (!confirmed) {
        return
    }

    try {
        await deletePlayer(player.id)
        
        await loadPlayers()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to delete player.'
    }
}

const handleEdit = (player) => {
    editingPlayer.value = { ...player }
}

const savePlayer = async (formData) => {
    try {
        await updatePlayer(
            editingPlayer.value.id,
            formData
        )

        editingPlayer.value = null

        await loadPlayers()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to update player.'
    }
}



const addPlayer = async (formData) => {
    try {
        await createPlayer(formData)

        showAddPlayer.value = false
        currentPage.value = 1

        await loadPlayers()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to create player.'
    }
}

let searchTimeout = null
watch(search, ()=>{
    currentPage.value = 1
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(()=>{
         loadPlayers()
}, 500)
   
})

onUnmounted(()=>{
    clearTimeout(searchTimeout)
})

onMounted(() => {
    loadPlayers()
})
</script>

<template>
    <div>
        <div class="flex items-start justify-between gap-4">
            <div>
                <h2 class="text-2xl font-bold text-gray-900">
                    Players
                </h2>

                <p class="mt-2 text-gray-600">
                    Manage your football players.
                </p>
            </div>
            <button
                type="button"
                class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
                @click="showAddPlayer=true"
            >
                Add Player
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
                placeholder="Search players..."
            />
        </div>

        
        <div class="relative mt-6">
            <AppTable
                :columns="columns"
                :rows="players"
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
                                Player #{{ row.id }}
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
                        :total-rows="players.length"
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
                :open="!!editingPlayer"
                title="Edit Player"
                description="Update player information."
                @close="editingPlayer = null"
            >
                <PlayerForm
                    id="player-form"
                    :player="editingPlayer"
                    @save="savePlayer"
                />

                <template #footer>
                    <button
                        type="button"
                        class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
                        @click="editingPlayer = null"
                    >
                        Cancel
                    </button>

                    <button
                        type="submit"
                        form="player-form"
                        class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
                    >
                        Save
                    </button>
                </template>
            </AppModal>

            <AppModal
                :open="showAddPlayer"
                title="Add Player"
                description="Add a new football player."
                @close="showAddPlayer = false"
            >
                <PlayerForm
                    id="add-player-form"
                    :player="null"
                    @save="addPlayer"
                />

                <template #footer>
                    <button
                        type="button"
                        class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
                        @click="showAddPlayer = false"
                    >
                        Cancel
                    </button>

                    <button
                        type="submit"
                        form="add-player-form"
                        class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
                    >
                        Add Player
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