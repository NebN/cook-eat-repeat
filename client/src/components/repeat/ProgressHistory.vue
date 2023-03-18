<template>
    <DataTable 
      stripedRows
      v-model:expandedRows="expandedRows"
      v-model:selection="selectedDay"
      selectionMode="single"
      dataKey="day" 
      :value="mealStore.allProgress" 
      :rowClass="rowClass" 
      responsiveLayout="scroll">

    <template #header>
      Daily Intake
    </template>

    <Column expander style="width: 5rem" />

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

    <template #expansion="slotProps">
      <div v-if="slotProps.data.meals.length == 0">
        No meals eaten on {{slotProps.data.day}}
      </div>
      <div v-else>
        <DataTable 
        :value="slotProps.data.meals" 
        responsiveLayout="scroll">
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
      </div>
    </template>

  </DataTable>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useMealStore } from '@/script/stores/mealStore'

const mealStore = useMealStore()
const rowClass = ref(() => '')
const expandedRows = ref([])
const selectedDay = ref()

watch(selectedDay, (newValue, ) => {
  expandedRows.value = [newValue]
})

</script>

<style scoped>

</style>