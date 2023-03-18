<template>
<div>
  <div class="quantity-input">
    <SelectButton v-model="selectedInputMode" :options="quantityInputModes" :unselectable="false" :disabled="ingredient.serving_size == null"/>
    <InputText @keyup.enter="quantity > 0 ? confirm() : null" type="number" v-model="quantity" style="margin-top: 0.5rem" autofocus/>
    <SelectButton v-model="selectedAddMode" :options="addModes" :unselectable="false" style="margin-top: .5rem" />
  </div>
  <div v-if="computedGrams >= 0">
    <Divider >
      <div  class="inline-flex align-items-center">
        <b>Total for {{computedGrams}} grams</b>
      </div>
    </Divider>
    <div v-if="computedCalories != null">{{ computedCalories.toFixed() }} calories</div>
    <div v-if="computedProtein != null">{{ computedProtein.toFixed(1) }} protein</div>
    <ConfirmOrCancel v-if="computedGrams > 0" @confirm="confirm" @cancel="cancel"/>
  </div>
</div>
</template>

<script setup>
import { ref, computed, inject, onMounted } from 'vue'

const dialogRef = inject('dialogRef')
const ingredient = ref({})
const quantity = ref()
const quantityInputModes = ref(['grams', 'servings'])
const selectedInputMode = ref(quantityInputModes.value[0])
const addModes = ref(['In total','For each meal'])
const selectedAddMode = ref(addModes.value[0])
let caloriesPer1Gram = 0
let proteinPer1Gram = 0

onMounted(() => {
  quantity.value = null



  const inputIngredient = dialogRef.value.data.ingredient
  ingredient.value = inputIngredient

  const inputIngredientGrams = parseFloat(inputIngredient.grams) || 100
  caloriesPer1Gram = parseFloat(inputIngredient.calories) / inputIngredientGrams
  proteinPer1Gram = parseFloat(inputIngredient.protein) / inputIngredientGrams

  if (inputIngredient.per_meal) {
    selectedAddMode.value = addModes.value[1]
  }

  if (inputIngredient.servings != null) {
    selectedInputMode.value = quantityInputModes.value[1]
    quantity.value = inputIngredient.servings
  } else if (inputIngredient.grams != null) {
    quantity.value = inputIngredient.grams
  }
})

const confirm = () => {
  dialogRef.value.close({
    calories: computedCalories.value,
    protein: computedProtein.value,
    grams: computedGrams.value,
    servings: servings(),
    ratio: ratio(),
    per_meal: per_meal()
  })
}

const cancel = () => {
    dialogRef.value.close()
}

const computedGrams = computed(() => {
  if (selectedInputMode.value == 'grams') {
    return parseInt(quantity.value)
  }
  return quantity.value * ingredient.value.serving_size
})

const computedCalories = computed(() => {
  return computedGrams.value * caloriesPer1Gram
})

const computedProtein = computed(() =>  {
  return computedGrams.value * proteinPer1Gram
})

const servings = () => {
  if (selectedInputMode.value == 'grams') {
    return null
  }
  return parseInt(quantity.value)
}

const ratio = () => {
  return (computedProtein.value / computedCalories.value) * 25 // 4 calories for 1 protein (100/4=25)
}

const per_meal = () => {
  return selectedAddMode.value == addModes.value[1]
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