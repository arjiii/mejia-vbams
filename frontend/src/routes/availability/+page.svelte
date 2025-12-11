<script lang="ts">
	let isAvailable = $state(true);
	let workingHours = $state({
		monday: { start: '08:00', end: '18:00', enabled: true },
		tuesday: { start: '08:00', end: '18:00', enabled: true },
		wednesday: { start: '08:00', end: '18:00', enabled: true },
		thursday: { start: '08:00', end: '18:00', enabled: true },
		friday: { start: '08:00', end: '18:00', enabled: true },
		saturday: { start: '09:00', end: '15:00', enabled: true },
		sunday: { start: '09:00', end: '15:00', enabled: false }
	});

	function toggleAvailability() {
		isAvailable = !isAvailable;
	}

	function saveSchedule() {
		console.log('Saving schedule:', workingHours);
	}
</script>

<svelte:head>
	<title>Availability - VBAMS</title>
</svelte:head>

<div class="space-y-6">
	<div>
		<h1 class="text-3xl font-bold text-gray-900">Availability Settings</h1>
		<p class="mt-2 text-sm text-gray-600">Manage your working hours and availability</p>
	</div>

	<!-- Current Status -->
	<div
		class="rounded-xl border-2 border-purple-200 bg-gradient-to-r from-purple-50 to-pink-50 p-6 shadow-lg"
	>
		<div class="flex items-center justify-between">
			<div>
				<h2 class="text-xl font-bold text-gray-900">Current Status</h2>
				<p class="mt-2 text-sm text-gray-600">
					You are currently <span
						class={isAvailable ? 'font-bold text-green-600' : 'font-bold text-red-600'}
						>{isAvailable ? 'AVAILABLE' : 'UNAVAILABLE'}</span
					> for new requests
				</p>
			</div>
			<button
				onclick={toggleAvailability}
				class={`relative inline-flex h-8 w-16 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out ${isAvailable ? 'bg-green-600' : 'bg-gray-300'}`}
			>
				<span
					class={`pointer-events-none inline-block h-7 w-7 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${isAvailable ? 'translate-x-8' : 'translate-x-0'}`}
				></span>
			</button>
		</div>
	</div>

	<!-- Weekly Schedule -->
	<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-lg">
		<h2 class="mb-6 text-xl font-bold text-gray-900">Weekly Schedule</h2>
		<div class="space-y-4">
			{#each Object.entries(workingHours) as [day, hours]}
				<div class="flex items-center gap-4 rounded-lg border border-gray-200 p-4">
					<div class="w-32">
						<span class="font-medium capitalize text-gray-900">{day}</span>
					</div>
					<div class="flex flex-1 items-center gap-4">
						<input
							type="time"
							bind:value={hours.start}
							disabled={!hours.enabled}
							class="rounded-lg border border-gray-300 px-3 py-2 disabled:bg-gray-100"
						/>
						<span class="text-gray-500">to</span>
						<input
							type="time"
							bind:value={hours.end}
							disabled={!hours.enabled}
							class="rounded-lg border border-gray-300 px-3 py-2 disabled:bg-gray-100"
						/>
					</div>
					<button
						onclick={() => (hours.enabled = !hours.enabled)}
						class={`rounded-lg px-4 py-2 text-sm font-medium ${hours.enabled ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'}`}
					>
						{hours.enabled ? 'Enabled' : 'Disabled'}
					</button>
				</div>
			{/each}
		</div>
		<div class="mt-6 flex justify-end">
			<button
				onclick={saveSchedule}
				class="rounded-lg bg-gradient-to-r from-purple-600 to-pink-600 px-6 py-3 text-sm font-bold text-white shadow-lg transition-all hover:from-purple-700 hover:to-pink-700"
			>
				<i class="fas fa-save mr-2"></i>
				Save Schedule
			</button>
		</div>
	</div>
</div>
