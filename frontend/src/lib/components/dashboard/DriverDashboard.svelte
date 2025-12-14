<script lang="ts">
	import { onMount } from 'svelte';
	import { user } from '$lib/stores/auth';
	import api from '$lib/utils/api';
	import StatsCard from '$lib/components/common/StatsCard.svelte';

	interface Breakdown {
		id: number;
		vehicle_id: number;
		category: string;
		description: string;
		status: string;
		created_at: string;
		address: string;
	}

	import { driverStore } from '$lib/stores/dashboard';

	let vehicleCount = $derived($driverStore.data?.vehicleCount || 0);
	let breakdownCount = $derived($driverStore.data?.breakdownCount || 0);
	let assistanceCount = $derived($driverStore.data?.assistanceCount || 0);
	let recentBreakdowns = $derived($driverStore.data?.recentBreakdowns || []);
	let loading = $derived($driverStore.loading);

	onMount(() => {
		driverStore.load();
	});

	function getStatusColor(status: string) {
		const colors: Record<string, string> = {
			reported: 'bg-gray-100 text-gray-800',
			assigned: 'bg-yellow-100 text-yellow-800',
			in_progress: 'bg-blue-100 text-blue-800',
			completed: 'bg-green-100 text-green-800',
			cancelled: 'bg-red-100 text-red-800'
		};
		return colors[status] || 'bg-gray-100 text-gray-800';
	}
</script>

