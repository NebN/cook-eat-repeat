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

  </DataTable>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useMealStore } from '@/script/stores/mealStore'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { useDialog } from 'primevue/usedialog'
import CommitEatingForm from '@/components/eat/CommitEatingForm.vue'

const confirm = useConfirm()
const toast = useToast()
const mealStore = useMealStore()
const rowClass = ref(() => '')

const selectedMeal = ref()

onMounted(async () => {
  if (mealStore.meals.length == 0) {
    try {
      const response = await axios.get('/api/meal')
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

const dialog = useDialog()
const eat = () => {
  dialog.open(CommitEatingForm, {
    props: {
      modal: true,
      header: 'Eat' + selectedMeal.value.label + '?',
      style: {
          width: '80%',
          maxWidth: '600px'
      },
      
    },
    data: {
      meal: selectedMeal.value
    },
    onClose: () => {
    }
  })
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