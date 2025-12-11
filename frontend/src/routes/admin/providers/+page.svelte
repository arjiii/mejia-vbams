<script lang="ts">
	import { onMount } from 'svelte';

	interface Provider {
		id: number;
		businessName: string;
		email: string;
		phone: string;
		status: string;
		rating: number;
		completedJobs: number;
		joined: string;
	}

	let providers: Provider[] = $state([]);
	let filteredProviders: Provider[] = $state([]);
	let searchQuery = $state('');
	let filterStatus = $state('all');

	onMount(() => {
		providers = [
			{
				id: 1,
				businessName: 'Quick Fix Auto',
				email: 'contact@quickfix.com',
				phone: '+1234567800',
				status: 'verified',
				rating: 4.8,
				completedJobs: 156,
				joined: '2023-06-15'
			},
			{
				id: 2,
				businessName: 'Mobile Mechanic Pro',
				email: 'mike@mobilemech.com',
				phone: '+1234567801',
				status: 'pending',
				rating: 0.0,
				completedJobs: 0,
				joined: '2024-11-20'
			},
			{
				id: 3,
				businessName: 'Road Rescue Services',
				email: 'info@roadrescue.com',
				phone: '+1234567802',
				status: 'verified',
				rating: 4.5,
				completedJobs: 98,
				joined: '2023-09-10'
			},
			{
				id: 4,
				businessName: 'Emergency Tow',
				email: 'support@emergtow.com',
				phone: '+1234567803',
				status: 'verified',
				rating: 4.9,
				completedJobs: 234,
				joined: '2023-03-22'
			}
		];
		filteredProviders = providers;
	});

	function searchProviders() {
		filteredProviders = providers.filter((p) => {
			const matchesSearch =
				p.businessName.toLowerCase().includes(searchQuery.toLowerCase()) ||
				p.email.toLowerCase().includes(searchQuery.toLowerCase());
			const matchesStatus = filterStatus === 'all' || p.status === filterStatus;
			return matchesSearch && matchesStatus;
		});
	}

	$effect(() => {
		searchQuery;
		filterStatus;
		searchProviders();
	});

	function approveProvider(id: number) {
		console.log('Approving provider:', id);
		// Update provider status
	}
</script>

<svelte:head>
	<title>Manage Providers - VBAMS</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold text-gray-900">Manage Service Providers</h1>
			<p class="mt-2 text-sm text-gray-600">Verify and manage service provider accounts</p>
		</div>
		<button
			class="rounded-lg bg-gradient-to-r from-purple-600 to-purple-700 px-4 py-2 text-sm font-bold text-white shadow-lg transition-all hover:from-purple-700 hover:to-purple-800"
		>
			<i class="fas fa-plus mr-2"></i>
			Add Provider
		</button>
	</div>

	<!-- Filters -->
	<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-lg">
		<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700">Search Providers</label>
				<div class="relative">
					<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
						<i class="fas fa-search text-gray-400"></i>
					</div>
					<input
						type="text"
						bind:value={searchQuery}
						placeholder="Search by business name or email..."
						class="block w-full rounded-lg border border-gray-300 py-2 pl-10 pr-3 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
					/>
				</div>
			</div>
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700">Filter by Status</label>
				<select
					bind:value={filterStatus}
					class="block w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
				>
					<option value="all">All Status</option>
					<option value="verified">Verified</option>
					<option value="pending">Pending</option>
					<option value="suspended">Suspended</option>
				</select>
			</div>
		</div>
	</div>

	<!-- Providers Grid -->
	<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
		{#each filteredProviders as provider}
			<div
				class="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-lg transition-all hover:shadow-xl"
			>
				<div class="bg-gradient-to-r from-purple-600 to-pink-600 p-4">
					<div class="flex items-center justify-between">
						<div class="flex h-12 w-12 items-center justify-center rounded-full bg-white">
							<i class="fas fa-store text-2xl text-purple-600"></i>
						</div>
						<span
							class={`rounded-full px-3 py-1 text-xs font-bold ${provider.status === 'verified' ? 'bg-green-500 text-white' : provider.status === 'pending' ? 'bg-yellow-500 text-white' : 'bg-red-500 text-white'}`}
						>
							{provider.status.toUpperCase()}
						</span>
					</div>
				</div>

				<div class="p-6">
					<h3 class="text-lg font-bold text-gray-900">{provider.businessName}</h3>
					<div class="mt-4 space-y-2">
						<div class="flex items-center text-sm text-gray-600">
							<i class="fas fa-envelope w-5 text-gray-400"></i>
							<span class="ml-2">{provider.email}</span>
						</div>
						<div class="flex items-center text-sm text-gray-600">
							<i class="fas fa-phone w-5 text-gray-400"></i>
							<span class="ml-2">{provider.phone}</span>
						</div>
						<div class="flex items-center text-sm text-gray-600">
							<i class="fas fa-calendar w-5 text-gray-400"></i>
							<span class="ml-2">Joined {new Date(provider.joined).toLocaleDateString()}</span>
						</div>
					</div>

					<div class="mt-4 grid grid-cols-2 gap-4 rounded-lg bg-gray-50 p-3">
						<div class="text-center">
							<div class="text-2xl font-bold text-gray-900">{provider.completedJobs}</div>
							<div class="text-xs text-gray-500">Jobs</div>
						</div>
						<div class="text-center">
							<div class="text-2xl font-bold text-gray-900">
								{provider.rating > 0 ? provider.rating : 'N/A'}
							</div>
							<div class="text-xs text-gray-500">Rating</div>
						</div>
					</div>

					<div class="mt-4 flex gap-2">
						{#if provider.status === 'pending'}
							<button
								onclick={() => approveProvider(provider.id)}
								class="flex-1 rounded-lg bg-green-600 px-3 py-2 text-sm font-bold text-white transition-colors hover:bg-green-700"
							>
								<i class="fas fa-check mr-1"></i>
								Approve
							</button>
						{/if}
						<button
							class="flex-1 rounded-lg border-2 border-gray-200 px-3 py-2 text-sm font-medium text-gray-700 transition-all hover:border-purple-500 hover:text-purple-600"
						>
							<i class="fas fa-eye mr-1"></i>
							View Details
						</button>
					</div>
				</div>
			</div>
		{/each}

		{#if filteredProviders.length === 0}
			<div class="col-span-full flex flex-col items-center py-12">
				<i class="fas fa-store mb-4 text-6xl text-gray-300"></i>
				<p class="text-gray-500">No providers found</p>
			</div>
		{/if}
	</div>
</div>
