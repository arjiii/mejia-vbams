<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import api from '$lib/utils/api';

	let breakdownId = $derived($page.params.id);
	let breakdown: any = $state(null);
	let isLoading = $state(true);
	let error = $state('');
	let isEditing = $state(false);
	let isDeleting = $state(false);

	// Edit form state
	let editForm = $state({
		description: '',
		category: '',
		severity: '',
		status: ''
	});

	const statusColors: Record<string, string> = {
		reported: 'bg-yellow-100 text-yellow-800',
		assigned: 'bg-blue-100 text-blue-800',
		in_progress: 'bg-purple-100 text-purple-800',
		completed: 'bg-green-100 text-green-800',
		cancelled: 'bg-red-100 text-red-800'
	};

	const severityColors: Record<string, string> = {
		low: 'bg-gray-100 text-gray-800',
		medium: 'bg-yellow-100 text-yellow-800',
		high: 'bg-orange-100 text-orange-800',
		critical: 'bg-red-100 text-red-800'
	};

	onMount(async () => {
		await loadBreakdown();
	});

	async function loadBreakdown() {
		isLoading = true;
		try {
			const res = await api.get(`/breakdowns/${breakdownId}`);
			breakdown = res.data;
			// Initialize edit form
			editForm = {
				description: breakdown.description || '',
				category: breakdown.category || '',
				severity: breakdown.severity || '',
				status: breakdown.status || ''
			};
		} catch (e: any) {
			console.error('Failed to load breakdown', e);
			error = e.response?.data?.detail || 'Failed to load breakdown details';
		} finally {
			isLoading = false;
		}
	}

	async function handleUpdate() {
		try {
			await api.put(`/breakdowns/${breakdownId}`, editForm);
			alert('Breakdown updated successfully!');
			isEditing = false;
			await loadBreakdown();
		} catch (e: any) {
			console.error('Update failed', e);
			alert(e.response?.data?.detail || 'Failed to update breakdown');
		}
	}

	async function handleDelete() {
		if (
			!confirm(
				'Are you sure you want to delete this breakdown report? This action cannot be undone.'
			)
		) {
			return;
		}

		isDeleting = true;
		try {
			await api.delete(`/breakdowns/${breakdownId}`);
			alert('Breakdown deleted successfully!');
			goto('/breakdowns');
		} catch (e: any) {
			console.error('Delete failed', e);
			alert(e.response?.data?.detail || 'Failed to delete breakdown');
			isDeleting = false;
		}
	}

	function formatDate(dateString: string) {
		return new Date(dateString).toLocaleString();
	}
</script>

<svelte:head>
	<title>Breakdown Details - VBAMS</title>
</svelte:head>

