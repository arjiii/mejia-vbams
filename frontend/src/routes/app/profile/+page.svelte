<script lang="ts">
  export let title = 'Profile';
</script>

<svelte:head>
  <title>App - Profile</title>
</svelte:head>

<div class="p-6 bg-white rounded shadow">
  <h2 class="text-2xl font-semibold mb-4">Profile</h2>
  <div class="space-y-4 text-sm text-gray-700">
    <div>
      <div class="text-xs text-gray-500">Name</div>
      <div class="font-medium">Guest User</div>
    </div>
    <div>
      <div class="text-xs text-gray-500">Email</div>
      <div class="font-medium">guest@example.com</div>
    </div>
    <div>
      <div class="text-xs text-gray-500">Role</div>
      <div class="font-medium">Driver</div>
    </div>
  </div>
</div>
