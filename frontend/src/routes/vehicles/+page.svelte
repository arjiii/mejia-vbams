<script lang="ts">
	import { onMount } from 'svelte';
	import api from '$lib/utils/api';
	import { goto } from '$app/navigation';
	import AddVehicleModal from '$lib/components/vehicles/AddVehicleModal.svelte';

	import { driverStore } from '$lib/stores/dashboard';

	let { title = 'Vehicles' } = $props();

	let query = $state('');
	let vehicles = $derived($driverStore.data?.vehicles || []);
	let loading = $derived($driverStore.loading);
	let showAddModal = $state(false);

	onMount(() => {
		driverStore.load();
	});

	let filtered = $derived(
		query
			? vehicles.filter((v) =>
					[v.license_plate, v.make, v.model, String(v.year)]
						.join(' ')
						.toLowerCase()
						.includes(query.trim().toLowerCase())
				)
			: vehicles
	);

	function addVehicle() {
		showAddModal = true;
	}

	function handleVehicleAdded() {
		driverStore.load(true);
	}

	function viewVehicle(v: any) {
		// Navigate to details
		// goto(`/app/vehicles/${v.id}`);
		alert(`Vehicle ID: ${v.id}`);
	}

	function statusClass(isActive: boolean) {
		return isActive ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800';
	}
</script>

<svelte:head>
	<title>My Vehicles - VBAMS</title>
</svelte:head>

<div class="space-y-6">
	<AddVehicleModal bind:isOpen={showAddModal} onSuccess={handleVehicleAdded} />

	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold text-gray-900">My Vehicles</h1>
			<p class="mt-2 text-sm text-gray-600">Manage your registered vehicles</p>
		</div>
		<button
			onclick={addVehicle}
			class="rounded-lg bg-gradient-to-r from-blue-600 to-cyan-600 px-4 py-2 text-sm font-bold text-white shadow-lg transition-all hover:from-blue-700 hover:to-cyan-700"
		>
			<i class="fas fa-plus mr-2"></i>
			Add Vehicle
		</button>
	</div>

	<!-- Toolbar -->
	<div class="flex items-center space-x-4">
		<div class="relative flex-1">
			<input
				type="search"
				placeholder="Search by plate, model..."
				bind:value={query}
				class="w-full rounded-md border bg-white py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
			/>
			<div class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
				<i class="fas fa-search"></i>
			</div>
		</div>
	</div>

	<div class="mt-6">
		{#if loading}
			<div class="p-8 text-center text-gray-500">Loading vehicles...</div>
		{:else if vehicles.length === 0}
			<div class="rounded border border-dashed p-8 text-center text-gray-500">
				<i class="fas fa-car mb-4 text-4xl text-gray-300"></i>
				<p class="mb-4">No vehicles found. Add one to get started.</p>
				<button onclick={addVehicle} class="font-bold text-blue-600 hover:underline">
					Add Vehicle Now
				</button>
			</div>
		{:else}
			<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
				{#each filtered as v}
					<div
						class="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-lg transition-all hover:shadow-xl"
					>
						<!-- Vehicle Header -->
						<div class="bg-gradient-to-r from-blue-600 to-cyan-600 p-6 text-white">
							<div class="flex items-center justify-between">
								<div>
									<h3 class="text-2xl font-bold">{v.year} {v.make} {v.model}</h3>
									<p class="mt-1 text-blue-100">{v.license_plate}</p>
								</div>
								<div
									class="flex h-16 w-16 items-center justify-center rounded-full bg-white/20 backdrop-blur-sm"
								>
									<i class="fas fa-car text-3xl"></i>
								</div>
							</div>
						</div>

						<!-- Vehicle Details -->
						<div class="p-6">
							<div class="mb-4 grid grid-cols-2 gap-4">
								<div>
									<p class="text-sm text-gray-500">Color</p>
									<p class="font-medium text-gray-900">{v.color}</p>
								</div>
								<div>
									<p class="text-sm text-gray-500">Status</p>
									<span
										class={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${statusClass(v.is_active)}`}
									>
										{v.is_active ? 'Active' : 'Inactive'}
									</span>
								</div>
							</div>

							<div class="mb-4">
								<p class="text-sm text-gray-500">VIN</p>
								<p class="font-mono text-sm text-gray-900">{v.vin || 'N/A'}</p>
							</div>

							<!-- Actions -->
							<div class="flex gap-2">
								<button
									onclick={() => viewVehicle(v)}
									class="flex-1 rounded-lg border-2 border-blue-500 px-4 py-2 text-sm font-medium text-blue-600 transition-all hover:bg-blue-50"
								>
									<i class="fas fa-eye mr-1"></i>
									View
								</button>
							</div>
						</div>
					</div>
				{/each}
			</div>
		{/if}
	</div>
</div>
