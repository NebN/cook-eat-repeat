<template>
  <div>
    <span>
      <h4 style="margin-left: 1rem">Calories: {{(mealStore.todaysProgress != null ? mealStore.todaysProgress.calories : 0).toFixed()}}{{ (mealStore.selectedMeal != null ? ' -> ' + (mealStore.selectedMeal.calories + mealStore.todaysProgress.calories).toFixed() : null) }} / {{ mealStore.currentGoal.calories }}</h4>
      <h4 style="margin-left: 1rem">Protein: {{(mealStore.todaysProgress != null ? mealStore.todaysProgress.protein : 0).toFixed(1)}}{{ (mealStore.selectedMeal != null ? ' -> ' + (mealStore.selectedMeal.protein + mealStore.todaysProgress.protein).toFixed(1) : null) }} / {{ mealStore.currentGoal.protein }}</h4>
    </span>
    <Chart 
    ref="primeChart" 
    style="height: 100%; min-height: 360px;" 
    type="bar" 
    :data="chartData" 
    :options="chartOptions" />
  </div>
</template>

<script setup> 
import { ref, onMounted, computed } from 'vue'
import { useMealStore } from '@/script/stores/mealStore'

const mealStore = useMealStore()

const primeChart = ref()

onMounted(() => {
  mealStore.initGoal()
})

const chartData = computed(() =>({
  labels: ['Calories', 'Protein (x10)'],
  datasets: [
    { 
      label: 'Goal',
      data: [
        mealStore.currentGoal.calories, 
        mealStore.currentGoal.protein * 10
      ],
      backgroundColor: '#CCC',
    },
    {
      label: 'Consoomed',
      data: [
        (mealStore.todaysProgress != null ? mealStore.todaysProgress.calories : 0) + (mealStore.selectedMeal != null ? mealStore.selectedMeal.calories : 0), 
        (mealStore.todaysProgress != null ? mealStore.todaysProgress.protein * 10 : 0)  + (mealStore.selectedMeal != null ? mealStore.selectedMeal.protein * 10 : 0), 
      ],
      backgroundColor: '#FF7043',
    },
  ]
}))
const chartOptions = ref({
  maintainAspectRatio: false,
  plugins: {
  }
})
</script>

<style scoped>

</style>
