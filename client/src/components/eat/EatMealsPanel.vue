<template>
  <DataTable 
  v-model:selection="selectedMeal" 
  @rowSelect="onRowSelect"
  selectionMode="single" 
  dataKey="id" 
  :value="mealStore.meals" 
  :rowClass="rowClass" 
  responsiveLayout="scroll">
    <template #header>
        <Button type="button" :label="'Eat ' + (selectedMeal != null ? selectedMeal.label : '')" @click="eat(selectedMeal)" :disabled="selectedMeal == null"/>
        <Button type="button" icon="pi pi-trash" class="p-button-raised p-button-danger" @click="deleteMeal(selectedMeal)" :disabled="selectedMeal == null" style="float: right"/>
    </template>

    <Column header="Name">
      <template #body="slotProps">
          {{slotProps.data.label}}
      </template>
    </Column>

    <Column header="Calories">
      <template #body="slotProps">
          {{slotProps.data.calories.toFixed()}}
      </template>
    </Column>

    <Column header="Protein">
      <template #body="slotProps">
          {{slotProps.data.protein.toFixed(1)}}
      </template>
    </Column>

    <Column header="Remaining">
      <template #body="slotProps">
          {{slotProps.data.meals_remaining}}
      </template>
    </Column>

    <template #expansion="slotProps">
      <div>
        <div>Eating {{ slotProps.data.label }} will bring you to a total of</div>
        <div> {{ slotProps.data.calories.toFixed() }} calories and {{ slotProps.data.protein.toFixed(1) }} protein</div>
        <Button type="button" label="Eat" @click="eat(slotProps.data)" class="p-button-primary" style="margin-top: 0.5rem" />
      </div>
    </template>

  </DataTable>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useMealStore } from '@/script/stores/mealStore'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'

const confirm = useConfirm()
const toast = useToast()
const mealStore = useMealStore()
const expandedRows = ref()
const rowClass = ref(() => '')

const selectedMeal = ref()

onMounted(async () => {
  if (mealStore.meals.length == 0) {
    try {
      const response = await axios.get('http://192.168.1.23:5000/api/meal')
      const meals = response.data
      meals.sort((a, b) => b.protein - a.protein)
      mealStore.$patch(store => store.meals = meals)
    } catch (error) {
      alert(error)
    }
  }
})

const onRowSelect = (row) => {
  mealStore.selectMeal(row.data)
}

const eat = async (meal) => {
  try {
    await mealStore.eatMeal(meal)
    expandedRows.value = []
    toast.add({severity:'success', summary: 'Nom!', detail:'Meal has been eaten.', life: 3000})
  } catch (error) {
    console.log(error)
    toast.add({severity:'error', summary: 'Error!', detail:'Unable to eat meal 😢. Try again later.', life: 3000})
  }
}

const deleteMeal = async (meal) => {
  confirm.require({
      message: 'Are you sure you want to delete ' + meal.label + '? This cannot be undone.',
      header: 'Confirm deletion',
      icon: 'pi pi-exclamation-triangle',
      accept: async () => {
        try {
          await mealStore.deleteMeal(meal)
        } catch (error) {
          toast.add({severity:'error', summary: 'Error!', detail:'Unable to delete meal 😢. Try again later.', life: 3000})
          console.log(error)
        }
      },
      reject: () => {
      },
      onShow: () => {
      },
      onHide: () => {
      }
  });
}

</script>

<style scoped>

</style>