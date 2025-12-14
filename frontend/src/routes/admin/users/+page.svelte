<script lang="ts">
	import { onMount } from 'svelte';
	import api from '$lib/utils/api';

	let users: any[] = $state([]);
	let filteredUsers: any[] = $state([]);
	let isLoading = $state(true);
	let searchQuery = $state('');
	let filterRole = $state('all');
	let filterStatus = $state('all');

	onMount(async () => {
		await loadUsers();
	});

	async function loadUsers() {
		isLoading = true;
		try {
			const res = await api.get('/users/');
			users = res.data;
			applyFilters();
		} catch (e) {
			console.error('Failed to load users', e);
		} finally {
			isLoading = false;
		}
	}

	function applyFilters() {
		filteredUsers = users.filter((user) => {
			const matchesSearch =
				!searchQuery ||
				user.first_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
				user.last_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
				user.email.toLowerCase().includes(searchQuery.toLowerCase());

			const matchesRole = filterRole === 'all' || user.role === filterRole;

			const matchesStatus =
				filterStatus === 'all' ||
				(filterStatus === 'active' && user.is_active) ||
				(filterStatus === 'inactive' && !user.is_active);

			return matchesSearch && matchesRole && matchesStatus;
		});
	}

	$effect(() => {
		// Re-apply filters when search or filters change
		searchQuery;
		filterRole;
		filterStatus;
		applyFilters();
	});

	async function handleSuspend(userId: number, userName: string) {
		if (!confirm(`Are you sure you want to suspend ${userName}?`)) return;

		try {
			await api.put(`/users/${userId}/suspend`);
			alert('User suspended successfully!');
			await loadUsers();
		} catch (e: any) {
			alert(e.response?.data?.detail || 'Failed to suspend user');
		}
	}

	async function handleActivate(userId: number, userName: string) {
		if (!confirm(`Are you sure you want to activate ${userName}?`)) return;

		try {
			await api.put(`/users/${userId}/activate`);
			alert('User activated successfully!');
			await loadUsers();
		} catch (e: any) {
			alert(e.response?.data?.detail || 'Failed to activate user');
		}
	}

	async function handleDelete(userId: number, userName: string) {
		if (
			!confirm(
				`⚠️ WARNING: Are you sure you want to PERMANENTLY DELETE ${userName}?\n\nThis action CANNOT be undone!`
			)
		)
			return;

		try {
			await api.delete(`/users/${userId}`);
			alert('User deleted successfully!');
			await loadUsers();
		} catch (e: any) {
			alert(e.response?.data?.detail || 'Failed to delete user');
		}
	}

	function getRoleBadgeClass(role: string): string {
		const classes = {
			admin: 'bg-purple-100 text-purple-800',
			driver: 'bg-blue-100 text-blue-800',
			service_provider: 'bg-green-100 text-green-800'
		};
		return classes[role as keyof typeof classes] || 'bg-gray-100 text-gray-800';
	}
</script>

