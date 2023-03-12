<template>
  <div style="margin-top:0.5rem">
    <Button type="button" label="Confirm" @click="$emit('confirm')" />
    <Button type="button" label="Cancel" class="p-button-secondary" @click="$emit('cancel')" style="float: right; margin-right: 0.5rem" />
  </div>
</template>

<script setup>
// eslint-disable-next-line
defineEmits(['confirm', 'cancel'])
</script>

<style scoped>

</style>