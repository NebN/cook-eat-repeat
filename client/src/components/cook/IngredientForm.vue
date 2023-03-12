<template>
  <div class="card">
    <div class="input-block">
      <span class="p-float-label">
          <InputText id="label" type="text" v-model="label" />
          <label for="label">Name</label>
      </span>
    </div>
    <div class="p-inputgroup">
      <div class="input-block">
          <span class="p-float-label">
            <InputText id="calories" type="number" v-model="calories" />
            <label for="calories">Calories (100g)</label>
        </span>
      </div>
      <div class="input-block">
          <span class="p-float-label">
            <InputText id="proteins" type="number" v-model="proteins" />
            <label for="proteins">Protein (100g)</label>
        </span>
      </div>
    </div>
    <div class="input-block">
      <span class="p-float-label">
          <InputText id="serving_size" type="number" v-model="serving_size" />
          <label for="serving_size">Serving size (g)</label>
      </span>
    </div>
    <Button type="button" label="Confirm" @click="confirmEdit" />
    <Button type="button" label="Cancel" class="p-button-secondary" @click="cancelEdit" style="float: right; margin-right: 0.5rem" />
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from "vue"

const dialogRef = inject('dialogRef')
const item = ref({})

const label = ref(null)
const calories = ref(null)
const proteins = ref(null)
const serving_size = ref(null)

onMounted(() => {
  if (dialogRef.value.data.item != null) {
    item.value = dialogRef.value.data.item
    label.value = item.value.label
    calories.value = item.value.calories
    proteins.value = item.value.proteins
    serving_size.value = item.value.serving_size
  }
})

const confirmEdit = () => {
    dialogRef.value.close({
      id: item.value.id,
      label: label.value,
      calories: calories.value,
      proteins: proteins.value,
      serving_size: serving_size.value,
    })
}
const cancelEdit = () => {
    dialogRef.value.close()
}
</script>

<style scoped>
.input-block {
  margin-top: 2rem;
  margin-bottom: 1rem;
  width: 100%;
  margin-left: 0.2rem;
  margin-right: 0.2rem;
}
.p-inputtext {
  width: 100%
}
.p-inputgroup {
  width: 100%
}
</style>