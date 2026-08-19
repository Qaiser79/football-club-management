<script setup>
import { reactive, watch } from 'vue'
import AppInput from '@/components/common/AppInput.vue'
import AppSelect from '@/components/common/AppSelect.vue'

const props = defineProps({
    player: {
        type: Object,
        default: null,
    },

    id: {
        type: String,
        default: 'player-form'
    },
})

const emit = defineEmits(['save'])

const statusOptions = [
    { value: 'Active', label: 'Active' },
    { value: 'Injured', label: 'Injured' },
]

const form = reactive({
    name: '',
    team: '',
    position: '',
    status: 'Active',
})

watch(
    () => props.player,
    (player) => {
        form.name = player?.name ?? ''
        form.team = player?.team ?? ''
        form.position = player?.position ?? ''
        form.status = player?.status ?? 'Active'
    },
    {immediate: true}
)

const save = () => {
    emit('save', {
        ...form
    })
}

</script>

<template>
    <form
        :id="props.id"
        class="space-y-4"
        @submit.prevent="save"
    >
            <div>
                <label class="text-sm font-medium text-gray-700">
                    Name
                </label>

                <AppInput
                    v-model="form.name"
                    placeholder="Player name"
                />
            </div>

            <div>
                <label class="text-sm font-medium text-gray-700">
                    Team
                </label>

                <AppInput
                    v-model="form.team"
                    placeholder="Team"
                />
            </div>

            <div>
                <label class="text-sm font-medium text-gray-700">
                    Position
                </label>

                <AppInput
                    v-model="form.position"
                    placeholder="Position"
                />
            </div>

            <div>
                <label class="text-sm font-medium text-gray-700">
                    Status
                </label>
                <AppSelect
                v-model="form.status"
                :options="statusOptions"
                placeholder="Select status"
                />
            </div>
            <button
                type="submit"
                class="hidden"
            >
                Save
            </button>
        </form>
</template>
