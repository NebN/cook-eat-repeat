<template>
    <DataTable 
      dataKey="day" 
      :value="mealStore.allProgress" 
      :rowClass="rowClass" 
      responsiveLayout="scroll">

    <template #header>
      Daily Intake
    </template>

    <Column header="Day">
      <template #body="slotProps">
          {{slotProps.data.day}}
      </template>
    </Column>

    <Column header="Calories">
      <template #body="slotProps">
          {{slotProps.data.calories.toFixed()}}
      </template>
    </Column>

    <Column header="Protein">
      <template #body="slotProps">
          {{slotProps.data.protein.toFixed(1)}}
      </template>
    </Column>

  </DataTable>
</template>

<script setup>
import { ref } from 'vue'
import { useMealStore } from '@/script/stores/mealStore'

const mealStore = useMealStore()
const rowClass = ref(() => '')
</script>

<style scoped>

</style>