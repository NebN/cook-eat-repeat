<template>
<div>
  <div class="quantity-input">
    <SelectButton v-model="ingredientStore.selectedInputMode" :options="ingredientStore.quantityInputModes" optionLabel="name" :unselectable="false" :disabled="ingredientStore.selectedIngredient.serving_size == null"/>
    <InputText @focus="$event.target.select()" type="number" v-model="ingredientStore.quantity" />
  </div>
  <div v-if="ingredientStore.quantity > 0">
    <Divider align="left">
  <div v-if="ingredientStore.totalGrams != null" class="inline-flex align-items-center">
    <b>Total for {{ingredientStore.totalGrams}} grams</b>
  </div>
  </Divider>
    <div v-if="ingredientStore.computedCalories != null">{{ ingredientStore.computedCalories.toFixed() }} calories</div>
    <div v-if="ingredientStore.computedProtein != null">{{ ingredientStore.computedProtein.toFixed() }} protein</div>
  </div>
</div>
</template>

<script setup>
import { useIngredientStore } from '../script/stores/ingredientStore'

const ingredientStore = useIngredientStore()
</script>

<style scoped>

</style>