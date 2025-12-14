<script lang="ts">
	import { onMount } from 'svelte';
	import api from '$lib/utils/api';

	let providers: any[] = $state([]);
	let filteredProviders: any[] = $state([]);
	let isLoading = $state(true);
	let searchQuery = $state('');
	let filterStatus = $state('all');

	onMount(async () => {
		await loadProviders();
	});

	async function loadProviders() {
		isLoading = true;
		try {
			const res = await api.get('/service-providers/');
			providers = res.data;
			applyFilters();
		} catch (e) {
			console.error('Failed to load providers', e);
		} finally {
			isLoading = false;
		}
	}

	function applyFilters() {
		filteredProviders = providers.filter((provider) => {
			const matchesSearch =
				!searchQuery ||
				provider.business_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
				provider.user?.first_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
				provider.user?.last_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
				provider.user?.email?.toLowerCase().includes(searchQuery.toLowerCase());

			const matchesStatus =
				filterStatus === 'all' ||
				(filterStatus === 'verified' && provider.is_verified) ||
				(filterStatus === 'pending' && !provider.is_verified && provider.is_active) ||
				(filterStatus === 'suspended' && !provider.is_active);

			return matchesSearch && matchesStatus;
		});
	}

	$effect(() => {
		searchQuery;
		filterStatus;
		applyFilters();
	});

	async function handleApprove(userId: number, businessName: string) {
		if (!confirm(`Approve ${businessName} as a verified service provider?`)) return;

		try {
			await api.put(`/service-providers/${userId}/approve`);
			alert('Service provider approved successfully!');
			await loadProviders();
		} catch (e: any) {
			alert(e.response?.data?.detail || 'Failed to approve provider');
		}
	}

	async function handleSuspend(userId: number, businessName: string) {
		if (!confirm(`Suspend ${businessName}?`)) return;

		try {
			await api.put(`/service-providers/${userId}/suspend`);
			alert('Service provider suspended successfully!');
			await loadProviders();
		} catch (e: any) {
			alert(e.response?.data?.detail || 'Failed to suspend provider');
		}
	}

	async function handleDelete(userId: number, businessName: string) {
		if (!confirm(`⚠️ PERMANENTLY DELETE ${businessName}?\n\nThis cannot be undone!`)) return;

		try {
			await api.delete(`/service-providers/${userId}`);
			alert('Service provider deleted successfully!');
			await loadProviders();
		} catch (e: any) {
			alert(e.response?.data?.detail || 'Failed to delete provider');
		}
	}
</script>

