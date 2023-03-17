<template>
  <div class="card">
    <div v-if="recipe != null">Each one for {{recipe.calories.toFixed()}} calories and {{recipe.protein.toFixed(1)}} protein.</div>
    <div class="input-block">
      <span class="p-float-label">
        <InputText id="label" type="text" v-model="label" />
        <label for="label">Meal name</label>
      </span>

    </div>
    <ConfirmOrCancel v-if="label != null && label.length > 0" @confirm="confirmCommit" @cancel="cancelCommit"/>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { useToast } from 'primevue/usetoast'
import axios from 'axios'
import { useRecipeStore } from '@/script/stores/recipeStore'

const recipeStore = useRecipeStore()

const dialogRef = inject('dialogRef')
const recipe = ref()
const label = ref()


onMounted(() => {
    recipe.value = dialogRef.value.data.recipe
})

const toast = useToast()

const confirmCommit = async () => {
  try {
    await axios({
      method: 'post',
      url: '/api/meal',
      data: ({
        label: label.value || null,
        calories: recipe.value.calories,
        protein: recipe.value.protein,
        meals_created: recipe.value.meals,
        ingredients: recipeStore.currentIngredients
      })
    })
    toast.add({severity:'success', summary: 'Saved!', detail:'Meals have been saved.', life: 3000})
    recipeStore.startNewRecipe()
    dialogRef.value.close()
  } catch (error) {
    toast.add({severity:'error', summary: 'Error!', detail:'Unable to save meal 😢. Try again later.', life: 3000})
  }
}

const cancelCommit = () => {
    dialogRef.value.close()
}
</script>

<style scoped>
.input-block {
  margin-top: 2rem;
  margin-bottom: 1rem;
  width: 100%;
  margin-left: 0.2rem;
  margin-right: 0.2rem;
}
.p-inputtext {
  width: 100%
}
.p-inputgroup {
  width: 100%
}
</style>