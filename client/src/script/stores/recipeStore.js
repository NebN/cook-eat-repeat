import { defineStore } from 'pinia'

export const useRecipeStore = defineStore('recipes', {
  state: () => ({
    recipes: [],
    selectedRecipe: null
  }),
  actions: {
    addIngredient(ingredient) {
      if (this.selectedRecipe == null) {
        this.startNewRecipe()
      }
      this.selectedRecipe.ingredients.push(ingredient)
    },
    deleteIngredient(ingredient) {
      this.selectedRecipe.ingredients = this.selectedRecipe.ingredients.filter(function(e) {return e.id != ingredient.id})
    },
    startNewRecipe() {
      this.selectedRecipe = {
        ingredients: []
      }
    }
  },
  getters: {
    currentIngredients(state) {
      if (state.selectedRecipe == null) {
        return []
      }
      return state.selectedRecipe.ingredients
    },
    totalCalories() {
      return this.currentIngredients.map(i => i.calories).reduce((a, b) => a + b, 0)
    },
    totalProtein() {
      return this.currentIngredients.map(i => i.protein).reduce((a, b) => a + b, 0)
    },
    totalGrams() {
      return this.currentIngredients.map(i => i.grams).reduce((a, b) => a + b, 0)
    },
    averageRatio() {
      const totalGrams = this.totalGrams
      if (totalGrams == 0) {
        return 0
      }
      return (this.totalProtein / this.totalCalories) * 100
    }
  }
})