<script setup>
import { ref, onMounted, computed } from 'vue'
import { getMatchEvents,createMatchEvent, deleteMatchEvent, updateMatchEvent, getMatchSquad } from '@/services/matchService'
import AppActionsMenue from '@/components/common/AppActionsMenu.vue'
import AppModal from '@/components/common/AppModal.vue'

const props = defineProps({
    matchId: {
        type: Number,
        required: true,
    },
    squadPlayerIds: {
        type: Array,
        default: () => [],
    },
    players: {
        type: Array,
        default: () => [],
    },
    matchStatus: {
        type: String,
        default: '',
    },
})

const squadPlayers = computed(() => {
    return props.players.filter(
        player => props.squadPlayerIds.includes(Number(player.id))
    )
})

const substitutionPlayersIn = computed(() => {
    return squadPlayers.value.filter(
        player => !selectedPlayerId.value ||
        Number(player.id) !== Number(selectedPlayerId.value)
    )
})


const events = ref([])
const loading = ref(false)
const squad = ref([])
const squadLoading = ref(false)

const error = ref(null)
const selectedPlayerId = ref('')
const selectedRelatedPlayerId = ref('')
const selectedEventType = ref('')
const eventMinute = ref('')

const saving = ref(false)
const saveError = ref(null)
const saveSuccess = ref(false)
const editingEvent = ref(null)
const editPlayerId = ref('')
const editEventType = ref('')
const editEventMinute = ref('')
const updating = ref(false)
const updateError = ref(null)

const eventLabels = {
    goal: 'Goal',
    assist: 'Assist',
    yellow_card: 'Yellow Card',
    red_card: 'Red Card',
    foul: 'Foul',
    substitution: 'Substitution',
}


const eventTypes = [
    { value: 'goal', label: 'Goal' },
    { value: 'assist', label: 'Assist' },
    { value: 'yellow_card', label: 'Yellow Card' },
    { value: 'red_card', label: 'Red Card' },
    { value: 'foul', label: 'Foul' },
    { value: 'substitution', label: 'Substitution' },
]

const loadEvents = async () => {
    loading.value=true
    error.value=null

    try {
        events.value = await getMatchEvents(props.matchId)
    } catch (err) {
        console.error(err)
        error.value="Failed to load match events"
    } finally {
        loading.value = false
    }
}

const loadSquad= async () => {
    squadLoading.value = true

    try {
        const data = await getMatchSquad(props.matchId)

        squad.value = data.players
    } catch (err) {
        console.error(err)
    } finally {
        squadLoading.value = false
    }
}

const currentOnFieldPlayerIds = computed(()=>{
    const onField = new Set()
    squad.value.forEach(player=> {
        if (player.is_starter) {
            onField.add(Number(player.player_id))
        }
    })

    events.value
        .filter(event=> event.event_type === 'substitution')
        .sort((a,b)=>{
            const minuteA = a.minute ?? 0
            const minuteB = b.minute ?? 0

            if (minuteA !== minuteB) {
                return minuteA - minuteB
            }
            return a.id-b.id
        })
        .forEach(event => {
            onField.delete(Number(event.player_id))
            if (event.related_player_id !== null){
                onField.add(Number(event.related_player_id))
            }
        })

        return onField
})

const playerOut = computed(() => {
    return squadPlayers.value.filter(
        player => currentOnFieldPlayerIds.value.has(Number(player.id))
    )
})

const playersIn = computed(()=>{
    return squadPlayers.value.filter(
        player => !currentOnFieldPlayerIds.value.has(Number(player.id))
    )
})


const emit = defineEmits(['event-created'])

const addEvent = async () => {
    saving.value = true
    saveError.value = null
    saveSuccess.value=false

    try {
        await createMatchEvent(
            props.matchId,
            {
                player_id: Number(selectedPlayerId.value),
                related_player_id: selectedRelatedPlayerId.value
                ? Number(selectedRelatedPlayerId.value)
                : null,
                event_type: selectedEventType.value,
                minute: eventMinute.value
                    ? Number(eventMinute.value)
                    : null,
            }
        )

        saveSuccess.value = true
        selectedPlayerId.value = ''
        selectedRelatedPlayerId.value = ''
        eventMinute.value = ''

        await loadEvents()
        emit('event-created')
    } catch (err) {
        console.error(err)
        saveError.value = 'Failed to add event'
    } finally {
        saving.value = false
    }
}

const deleteEvent = async (eventId) => {
    try {
        await deleteMatchEvent(
            props.matchId,
            eventId
        )

        await loadEvents()

        emit('event-created')
    } catch (err) {
        console.error(err)
        saveError.value = 'Failed to delete event'
    }
}

const startEdit = (event) => {
    editingEvent.value = event
    editPlayerId.value = event.player_id
    editEventType.value = event.event_type
    editEventMinute.value = event.minute ?? ''
    updateError.value = null
}

const cancelEdit = () => {
    editingEvent.value = null
    editPlayerId.value = ''
    editEventType.value = ''
    editEventMinute.value = ''
    updateError.value = null
}

const updateEvent = async () => {
    if (!editingEvent.value) {
        return
    }

    updating.value = true
    updateError.value = null

    try {
        await updateMatchEvent(
            props.matchId,
            editingEvent.value.id,
            {
                player_id: Number(editPlayerId.value),
                event_type: editEventType.value,
                minute: editEventMinute.value
                    ? Number(editEventMinute.value)
                    : null,
            }
        )

        await loadEvents()

        cancelEdit()

        emit('event-created')
    } catch (err) {
        console.error(err)
        updateError.value = 'Failed to update event'
    } finally {
        updating.value = false
    }
}

onMounted(async ()=>{
    await loadSquad()
    await loadEvents()
})



