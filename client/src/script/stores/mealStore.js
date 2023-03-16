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
      const respGoal = await axios.get('http://192.168.1.23:5000/api/goal')
      const goal = respGoal.data
      this.currentGoal =  goal
      const respToday = await axios.get('http://192.168.1.23:5000/api/goal/today')
      const today = respToday.data
      this.todaysProgress = today
      const respAll = await axios.get('http://192.168.1.23:5000/api/goal/all')
      const all = respAll.data
      this.allProgress = all
      const respMealHistory = await axios.get('http://192.168.1.23:5000/api/meal/history')
      const mealHistory = respMealHistory.data
      console.log(mealHistory)
      this.mealHistory = mealHistory
    },
    async eatMeal(meal) {
      const resp = await axios({
        method: 'post',
        url: 'http://192.168.1.23:5000/api/meal/eat',
        data: ({
          id: meal.id
        })
      })
      
      const data = resp.data 

      if (data.meals_remaining <= 0) {
        this.meals = this.meals.filter(m => m.id != data.id)
      } else {
        meal.meals_remaining = data.meals_remaining
        meal.times_eaten = data.times_eaten
      }
      
      this.todaysProgress.calories = data.progress.calories
      this.todaysProgress.protein = data.progress.protein

      this.selectedMeal = null
    },
    async deleteMeal(meal) {
      await axios({
        method: 'delete',
        url: 'http://192.168.1.23:5000/api/meal',
        data: ({
          id: meal.id
        })
      })
      this.meals = this.meals.filter(m => m.id != meal.id)
    },
    async updateGoal(goal) {
      await axios({
        method: 'post',
        url: 'http://192.168.1.23:5000/api/goal',
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