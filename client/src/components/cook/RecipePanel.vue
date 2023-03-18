<template>
<div>
  <DataTable :value="recipeStore.currentIngredients" :rowClass="rowClass" responsiveLayout="scroll">
      
      <template #header>
          <div class="table-header">
              Recipe
          </div>
      </template>
      
      <Column header="Name">
        <template #body="slotProps">
            {{slotProps.data.label}}
        </template>
      </Column>
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
            {{slotProps.data.protein.toFixed(1)}}g
        </template>
      </Column>
      <Column header="Ratio">
        <template #body="slotProps">
            {{slotProps.data.ratio.toFixed(2)}}%
        </template>
      </Column>
      <Column>
        <template #body="slotProps">
            <div >
                <Button @click="deleteIngredient(slotProps.data)" icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger" style="float: right" />
                <Button @click="editIngredient(slotProps.data)" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-secondary" style="float: right" />
            </div>
        </template>
      </Column>

  </DataTable>
  <CookMealsPanel v-if="recipeStore.currentIngredients.length > 0"/>
</div>
</template>

<script setup>
import { ref } from 'vue'
import { useRecipeStore } from '@/script/stores/recipeStore'
import { useDialog } from 'primevue/usedialog'
import IngredientAmountForm from '@/components/cook/IngredientAmountForm'

const recipeStore = useRecipeStore()
const dialog = useDialog()

const rowClass = ref((rowIngredient) => {
  if (rowIngredient.per_meal) {
    return 'per-meal'
  }
})

const editIngredient = (ingredient) => {
  dialog.open(IngredientAmountForm, {
    props: {
      modal: true,
      header: ingredient.label,
      style: {
          width: '80%',
          maxWidth: '600px'
      },
      
    },
    data: {
      ingredient: ingredient,
    },
    onClose: (item) => {
      if (item.data != null) {
        const data = item.data
        ingredient.grams = data.grams
        ingredient.servings = data.servings
        ingredient.calories = data.calories
        ingredient.protein = data.protein
        ingredient.ratio = data.ratio
        ingredient.per_meal = data.per_meal
      }
    }
  })
}

const deleteIngredient = (ingredient) => {
    recipeStore.deleteIngredient(ingredient)
}

</script>

<style>
.per-meal {
  font-weight: bold;
  font-style: italic;
}
</style>