<svelte:head>
	<title>Provider Management - Admin - VBAMS</title>
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8">
	<div class="mb-8">
		<h1 class="text-3xl font-bold text-gray-900">Service Provider Management</h1>
		<p class="mt-2 text-gray-600">Approve, suspend, or manage service providers</p>
	</div>

	<!-- Filters -->
	<div class="mb-6 rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
		<div class="grid gap-4 md:grid-cols-[1fr_auto_auto]">
			<div class="relative">
				<i class="fas fa-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
				<input
					type="text"
					bind:value={searchQuery}
					placeholder="Search providers..."
					class="w-full rounded-lg border border-gray-300 py-2 pl-10 pr-4"
				/>
			</div>

			<select bind:value={filterStatus} class="rounded-lg border border-gray-300 px-4 py-2">
				<option value="all">All Status</option>
				<option value="verified">Verified</option>
				<option value="pending">Pending Approval</option>
				<option value="suspended">Suspended</option>
			</select>

			<button
				onclick={loadProviders}
				class="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
			>
				<i class="fas fa-sync-alt mr-2"></i> Refresh
			</button>
		</div>

		<div class="mt-3 text-sm text-gray-600">
			Showing {filteredProviders.length} of {providers.length} providers
		</div>
	</div>

	{#if isLoading}
		<div class="text-center">
			<i class="fas fa-spinner fa-spin text-4xl text-gray-400"></i>
			<p class="mt-4 text-gray-600">Loading providers...</p>
		</div>
	{:else if filteredProviders.length === 0}
		<div class="rounded-xl border border-gray-200 bg-white p-12 text-center shadow-sm">
			<i class="fas fa-store text-6xl text-gray-300"></i>
			<p class="mt-4 text-lg text-gray-600">No providers found</p>
		</div>
	{:else}
		<div class="grid gap-6">
			{#each filteredProviders as provider}
				<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
					<div class="flex items-start justify-between">
						<div class="flex-1">
							<div class="flex items-center gap-3">
								<h3 class="text-xl font-bold text-gray-900">{provider.business_name}</h3>
								{#if provider.is_verified}
									<span
										class="rounded-full bg-green-100 px-3 py-1 text-xs font-medium text-green-800"
									>
										<i class="fas fa-check-circle mr-1"></i> Verified
									</span>
								{:else if provider.is_active}
									<span
										class="rounded-full bg-yellow-100 px-3 py-1 text-xs font-medium text-yellow-800"
									>
										<i class="fas fa-clock mr-1"></i> Pending Approval
									</span>
								{:else}
									<span class="rounded-full bg-red-100 px-3 py-1 text-xs font-medium text-red-800">
										<i class="fas fa-ban mr-1"></i> Suspended
									</span>
								{/if}
								{#if provider.is_online}
									<span
										class="rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-800"
									>
										<i class="fas fa-circle mr-1 text-xs"></i> Online
									</span>
								{/if}
							</div>

							<div class="mt-4 grid gap-4 md:grid-cols-2">
								<div>
									<p class="text-sm text-gray-600">Owner</p>
									<p class="font-medium text-gray-900">
										{provider.user.first_name}
										{provider.user.last_name}
									</p>
									<p class="text-sm text-gray-600">{provider.user.email}</p>
									<p class="text-sm text-gray-600">{provider.user.phone}</p>
								</div>

								<div>
									<p class="text-sm text-gray-600">Business License</p>
									<p class="font-medium text-gray-900">{provider.business_license}</p>
								</div>

								<div>
									<p class="text-sm text-gray-600">Services</p>
									<div class="mt-1 flex flex-wrap gap-1">
										{#each provider.services as service}
											<span class="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-700">
												{service.replace('_', ' ')}
											</span>
										{/each}
									</div>
								</div>

								<div>
									<p class="text-sm text-gray-600">Rates</p>
									<p class="text-sm text-gray-900">Base: ₱{provider.base_rate}</p>
									<p class="text-sm text-gray-900">Per km: ₱{provider.per_km_rate}</p>
									<p class="text-sm text-gray-900">Hourly: ₱{provider.hourly_rate}</p>
								</div>

								<div>
									<p class="text-sm text-gray-600">Rating</p>
									<div class="flex items-center">
										<span class="font-medium text-gray-900"
											>{provider.average_rating.toFixed(1)}</span
										>
										<i class="fas fa-star ml-1 text-yellow-400"></i>
										<span class="ml-1 text-sm text-gray-600">({provider.rating_count} reviews)</span
										>
									</div>
								</div>

								<div>
									<p class="text-sm text-gray-600">Service Radius</p>
									<p class="font-medium text-gray-900">{provider.service_radius} km</p>
								</div>
							</div>
						</div>

						<div class="ml-6 flex flex-col gap-2">
							{#if !provider.is_verified && provider.is_active}
								<button
									onclick={() => handleApprove(provider.user_id, provider.business_name)}
									class="rounded-lg bg-green-600 px-4 py-2 text-sm text-white hover:bg-green-700"
								>
									<i class="fas fa-check mr-2"></i> Approve
								</button>
							{/if}

							{#if provider.is_active}
								<button
									onclick={() => handleSuspend(provider.user_id, provider.business_name)}
									class="rounded-lg bg-yellow-600 px-4 py-2 text-sm text-white hover:bg-yellow-700"
								>
									<i class="fas fa-ban mr-2"></i> Suspend
								</button>
							{/if}

							<button
								onclick={() => handleDelete(provider.user_id, provider.business_name)}
								class="rounded-lg bg-red-600 px-4 py-2 text-sm text-white hover:bg-red-700"
							>
								<i class="fas fa-trash mr-2"></i> Delete
							</button>
						</div>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>
