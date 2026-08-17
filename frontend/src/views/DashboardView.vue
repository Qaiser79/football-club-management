<script setup>
import { ref } from 'vue'
import AppTable from '@/components/common/AppTable.vue'

const columns = [
    { key: 'name', label: 'Player' },
    { key: 'team', label: 'Team' },
    { key: 'position', label: 'Position' },
    { key: 'status', label: 'Status' },
]

const players1 = []

const players = [
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
]

</script>

<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900">
      Players
    </h2>

    <p class="mt-2 text-gray-600">
      Manage your football players.
    </p>

    <div class="mt-6">
        <AppTable
            :columns="columns"
            :rows="players"
            >
            <template #cell-name="{ row }">
                <div class="flex items-center gap-3">
                <div
                    class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-gray-900 text-sm font-semibold text-white"
                >
                    {{ row.name.charAt(0) }}
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
        </AppTable>
    </div>
</div>
</template>