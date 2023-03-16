<template>
  <div class="card" >
    <Message v-if="errorMessage != null" severity="error" :life="4000" :sticky="false" @close="errorClosed">{{ errorMessage }}</Message>
    <Card>
      <template #title>
        <div>
          {{ title }}
          <Button @click="deleteItem()" icon="pi pi-trash" class="p-button-raised p-button-danger" style="float: right" />
          <Button @click="editItem()" icon="pi pi-pencil" class="p-button-raised p-button-secondary" style="float: right" />
          <Button @click="toggleFavourite()" :icon="favouriteIcon" class="p-button-raised p-button-secondary" style="float: right" />
        </div>
      </template>

      <template #subtitle>
        {{ selectedIngredient.calories }} cal, {{ selectedIngredient.proteins }}g protein
      </template>

      <template #content>
        <Button icon="pi pi-plus" @click="$emit('addIngredient')" label="Add to meal" />
      </template>
    </Card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import axios from 'axios'
import { useDialog } from 'primevue/usedialog'
import { useConfirm } from 'primevue/useconfirm'
import IngredientForm from '@/components/cook/IngredientForm'
import { useIngredientStore } from '@/script/stores/ingredientStore'


// eslint-disable-next-line
const emit = defineEmits(['addIngredient'])

const dialog = useDialog()
const confirm = useConfirm()

const ingredientStore = useIngredientStore()
const { selectedIngredient } = storeToRefs(ingredientStore)

const favouriteIcon = computed(() => selectedIngredient.value.favourite == null ? 'pi pi-spin pi-spinner' : selectedIngredient.value.favourite ? 'pi pi-heart-fill' : 'pi pi-heart')
const errorMessage = ref(null)

const title = computed(() => 
  selectedIngredient.value.label + (selectedIngredient.value.serving_size != null ? ' ('+selectedIngredient.value.serving_size+'g)' : '')
)

const toggleFavourite = async () => {
  const oldValue = selectedIngredient.value.favourite

  // trigger loading animation
  selectedIngredient.value.favourite = null

  try {
    const response = await axios({
      method: 'post',
      url: 'http://192.168.1.23:5000/api/ingredient/favourite',
      data: {
        id: selectedIngredient.value.id
      }
    })

    selectedIngredient.value.favourite = response.data['newFavourite']
  } catch (error) {
    errorMessage.value = 'Unable to update favourite 😢. Please try again later.'
    selectedIngredient.value.favourite = oldValue
  }
}

const errorClosed = () => errorMessage.value = null

const editItem = () => {
  dialog.open(IngredientForm, {
    props: {
      header: title.value,
      style: {
          width: '80%',
          maxWidth: '600px'
      },
      
    },
    modal: true,
    data: {
      item: selectedIngredient.value,
    },
    onClose: async (data) => {
      if (data.data != null) {
        try {
          const response = await axios({
            method: 'post',
            url: 'http://192.168.1.23:5000/api/ingredient',
            data: data.data
          })

          selectedIngredient.value.label = response.data.label
          selectedIngredient.value.calories = response.data.calories
          selectedIngredient.value.proteins = response.data.proteins
          selectedIngredient.value.serving_size = response.data.serving_size
        } catch (error) {
          errorMessage.value = 'Unable to update ingredient 😢. Please try again later.'
        }
      }
    }
  })
}

const deleteItem = () => {
  confirm.require({
      message: 'Are you sure you want to delete ' + selectedIngredient.value.label + '? This cannot be undone.',
      header: 'Confirm deletion',
      icon: 'pi pi-exclamation-triangle',
      accept: async () => {
        try {
          await axios({
            method: 'delete',
            url: 'http://192.168.1.23:5000/api/ingredient',
            data: {
              id: selectedIngredient.value.id
            }
          })
          ingredientStore.deleteIngredient(selectedIngredient.value)
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