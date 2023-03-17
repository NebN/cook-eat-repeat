import { defineStore } from 'pinia'

export const useRecipeStore = defineStore('recipes', {
  state: () => ({
    recipes: [],
    selectedRecipe: null
  }),
  actions: {
    addIngredient(ingredient) {
      if (this.selectedRecipe == null) {
        this.startNewRecipe(null)
      }
      this.selectedRecipe.ingredients.push(ingredient)
    },
    deleteIngredient(ingredient) {
      this.selectedRecipe.ingredients = this.selectedRecipe.ingredients.filter(function(e) {return e.label != ingredient.label})
    },
    startNewRecipe(label) {
      this.selectedRecipe = {
        ingredients: [],
        label: label
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
    calories() {
      return (numberOfMeals) => {
        return this.currentIngredients.map(i => {
          if (i.per_meal) {
            return i.calories
          } else {
            return i.calories / numberOfMeals
          }
        }).reduce((a, b) => a + b, 0)
      }
    },
    protein() {
      return (numberOfMeals) => {
        return this.currentIngredients.map(i => {
          if (i.per_meal) {
            return i.protein
          } else {
            return i.protein / numberOfMeals
          }
        }).reduce((a, b) => a + b, 0)
      }
    },
    grams() {
      return (numberOfMeals) => {
        return this.currentIngredients.map(i => {
          if (i.per_meal) {
            return i.grams
          } else {
            return i.grams / numberOfMeals
          }
        }).reduce((a, b) => a + b, 0)
      }
    }
  }
})