<div class="mx-auto max-w-5xl px-4 py-8">
	<!-- Header -->
	<div class="mb-6 flex items-center justify-between">
		<div>
			<button
				onclick={() => goto('/breakdowns')}
				class="mb-2 flex items-center text-sm text-gray-600 hover:text-gray-900"
			>
				<i class="fas fa-arrow-left mr-2"></i>
				Back to Breakdown History
			</button>
			<h1 class="text-3xl font-bold text-gray-900">Breakdown Details</h1>
		</div>

		{#if breakdown && !isEditing}
			<div class="flex gap-2">
				<button
					onclick={() => (isEditing = true)}
					class="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
				>
					<i class="fas fa-edit mr-2"></i>Edit
				</button>
				<button
					onclick={handleDelete}
					disabled={isDeleting}
					class="rounded-lg bg-red-600 px-4 py-2 text-white hover:bg-red-700 disabled:opacity-50"
				>
					<i class="fas fa-trash mr-2"></i>
					{isDeleting ? 'Deleting...' : 'Delete'}
				</button>
			</div>
		{/if}
	</div>

	{#if isLoading}
		<div class="text-center">
			<i class="fas fa-spinner fa-spin text-4xl text-gray-400"></i>
			<p class="mt-4 text-gray-600">Loading breakdown details...</p>
		</div>
	{:else if error}
		<div class="rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
			<i class="fas fa-exclamation-circle mr-2"></i>{error}
		</div>
	{:else if breakdown}
		{#if isEditing}
			<!-- Edit Form -->
			<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
				<h2 class="mb-4 text-xl font-bold">Edit Breakdown</h2>

				<div class="space-y-4">
					<div>
						<label class="mb-2 block text-sm font-semibold text-gray-700">Description</label>
						<textarea
							bind:value={editForm.description}
							rows="3"
							class="w-full rounded-lg border border-gray-300 p-3 focus:border-blue-500 focus:outline-none"
						></textarea>
					</div>

					<div class="grid gap-4 md:grid-cols-3">
						<div>
							<label class="mb-2 block text-sm font-semibold text-gray-700">Category</label>
							<select
								bind:value={editForm.category}
								class="w-full rounded-lg border border-gray-300 p-2.5"
							>
								<option value="mechanical">Mechanical</option>
								<option value="electrical">Electrical</option>
								<option value="tire">Tire</option>
								<option value="fuel">Fuel</option>
								<option value="accident">Accident</option>
								<option value="other">Other</option>
							</select>
						</div>

						<div>
							<label class="mb-2 block text-sm font-semibold text-gray-700">Severity</label>
							<select
								bind:value={editForm.severity}
								class="w-full rounded-lg border border-gray-300 p-2.5"
							>
								<option value="low">Low</option>
								<option value="medium">Medium</option>
								<option value="high">High</option>
								<option value="critical">Critical</option>
							</select>
						</div>

						<div>
							<label class="mb-2 block text-sm font-semibold text-gray-700">Status</label>
							<select
								bind:value={editForm.status}
								class="w-full rounded-lg border border-gray-300 p-2.5"
							>
								<option value="reported">Reported</option>
								<option value="assigned">Assigned</option>
								<option value="in_progress">In Progress</option>
								<option value="completed">Completed</option>
								<option value="cancelled">Cancelled</option>
							</select>
						</div>
					</div>

					<div class="flex gap-2 pt-4">
						<button
							onclick={handleUpdate}
							class="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-700"
						>
							Save Changes
						</button>
						<button
							onclick={() => (isEditing = false)}
							class="rounded-lg border border-gray-300 px-6 py-2 text-gray-700 hover:bg-gray-50"
						>
							Cancel
						</button>
					</div>
				</div>
			</div>
		{:else}
			<!-- View Mode -->
			<div class="grid gap-6 lg:grid-cols-3">
				<!-- Main Info -->
				<div class="space-y-6 lg:col-span-2">
					<!-- Status Card -->
					<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
						<div class="mb-4 flex items-start justify-between">
							<div>
								<h2 class="text-2xl font-bold capitalize text-gray-900">
									{breakdown.category} Issue
								</h2>
								<p class="mt-1 text-sm text-gray-600">
									Reported on {formatDate(breakdown.created_at)}
								</p>
							</div>
							<div class="flex gap-2">
								<span
									class={`rounded-full px-3 py-1 text-sm font-medium ${statusColors[breakdown.status]}`}
								>
									{breakdown.status.replace('_', ' ').toUpperCase()}
								</span>
								<span
									class={`rounded-full px-3 py-1 text-sm font-medium ${severityColors[breakdown.severity]}`}
								>
									{breakdown.severity.toUpperCase()}
								</span>
							</div>
						</div>

						<div class="border-t border-gray-200 pt-4">
							<h3 class="mb-2 font-semibold text-gray-900">Description</h3>
							<p class="text-gray-700">{breakdown.description}</p>
						</div>
					</div>

					<!-- Location Card -->
					<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
						<h3 class="mb-4 text-lg font-bold text-gray-900">Location</h3>
						<div class="space-y-2">
							<p class="text-sm text-gray-600">
								<i class="fas fa-map-marker-alt mr-2 text-red-600"></i>
								{breakdown.address}
							</p>
							<p class="text-sm text-gray-600">
								<i class="fas fa-location-arrow mr-2 text-blue-600"></i>
								Coordinates: {breakdown.latitude}, {breakdown.longitude}
							</p>
						</div>
					</div>

					<!-- Costs Card -->
					{#if breakdown.estimated_cost || breakdown.actual_cost}
						<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
							<h3 class="mb-4 text-lg font-bold text-gray-900">Cost Information</h3>
							<div class="grid gap-4 md:grid-cols-2">
								<div>
									<p class="text-sm text-gray-600">Estimated Cost</p>
									<p class="text-2xl font-bold text-gray-900">
										₱{breakdown.estimated_cost.toFixed(2)}
									</p>
								</div>
								<div>
									<p class="text-sm text-gray-600">Actual Cost</p>
									<p class="text-2xl font-bold text-green-600">
										₱{breakdown.actual_cost.toFixed(2)}
									</p>
								</div>
							</div>
						</div>
					{/if}
				</div>

				<!-- Sidebar -->
				<div class="space-y-6">
					<!-- Quick Info -->
					<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
						<h3 class="mb-4 text-lg font-bold text-gray-900">Quick Info</h3>
						<div class="space-y-3 text-sm">
							<div>
								<p class="text-gray-600">Breakdown ID</p>
								<p class="font-medium text-gray-900">#{breakdown.id}</p>
							</div>
							<div>
								<p class="text-gray-600">Vehicle ID</p>
								<p class="font-medium text-gray-900">#{breakdown.vehicle_id}</p>
							</div>
							<div>
								<p class="text-gray-600">Resolved</p>
								<p class="font-medium">
									{#if breakdown.is_resolved}
										<span class="text-green-600"><i class="fas fa-check-circle mr-1"></i>Yes</span>
									{:else}
										<span class="text-yellow-600"><i class="fas fa-clock mr-1"></i>Pending</span>
									{/if}
								</p>
							</div>
						</div>
					</div>

					<!-- Timeline -->
					<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
						<h3 class="mb-4 text-lg font-bold text-gray-900">Timeline</h3>
						<div class="space-y-3 text-sm">
							<div>
								<p class="text-gray-600">Reported</p>
								<p class="font-medium text-gray-900">{formatDate(breakdown.created_at)}</p>
							</div>
							{#if breakdown.updated_at}
								<div>
									<p class="text-gray-600">Last Updated</p>
									<p class="font-medium text-gray-900">{formatDate(breakdown.updated_at)}</p>
								</div>
							{/if}
							{#if breakdown.actual_completion_time}
								<div>
									<p class="text-gray-600">Completed</p>
									<p class="font-medium text-green-600">
										{formatDate(breakdown.actual_completion_time)}
									</p>
								</div>
							{/if}
						</div>
					</div>

					<!-- Rating -->
					{#if breakdown.rating}
						<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
							<h3 class="mb-4 text-lg font-bold text-gray-900">Rating & Feedback</h3>
							<div class="mb-3">
								<div class="flex items-center">
									{#each Array(5) as _, i}
										<i
											class={`fas fa-star ${i < breakdown.rating ? 'text-yellow-400' : 'text-gray-300'}`}
										></i>
									{/each}
									<span class="ml-2 text-sm font-medium text-gray-700">{breakdown.rating}/5</span>
								</div>
							</div>
							{#if breakdown.feedback}
								<p class="text-sm text-gray-700">{breakdown.feedback}</p>
							{/if}
						</div>
					{/if}
				</div>
			</div>
		{/if}
	{/if}
</div>
