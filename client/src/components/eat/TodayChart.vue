<template>
    <Chart 
    ref="primeChart" 
    style="height: 100%;" 
    type="bar" 
    :data="chartData" 
    :options="chartOptions" />
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
    title: {
      display: true,
      text: 'Calories and protein intake for today',
      padding: {
          top: 10,
          bottom: 30
      }
    }
  }
})
</script>

<style scoped>

</style>
