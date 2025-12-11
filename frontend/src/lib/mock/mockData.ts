export const mockVehicles = [
  { id: 1, make: 'Toyota', model: 'Vios', year: 2018, license_plate: 'ABC-123', vin: 'VIN1234', vehicle_type: 'sedan', fuel_type: 'gasoline', mileage: 45200, color: 'white', insurance_provider: 'Acme Ins.' },
  { id: 2, make: 'Honda', model: 'Civic', year: 2017, license_plate: 'XYZ-789', vin: 'VIN5678', vehicle_type: 'sedan', fuel_type: 'gasoline', mileage: 128000, color: 'black', insurance_provider: null }
];

export const mockBreakdowns = [
  {
    id: 1,
    vehicle: { make: 'Toyota', model: 'Vios', license_plate: 'ABC-123' },
    category: 'tire',
    description: 'Rear left tire punctured on the highway',
    address: 'M. dela Cruz St., Pasay City',
    status: 'reported',
    created_at: new Date().toISOString()
  },
  {
    id: 2,
    vehicle: { make: 'Honda', model: 'Civic', license_plate: 'XYZ-789' },
    category: 'electrical',
    description: 'Battery dead, engine wont start',
    address: 'LRT-1 Station, Manila',
    status: 'assigned',
    created_at: new Date(Date.now() - 86400000).toISOString()
  }
];

export const mockAssistance = [
  { id: 1, provider: 'QuickFix', status: 'assigned' }
];
