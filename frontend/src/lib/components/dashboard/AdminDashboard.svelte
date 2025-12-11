<script lang="ts">
	import { onMount } from 'svelte';

	interface User {
		id: number;
		name: string;
		email: string;
		role: string;
		status: string;
	}

	interface Provider {
		id: number;
		name: string;
		email: string;
		status: string;
		rating: number;
	}

	let users: User[] = $state([]);
	let providers: Provider[] = $state([]);
	let stats = $state({
		totalUsers: 150,
		totalProviders: 25,
		activeBreakdowns: 3
	});

	let activeTab = $state('users');

	onMount(() => {
		// Mock data
		users = [
			{ id: 1, name: 'John Doe', email: 'john@example.com', role: 'driver', status: 'active' },
			{ id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'driver', status: 'active' },
			{ id: 3, name: 'Bob Wilson', email: 'bob@example.com', role: 'driver', status: 'inactive' }
		];

		providers = [
			{
				id: 101,
				name: 'Quick Fix Auto',
				email: 'contact@quickfix.com',
				status: 'verified',
				rating: 4.8
			},
			{
				id: 102,
				name: 'Mobile Mechanic',
				email: 'mike@mobilemech.com',
				status: 'pending',
				rating: 0.0
			}
		];
	});
</script>

<div class="space-y-6">
	<!-- Welcome Header -->
	<div class="rounded-2xl bg-gradient-to-r from-red-600 to-orange-600 p-6 text-white shadow-lg">
		<div class="flex items-center justify-between">
			<div>
				<h1 class="text-3xl font-bold">Admin Dashboard</h1>
				<p class="mt-2 text-red-100">Manage users and service providers across the system</p>
			</div>
			<div class="hidden md:block">
				<i class="fas fa-shield-alt text-6xl opacity-30"></i>
			</div>
		</div>
		<div class="mt-4">
			<button
				class="rounded-lg bg-white px-4 py-2 text-sm font-bold text-red-600 shadow-md transition-colors hover:bg-red-50"
			>
				<i class="fas fa-download mr-2"></i> Export Report
			</button>
		</div>
	</div>

	<!-- Stats -->
	<div class="grid grid-cols-1 gap-5 sm:grid-cols-3">
		<div
			class="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-lg transition-shadow duration-300 hover:shadow-xl"
		>
			<div class="p-5">
				<div class="flex items-center">
					<div class="flex-shrink-0 rounded-lg bg-blue-50 p-3">
						<i class="fas fa-users text-2xl text-blue-600"></i>
					</div>
					<div class="ml-5 w-0 flex-1">
						<dl>
							<dt class="truncate text-sm font-medium text-gray-500">Total Users</dt>
							<dd class="text-2xl font-bold text-gray-900">{stats.totalUsers}</dd>
						</dl>
					</div>
				</div>
			</div>
		</div>
		<div
			class="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-lg transition-shadow duration-300 hover:shadow-xl"
		>
			<div class="p-5">
				<div class="flex items-center">
					<div class="flex-shrink-0 rounded-lg bg-purple-50 p-3">
						<i class="fas fa-tools text-2xl text-purple-600"></i>
					</div>
					<div class="ml-5 w-0 flex-1">
						<dl>
							<dt class="truncate text-sm font-medium text-gray-500">Service Providers</dt>
							<dd class="text-2xl font-bold text-gray-900">{stats.totalProviders}</dd>
						</dl>
					</div>
				</div>
			</div>
		</div>
		<div
			class="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-lg transition-shadow duration-300 hover:shadow-xl"
		>
			<div class="p-5">
				<div class="flex items-center">
					<div class="flex-shrink-0 rounded-lg bg-red-50 p-3">
						<i class="fas fa-car-crash text-2xl text-red-600"></i>
					</div>
					<div class="ml-5 w-0 flex-1">
						<dl>
							<dt class="truncate text-sm font-medium text-gray-500">Active Breakdowns</dt>
							<dd class="text-2xl font-bold text-gray-900">{stats.activeBreakdowns}</dd>
						</dl>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Tabs -->
	<div class="border-b border-gray-200">
		<nav class="-mb-px flex space-x-8">
			<button
				class={`whitespace-nowrap border-b-2 px-1 py-4 text-sm font-medium transition-colors duration-200 ${activeTab === 'users' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'}`}
				onclick={() => (activeTab = 'users')}
			>
				<i class="fas fa-users mr-2"></i> Users
			</button>
			<button
				class={`whitespace-nowrap border-b-2 px-1 py-4 text-sm font-medium transition-colors duration-200 ${activeTab === 'providers' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'}`}
				onclick={() => (activeTab = 'providers')}
			>
				<i class="fas fa-tools mr-2"></i> Service Providers
			</button>
		</nav>
	</div>

	<!-- Content -->
	<div class="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-lg">
		{#if activeTab === 'users'}
			<div class="overflow-x-auto">
				<table class="min-w-full divide-y divide-gray-200">
					<thead class="bg-gray-50">
						<tr>
							<th
								class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>Name</th
							>
							<th
								class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>Email</th
							>
							<th
								class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>Role</th
							>
							<th
								class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>Status</th
							>
							<th
								class="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-gray-500"
								>Actions</th
							>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-200 bg-white">
						{#each users as u}
							<tr class="transition-colors hover:bg-gray-50">
								<td class="whitespace-nowrap px-6 py-4">
									<div class="flex items-center">
										<div class="h-10 w-10 flex-shrink-0">
											<span
												class="flex h-10 w-10 items-center justify-center rounded-full bg-gray-100 font-bold text-gray-500"
											>
												{u.name.charAt(0)}
											</span>
										</div>
										<div class="ml-4">
											<div class="text-sm font-medium text-gray-900">{u.name}</div>
										</div>
									</div>
								</td>
								<td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">{u.email}</td>
								<td class="whitespace-nowrap px-6 py-4 text-sm capitalize text-gray-500">
									<span
										class="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800"
									>
										{u.role}
									</span>
								</td>
								<td class="whitespace-nowrap px-6 py-4">
									<span
										class={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${u.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}
									>
										{u.status}
									</span>
								</td>
								<td class="whitespace-nowrap px-6 py-4 text-right text-sm font-medium">
									<button class="font-medium text-blue-600 hover:text-blue-900">Edit</button>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{:else}
			<div class="overflow-x-auto">
				<table class="min-w-full divide-y divide-gray-200">
					<thead class="bg-gray-50">
						<tr>
							<th
								class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>Business Name</th
							>
							<th
								class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>Email</th
							>
							<th
								class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>Status</th
							>
							<th
								class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>Rating</th
							>
							<th
								class="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-gray-500"
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
											<div class="text-sm font-medium text-gray-900">{p.name}</div>
										</div>
									</div>
								</td>
								<td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">{p.email}</td>
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
									{#if p.status === 'pending'}
										<button class="mr-3 font-medium text-green-600 hover:text-green-900"
											>Verify</button
										>
									{/if}
									<button class="font-medium text-blue-600 hover:text-blue-900">Details</button>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}
	</div>
</div>
