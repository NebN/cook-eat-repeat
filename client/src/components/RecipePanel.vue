<template>
<div>
  <DataTable :value="recipeStore.currentIngredients.concat([totalsRow])" responsiveLayout="scroll">
      
      <template #header>
          <div class="table-header">
              Recipe
          </div>
      </template>
      
      <Column field="label" header="Name"></Column>
      <Column header="Amount">
        <template #body="slotProps">
            {{slotProps.data.grams.toFixed()}}g{{slotProps.data.portions != null ? ' ('+slotProps.data.portions+')' : ''}}
        </template>
      </Column>
      <Column header="Calories">
        <template #body="slotProps">
            {{slotProps.data.calories.toFixed()}}
        </template>
      </Column>
      <Column header="Protein">
        <template #body="slotProps">
            {{slotProps.data.protein.toFixed()}}g
        </template>
      </Column>
      <Column header="Ratio">
        <template #body="slotProps">
            {{slotProps.data.ratio.toFixed(2)}}%
        </template>
      </Column>
      <Column>
        <template #body="slotProps">
            <div v-if="slotProps.data.id != null">
                <Button @click="deleteIngredient(slotProps.data)" icon="pi pi-trash" class="p-button-rounded p-button-secondary p-button-text p-button-danger" style="float: right" />
                <Button @click="editIngredient(slotProps.data)" icon="pi pi-pencil" class="p-button-rounded p-button-secondary p-button-text p-button-secondary" style="float: right" />
            </div>
        </template>
      </Column>

  </DataTable>
  <ServingsPanel/>
</div>
</template>

<script setup>
import { computed } from 'vue'
import { useRecipeStore } from '../script/stores/recipeStore'
import { useDialog } from 'primevue/usedialog'
import RecipeIngredientForm from './RecipeIngredientForm'

const recipeStore = useRecipeStore()
const totalsRow = computed(() => {
    return {
        label: 'Total',
        grams: recipeStore.totalGrams,
        calories: recipeStore.totalCalories,
        protein: recipeStore.totalProtein,
        ratio: recipeStore.averageRatio
    }
})
const dialog = useDialog()
const editIngredient = (ingredient) => {
  dialog.open(RecipeIngredientForm, {
    props: {
      header: ingredient.label,
      style: {
          width: '80%',
          maxWidth: '600px'
      },
      
    },
    modal: true,
    data: {
      item: ingredient,
    },
    onClose: () => {
     
    }
  })
}

const deleteIngredient = (ingredient) => {
    recipeStore.deleteIngredient(ingredient)
}

</script>

<style scoped>
.p-button {
  margin-left: .5rem;
}
</style>