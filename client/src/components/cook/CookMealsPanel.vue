<template>
  <div>
    <DataTable 
    v-model:selection="selectedMeal" 
    @rowSelect="commitMeals"
    selectionMode="single" 
    dataKey="meals" 
    :value="mealsRows" 
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

const mealsRows = computed(() => {
  const oneToTen = Array.from(Array(11).keys())
  oneToTen.splice(0, 1)
  return oneToTen.map(n => {
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
      header: selectedMeal.value.meals + ' meals',
      style: {
          width: '80%',
          maxWidth: '600px'
      },
      
    },
    modal: true,
    data: {
      recipe: selectedMeal.value
    },
    onClose: () => {
    }
  })
}
</script>

<style scoped>

</style>