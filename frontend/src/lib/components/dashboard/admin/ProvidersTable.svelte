<script lang="ts">
	import api from '$lib/utils/api';
	import { adminStore } from '$lib/stores/dashboard';

	interface Provider {
		id: number;
		userId: number;
		name: string;
		contactName: string;
		email: string;
		status: string;
		rating: number;
		license: string;
		baseRate: number;
		services: string[];
		documents: string[];
	}

	let { providers } = $props<{ providers: Provider[] }>();

	let selectedProvider: Provider | null = $state(null);
	let showDetailsModal = $state(false);

	function openDetails(provider: Provider) {
		selectedProvider = provider;
		showDetailsModal = true;
	}

	function closeDetails() {
		showDetailsModal = false;
		selectedProvider = null;
	}

	async function verifyProvider(userId: number) {
		if (!confirm('Are you sure you want to verify this provider?')) return;
		try {
			await api.put(`/service-providers/${userId}/approve`);
			alert('Provider verified successfully.');
			closeDetails();
			await adminStore.load(true);
		} catch (e) {
			console.error('Failed to verify provider:', e);
			alert('Failed to verify provider. Ensure you have permissions.');
		}
	}
</script>

<div class="overflow-x-auto">
	<table class="min-w-full divide-y divide-gray-200">
		<thead class="bg-gray-50">
			<tr>
				<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
					>Business Name</th
				>
				<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
					>Contact Info</th
				>
				<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
					>Status</th
				>
				<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
					>Rating</th
				>
				<th class="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-gray-500"
					>Actions</th
				>
			</tr>
		</thead>
		<tbody class="divide-y divide-gray-200 bg-white">
			{#each providers as p}
				<tr class="transition-colors hover:bg-gray-50">
					<td class="whitespace-nowrap px-6 py-4">
						<div class="flex items-center">
							<div class="h-10 w-10 flex-shrink-0">
								<span
									class="flex h-10 w-10 items-center justify-center rounded-full bg-purple-100 font-bold text-purple-600"
								>
									<i class="fas fa-store"></i>
								</span>
							</div>
							<div class="ml-4">
								<div class="text-sm font-bold text-gray-900">{p.name}</div>
								<div class="text-xs text-gray-500">License: {p.license}</div>
							</div>
						</div>
					</td>
					<td class="whitespace-nowrap px-6 py-4">
						<div class="text-sm text-gray-900">{p.contactName}</div>
						<div class="text-sm text-gray-500">{p.email}</div>
					</td>
					<td class="whitespace-nowrap px-6 py-4">
						<span
							class={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${p.status === 'verified' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}
						>
							{p.status}
						</span>
					</td>
					<td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
						<div class="flex items-center">
							<i class="fas fa-star mr-1 text-yellow-400"></i>
							{p.rating}
						</div>
					</td>
					<td class="whitespace-nowrap px-6 py-4 text-right text-sm font-medium">
						<button
							class="font-medium text-red-600 hover:text-red-900"
							onclick={() => openDetails(p)}
						>
							Details
						</button>
					</td>
				</tr>
			{/each}
			{#if providers.length === 0}
				<tr>
					<td colspan="5" class="px-6 py-8 text-center text-gray-500">
						No service providers found.
					</td>
				</tr>
			{/if}
		</tbody>
	</table>
</div>

{#if showDetailsModal && selectedProvider}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-50 p-4"
		role="dialog"
		aria-modal="true"
	>
		<div class="w-full max-w-lg overflow-hidden rounded-2xl bg-white shadow-2xl">
			<!-- Modal Header -->
			<div class="bg-gradient-to-r from-red-600 to-orange-600 px-6 py-4">
				<div class="flex items-center justify-between">
					<h3 class="text-lg font-bold text-white">Application Details</h3>
					<button onclick={closeDetails} class="text-white hover:text-gray-200" aria-label="Close">
						<i class="fas fa-times text-xl"></i>
					</button>
				</div>
			</div>

			<!-- Modal Body -->
			<div class="space-y-4 p-6">
				<div>
					<p class="block text-sm font-medium text-gray-500">Identity</p>
					<div class="mt-1 flex items-center">
						<div
							class="flex h-12 w-12 items-center justify-center rounded-full bg-purple-100 font-bold text-purple-600"
						>
							{selectedProvider.name.charAt(0)}
						</div>
						<div class="ml-4">
							<h4 class="text-lg font-bold text-gray-900">{selectedProvider.name}</h4>
							<p class="text-sm text-gray-500">
								{selectedProvider.contactName} ({selectedProvider.email})
							</p>
						</div>
					</div>
				</div>

				<div class="grid grid-cols-2 gap-4">
					<div class="rounded-lg bg-gray-50 p-3">
						<p class="block text-xs font-medium text-gray-500">License Number</p>
						<p class="font-mono text-sm font-bold text-gray-900">{selectedProvider.license}</p>
					</div>
					<div class="rounded-lg bg-gray-50 p-3">
						<p class="block text-xs font-medium text-gray-500">Base Rate</p>
						<p class="text-sm font-bold text-green-600">₱{selectedProvider.baseRate}</p>
					</div>
				</div>

				<!-- Documents Section -->
				<div>
					<p class="mb-2 block text-xs font-medium text-gray-500">Submitted Documents</p>
					{#if selectedProvider.documents && selectedProvider.documents.length > 0}
						<ul class="space-y-2 rounded-lg bg-gray-50 p-2">
							{#each selectedProvider.documents as doc}
								<li>
									<a
										href={`http://localhost:8000${doc}`}
										target="_blank"
										class="flex items-center rounded-md bg-white p-2 text-sm text-red-600 shadow-sm hover:text-red-800"
									>
										<i class="fas fa-file-alt mr-2 text-gray-400"></i>
										<span class="truncate">{doc.split('/').pop()}</span>
										<i class="fas fa-external-link-alt ml-auto text-xs text-gray-400"></i>
									</a>
								</li>
							{/each}
						</ul>
					{:else}
						<p class="text-sm italic text-gray-400">No documents submitted.</p>
					{/if}
				</div>

				<div>
					<p class="block text-sm font-medium text-gray-500">Verification Status</p>
					<div class="mt-2 flex items-center justify-between">
						<span
							class={`inline-flex rounded-full px-3 py-1 text-sm font-semibold ${selectedProvider.status === 'verified' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}
						>
							{selectedProvider.status.toUpperCase()}
						</span>
						{#if selectedProvider.status === 'pending'}
							<button
								onclick={() => verifyProvider(selectedProvider!.userId)}
								class="rounded-lg bg-green-600 px-4 py-2 text-sm font-bold text-white shadow hover:bg-green-700"
							>
								Approve & Verify
							</button>
						{/if}
					</div>
				</div>
			</div>

			<!-- Modal Footer -->
			<div class="bg-gray-50 px-6 py-4 text-right">
				<button
					onclick={closeDetails}
					class="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-bold text-gray-700 hover:bg-gray-50"
				>
					Close
				</button>
			</div>
		</div>
	</div>
{/if}
