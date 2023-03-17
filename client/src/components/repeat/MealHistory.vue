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

  <Column header="">
    <template #body="slotProps">
        <Button 
        @click="repeatRecipe(slotProps.data)"
        class="p-button-outlined p-button-secondary" 
        icon="pi pi-replay" 
        style="margin-right: 0.5rem"/>
        <Button @click="toggleFavourite(slotProps.data)" 
        :icon="favouriteIcon(slotProps.data)" 
        class="p-button-raised p-button-secondary" />
    </template>
  </Column>

</DataTable>
</template>

<script setup>
import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useMealStore } from '@/script/stores/mealStore'
import { useRecipeStore } from '@/script/stores/recipeStore'
import axios from 'axios'
import router from '@/main'

const toast = useToast()
const mealStore = useMealStore()
const recipeStore = useRecipeStore()
const rowClass = ref(() => '')

const favouriteIcon = (data) => data == null || data.favourite == null ? 'pi pi-spin pi-spinner' : data.favourite ? 'pi pi-heart-fill' : 'pi pi-heart'

const dateTimeFormats = {
  day: new Intl.DateTimeFormat('en', {day: '2-digit'}),
  month: new Intl.DateTimeFormat('en', {month: '2-digit'}),
  year: new Intl.DateTimeFormat('en', {year: 'numeric'})
}

const formatEpoch = (epochSeconds) => {
  const date = new Date(Date.parse(epochSeconds))
  return [dateTimeFormats.year.format(date), dateTimeFormats.month.format(date), dateTimeFormats.day.format(date)].join('-')
}

const repeatRecipe = (recipe) => {
  recipeStore.startNewRecipe(recipe.label)
  recipe.ingredients.forEach(i => {
    const ingredient = i[0]
    const amount = i[1]
    recipeStore.addIngredient({
      ...ingredient,
      ...amount,
      ratio: (ingredient.protein / ingredient.calories) * 25 // 4 calories for 1 protein (100/4=25)
    })
  })
  router.push('/cook')
}

const toggleFavourite = async (data) => {
  const oldValue = data.favourite || false

  // trigger loading animation
  data.favourite = null

  try {
    const response = await axios({
      method: 'post',
      url: '/api/meal/favourite',
      data: {
        id: data.id
      }
    })

    data.favourite = response.data['newFavourite']
  } catch (error) {
    toast.add({severity:'error', summary: 'Error!', detail: 'Unable to update favourite 😢. Please try again later.', life: 3000})
    console.log(error)
    data.favourite = oldValue
  }
}

</script>

<style scoped>

</style>