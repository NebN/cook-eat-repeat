<template>
  <div class="panel-wrapper" >
    <Button @click="newIngredient" icon="pi pi-plus" label="New Ingredient" class="p-button-outlined"/>
    <Listbox ref="listboxRef" 
    @keyup.enter="onEnter" 
    v-model="ingredientStore.selectedIngredient" 
    @filter="onFilter" 
    :options="ingredientStore.ingredients" 
    optionLabel="label" 
    :filter="true" 
    listStyle="max-height: 30rem" >
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
      <IngredientCard @addIngredient="addIngredient" class="ingredient-card" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useDialog } from 'primevue/usedialog'
import axios from 'axios'
import { useIngredientStore } from '@/script/stores/ingredientStore'
import { useRecipeStore } from '@/script/stores/recipeStore'
import IngredientForm from '@/components/cook/IngredientForm'
import IngredientAmountForm from '@/components/cook/IngredientAmountForm'


const ingredientStore = useIngredientStore()
const recipeStore = useRecipeStore()
const listboxRef = ref(null)

onMounted(async () => {
  if (ingredientStore.ingredients.length == 0) {
    try {
      const response = await axios.get('/api/ingredient')
      const ingredients = response.data
      ingredients.sort((a, b) => Number(b.favourite) - Number(a.favourite))
      ingredientStore.$patch(store => store.ingredients = ingredients)
    } catch (error) {
      alert(error)
    }
  }
})

const dialog = useDialog()
const newIngredient = () => {
  dialog.open(IngredientForm, {
    props: {
      header: 'New Ingredient',
      style: {
          width: '80%',
          maxWidth: '600px'
      },
    },
    modal: true,
    data: { 
      item: {
        label: listboxRef.value.filterValue 
      }
    },
    onClose: async (data) => {
      if (data.data != null) {
        try {
          const response = await axios({
            method: 'post',
            url: '/api/ingredient',
            data: data.data
          })

          ingredientStore.addIngredient(response.data)
        } catch (error) {
          alert('Unable to save ingredient 😢. Please try again later.')
          console.log(error)
        }
      }
    }
  })
}

const onFilter = () => {
  if (listboxRef.value.visibleOptions.length > 0) {
    ingredientStore.selectedIngredient = listboxRef.value.visibleOptions[0]
  } else {
    ingredientStore.selectedIngredient = null
  }
}

const onEnter = () => {
  if (ingredientStore.selectedIngredient != null) {
    addIngredient(ingredientStore.selectedIngredient)
  } else {
    newIngredient()
  }
}

const addIngredient = () => {
  dialog.open(IngredientAmountForm, {
    props: {
      header: ingredientStore.selectedIngredient.label + (ingredientStore.selectedIngredient.serving_size != null ? ' ('+ingredientStore.selectedIngredient.serving_size+'g)' : ''),
      style: {
          width: '80%',
          maxWidth: '600px'
      },
    },
    modal: true,
    data: {
      ingredient: ingredientStore.selectedIngredient,
    },
    onClose: (item) => {
      if (item.data != null) {
        const data = item.data
        const recipeIngredient = {
          ...ingredientStore.selectedIngredient,
          ...data
        }
        recipeStore.addIngredient(recipeIngredient)
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
.ingredient-card {
  flex-grow: 1;
}
</style>