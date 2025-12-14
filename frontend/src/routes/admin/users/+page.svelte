<script lang="ts">
	import { onMount } from 'svelte';
	import { user } from '$lib/stores/auth';
	import api from '$lib/utils/api';

	interface User {
		id: number;
		name: string;
		email: string;
		role: string;
		status: string;
		created_at: string;
		phone: string;
	}

	import { adminStore } from '$lib/stores/dashboard';

	let users = $derived($adminStore.data?.hiddenUsers || []);
	let filteredUsers: User[] = $state([]);
	let searchQuery = $state('');
	let filterRole = $state('all');
	let loading = $derived($adminStore.loading);

	onMount(() => {
		adminStore.load();
	});

	function refreshData() {
		adminStore.load(true);
	}

	$effect(() => {
		if (users.length > 0) {
			searchUsers();
		}
	});

	function searchUsers() {
		filteredUsers = users.filter((u) => {
			const matchesSearch =
				u.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
				u.email.toLowerCase().includes(searchQuery.toLowerCase());
			const matchesRole = filterRole === 'all' || u.role === filterRole;
			return matchesSearch && matchesRole;
		});
	}

	$effect(() => {
		searchQuery;
		filterRole;
		searchUsers();
	});
</script>

<svelte:head>
	<title>Manage Users - VBAMS</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold text-gray-900">Manage Users</h1>
			<p class="mt-2 text-sm text-gray-600">View and manage all registered users</p>
		</div>
		<button
			class="rounded-lg bg-gradient-to-r from-blue-600 to-blue-700 px-4 py-2 text-sm font-bold text-white shadow-lg transition-all hover:from-blue-700 hover:to-blue-800"
		>
			<i class="fas fa-user-plus mr-2"></i>
			Add User
		</button>
		<button
			onclick={refreshData}
			class="ml-2 h-10 w-10 rounded-lg bg-gray-100 text-gray-600 hover:bg-gray-200"
			title="Refresh Data"
		>
			<i class="fas fa-sync-alt"></i>
		</button>
	</div>

	<!-- Filters -->
	<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-lg">
		<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700">Search Users</label>
				<div class="relative">
					<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
						<i class="fas fa-search text-gray-400"></i>
					</div>
					<input
						type="text"
						bind:value={searchQuery}
						placeholder="Search by name or email..."
						class="block w-full rounded-lg border border-gray-300 py-2 pl-10 pr-3 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
					/>
				</div>
			</div>
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700">Filter by Role</label>
				<select
					bind:value={filterRole}
					class="block w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
				>
					<option value="all">All Roles</option>
					<option value="driver">Driver</option>
					<option value="service_provider">Service Provider</option>
					<option value="admin">Admin</option>
				</select>
			</div>
		</div>
	</div>

	<!-- Users Table -->
	<div class="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-lg">
		<div class="overflow-x-auto">
			<table class="min-w-full divide-y divide-gray-200">
				<thead class="bg-gray-50">
					<tr>
						<th
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>User</th
						>
						<th
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>Contact</th
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
							class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
							>Joined</th
						>
						<th
							class="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-gray-500"
							>Actions</th
						>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-200 bg-white">
					{#each filteredUsers as u}
						<tr class="transition-colors hover:bg-gray-50">
							<td class="whitespace-nowrap px-6 py-4">
								<div class="flex items-center">
									<div class="h-10 w-10 flex-shrink-0">
										<span
											class="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 font-bold text-blue-600"
										>
											{u.name.charAt(0)}
										</span>
									</div>
									<div class="ml-4">
										<div class="text-sm font-bold text-gray-900">{u.name}</div>
										<div class="text-sm text-gray-500">{u.email}</div>
									</div>
								</div>
							</td>
							<td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
								<i class="fas fa-phone mr-2 text-gray-400"></i>
								{u.phone}
							</td>
							<td class="whitespace-nowrap px-6 py-4">
								<span
									class="inline-flex items-center rounded-full bg-blue-100 px-3 py-1 text-xs font-medium capitalize text-blue-800"
								>
									{u.role.replace('_', ' ')}
								</span>
							</td>
							<td class="whitespace-nowrap px-6 py-4">
								<span
									class={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${u.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}
								>
									{u.status}
								</span>
							</td>
							<td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
								{new Date(u.created_at).toLocaleDateString()}
							</td>
							<td class="whitespace-nowrap px-6 py-4 text-right text-sm font-medium">
								<button class="mr-3 text-blue-600 hover:text-blue-900">
									<i class="fas fa-edit"></i>
								</button>
								<button class="text-red-600 hover:text-red-900">
									<i class="fas fa-trash"></i>
								</button>
							</td>
						</tr>
					{/each}
					{#if filteredUsers.length === 0}
						<tr>
							<td colspan="6" class="px-6 py-12 text-center">
								<div class="flex flex-col items-center">
									<i class="fas fa-users mb-3 text-4xl text-gray-300"></i>
									<p class="text-gray-500">No users found</p>
								</div>
							</td>
						</tr>
					{/if}
				</tbody>
			</table>
		</div>
	</div>
</div>
