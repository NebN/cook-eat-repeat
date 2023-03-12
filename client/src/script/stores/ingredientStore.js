import { defineStore } from 'pinia'

export const useIngredientStore = defineStore('ingredients', {
  state: () => ({
    ingredients: [],
    selectedIngredient: null,
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
    }
  }
})