<svelte:head>
	<title>User Management - Admin - VBAMS</title>
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8">
	<!-- Header -->
	<div class="mb-8">
		<h1 class="text-3xl font-bold text-gray-900">User Management</h1>
		<p class="mt-2 text-gray-600">Manage all users, suspend accounts, and monitor activity</p>
	</div>

	<!-- Filters & Search -->
	<div class="mb-6 rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
		<div class="grid gap-4 md:grid-cols-[1fr_auto_auto_auto]">
			<div class="relative">
				<i class="fas fa-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
				<input
					type="text"
					bind:value={searchQuery}
					placeholder="Search by name or email..."
					class="w-full rounded-lg border border-gray-300 py-2 pl-10 pr-4 focus:border-blue-500 focus:outline-none"
				/>
			</div>

			<select
				bind:value={filterRole}
				class="rounded-lg border border-gray-300 px-4 py-2 focus:border-blue-500 focus:outline-none"
			>
				<option value="all">All Roles</option>
				<option value="driver">Drivers</option>
				<option value="service_provider">Providers</option>
				<option value="admin">Admins</option>
			</select>

			<select
				bind:value={filterStatus}
				class="rounded-lg border border-gray-300 px-4 py-2 focus:border-blue-500 focus:outline-none"
			>
				<option value="all">All Status</option>
				<option value="active">Active</option>
				<option value="inactive">Inactive</option>
			</select>

			<button
				onclick={loadUsers}
				class="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
			>
				<i class="fas fa-sync-alt mr-2"></i> Refresh
			</button>
		</div>

		<div class="mt-3 text-sm text-gray-600">
			Showing {filteredUsers.length} of {users.length} users
		</div>
	</div>

	<!-- Users Table -->
	{#if isLoading}
		<div class="text-center">
			<i class="fas fa-spinner fa-spin text-4xl text-gray-400"></i>
			<p class="mt-4 text-gray-600">Loading users...</p>
		</div>
	{:else if filteredUsers.length === 0}
		<div class="rounded-xl border border-gray-200 bg-white p-12 text-center shadow-sm">
			<i class="fas fa-users text-6xl text-gray-300"></i>
			<p class="mt-4 text-lg text-gray-600">No users found</p>
		</div>
	{:else}
		<div class="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm">
			<div class="overflow-x-auto">
				<table class="w-full">
					<thead class="bg-gray-50">
						<tr>
							<th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">User</th>
							<th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">Role</th>
							<th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">Phone</th>
							<th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">Status</th>
							<th class="px-6 py-4 text-left text-sm font-semibold text-gray-700">Joined</th>
							<th class="px-6 py-4 text-right text-sm font-semibold text-gray-700">Actions</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-200">
						{#each filteredUsers as user}
							<tr class="hover:bg-gray-50">
								<td class="px-6 py-4">
									<div>
										<p class="font-medium text-gray-900">
											{user.first_name}
											{user.last_name}
										</p>
										<p class="text-sm text-gray-600">{user.email}</p>
									</div>
								</td>
								<td class="px-6 py-4">
									<span
										class={`rounded-full px-3 py-1 text-xs font-medium ${getRoleBadgeClass(user.role)}`}
									>
										{user.role.replace('_', ' ').toUpperCase()}
									</span>
								</td>
								<td class="px-6 py-4">
									<p class="text-sm text-gray-700">{user.phone}</p>
								</td>
								<td class="px-6 py-4">
									<div class="flex items-center gap-2">
										{#if user.is_active}
											<span class="flex items-center text-sm font-medium text-green-600">
												<i class="fas fa-check-circle mr-1"></i> Active
											</span>
										{:else}
											<span class="flex items-center text-sm font-medium text-red-600">
												<i class="fas fa-times-circle mr-1"></i> Suspended
											</span>
										{/if}
										{#if user.is_verified}
											<i class="fas fa-shield-check text-blue-600" title="Verified"></i>
										{/if}
									</div>
								</td>
								<td class="px-6 py-4">
									<p class="text-sm text-gray-700">
										{new Date(user.created_at).toLocaleDateString()}
									</p>
								</td>
								<td class="px-6 py-4">
									<div class="flex justify-end gap-2">
										{#if user.is_active}
											<button
												onclick={() =>
													handleSuspend(user.id, `${user.first_name} ${user.last_name}`)}
												class="rounded-lg bg-yellow-600 px-3 py-1.5 text-xs text-white hover:bg-yellow-700"
												title="Suspend User"
											>
												<i class="fas fa-ban mr-1"></i> Suspend
											</button>
										{:else}
											<button
												onclick={() =>
													handleActivate(user.id, `${user.first_name} ${user.last_name}`)}
												class="rounded-lg bg-green-600 px-3 py-1.5 text-xs text-white hover:bg-green-700"
												title="Activate User"
											>
												<i class="fas fa-check mr-1"></i> Activate
											</button>
										{/if}

										<button
											onclick={() => handleDelete(user.id, `${user.first_name} ${user.last_name}`)}
											class="rounded-lg bg-red-600 px-3 py-1.5 text-xs text-white hover:bg-red-700"
											title="Delete User"
										>
											<i class="fas fa-trash mr-1"></i> Delete
										</button>
									</div>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	{/if}
</div>
