<template>
  <div >
    <DataTable 
    v-model:selection="selectedMeal" 
    @rowSelect="commitMeals"
    selectionMode="single" 
    dataKey="meals" 
    :value="mealsRows" 
    :scrollable="false"
    responsiveLayout="scroll">
        
        <template #header>
            <div class="table-header">
                Nutrients per Meal
            </div>
        </template>
        
        <Column header="Meals">
          <template #body="slotProps">
              {{slotProps.data.meals}}
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
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useDialog } from 'primevue/usedialog'
import { useRecipeStore } from '@/script/stores/recipeStore'
import CommitMealsForm from '@/components/cook/CommitMealsForm.vue'

const recipeStore = useRecipeStore()

const maxMeals = 20 // How to make this respond to scrolling :/

const mealsRows = computed(() => {
  const range = Array.from(Array(maxMeals + 1).keys())
  range.splice(0, 1)
  return range.map(n => {
    return {
      meals: n,
      calories: recipeStore.calories(n),
      protein: recipeStore.protein(n)
    }
  })
})

const selectedMeal = ref()

const dialog = useDialog()
const commitMeals = () => {
  dialog.open(CommitMealsForm, {
    props: {
      modal: true,
      header: selectedMeal.value.meals + ' meals',
      style: {
          width: '80%',
          maxWidth: '600px'
      },
      
    },
    data: {
      recipe: selectedMeal.value
    },
    onClose: () => {
    }
  })
}
</script>

<style scoped>

.p-datatable-wrapper {
  max-height: 25rem;
}

</style>