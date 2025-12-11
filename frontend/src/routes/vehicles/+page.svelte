<script lang="ts">
	import { onMount } from 'svelte';
	import { vehicleAPI } from '$lib/utils/api';
	import type { Vehicle } from '$lib/server/db'; // Or define locally if simpler, but let's try to reuse or define matching types.

	// Define local interface matching the DB response if import fails or to be explicit
	interface VehicleData {
		id: number;
		make: string;
		model: string;
		year: number;
		license_plate: string;
		color: string;
		vin: string;
		is_active: number;
		vehicle_type: string;
		fuel_type: string;
		mileage: number;
	}

	let vehicles: VehicleData[] = $state([]);
	let showAddModal = $state(false);
	let loading = $state(true);
	let error = $state('');

	onMount(async () => {
		try {
			const response = await vehicleAPI.getAll();
			vehicles = response.data;
		} catch (err: any) {
			console.error('Failed to load vehicles:', err);
			error = 'Failed to load vehicles';
		} finally {
			loading = false;
		}
	});

	function openAddModal() {
		showAddModal = true;
	}
</script>

<svelte:head>
	<title>My Vehicles - VBAMS</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold text-gray-900">My Vehicles</h1>
			<p class="mt-2 text-sm text-gray-600">Manage your registered vehicles</p>
		</div>
		<button
			onclick={openAddModal}
			class="rounded-lg bg-gradient-to-r from-blue-600 to-cyan-600 px-4 py-2 text-sm font-bold text-white shadow-lg transition-all hover:from-blue-700 hover:to-cyan-700"
		>
			<i class="fas fa-plus mr-2"></i>
			Add Vehicle
		</button>
	</div>

	<!-- Error Message -->
	{#if error}
		<div class="rounded-lg bg-red-50 p-4 text-red-600 border border-red-200">
			<i class="fas fa-exclamation-circle mr-2"></i> {error}
		</div>
	{/if}

	<!-- Vehicles Grid -->
	{#if loading}
		<div class="flex h-64 items-center justify-center">
			<div class="h-12 w-12 animate-spin rounded-full border-b-2 border-blue-600"></div>
		</div>
	{:else}
		<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
			{#each vehicles as vehicle}
				<div
					class="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-lg transition-all hover:shadow-xl"
				>
					<!-- Vehicle Header -->
					<div class="bg-gradient-to-r from-blue-600 to-cyan-600 p-6 text-white">
						<div class="flex items-center justify-between">
							<div>
								<h3 class="text-2xl font-bold">{vehicle.year} {vehicle.make} {vehicle.model}</h3>
								<p class="mt-1 text-blue-100">{vehicle.license_plate}</p>
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
								<p class="font-medium text-gray-900">{vehicle.color}</p>
							</div>
							<div>
								<p class="text-sm text-gray-500">Status</p>
								<span
									class={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${vehicle.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}
								>
									{vehicle.is_active ? 'Active' : 'Inactive'}
								</span>
							</div>
						</div>

						<div class="mb-4">
							<p class="text-sm text-gray-500">VIN</p>
							<p class="font-mono text-sm text-gray-900">{vehicle.vin}</p>
						</div>

						<!-- Actions -->
						<div class="flex gap-2">
							<button
								class="flex-1 rounded-lg border-2 border-blue-500 px-4 py-2 text-sm font-medium text-blue-600 transition-all hover:bg-blue-50"
							>
								<i class="fas fa-edit mr-1"></i>
								Edit
							</button>
							<button
								class="flex-1 rounded-lg border-2 border-red-500 px-4 py-2 text-sm font-medium text-red-600 transition-all hover:bg-red-50"
							>
								<i class="fas fa-trash mr-1"></i>
								Delete
							</button>
						</div>
					</div>
				</div>
			{/each}

			{#if vehicles.length === 0}
				<div class="col-span-full flex flex-col items-center py-12">
					<i class="fas fa-car mb-4 text-6xl text-gray-300"></i>
					<p class="mb-4 text-gray-500">No vehicles registered</p>
					<button
						onclick={openAddModal}
						class="rounded-lg bg-blue-600 px-6 py-3 font-medium text-white hover:bg-blue-700"
					>
						Add Your First Vehicle
					</button>
				</div>
			{/if}
		</div>
	{/if}
</div>

<!-- Add Vehicle Modal (placeholder) -->
{#if showAddModal}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
		onclick={() => (showAddModal = false)}
	>
		<div class="mx-4 w-full max-w-md rounded-2xl bg-white p-8" onclick={(e) => e.stopPropagation()}>
			<h2 class="mb-4 text-2xl font-bold">Add New Vehicle</h2>
			<p class="mb-4 text-gray-600">Vehicle registration form will be implemented here.</p>
			<button
				onclick={() => (showAddModal = false)}
				class="w-full rounded-lg bg-blue-600 py-3 font-medium text-white hover:bg-blue-700"
			>
				Close
			</button>
		</div>
	</div>
{/if}
