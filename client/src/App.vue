<template>
  <div>
    <ConfirmDialog/>
    <Toast position="center" />
    <DynamicDialog/>
    <TabMenu :model="items"/> 
    <router-view/>
  </div>
</template>


<script setup>
import { ref } from 'vue'

const items = ref([
  {
      label: 'Cook',
      icon: 'pi pi-fw pi-plus-circle',
      to: '/cook'
  },
  {
      label: 'Eat',
      icon: 'pi pi-fw pi-minus-circle',
      to: '/eat'
  },
  {
      label: 'Repeat',
      icon: 'pi pi-fw pi-chart-line',
      to: '/repeat'
  },
])
</script>

<style>
</style>