{#if loading}
	<div class="flex h-64 items-center justify-center">
		<div class="h-32 w-32 animate-spin rounded-full border-b-2 border-blue-600"></div>
	</div>
{:else}
	<div class="space-y-6">
		<!-- Welcome Section -->
		<div class="rounded-2xl bg-gradient-to-r from-blue-600 to-cyan-600 p-6 text-white shadow-lg">
			<div class="flex items-center justify-between">
				<div>
					<h1 class="text-3xl font-bold">
						Welcome back{#if $user}, {$user.first_name}{/if}!
					</h1>
					<p class="mt-1 text-blue-100">Here's your vehicle and breakdown status</p>
				</div>
				<div class="hidden md:block">
					<i class="fas fa-car text-6xl opacity-30"></i>
				</div>
			</div>
		</div>

		<!-- Stats Grid -->
		<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
			<StatsCard title="Total Vehicles" value={vehicleCount} icon="fa-car" color="blue" />
			<StatsCard
				title="Breakdowns"
				value={breakdownCount}
				icon="fa-exclamation-triangle"
				color="yellow"
			/>
			<StatsCard
				title="Assistance Requests"
				value={assistanceCount}
				icon="fa-handshake"
				color="green"
			/>
			<StatsCard
				title="Location Status"
				value="Online"
				icon="fa-map-marker-alt"
				color="purple"
				description="GPS is active"
			/>
		</div>

		<!-- Main Content Grid -->
		<div class="grid grid-cols-1 gap-8 lg:grid-cols-3">
			<!-- Recent Breakdowns -->
			<div class="lg:col-span-2">
				<div class="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-lg">
					<div class="flex items-center justify-between border-b border-gray-100 px-6 py-5">
						<h3 class="text-lg font-bold leading-6 text-gray-900">Recent Breakdowns</h3>
						<a href="/breakdowns" class="text-sm font-medium text-blue-600 hover:text-blue-500"
							>View all</a
						>
					</div>
					<div class="px-6 py-6">
						{#if recentBreakdowns.length === 0}
							<div class="py-10 text-center">
								<div
									class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-gray-50"
								>
									<i class="fas fa-car-crash text-2xl text-gray-400"></i>
								</div>
								<p class="mb-4 text-gray-500">No recent breakdowns reported</p>
								<a
									href="/assistance"
									class="inline-flex items-center rounded-lg border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-700 transition-colors hover:bg-blue-200"
								>
									<i class="fas fa-plus mr-2"></i>
									Request Assistance
								</a>
							</div>
						{:else}
							<div class="space-y-4">
								{#each recentBreakdowns as breakdown}
									<div
										class="group rounded-lg border border-gray-200 p-4 transition-all duration-200 hover:border-blue-300 hover:shadow-md"
									>
										<div class="flex items-center justify-between">
											<div class="flex items-start space-x-4">
												<div class="mt-1 flex-shrink-0">
													<span
														class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 text-blue-600"
													>
														<i class="fas fa-tools"></i>
													</span>
												</div>
												<div>
													<h4 class="text-sm font-bold text-gray-900">
														{breakdown.category.charAt(0).toUpperCase() +
															breakdown.category.slice(1)} Breakdown
													</h4>
													<p class="mt-1 line-clamp-2 text-sm text-gray-600">
														{breakdown.description}
													</p>
													<div class="mt-2 flex items-center space-x-4 text-xs text-gray-500">
														<span class="flex items-center">
															<i class="fas fa-map-marker-alt mr-1.5 text-gray-400"></i>
															{breakdown.address}
														</span>
														<span class="flex items-center">
															<i class="far fa-clock mr-1.5 text-gray-400"></i>
															{new Date(breakdown.created_at).toLocaleDateString()}
														</span>
													</div>
												</div>
											</div>
											<div class="ml-4 flex-shrink-0">
												<span
													class="inline-flex items-center rounded-full px-3 py-1 text-xs font-medium {getStatusColor(
														breakdown.status
													)}"
												>
													{breakdown.status.replace('_', ' ')}
												</span>
											</div>
										</div>
									</div>
								{/each}
							</div>
						{/if}
					</div>
				</div>
			</div>

			<!-- Quick Actions -->
			<div class="lg:col-span-1">
				<div class="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-lg">
					<div class="border-b border-gray-100 px-6 py-5">
						<h3 class="text-lg font-bold leading-6 text-gray-900">Quick Actions</h3>
					</div>
					<div class="space-y-4 p-6">
						<a
							href="/assistance"
							class="flex w-full transform items-center justify-between rounded-lg border border-transparent bg-gradient-to-r from-blue-600 to-blue-700 px-4 py-3 text-sm font-medium text-white shadow-md transition-all duration-200 hover:-translate-y-0.5 hover:from-blue-700 hover:to-blue-800"
						>
							<span class="flex items-center">
								<i class="fas fa-plus-circle mr-3 text-lg"></i>
								Request Assistance
							</span>
							<i class="fas fa-chevron-right opacity-50"></i>
						</a>
						<a
							href="/vehicles/new"
							class="flex w-full items-center justify-between rounded-lg border border-gray-200 bg-white px-4 py-3 text-sm font-medium text-gray-700 transition-all duration-200 hover:border-gray-300 hover:bg-gray-50"
						>
							<span class="flex items-center">
								<i class="fas fa-car mr-3 text-lg text-gray-400"></i>
								Add Vehicle
							</span>
							<i class="fas fa-chevron-right opacity-30"></i>
						</a>
						<a
							href="/profile"
							class="flex w-full items-center justify-between rounded-lg border border-gray-200 bg-white px-4 py-3 text-sm font-medium text-gray-700 transition-all duration-200 hover:border-gray-300 hover:bg-gray-50"
						>
							<span class="flex items-center">
								<i class="fas fa-map-marker-alt mr-3 text-lg text-gray-400"></i>
								Update Location
							</span>
							<i class="fas fa-chevron-right opacity-30"></i>
						</a>
					</div>
				</div>

				<!-- Emergency Contact Card -->
				<div class="mt-6 rounded-xl border border-red-100 bg-red-50 p-6">
					<div class="mb-4 flex items-center">
						<i class="fas fa-phone-alt mr-3 text-xl text-red-600"></i>
						<h3 class="text-lg font-bold text-red-800">Emergency Support</h3>
					</div>
					<p class="mb-4 text-sm text-red-700">Need immediate assistance? Call our 24/7 hotline.</p>
					<a
						href="tel:911"
						class="block w-full rounded-lg border border-red-200 bg-white px-4 py-2 text-center font-bold text-red-600 transition-colors hover:bg-red-50"
					>
						Call Emergency
					</a>
				</div>
			</div>
		</div>
	</div>
{/if}
