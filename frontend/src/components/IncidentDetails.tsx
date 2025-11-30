import { Incident, IncidentAction } from '@/types/incident';
import { format } from 'date-fns';
import { CheckCircleIcon, XCircleIcon, ClockIcon } from '@heroicons/react/24/outline';

interface Props {
  incident: Incident;
  actions: IncidentAction[];
}

export function IncidentDetails({ incident, actions }: Props) {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'resolved':
        return <CheckCircleIcon className="w-6 h-6 text-green-500" />;
      case 'failed':
        return <XCircleIcon className="w-6 h-6 text-red-500" />;
      default:
        return <ClockIcon className="w-6 h-6 text-yellow-500" />;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{incident.title}</h1>
          <p className="text-gray-600 mt-2">{incident.description}</p>
        </div>
        <div className="flex items-center">
          {getStatusIcon(incident.status)}
          <span className="ml-2 text-sm font-medium text-gray-700">
            {incident.status.toUpperCase()}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div>
          <p className="text-sm text-gray-500">Service</p>
          <p className="font-semibold">{incident.service_name}</p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Severity</p>
          <p className="font-semibold capitalize">{incident.severity}</p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Detected At</p>
          <p className="font-semibold">
            {format(new Date(incident.detected_at), 'MMM dd, yyyy HH:mm')}
          </p>
        </div>
        {incident.resolved_at && (
          <div>
            <p className="text-sm text-gray-500">Resolved At</p>
            <p className="font-semibold">
              {format(new Date(incident.resolved_at), 'MMM dd, yyyy HH:mm')}
            </p>
          </div>
        )}
      </div>

      {incident.root_cause && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-2">Root Cause</h3>
          <p className="text-gray-700 bg-gray-50 p-4 rounded">{incident.root_cause}</p>
        </div>
      )}

      {incident.resolution_steps && incident.resolution_steps.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-2">Resolution Steps</h3>
          <ol className="list-decimal list-inside space-y-2">
            {incident.resolution_steps.map((step, index) => (
              <li key={index} className="text-gray-700">{step}</li>
            ))}
          </ol>
        </div>
      )}

      <div>
        <h3 className="text-lg font-semibold mb-4">Actions Taken</h3>
        <div className="space-y-3">
          {actions.map((action) => (
            <div key={action.id} className="border-l-4 border-blue-500 pl-4 py-2">
              <div className="flex justify-between">
                <p className="font-medium">{action.action_type}</p>
                <span className="text-sm text-gray-500">
                  {format(new Date(action.created_at), 'HH:mm:ss')}
                </span>
              </div>
              <p className="text-sm text-gray-600">{action.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
