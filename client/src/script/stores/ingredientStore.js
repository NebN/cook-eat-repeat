import { defineStore } from 'pinia'
import { useRecipeStore } from './recipeStore'

export const useIngredientStore = defineStore('ingredients', {
  state: () => ({
    recipeStore: useRecipeStore(),
    ingredients: [],
    selectedIngredient: null,
    quantityInputModes: [
      {
        name: 'grams',
        label: 'g'
      },
      {
        name: 'servings',
        label: 's'
      }
    ],
    selectedInputMode: {
      name: 'grams',
      label: 'g'
    },
    quantity: 0
  }),
  actions: {
    addIngredient(ingredient) {
      this.ingredients.push(ingredient)
      this.selectedIngredient = ingredient
    },
    deleteIngredient(ingredient) {
      if (this.selectedIngredient != null && this.selectedIngredient.id == ingredient.id) {
        this.selectedIngredient = null
      }
      this.ingredients = this.ingredients.filter(function(e) {return e.id != ingredient.id})
    },
    addSelectedIngredientToRecipe() {
      const recipeIngredient = {
        id: this.selectedIngredient.id,
        label: this.selectedIngredient.label,
        calories: this.computedCalories,
        protein: this.computedProtein,
        grams: this.totalGrams,
        ratio: this.computedRatio,
        portions: this.computedProtions
      }
      this.recipeStore.addIngredient(recipeIngredient)
    }
  },
  getters: {
    totalGrams(state) {
      if (state.selectedIngredient == null) {
        return null
      }
      if (state.selectedInputMode.name == 'grams') {
        return parseInt(state.quantity)
      }
      return state.quantity * state.selectedIngredient.serving_size
    },
    computedCalories(state) {
      if (state.selectedIngredient == null) {
        return null
      }
      return this.totalGrams * state.selectedIngredient.calories / 100
    },
    computedProtein(state) {
      if (state.selectedIngredient == null) {
        return null
      }
      return this.totalGrams * state.selectedIngredient.proteins / 100
    },
    computedPortions(state) {
      if (state.selectedIngredient == null) {
        return null
      }
      if (state.selectedInputMode.name == 'grams') {
        return null
      }
      return state.quantity
    },
    computedRatio(state) {
      if (state.selectedIngredient == null) {
        return null
      }
      return (this.computedProtein / this.computedCalories) * 100
    }
  }
})