 
'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { incidentApi } from '@/lib/api';
import { Incident, IncidentAction } from '@/types/incident';
import { IncidentDetails } from '@/components/IncidentDetails';

export default function IncidentPage() {
  const params = useParams();
  const id = parseInt(params.id as string);
  
  const [incident, setIncident] = useState<Incident | null>(null);
  const [actions, setActions] = useState<IncidentAction[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [incidentData, actionsData] = await Promise.all([
          incidentApi.getIncident(id),
          incidentApi.getIncidentActions(id),
        ]);
        setIncident(incidentData);
        setActions(actionsData);
      } catch (error) {
        console.error('Error fetching incident:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  if (loading) {
    return <div className="flex justify-center items-center min-h-screen">Loading...</div>;
  }

  if (!incident) {
    return <div className="flex justify-center items-center min-h-screen">Incident not found</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-5xl mx-auto">
        <IncidentDetails incident={incident} actions={actions} />
      </div>
    </div>
  );
}
