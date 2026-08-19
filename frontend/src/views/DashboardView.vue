<script setup>
import { ref, computed } from 'vue'
import AppTable from '@/components/common/AppTable.vue'
import AppModal from '@/components/common/AppModal.vue'
import PlayerForm from '@/components/players/PlayerForm.vue'
import AppPagination from '@/components/common/AppPagination.vue'

const columns = [
    { key: 'name', label: 'Player' },
    { key: 'team', label: 'Team' },
    { key: 'position', label: 'Position' },
    { key: 'status', label: 'Status' },
]


const players = ref([
    {
    id: 1,
    name: 'Marcus Rashford',
    team: 'Manchester United',
    position: 'Forward',
    status: 'Active',
  },
  {
    id: 2,
    name: 'Bukayo Saka',
    team: 'Arsenal',
    position: 'Winger',
    status: 'Active',
  },
  {
    id: 3,
    name: 'Mohamed Salah',
    team: 'Liverpool',
    position: 'Forward',
    status: 'Injured',
  },
  {
    id: 4,
    name: 'Jude Bellingham',
    team: 'Real Madrid',
    position: 'Midfielder',
    status: 'Active',
  },
])

const currentPage=ref(1)
const pageSize=2

const totalPages= computed(() => {
    return Math.ceil(players.value.length/pageSize)
})
const paginatedPlayers = computed(() => {
    const start = (currentPage.value - 1) * pageSize

    return players.value.slice(start, start + pageSize)
})

const openActionId = ref(null)
const editingPlayer = ref(null)
const showAddPlayer = ref(false)


const handleAction = (action, row) => {
    if (action === 'delete') {
        const confirmed = window.confirm(
            `Are you sure you want to delete ${row.name}?`
        )

        if (!confirmed) {
            return
        }

        players.value = players.value.filter(
            player => player.id !== row.id
        )
    }
    if (action === 'edit') {
        editingPlayer.value = { ...row }
    }

    openActionId.value = null
}


const savePlayer = (formData) => {
    const index = players.value.findIndex(
        player => player.id === editingPlayer.value.id
    )

    if (index === -1) {
        return
    }

    players.value[index] = { 
        ...editingPlayer.value,
        ...formData
     }

    editingPlayer.value = null
}

const addPlayer = (formData) => {
    const nextId = players.value.length
        ? Math.max(...players.value.map(player => player.id)) + 1
        : 1

    players.value.push({
        id: nextId,
        ...formData,
    })

    showAddPlayer.value = false
}

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
            class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-gray-800"
            @click="showAddPlayer = true"
        >
            Add Player
        </button>
    </div>

    <div class="mt-6">
        <AppTable
            :columns="columns"
            :rows="paginatedPlayers"
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
                <div class="relative flex justify-end">
                    <button
                        type="button"
                        class="rounded-lg p-2 text-gray-500 transition-colors hover:bg-gray-100 hover:text-gray-900"
                        :aria-label="`Actions for ${row.name}`"
                        @click="openActionId = openActionId === row.id ? null : row.id"
                    >
                        ⋮
                    </button>

                    <div
                        v-if="openActionId === row.id"
                        :class="[
                            'absolute right-0 z-10 w-32 rounded-lg border border-gray-200 bg-white py-1 shadow-lg',
                            rowIndex === players.length - 1 ? 'bottom-10' : 'top-10'
                        ]"
                    >
                        <button
                            type="button"
                            class="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50"
                            @click="handleAction('edit', row)"
                            >
                            Edit
                        </button>

                        <button
                            type="button"
                            class="block w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50"
                            @click="handleAction('delete', row)"
                            >
                            Delete
                        </button>
                    </div>
                </div>
            </template>

        </AppTable>
        <AppPagination
            v-model:currentPage="currentPage"
            :total-pages="totalPages"
        />
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


    </div>
</div>
</template>