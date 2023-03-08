<template>
  <div class="card" >
    <ConfirmDialog></ConfirmDialog>
    <Message v-if="errorMessage != null" severity="error" :life="4000" :sticky="false" @close="errorClosed">{{ errorMessage }}</Message>
    <Card >
      <template #title>
        <div>
          {{ item.label }} {{ item.serving_size != null ? '('+item.serving_size+'g)' : null }}
          <Button @click="toggleFavourite()" :icon="favouriteIcon" class="p-button-raised p-button-secondary" style="float: right" />
          <Button @click="editItem()" icon="pi pi-pencil" class="p-button-raised p-button-secondary" style="float: right" />
        </div>
      </template>

      <template #subtitle>
        {{ item.calories }} cal, {{ item.proteins }}g protein
      </template>

      <template #content>
        <IngredientQuantity />
      </template>

      <template #footer>
        <Button icon="pi pi-check" @click="addIngredient" label="Add" :disabled="ingredientStore.quantity <= 0" />
        <Button icon="pi pi-plus-circle" class="p-button-secondary" label="Add per serving" :disabled="ingredientStore.quantity <= 0" />
        <Button @click="deleteItem()" icon="pi pi-trash" class="p-button-raised p-button-danger" style="float: right" />
      </template>

    </Card>
  </div>
</template>

<script setup>
import { toRefs, ref, computed, watch } from 'vue'
import { storeToRefs } from 'pinia'
import axios from 'axios'
import { useIngredientStore } from '../script/stores/ingredientStore'

import { useDialog } from 'primevue/usedialog'
import { useConfirm } from 'primevue/useconfirm'
import IngredientForm from './IngredientForm'

// eslint-disable-next-line
const props = defineProps({
  item: Object
})
const { item } = toRefs(props)
const favouriteIcon = computed(() => item.value.favourite == null ? 'pi pi-spin pi-spinner' : item.value.favourite ? 'pi pi-heart-fill' : 'pi pi-heart')
const errorMessage = ref(null)

const toggleFavourite = async () => {
  const oldValue = item.value.favourite
  const newValue = !oldValue

  // trigger loading animation
  item.value.favourite = null

  try {
    const response = await axios({
      method: 'post',
      url: 'http://192.168.1.23:5000/api/ingredient/favourite',
      data: {
        id: item.value.id,
        oldFavourite: oldValue,
        newFavourite: newValue
      }
    })

    item.value.favourite = response.data['newFavourite']
  } catch (error) {
    errorMessage.value = 'Unable to update favourite 😢. Please try again later.'
    item.value.favourite = oldValue
  }
}

const errorClosed = () => errorMessage.value = null


const dialog = useDialog()
const editItem = () => {
  dialog.open(IngredientForm, {
    props: {
      header: item.value.label,
      style: {
          width: '80%',
          maxWidth: '600px'
      },
      
    },
    modal: true,
    data: {
      item: item.value,
    },
    onClose: async (data) => {
      if (data.data != null) {
        try {
          const response = await axios({
            method: 'post',
            url: 'http://192.168.1.23:5000/api/ingredient',
            data: data.data
          })

          item.value.label = response.data.label
          item.value.calories = response.data.calories
          item.value.proteins = response.data.proteins
          item.value.serving_size = response.data.serving_size
        } catch (error) {
          errorMessage.value = 'Unable to update item 😢. Please try again later.'
        }
      }
    }
  })
}

const ingredientStore = useIngredientStore()

const { selectedIngredient } = storeToRefs(ingredientStore)

watch(selectedIngredient, (newValue, oldValue) => {
  if (newValue != oldValue) {
    ingredientStore.quantity = 0
  }
  if (newValue.serving_size == null) {
    ingredientStore.selectedInputMode = ingredientStore.quantityInputModes[0]
  }
})

const confirm = useConfirm()
const deleteItem = () => {
  confirm.require({
      message: 'Are you sure you want to delete ' + item.value.label + '? This cannot be undone.',
      header: 'Confirm deletion',
      icon: 'pi pi-exclamation-triangle',
      accept: async () => {
        try {
          await axios({
            method: 'delete',
            url: 'http://192.168.1.23:5000/api/ingredient',
            data: {
              id: item.value.id
            }
          })
          ingredientStore.deleteIngredient(item.value)
        } catch (error) {
          errorMessage.value = 'Unable to delete item 😢. Please try again later.'
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

const addIngredient = () => {
  ingredientStore.addSelectedIngredientToRecipe()
}
</script>

<style scoped>
.p-button {
  margin-right: .5rem;
}
.quantity-input {
  display: inline-block;
  width: 100%;
}
.p-inputtext {
  width: 100%;
  margin-top: 0.3rem;
}
</style>