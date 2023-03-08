import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

import { createPinia } from 'pinia'

import PrimeVue from 'primevue/config'

import "primevue/resources/themes/saga-blue/theme.css"; //theme
import "primevue/resources/primevue.min.css"; //core CSS
import "primeicons/primeicons.css"; //icons
import "/node_modules/primeflex/primeflex.css"
import DialogService from 'primevue/dialogservice'
import ConfirmationService from 'primevue/confirmationservice'
import ToastService from 'primevue/toastservice'

import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import Toolbar from 'primevue/toolbar'
import TabMenu from 'primevue/tabmenu'
import Listbox from 'primevue/listbox'
import SelectButton from 'primevue/selectbutton'
import InputNumber from 'primevue/inputnumber'
import InputText from 'primevue/inputtext'
import Divider from 'primevue/divider'
import Card from 'primevue/card'
import Fieldset from 'primevue/fieldset'
import Message from 'primevue/message'
import DynamicDialog from 'primevue/dynamicdialog'
import ConfirmDialog from 'primevue/confirmdialog'
import Splitter from 'primevue/splitter'
import SplitterPanel from 'primevue/splitterpanel'
import DataTable from 'primevue/datatable'
import ToggleButton from 'primevue/togglebutton'
import Column from 'primevue/column'
import Toast from 'primevue/toast'

import IngredientsPanel from './components/IngredientsPanel'
import ServingsPanel from './components/ServingsPanel'
import IngredientCard from './components/IngredientCard'
import RecipePanel from './components/RecipePanel'
import IngredientForm from './components/IngredientForm'
import RecipeIngredientForm from './components/RecipeIngredientForm'
import IngredientQuantity from './components/IngredientQuantity'
import CommitServingsForm from './components/CommitServingsForm'


const routes = [
  {
    path: '/',
    redirect: '/cook',
    name: 'home',
    component: () => import(/* webpackChunkName: "about" */ './views/CookView.vue')
  },
  {
    path: '/cook',
    name: 'cook',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ './views/CookView.vue')
  },
  {
    path: '/eat',
    name: 'eat',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ './views/EatView.vue')
  },
  {
    path: '/repeat',
    name: 'repeat',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ './views/RepeatView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

const pinia = createPinia()

createApp(App)
.use(router)
.use(PrimeVue)
.use(pinia)
.use(DialogService)
.use(ConfirmationService)
.use(ToastService)
.component('Button', Button)
.component('Dialog', Dialog)
.component('Toolbar', Toolbar)
.component('TabMenu', TabMenu)
.component('Listbox', Listbox)
.component('InputNumber', InputNumber)
.component('SelectButton', SelectButton)
.component('Divider', Divider)
.component('Card', Card)
.component('InputText', InputText)
.component('Fieldset', Fieldset)
.component('Message', Message)
.component('DynamicDialog', DynamicDialog)
.component('ConfirmDialog', ConfirmDialog)
.component('SplitterPanel', SplitterPanel)
.component('Splitter', Splitter)
.component('DataTable', DataTable)
.component('Column', Column)
.component('Toast', Toast)
.component('ToggleButton', ToggleButton)
.component('IngredientsPanel', IngredientsPanel)
.component('RecipePanel', RecipePanel)
.component('IngredientCard', IngredientCard)
.component('IngredientForm', IngredientForm)
.component('RecipeIngredientForm', RecipeIngredientForm)
.component('ServingsPanel', ServingsPanel)
.component('IngredientQuantity', IngredientQuantity)
.component('CommitServingsForm', CommitServingsForm)
.mount('#app')
