 
'use client';

import { useEffect, useState } from 'react';

interface ServiceStatus {
  service: string;
  status: 'healthy' | 'degraded' | 'down';
  incidents: number;
}

export function ServiceHealth() {
  const [services, setServices] = useState<ServiceStatus[]>([
    { service: 'api-gateway', status: 'healthy', incidents: 0 },
    { service: 'user-service', status: 'healthy', incidents: 0 },
    { service: 'payment-service', status: 'degraded', incidents: 2 },
    { service: 'notification-service', status: 'healthy', incidents: 0 },
  ]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'bg-green-500';
      case 'degraded':
        return 'bg-yellow-500';
      case 'down':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold mb-4">Service Health</h3>
      <div className="space-y-3">
        {services.map((service) => (
          <div key={service.service} className="flex items-center justify-between">
            <div className="flex items-center">
              <div className={`w-3 h-3 rounded-full ${getStatusColor(service.status)} mr-3`} />
              <span className="font-medium">{service.service}</span>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                {service.incidents} active incidents
              </span>
              <span className="text-sm font-medium capitalize">{service.status}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
