<script module>
	import { invalidateAll } from '$app/navigation';

	async function updateProviderStatus(userId: number, action: string) {
		// Placeholder for direct status updates if needed
	}
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { adminStore } from '$lib/stores/dashboard';
	import api from '$lib/utils/api';

	interface Provider {
		id: number;
		userId: number;
		businessName: string;
		email: string;
		phone: string;
		status: string;
		rating: number;
		completedJobs: number;
		joined: string;
		documents: string[];
		license: string;
		baseRate: number;
		services: string[];
	}

	let providers = $derived(($adminStore.data?.providers as unknown as Provider[]) || []);
	let filteredProviders: Provider[] = $state([]);
	let searchQuery = $state('');
	let filterStatus = $state('all');

	let showDetailsModal = $state(false);
	let selectedProvider: any = $state(null);

	onMount(() => {
		adminStore.load();
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

	async function verifyProviderAction(userId: number) {
		if (!confirm('Are you sure you want to verify this provider?')) return;
		try {
			await api.put(`/service-providers/${userId}/approve`);
			alert('Provider verified successfully');
			showDetailsModal = false;
			// Reload page data
			adminStore.load(true);
		} catch (e) {
			console.error('Failed to verify:', e);
			alert('Failed to verify provider');
		}
	}

	function openDetails(provider: Provider) {
		selectedProvider = provider;
		showDetailsModal = true;
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
		<div class="flex items-center space-x-2">
			<button
				onclick={() => adminStore.load(true)}
				class="h-10 w-10 rounded-lg bg-gray-100 text-gray-600 hover:bg-gray-200"
				title="Refresh Data"
			>
				<i class="fas fa-sync-alt"></i>
			</button>
			<button
				class="rounded-lg bg-gradient-to-r from-purple-600 to-purple-700 px-4 py-2 text-sm font-bold text-white shadow-lg transition-all hover:from-purple-700 hover:to-purple-800"
			>
				<i class="fas fa-plus mr-2"></i>
				Add Provider
			</button>
		</div>
	</div>

	<!-- Filters -->
	<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-lg">
		<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
			<div>
				<label for="searchProviders" class="mb-2 block text-sm font-medium text-gray-700"
					>Search Providers</label
				>
				<div class="relative">
					<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
						<i class="fas fa-search text-gray-400"></i>
					</div>
					<input
						id="searchProviders"
						type="text"
						bind:value={searchQuery}
						placeholder="Search by business name or email..."
						class="block w-full rounded-lg border border-gray-300 py-2 pl-10 pr-3 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
					/>
				</div>
			</div>
			<div>
				<label for="filterStatus" class="mb-2 block text-sm font-medium text-gray-700"
					>Filter by Status</label
				>
				<select
					id="filterStatus"
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
						<button
							onclick={() => openDetails(provider)}
							class="flex-1 rounded-lg border-2 border-purple-500 bg-purple-50 px-3 py-2 text-sm font-bold text-purple-700 transition-all hover:bg-purple-100"
						>
							<i class="fas fa-eye mr-1"></i>
							Review Application
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

<!-- Details Modal -->
{#if showDetailsModal && selectedProvider}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4 backdrop-blur-sm"
	>
		<div class="max-h-[90vh] w-full max-w-lg overflow-y-auto rounded-2xl bg-white shadow-2xl">
			<div class="bg-gradient-to-r from-purple-600 to-pink-600 p-6 text-white">
				<h2 class="text-2xl font-bold">{selectedProvider.businessName}</h2>
				<p class="opacity-90">Provider Details</p>
			</div>

			<div class="space-y-4 p-6">
				<div class="grid grid-cols-2 gap-4">
					<div>
						<p class="text-xs text-gray-500">Contact Email</p>
						<p class="font-medium">{selectedProvider.email}</p>
					</div>
					<div>
						<p class="text-xs text-gray-500">Phone</p>
						<p class="font-medium">{selectedProvider.phone}</p>
					</div>
					<div>
						<p class="text-xs text-gray-500">Status</p>
						<span
							class={`inline-flex rounded-full px-2 py-1 text-xs font-bold ${selectedProvider.status === 'verified' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}
						>
							{selectedProvider.status.toUpperCase()}
						</span>
					</div>
					<div>
						<p class="text-xs text-gray-500">Joined</p>
						<p class="font-medium">{new Date(selectedProvider.joined).toLocaleDateString()}</p>
					</div>
				</div>

				<div class="border-t border-gray-100 pt-4">
					<h3 class="mb-3 font-bold text-gray-900">Application Details</h3>
					<div class="grid grid-cols-1 gap-4 rounded-lg bg-gray-50 p-4">
						<div>
							<p class="text-xs text-gray-500">Business License</p>
							<p class="font-mono text-sm font-medium text-gray-900">
								{selectedProvider.license || 'N/A'}
							</p>
						</div>
						<div>
							<p class="text-xs text-gray-500">Services Offered</p>
							<div class="mt-1 flex flex-wrap gap-2">
								{#each selectedProvider.services as service}
									<span
										class="inline-flex rounded-full bg-blue-100 px-2 py-0.5 text-xs text-blue-800"
									>
										{service}
									</span>
								{/each}
								{#if selectedProvider.services.length === 0}
									<span class="text-xs text-gray-500">None listed</span>
								{/if}
							</div>
						</div>
						<div>
							<p class="text-xs text-gray-500">Base Rate</p>
							<p class="font-medium text-green-600">₱{selectedProvider.baseRate}</p>
						</div>
					</div>
				</div>

				<div class="border-t border-gray-100 pt-4">
					<h3 class="mb-3 font-bold text-gray-900">Submitted Documents</h3>
					{#if selectedProvider.documents.length > 0}
						<ul class="space-y-2">
							{#each selectedProvider.documents as doc}
								<li>
									<a
										href={`http://localhost:8000${doc}`}
										target="_blank"
										class="flex items-center rounded-lg border border-gray-200 p-3 hover:bg-gray-50"
									>
										<i class="fas fa-file-alt mr-3 text-purple-600"></i>
										<span class="truncate text-sm font-medium text-blue-600"
											>{doc.split('/').pop()}</span
										>
										<i class="fas fa-external-link-alt ml-auto text-xs text-gray-400"></i>
									</a>
								</li>
							{/each}
						</ul>
					{:else}
						<p class="text-sm italic text-gray-500">No documents submitted.</p>
					{/if}
				</div>
			</div>

			<div class="flex justify-end space-x-3 bg-gray-50 p-6">
				<button
					onclick={() => (showDetailsModal = false)}
					class="rounded-lg px-4 py-2 text-gray-600 hover:bg-gray-200"
				>
					Close
				</button>
				{#if selectedProvider.status === 'pending'}
					<button
						onclick={() => verifyProviderAction(selectedProvider!.userId)}
						class="rounded-lg bg-green-600 px-4 py-2 font-bold text-white hover:bg-green-700"
					>
						Verify Provider
					</button>
				{/if}
			</div>
		</div>
	</div>
{/if}