</script>




<template>
    <div class="mt-6">
        <div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">

            <h3 class="text-lg font-semibold text-gray-900">
                Match Events
            </h3>

            <div
                v-if="props.matchStatus?.toLowerCase() === 'live'"
                class="mt-6 rounded-lg border border-gray-200 bg-gray-50 p-4"
            >

                <h4 class="text-sm font-semibold text-gray-900">
                    Add Event
                </h4>

                <div class="mt-4 grid gap-4 sm:grid-cols-3">

                    <div>
                        <label class="block text-sm font-medium text-gray-700">
                            Player
                        </label>

                        <select
                            v-model="selectedPlayerId"
                            class="mt-1 w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm"
                        >
                            <option value="" disabled>
                                Select player
                            </option>

                            <option
                                v-for="player in squadPlayers"
                                :key="player.id"
                                :value="player.id"
                            >
                                {{ player.name }}
                            </option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700">
                            Event Type
                        </label>

                        <select
                            v-model="selectedEventType"
                            class="mt-1 w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm"
                        >
                            <option value="" disabled>
                                Select event
                            </option>

                            <option
                                v-for="eventType in eventTypes"
                                :key="eventType.value"
                                :value="eventType.value"
                            >
                                {{ eventType.label }}
                            </option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700">
                            Minute
                        </label>

                        <input
                            v-model="eventMinute"
                            type="number"
                            min="1"
                            placeholder="e.g. 37"
                            class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
                        />
                    </div>

                </div>

                <div v-if="selectedEventType === 'substitution'">
                    <label class="block text-sm font-medium text-gray-700">
                        Player In
                    </label>

                    <select
                        v-model="selectedRelatedPlayerId"
                        class="mt-1 w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm"
                    >
                        <option value="" disabled>
                            Select player
                        </option>

                        <option
                            v-for="player in substitutionPlayersIn"
                            :key="player.id"
                            :value="player.id"
                        >
                            {{ player.name }}
                        </option>
                    </select>
                </div>

                <div class="mt-4 flex justify-end">
                    <button
                        type="button"
                        class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
                        :disabled="
                            saving ||
                            !selectedPlayerId ||
                            !selectedEventType ||
                            (selectedEventType === 'substitution' && !selectedRelatedPlayerId)
                        "
                        @click="addEvent"
                    >
                        {{ saving ? 'Adding...' : 'Add Event' }}
                    </button>
                </div>

                <p
                    v-if="saveSuccess"
                    class="mt-3 text-sm text-green-600"
                >
                    Event added successfully.
                </p>

                <p
                    v-if="saveError"
                    class="mt-3 text-sm text-red-600"
                >
                    {{ saveError }}
                </p>
            </div>


            <div
                v-if="loading"
                class="mt-4 text-sm text-gray-500"
            >
                Loading events...
            </div>

            <div
                v-else-if="error"
                class="mt-4 rounded-lg bg-red-50 p-4 text-sm text-red-700"
            >
                {{ error }}
            </div>

            <div
                v-else-if="events.length === 0"
                class="mt-4 text-sm text-gray-500"
            >
                No events recorded for this match.
            </div>

            <div
                v-else
                class="mt-4 space-y-3"
            >
                <div
                    v-for="(event, index) in events"
                    :key="event.id"
                    class="flex items-center gap-4 rounded-lg border border-gray-200 p-4"
                >
                    <div class="w-12 text-sm font-semibold text-gray-700">
                        {{ event.minute ? `${event.minute}'` : '-' }}
                    </div>

                    <div class="flex-1">
                        <p class="font-medium text-gray-900">
                            {{ event.player.name }}
                        </p>

                        <p class="mt-1 text-sm text-gray-500">
                            {{ eventLabels[event.event_type] || event.event_type }}
                        </p>
                        
                    </div>

                    <AppActionsMenue
                        v-if="props.matchStatus?.toLocaleLowerCase()==='live'"
                        :row-index="index"
                        :total-rows="events.length"
                        @edit="startEdit(event)"
                        @delete="deleteEvent(event.id)"
                    />
                </div>

            </div>

        </div>
    </div>

    <AppModal
        :open="!!editingEvent"
        title="Edit Match Event"
        description="Update the event details"
        @close="cancelEdit"
    >
        <div class="space-y-4">

            <div>
                <label class="block text-sm font-medium text-gray-700">
                    Player
                </label>

                <select
                    v-model="editPlayerId"
                    class="mt-1 w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm"
                >
                    <option
                        v-for="player in squadPlayers"
                        :key="player.id"
                        :value="player.id"
                    >
                        {{ player.name }}
                    </option>
                </select>
            </div>

            <div>
                <label class="block text-sm font-medium text-gray-700">
                    Event Type
                </label>

                <select
                    v-model="editEventType"
                    class="mt-1 w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm"
                >
                    <option
                        v-for="eventType in eventTypes"
                        :key="eventType.value"
                        :value="eventType.value"
                    >
                        {{ eventType.label }}
                    </option>
                </select>
            </div>

            <div>
                <label class="block text-sm font-medium text-gray-700">
                    Minute
                </label>

                <input
                    v-model="editEventMinute"
                    type="number"
                    min="1"
                    class="mt-1 w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm"
                />
            </div>

            <p
                v-if="updateError"
                class="text-sm text-red-600"
            >
                {{ updateError }}
            </p>

        </div>

        <template #footer>
            <button
                type="button"
                class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                @click="cancelEdit"
            >
                Cancel
            </button>

            <button
                type="button"
                class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
                :disabled="updating"
                @click="updateEvent"
            >
                {{ updating ? 'Saving...' : 'Save' }}
            </button>
        </template>
    </AppModal>

</template>