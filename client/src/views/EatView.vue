<template>
  <Splitter :gutterSize=8>
  <SplitterPanel :size="60">
    <EatMealsPanel />
	</SplitterPanel>
	<SplitterPanel :size="40">
		<TodayChart />
	</SplitterPanel>
</Splitter>

</template>

<script setup>
</script>

<style>
</style>