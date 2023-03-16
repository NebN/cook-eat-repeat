<template>
  <DataTable 
    dataKey="day" 
    :value="mealStore.mealHistory" 
    :rowClass="rowClass" 
    responsiveLayout="scroll">

  <template #header>
    Meal History
  </template>

  <Column header="Cooked">
    <template #body="slotProps">
        {{formatEpoch(slotProps.data.time_created)}}
    </template>
  </Column>

  <Column header="Meal">
    <template #body="slotProps">
      {{slotProps.data.label}}
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

const dateTimeFormats = {
  day: new Intl.DateTimeFormat('en', {day: '2-digit'}),
  month: new Intl.DateTimeFormat('en', {month: '2-digit'}),
  year: new Intl.DateTimeFormat('en', {year: 'numeric'})
}

const formatEpoch = (epochSeconds) => {
  const date = new Date(Date.parse(epochSeconds))
  return [dateTimeFormats.year.format(date), dateTimeFormats.month.format(date), dateTimeFormats.day.format(date)].join('-')
}
</script>

<style scoped>

</style>