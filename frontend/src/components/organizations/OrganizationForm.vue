<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
    organization: {
        type: Object,
        default: null,
    },
})

const emit = defineEmits(['save'])

const name = ref('')

watch(
    () => props.organization,
    (organization) => {
        name.value = organization?.name ?? ''
    },
    { immediate: true }
)

const handleSubmit = () => {
    emit('save', {
        name: name.value,
    })
}
</script>

<template>
    <form
        :id="$attrs.id"
        @submit.prevent="handleSubmit"
        class="space-y-4"
    >
        <div>
            <label
                for="organization-name"
                class="block text-sm font-medium text-gray-700"
            >
                Organization Name
            </label>

            <input
                id="organization-name"
                v-model="name"
                type="text"
                required
                minlength="2"
                maxlength="100"
                class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-gray-500 focus:outline-none"
                placeholder="Enter organization name"
            />
        </div>
    </form>
</template>