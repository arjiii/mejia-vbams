<script lang="ts">
  export let title = 'Assistance';
</script>

<svelte:head>
  <title>App - Assistance</title>
</svelte:head>

<div class="p-6 bg-white rounded shadow">
  <h2 class="text-2xl font-semibold mb-4">Assistance</h2>
  <div class="mb-4 text-sm text-gray-600">View assistance requests and their statuses.</div>
  <div class="space-y-3">
    <div class="p-3 border rounded flex justify-between items-center">
      <div>
        <div class="font-medium">QuickFix</div>
        <div class="text-xs text-gray-500">Assigned to: QuickFix team</div>
      </div>
      <div class="text-sm text-blue-700">Assigned</div>
    </div>
    <div class="p-3 border rounded flex justify-between items-center">
      <div>
        <div class="font-medium">TowPro</div>
        <div class="text-xs text-gray-500">En route</div>
      </div>
      <div class="text-sm text-green-700">On the way</div>
    </div>
  </div>
</div>
