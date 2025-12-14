<script lang="ts">
	interface Props {
		title: string;
		value: number | string;
		icon: string;
		color: 'blue' | 'red' | 'green' | 'purple' | 'orange' | 'yellow';
		description?: string;
	}

	let { title, value, icon, color, description } = $props<Props>();

	const colors = {
		blue: 'from-blue-500 to-blue-600',
		red: 'from-red-500 to-red-600',
		green: 'from-green-500 to-green-600',
		purple: 'from-purple-500 to-purple-600',
		orange: 'from-orange-500 to-orange-600',
		yellow: 'from-yellow-500 to-yellow-600'
	};
</script>

<div class={`rounded-xl bg-gradient-to-br ${colors[color]} p-6 text-white shadow-lg`}>
	<div class="flex items-center justify-between">
		<div>
			<div class="text-3xl font-bold">{value}</div>
			<div class="text-sm opacity-90">{title}</div>
			{#if description}
				<p class="mt-1 text-xs opacity-75">{description}</p>
			{/if}
		</div>
		<i class={`fas ${icon} text-4xl opacity-50`}></i>
	</div>
</div>
