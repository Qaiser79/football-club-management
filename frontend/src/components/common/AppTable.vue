<script setup>
const props = defineProps({
    columns: {
        type: Array,
        default: ()=>[],
    },
    rows: {
        type: Array,
        default: () => [],
    },
})
</script>

<template>
    <div class="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm">
        <div class="overflow-x-auto">
            <table class="min-w-full">
                <thead class="border-b border-gray-200 bg-gray-50">
                    <tr>
                        <th
                            v-for="column in props.columns"
                            :key="column.key"
                            scope="col"
                            class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-gray-500"
                        >
                            {{ column.label }}
                        </th>
                    </tr>
                </thead>

                <tbody class="divide-y divide-gray-100">
                    <tr
                        v-for="(row, rowIndex) in props.rows"
                        :key="row.id ?? rowIndex"
                        class="transition-colors hover:bg-gray-50"
                    >
                        <td
                            v-for="column in props.columns"
                            :key="column.key"
                            class="whitespace-nowrap px-6 py-4 text-sm text-gray-700"
                            >
                            <slot
                                :name="`cell-${column.key}`"
                                :row="row"
                                :value="row[column.key]"
                            >
                                {{ row[column.key] }}
                            </slot>
                        </td>
                    </tr>

                    <tr v-if="props.rows.length === 0">
                        <td
                        :colspan="props.columns.length"
                        class="px-6 py-12 text-center"
                        >
                        <div class="text-sm font-medium text-gray-900">
                            No data found
                        </div>

                        <div class="mt-1 text-sm text-gray-500">
                            There are no records to display.
                        </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>