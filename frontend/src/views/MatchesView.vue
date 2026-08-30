<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import AppTable from '@/components/common/AppTable.vue'
import AppPagination from '@/components/common/AppPagination.vue'
import AppSearch from '@/components/common/AppSearch.vue'
import { getMatches, createMatch, updateMatch,deleteMatch } from '@/services/matchService'
import MatchForm from '@/components/matches/MatchForm.vue'
import AppModal from '@/components/common/AppModal.vue'
import AppActionsMenu from '@/components/common/AppActionsMenu.vue'


const columns = [
    { key: 'team.name', label: 'Our Team' },
    { key: 'opponent_name', label: 'Opponent' },
    { key: 'competition', label: 'Competition' },
    { key: 'match_date', label: 'Date' },
    { key: 'venue', label: 'Venue' },
    { key: 'score', label: 'Score' },
    { key: 'result', label: 'Result' },
    { key: 'status', label: 'Status' },
]

const statusClasses = {
    scheduled: 'bg-blue-50 text-blue-700',
    completed: 'bg-green-50 text-green-700',
    cancelled: 'bg-red-50 text-red-700',
    postponed: 'bg-yellow-50 text-yellow-700',
}

const formatStatus = (status) => {
    if (!status) {
        return '-'
    }

    return status.charAt(0).toUpperCase() + status.slice(1)
}

const matches = ref([])
const search = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const totalPages = ref(1)
const loading = ref(false)
const error = ref(null)
const showAddMatch = ref(false)
const showEditMatch = ref(false)
const selectedMatch = ref(null)

const loadMatches = async () => {
    loading.value = true
    error.value = null

    try {
        const data = await getMatches({
            page: currentPage.value,
            limit: pageSize.value,
            search: search.value,
        })

        matches.value = data.items
        totalPages.value = data.pages
    } catch(err) {
        console.error(err)
        error.value = 'Failed to load matches'
    } finally {
        loading.value = false
    }
}

const addMatch = async (formData) => {
    try {
        await createMatch(formData)

        showAddMatch.value = false
        currentPage.value = 1

        await loadMatches()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to create match'
    }
}

const editMatch = (match)=>{
    selectedMatch.value=match
    showEditMatch.value = true
}


const saveEditMatch = async (formData)=>{
    try {
         await updateMatch(selectedMatch.value.id, formData)

            showEditMatch.value = false
            selectedMatch.value = null

            await loadMatches()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to update match'
    }
}

const removeMatch = async (match) => {
    const confirmed = window.confirm(
        `Are you sure you want to delete the match against ${match.opponent_name}?`
    )

    if (!confirmed) {
        return
    }

    try {
        await deleteMatch(match.id)

        await loadMatches()
    } catch (err) {
        console.error(err)
        error.value = 'Failed to delete match'
    }
}

const handlePageChange = (page) => {
    currentPage.value = page
    loadMatches()
}

const getMatchResult = (match) => {
    if (match.status !== 'completed') {
        return null
    }

    if (match.our_score>match.opponent_score) {
        return 'win'
    }

    if (match.our_score < match.opponent_score) {
        return 'loss'
    }

    return 'draw'
}

const resultClasses = {
    win: 'bg-green-50 text-green-700',
    draw: 'bg-yellow-50 text-yellow-700',
    loss: 'bg-red-50 text-red-700',
}

const resultLabels = {
    win: 'Win',
    draw: 'Draw',
    loss: 'Loss',
}


let searchTimeout = null
watch(search, ()=> {
    clearTimeout(searchTimeout)

    searchTimeout = setTimeout(() => {
        currentPage.value = 1
        loadMatches()
    }, 500)
})

onMounted(() => {
    loadMatches()
})

onUnmounted(() => {
    clearTimeout(searchTimeout)
})

</script>

<template>
    <div>
        <div class="flex items-center justify-between">
            <div>
                <h2 class="text-2xl font-bold text-gray-900">
                    Matches
                </h2>

                <p class="mt-2 text-gray-600">
                    Manage matches.
                </p>
            </div>

            <button
                type="button"
                class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
                @click="showAddMatch = true"
            >
                Add Match
            </button>
        </div>

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
            Loading matches...
        </div>

        <div class="mt-6 max-w-sm">
            <AppSearch
                v-model="search"
                placeholder="Search matches..."
            />
        </div>

        <div class="mt-6">
            <AppTable
                :columns="columns"
                :rows="matches"
                :actions="true"
            >
                <!-- match score -->
                <template #cell-score="{ row }">
                    <span
                        v-if="row.our_score !== null && row.our_score !== undefined
                            && row.opponent_score !== null && row.opponent_score !== undefined"
                        class="font-semibold text-gray-900"
                    >
                        {{ row.our_score }} - {{ row.opponent_score }}
                    </span>

                    <span
                        v-else
                        class="text-gray-400"
                    >
                        -
                    </span>
                </template>

                <!-- match result -->
                 <template #cell-result="{row}">
                    <span
                        v-if="getMatchResult(row)"
                        class="inline-flex rounded-full px-2.5 py-1 text-xs font-medium"
                        :class="resultClasses[getMatchResult(row)]"
                    >
                        {{ resultLabels[getMatchResult(row)] }}
                    </span>

                    <span
                        v-else
                        class="text-gray-400"
                    >
                        —
                    </span>
                 </template>

                <!-- Status -->
                <template #cell-status="{ value }">
                    <span
                        class="inline-flex rounded-full px-2.5 py-1 text-xs font-medium"
                        :class="statusClasses[value] || 'bg-gray-100 text-gray-700'"
                    >
                        {{ formatStatus(value) }}
                    </span>
                </template>
                <template #actions="{ row, rowIndex, totalRows }">
                    <AppActionsMenu
                        :row-index="rowIndex"
                        :total-rows="totalRows"
                        @edit="editMatch(row)"
                        @delete="removeMatch(row)"
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
        :open="showAddMatch"
        title="Add Match"
        description="Register a new match."
        @close="showAddMatch = false"
    >
        <MatchForm
            id="add-match-form"
            @save="addMatch"
        />

        <template #footer>
            <button
                type="button"
                class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
                @click="showAddMatch = false"
            >
                Cancel
            </button>

            <button
                type="submit"
                form="add-match-form"
                class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white"
            >
                Add Match
            </button>
        </template>
    </AppModal>

    <AppModal
        :open="showEditMatch"
        title="Edit Match"
        description="Update match details."
        @close="showEditMatch = false"
    >
        <MatchForm
            v-if="selectedMatch"
            id="edit-match-form"
            :match="selectedMatch"
            @save="saveEditMatch"
        />

        <template #footer>
            <button
                type="button"
                class="rounded-lg px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
                @click="showEditMatch = false"
            >
                Cancel
            </button>

            <button
                type="submit"
                form="edit-match-form"
                class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white"
            >
                Save Changes
            </button>
        </template>
    </AppModal>

</template>