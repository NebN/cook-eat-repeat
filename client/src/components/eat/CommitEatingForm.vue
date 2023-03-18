<template>
  <div class="card">
    <span>Counts towards progress of
    <Calendar dateFormat="yy-mm-dd" v-model="date" style="margin-left: 0.4rem"/>
    </span>
    <ConfirmOrCancel @confirm="commitEat()" @cancel="cancelCommit"/>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useMealStore } from '@/script/stores/mealStore'

const toast = useToast()
const mealStore = useMealStore()
const dialogRef = inject('dialogRef')
const meal = ref()
const date = ref(new Date())

onMounted(() => {
    meal.value = dialogRef.value.data.meal
})

const commitEat = async () => {
  try {
    await mealStore.eatMeal(meal.value, date.value)
    toast.add({severity:'success', summary: 'Nom!', detail:'Meal has been eaten.', life: 3000})
    dialogRef.value.close()
  } catch (error) {
    console.log(error)
    toast.add({severity:'error', summary: 'Error!', detail:'Unable to eat meal 😢. Try again later.', life: 3000})
  }
}

const cancelCommit = () => {
    dialogRef.value.close()
}
</script>