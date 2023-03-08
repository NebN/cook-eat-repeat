<template>
<Splitter :gutterSize=8>
  <SplitterPanel :size="40">
    <IngredientsPanel/>
	</SplitterPanel>
	<SplitterPanel :size="60">
		<RecipePanel/>
	</SplitterPanel>
</Splitter>
</template>

<script setup>
</script>

<style>
</style>