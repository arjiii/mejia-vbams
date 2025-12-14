import { writable, get } from 'svelte/store';
import api from '$lib/utils/api';

// Types (simplified for store usage, can import from a central types file later)
interface DashboardState<T> {
    data: T | null;
    loading: boolean;
    error: string | null;
    lastUpdated: number;
}

const CACHE_DURATION = 10 * 60 * 1000; // 10 minutes

function createDashboardStore<T>(fetchFn: () => Promise<T>) {
    const { subscribe, set, update } = writable<DashboardState<T>>({
        data: null,
        loading: false,
        error: null,
        lastUpdated: 0
    });

    return {
        subscribe,
        load: async (force = false) => {
            const state = get({ subscribe });
            const now = Date.now();

            // If data exists, is fresh, and not forcing reload, return current data
            if (!force && state.data && (now - state.lastUpdated < CACHE_DURATION)) {
                return;
            }

            update(s => ({ ...s, loading: true, error: null }));
            try {
                const data = await fetchFn();
                set({
                    data,
                    loading: false,
                    error: null,
                    lastUpdated: Date.now()
                });
            } catch (e: any) {
                console.error("Store fetch error:", e);
                update(s => ({
                    ...s,
                    loading: false,
                    error: e.response?.data?.detail || e.message || 'Failed to load data'
                }));
            }
        },
        reset: () => {
            set({ data: null, loading: false, error: null, lastUpdated: 0 });
        }
    };
}

// Admin Store
export const adminStore = createDashboardStore(async () => {
    const [usersRes, statsRes, assistanceRes, providersRes] = await Promise.all([
        api.get('/users/'),
        api.get('/users/stats/overview'),
        api.get('/assistance/').catch(() => ({ data: [] })),
        api.get('/service-providers/').catch(() => ({ data: [] }))
    ]);

    // Map all users with consistent formatting
    const allMappedUsers = usersRes.data.map((u: any) => ({
        id: u.id,
        name: `${u.first_name} ${u.last_name}`,
        email: u.email,
        role: u.role,
        status: u.is_active ? 'active' : 'inactive',
        created_at: u.created_at,
        phone: u.phone
    }));

    // Filtered users for Dashboard view (excluding providers usually)
    const users = allMappedUsers.filter((u: any) => u.role !== 'service_provider');

    const providers = providersRes.data.map((p: any) => ({
        id: p.id,
        userId: p.user.id,
        name: p.business_name || `${p.user.first_name}'s Business`,
        businessName: p.business_name || `${p.user.first_name}'s Business`, // Alias for comp
        contactName: `${p.user.first_name} ${p.user.last_name}`,
        email: p.user.email,
        phone: p.user.phone,
        status: !p.is_active ? 'suspended' : p.is_verified ? 'verified' : 'pending',
        rating: p.average_rating || 0,
        license: p.business_license,
        baseRate: p.base_rate,
        services: p.services || [],
        documents: p.documents || [],
        completedJobs: p.rating_count || 0,
        joined: p.created_at
    }));

    const activeBreakdownsCount = assistanceRes.data.filter((a: any) =>
        ['pending', 'assigned', 'in_progress'].includes(a.status)
    ).length;

    return {
        hiddenUsers: users, // Renaming to hiddenUsers or just keep as 'users' for back-compat but adding allUsers
        users, // Keep for AdminDashboard compatibility
        allUsers: allMappedUsers, // For Manage Users page
        providers,
        requests: assistanceRes.data, // Access to all assistance requests
        stats: {
            totalUsers: statsRes.data.total_users,
            totalProviders: statsRes.data.service_providers,
            activeBreakdowns: activeBreakdownsCount
        }
    };
});

// Driver Store
export const driverStore = createDashboardStore(async () => {
    const [vehRes, breakRes, assistRes] = await Promise.all([
        api.get('/vehicles/').catch(() => ({ data: [] })),
        api.get('/breakdowns/').catch(() => ({ data: [] })),
        api.get('/assistance/').catch(() => ({ data: [] }))
    ]);

    const breakdowns = breakRes.data.map((b: any) => ({
        ...b,
        status: b.status || 'reported'
    }));

    const recentBreakdowns = breakdowns.slice(0, 5);

    return {
        vehicles: vehRes.data,
        breakdowns: breakdowns,
        assistance: assistRes.data,
        vehicleCount: vehRes.data.length,
        breakdownCount: breakRes.data.length,
        assistanceCount: assistRes.data.length,
        recentBreakdowns
    };
});

// Service Provider Store
export const providerStore = createDashboardStore(async () => {
    const [availableRes, historyRes] = await Promise.all([
        api.get('/assistance/available').catch(() => ({ data: [] })),
        api.get('/assistance/').catch(() => ({ data: [] }))
    ]);

    const activeRequests = availableRes.data.map((r: any) => ({
        id: r.id,
        requester_id: r.requester_id,
        customer: `Customer #${r.requester_id}`,
        type: r.service_type.replace(/_/g, ' ').toUpperCase(),
        distance: 'Unknown distance',
        location: r.address || 'Unknown Location',
        status: r.status,
        urgency: r.priority || 'medium',
        estimatedPay: r.estimated_cost || 0
    }));

    const myJobs = historyRes.data;
    const completedJobs = myJobs.filter((j: any) => j.status === 'completed').length;
    // Mock earnings calculation from history
    const earnings = myJobs
        .filter((j: any) => j.status === 'completed')
        .reduce((sum: number, j: any) => sum + (j.actual_cost || 0), 0);

    return {
        pendingRequests: activeRequests.length,
        completedJobs,
        earnings,
        activeRequests,
        allJobs: myJobs,
        recentJobs: myJobs.slice(0, 5)
    };
});
