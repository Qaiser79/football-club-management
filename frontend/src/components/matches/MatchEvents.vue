<script setup>
import { ref, onMounted } from 'vue'
import { getMatchEvents,createMatchEvent, deleteMatchEvent, updateMatchEvent } from '@/services/matchService'
import AppActionsMenue from '@/components/common/AppActionsMenu.vue'

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

const events = ref([])
const loading = ref(false)
const error = ref(null)
const selectedPlayerId = ref('')
const selectedEventType = ref('')
const eventMinute = ref('')
const saving = ref(false)
const saveError = ref(null)
const saveSuccess = ref(false)
const editingEventId = ref(null)
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
                event_type: selectedEventType.value,
                minute: eventMinute.value
                    ? Number(eventMinute.value)
                    : null,
            }
        )

        saveSuccess.value = true
        selectedPlayerId.value = ''
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
    editingEventId.value = event.id
    editPlayerId.value = event.player_id
    editEventType.value = event.event_type
    editEventMinute.value = event.minute ?? ''
    updateError.value = null
}

onMounted(()=>{
    loadEvents()
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
                                v-for="player in props.players.filter(
                                    player => props.squadPlayerIds.includes(player.id)
                                )"
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

                <div class="mt-4 flex justify-end">
                    <button
                        type="button"
                        class="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
                        :disabled="
                            saving ||
                            !selectedPlayerId ||
                            !selectedEventType
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
                        :row-index="index"
                        :total-rows="events.length"
                        @delete="deleteEvent(event.id)"
                    />
                </div>

            </div>

        </div>
    </div>
</template>