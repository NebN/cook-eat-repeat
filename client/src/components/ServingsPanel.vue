<template>
  <div>
    <DataTable 
    v-model:selection="selectedServing" 
    @rowSelect="commitServings"
    selectionMode="single" 
    dataKey="id" 
    :value="servingsRows" 
    responsiveLayout="scroll">
        
        <template #header>
            <div class="table-header">
                Nutrients per serving
            </div>
        </template>
        
        <Column header="Servings">
          <template #body="slotProps">
              {{slotProps.data.servings}}
          </template>
        </Column>
        <Column header="Calories">
          <template #body="slotProps">
              {{slotProps.data.calories.toFixed(1)}}
          </template>
        </Column>
        <Column header="Protein">
          <template #body="slotProps">
              {{slotProps.data.protein.toFixed(1)}}g
          </template>
        </Column>
    </DataTable>
    <Toast position="center" />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useDialog } from 'primevue/usedialog'
import { useRecipeStore } from '../script/stores/recipeStore'
import CommitServingsForm from './CommitServingsForm.vue'

const recipeStore = useRecipeStore()

const servingsRows = computed(() => {
  const totalCalories = recipeStore.totalCalories
  const totalProtein = recipeStore.totalProtein

  if (totalCalories == 0) {
    return []
  }
  const oneToTen = Array.from(Array(11).keys())
  oneToTen.splice(0, 1)
  return oneToTen.map(n => {
    return {
      servings: n,
      calories: totalCalories / n,
      protein: totalProtein / n
    }
  })
})

const selectedServing = ref()

const dialog = useDialog()
const commitServings = () => {
  console.log(selectedServing.value)
  dialog.open(CommitServingsForm, {
    props: {
      header: selectedServing.value.servings + ' servings',
      style: {
          width: '80%',
          maxWidth: '600px'
      },
      
    },
    modal: true,
    data: {
      recipe: selectedServing.value
    },
    onClose: async () => {
    }
  })
}
</script>

<style scoped>

</style>