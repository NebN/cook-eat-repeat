import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

import axios from 'axios'

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
import Chart from 'primevue/chart'

import ConfirmOrCancel from './components/ConfirmOrCancel'

import IngredientsPanel from './components/cook/IngredientsPanel'
import CookMealsPanel from './components/cook/CookMealsPanel'
import IngredientCard from './components/cook/IngredientCard'
import RecipePanel from './components/cook/RecipePanel'
import IngredientForm from './components/cook/IngredientForm'
import IngredientAmountForm from './components/cook/IngredientAmountForm'
import CommitMealsForm from './components/cook/CommitMealsForm'

import EatMealsPanel from './components/eat/EatMealsPanel'
import TodayChart from './components/eat/TodayChart'

import GoalCard from './components/repeat/GoalCard'
import MealHistory from './components/repeat/MealHistory'
import ProgressHistory from './components/repeat/ProgressHistory'

axios.defaults.baseURL = 'http://localhost:5000'

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
.component('Chart', Chart)
.component('IngredientsPanel', IngredientsPanel)
.component('RecipePanel', RecipePanel)
.component('IngredientCard', IngredientCard)
.component('IngredientForm', IngredientForm)
.component('CookMealsPanel', CookMealsPanel)
.component('IngredientAmountForm', IngredientAmountForm)
.component('CommitMealsForm', CommitMealsForm)
.component('ConfirmOrCancel', ConfirmOrCancel)
.component('EatMealsPanel', EatMealsPanel)
.component('GoalCard', GoalCard)
.component('TodayChart', TodayChart)
.component('MealHistory', MealHistory)
.component('ProgressHistory', ProgressHistory)
.mount('#app')
