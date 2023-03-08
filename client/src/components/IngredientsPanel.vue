<template>
  <div class="panel-wrapper" >
    <Button @click="addIngredient" icon="pi pi-plus" label="New Ingredient" class="p-button-outlined"/>
    <Listbox v-model="ingredientStore.selectedIngredient" :options="ingredientStore.ingredients" optionLabel="label" :filter="true" listStyle="max-height: 50vh" >
      <template #option="itemProperties">
        <div class="country-item">
          <div>
            {{itemProperties.option.label}}
            <i style="float: right" 
            :class="{ 'pi pi-heart-fill' : itemProperties.option.favourite, 'pi pi-heart' : !itemProperties.option.favourite }"  />
          </div>
        </div>
      </template>
    </Listbox>
    <div v-if="ingredientStore.selectedIngredient != null">
      <Divider/>
      <IngredientCard class="ingredient-card" :item="ingredientStore.selectedIngredient" />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDialog } from 'primevue/usedialog'
import axios from 'axios'
import { useIngredientStore } from '../script/stores/ingredientStore'
import IngredientForm from './IngredientForm'

const ingredientStore = useIngredientStore()

onMounted(async () => {
  try {
    const response = await axios.get('http://192.168.1.23:5000/api/ingredient')
    ingredientStore.$patch(store => store.ingredients = response.data)
  } catch (error) {
    alert(error)
  }
})

const dialog = useDialog()
const addIngredient = () => {
  dialog.open(IngredientForm, {
    props: {
      header: 'New Ingredient',
      style: {
          width: '80%',
          maxWidth: '600px'
      },
    },
    modal: true,
    data: { },
    onClose: async (data) => {
      if (data.data != null) {
        try {
          const response = await axios({
            method: 'post',
            url: 'http://192.168.1.23:5000/api/ingredient',
            data: data.data
          })

          ingredientStore.addIngredient(response.data)
        } catch (error) {
          alert('Unable to update item 😢. Please try again later.')
          console.log(error)
        }
      }
    }
  })
}

</script>

<style scoped>
.p-button {
  width: 100%;
}
.panel-wrapper {
  display: flex;
  flex-direction: column;
}
.p-listbox {
  
}
.ingredient-card {
  flex-grow: 1;
}
</style>