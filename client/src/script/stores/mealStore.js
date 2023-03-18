import { defineStore } from 'pinia'
import axios from 'axios'

export const useMealStore = defineStore('meals', {
  state: () => ({
    meals: [],
    mealHistory: [],
    selectedMeal: null,
    currentGoal: {
      calories: 0,
      protein: 0
    },
    todaysProgress: {
      calories: 0,
      protein: 0
    },
    allProgress: []
  }),
  actions: {
    async initGoal() {
      const respGoal = await axios.get('/api/goal')
      const goal = respGoal.data
      this.currentGoal =  goal

      const respToday = await axios.get('/api/goal/today')
      const today = respToday.data
      this.todaysProgress = today

      const respAll = await axios.get('/api/goal/all')
      const all = respAll.data
      this.allProgress = all

      const respMealHistory = await axios.get('/api/meal/history')
      const mealHistory = respMealHistory.data
      mealHistory.sort((a, b) => Number(b.favourite) - Number(a.favourite))
      this.mealHistory = mealHistory
    },
    async eatMeal(meal, date) {
      const asd = {
        id: meal.id,
        date: date.toISOString()
      }

      const resp = await axios({
        method: 'post',
        url: '/api/meal/eat',
        data: asd
      })
      
      this.selectedMeal = null

      const data = resp.data

      if (data.meals_remaining <= 0) {
        this.meals = this.meals.filter(m => m.id != data.id)
      } else {
        meal.meals_remaining = data.meals_remaining
      }

      if (date.toDateString() == new Date().toDateString) {
        this.todaysProgress.calories = data.progress.calories
        this.todaysProgress.protein = data.progress.protein
      }
    },
    async deleteMeal(meal) {
      await axios({
        method: 'delete',
        url: '/api/meal',
        data: ({
          id: meal.id
        })
      })
      this.meals = this.meals.filter(m => m.id != meal.id)
    },
    async updateGoal(goal) {
      await axios({
        method: 'post',
        url: '/api/goal',
        data: {
          calories: goal.calories,
          protein: goal.protein
        }
      })
    },
    selectMeal(meal) {
      this.selectedMeal = meal
    }
  },
})