// 'use client';

// import { useEffect, useState } from 'react';
// import axios from 'axios';
// import { IncidentList } from '@/components/IncidentList';
// import { DashboardStats } from '@/components/DashboardStats';
// import { IncidentChart } from '@/components/IncidentChart';

// const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// export default function Home() {
//   const [stats, setStats] = useState<any>(null);
//   const [incidents, setIncidents] = useState<any[]>([]);
//   const [loading, setLoading] = useState(true);
//   const [ws, setWs] = useState<WebSocket | null>(null);

//   const fetchDashboardData = async () => {
//     try {
//       const [statsRes, incidentsRes] = await Promise.all([
//         axios.get(`${API_BASE_URL}/analytics/dashboard`),
//         axios.get(`${API_BASE_URL}/incidents?limit=20`)
//       ]);

//       setStats(statsRes.data);
//       setIncidents(incidentsRes.data);
//       setLoading(false);
//     } catch (error) {
//       console.error('Error fetching data:', error);
//       setLoading(false);
//     }
//   };

//   useEffect(() => {
//     // Fetch initial data
//     fetchDashboardData();

//     // Setup WebSocket for real-time updates
//     const websocket = new WebSocket(
//       process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws'
//     );

//     websocket.onmessage = (event) => {
//       const data = JSON.parse(event.data);
//       console.log('Real-time update:', data);
      
//       // Refresh data when new incident arrives
//       if (data.incident_id) {
//         fetchDashboardData();
//       }
//     };

//     websocket.onerror = (error) => {
//       console.error('WebSocket error:', error);
//     };

//     setWs(websocket);

//     return () => {
//       websocket.close();
//     };
//   }, []);

//   if (loading) {
//     return (
//       <div className="flex items-center justify-center min-h-screen">
//         <div className="text-xl">Loading...</div>
//       </div>
//     );
//   }

//   return (
//     <main className="min-h-screen bg-gray-50 p-8">
//       <div className="max-w-7xl mx-auto">
//         <h1 className="text-4xl font-bold mb-8">DevOps Co-Pilot Dashboard</h1>
        
//         <DashboardStats stats={stats} />
        
//         <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
//           <IncidentChart data={stats?.daily_trend || []} />
//           <div className="bg-white p-6 rounded-lg shadow">
//             <h3 className="text-lg font-semibold mb-4">Severity Distribution</h3>
//             {/* Add pie chart here */}
//           </div>
//         </div>

//         <div className="mt-8">
//           <IncidentList incidents={incidents} onRefresh={fetchDashboardData} />
//         </div>
//       </div>
//     </main>
//   );
// }
'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';
import { IncidentList } from '@/components/IncidentList';
import { DashboardStats } from '@/components/DashboardStats';
import { IncidentChart } from '@/components/IncidentChart';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export default function Home() {
  const [stats, setStats] = useState<any>(null);
  const [incidents, setIncidents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    // Fetch initial data
    fetchDashboardData();

    // Setup WebSocket for real-time updates
    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws';
    
    try {
      const websocket = new WebSocket(wsUrl);

      websocket.onopen = () => {
        console.log('WebSocket connected');
      };

      websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('Real-time update:', data);
        
        // Refresh data when new incident arrives
        if (data.incident_id) {
          fetchDashboardData();
        }
      };

      websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      websocket.onclose = () => {
        console.log('WebSocket disconnected');
      };

      setWs(websocket);

      return () => {
        websocket.close();
      };
    } catch (err) {
      console.error('WebSocket connection failed:', err);
    }
  }, []);

  const fetchDashboardData = async () => {
    try {
      setError(null);
      
      const [statsRes, incidentsRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/analytics/dashboard`),
        axios.get(`${API_BASE_URL}/incidents?limit=20`)
      ]);

      console.log('Stats:', statsRes.data);
      console.log('Incidents:', incidentsRes.data);

      setStats(statsRes.data);
      setIncidents(incidentsRes.data);
      setLoading(false);
    } catch (error: any) {
      console.error('Error fetching data:', error);
      setError(error.message || 'Failed to fetch data');
      setLoading(false);
      
      // Set default empty stats to prevent null errors
      setStats({
        total_incidents: 0,
        active_incidents: 0,
        resolved_today: 0,
        avg_resolution_time_minutes: 0,
        severity_distribution: {},
        top_services: [],
        daily_trend: []
      });
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <div className="text-xl text-gray-600">Loading dashboard...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
          <div className="text-red-600 text-xl font-semibold mb-4">⚠️ Connection Error</div>
          <p className="text-gray-700 mb-4">{error}</p>
          <p className="text-sm text-gray-500 mb-4">
            Make sure the backend is running at: <code className="bg-gray-100 px-2 py-1 rounded">{API_BASE_URL}</code>
          </p>
          <button
            onClick={fetchDashboardData}
            className="w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">DevOps Co-Pilot Dashboard</h1>
        
        {stats && <DashboardStats stats={stats} />}
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          {stats?.daily_trend && <IncidentChart data={stats.daily_trend} />}
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold mb-4">Severity Distribution</h3>
            {stats?.severity_distribution && Object.keys(stats.severity_distribution).length > 0 ? (
              <div className="space-y-2">
                {Object.entries(stats.severity_distribution).map(([severity, count]: any) => (
                  <div key={severity} className="flex justify-between items-center">
                    <span className="capitalize">{severity}</span>
                    <span className="font-semibold">{count}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No incidents yet</p>
            )}
          </div>
        </div>

        <div className="mt-8">
          <IncidentList incidents={incidents} onRefresh={fetchDashboardData} />
        </div>
      </div>
    </main>
  );
}
