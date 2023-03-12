<template>
  <Card>
    <template #title>
      Current Daily Goal
    </template>
    <template #content>
      <div class="formgroup-inline">
        <div class="field">
            <label for="calories">Calories</label>
            <InputText id="calories" 
            type="number" 
            placeholder="Calories"
            :readonly="inputDisabled"
            :style="textStyle"
            v-model="currentGoal.calories"
            :class="border" />
        </div>
        <div class="field">
            <label for="protein">Protein</label>
            <InputText id="protein" 
            type="number" 
            placeholder="Protein"
            :readonly="inputDisabled"
            :style="textStyle"
            v-model="currentGoal.protein"
            :class="border" />
        </div>
        <Button @click="toggleEdit" :icon="icon" :class="buttonClass"></Button>
      </div>
    </template>
  </Card>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useMealStore } from '@/script/stores/mealStore'

const inputDisabled = ref(true)

const mealStore = useMealStore()
const { currentGoal } = storeToRefs(mealStore)

onMounted(async () => {
  if (mealStore.currentGoal.protein == 0 && mealStore.currentGoal.calories == 0) {
    try {
      mealStore.initGoal()
    } catch (exception) {
      alert(exception)
    }
  }
})

const textStyle = computed(() => {
  if  (inputDisabled.value) {
    return 'pointer-events: none;'
  } else {
    return ''
  }
})

const buttonClass = computed(() => {
  if  (inputDisabled.value) {
    return 'p-button-outlined p-button-secondary'
  } else {
    return 'p-button-outlined p-button-primary'
  }
})

const icon = computed(() => {
  if  (inputDisabled.value) {
    return 'pi pi-pencil'
  } else {
    return 'pi pi-check'
  }
})

const border = computed(() => {
  if  (inputDisabled.value) {
    return 'border-solid'
  } else {
    return 'border-primary'
  }
})

const toggleEdit = () => {
  if  (inputDisabled.value) {
    inputDisabled.value = false
  } else {
    inputDisabled.value = true
    commitEdit()
  }
}


const commitEdit = async () => {
  try {
    mealStore.updateGoal(mealStore.currentGoal)
  } catch (exception) {
    alert(exception)
  }
}
</script>

<style scoped>

</style>