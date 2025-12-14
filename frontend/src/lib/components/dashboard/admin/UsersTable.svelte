<script lang="ts">
	import api from '$lib/utils/api';
	import { adminStore } from '$lib/stores/dashboard';

	interface User {
		id: number;
		name: string;
		email: string;
		role: string;
		status: string;
	}

	let { users } = $props<{ users: User[] }>();

	let editingUser: User | null = $state(null);
	let showEditModal = $state(false);
	let isSaving = $state(false);

	let editForm = $state({
		firstName: '',
		lastName: ''
	});

	function openEdit(user: User) {
		editingUser = user;
		// Split name roughly
		const nameParts = user.name.split(' ');
		editForm.firstName = nameParts[0] || '';
		editForm.lastName = nameParts.slice(1).join(' ') || '';
		showEditModal = true;
	}

	function closeEdit() {
		showEditModal = false;
		editingUser = null;
	}

	async function saveUser() {
		if (!editingUser) return;
		isSaving = true;
		try {
			// Try to update user
			// Assuming endpoint /users/{id}
			await api.put(`/users/${editingUser.id}`, {
				first_name: editForm.firstName,
				last_name: editForm.lastName
			});
			alert('User updated successfully');
			closeEdit();
			adminStore.load(true);
		} catch (e) {
			console.error('Failed to update user', e);
			alert('Failed to update user. Feature may not be available.');
		} finally {
			isSaving = false;
		}
	}
</script>

<div class="overflow-x-auto">
	<table class="min-w-full divide-y divide-gray-200">
		<thead class="bg-gray-50">
			<tr>
				<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
					>Name</th
				>
				<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
					>Email</th
				>
				<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
					>Role</th
				>
				<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
					>Status</th
				>
				<th class="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-gray-500"
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
							class="inline-flex items-center rounded-full bg-orange-100 px-2.5 py-0.5 text-xs font-medium text-orange-800"
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
						<button class="font-medium text-red-600 hover:text-red-900" onclick={() => openEdit(u)}>
							Edit
						</button>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>
</div>

{#if showEditModal && editingUser}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-50 p-4"
		role="dialog"
		aria-modal="true"
	>
		<div class="w-full max-w-md overflow-hidden rounded-2xl bg-white shadow-2xl">
			<div class="bg-gradient-to-r from-red-600 to-orange-600 px-6 py-4">
				<div class="flex items-center justify-between">
					<h3 class="text-lg font-bold text-white">Edit User</h3>
					<button onclick={closeEdit} class="text-white hover:text-gray-200">
						<i class="fas fa-times text-xl"></i>
					</button>
				</div>
			</div>

			<div class="p-6">
				<div class="space-y-4">
					<div>
						<label class="block text-sm font-medium text-gray-700">First Name</label>
						<input
							type="text"
							bind:value={editForm.firstName}
							class="mt-1 block w-full rounded-md border border-gray-300 p-2 text-sm focus:border-red-500 focus:ring-red-500"
						/>
					</div>
					<div>
						<label class="block text-sm font-medium text-gray-700">Last Name</label>
						<input
							type="text"
							bind:value={editForm.lastName}
							class="mt-1 block w-full rounded-md border border-gray-300 p-2 text-sm focus:border-red-500 focus:ring-red-500"
						/>
					</div>
					<div>
						<label class="block text-sm font-medium text-gray-700">Email (Read Only)</label>
						<input
							type="text"
							value={editingUser.email}
							readonly
							class="mt-1 block w-full rounded-md border border-gray-300 bg-gray-50 p-2 text-sm text-gray-500"
						/>
					</div>
				</div>

				<div class="mt-6 flex justify-end space-x-3">
					<button
						onclick={closeEdit}
						class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
					>
						Cancel
					</button>
					<button
						onclick={saveUser}
						disabled={isSaving}
						class="rounded-lg bg-red-600 px-4 py-2 text-sm font-bold text-white hover:bg-red-700 disabled:opacity-50"
					>
						{isSaving ? 'Saving...' : 'Save Changes'}
					</button>
				</div>
			</div>
		</div>
	</div>
{/if}
