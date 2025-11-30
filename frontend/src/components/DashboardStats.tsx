 
// import { ArrowTrendingUpIcon, CheckCircleIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';

// interface StatsProps {
//   stats: {
//     total_incidents: number;
//     active_incidents: number;
//     resolved_today: number;
//     avg_resolution_time_minutes: number;
//   };
// }

// export function DashboardStats({ stats }: StatsProps) {
//   const statCards = [
//     {
//       title: 'Total Incidents',
//       value: stats.total_incidents,
//       icon: ExclamationTriangleIcon,
//       color: 'text-blue-600',
//       bgColor: 'bg-blue-100'
//     },
//     {
//       title: 'Active Incidents',
//       value: stats.active_incidents,
//       icon: ArrowTrendingUpIcon,
//       color: 'text-orange-600',
//       bgColor: 'bg-orange-100'
//     },
//     {
//       title: 'Resolved Today',
//       value: stats.resolved_today,
//       icon: CheckCircleIcon,
//       color: 'text-green-600',
//       bgColor: 'bg-green-100'
//     },
//     {
//       title: 'Avg Resolution Time',
//       value: `${Math.round(stats.avg_resolution_time_minutes)}m`,
//       icon: ArrowTrendingUpIcon,
//       color: 'text-purple-600',
//       bgColor: 'bg-purple-100'
//     }
//   ];

//   return (
//     <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
//       {statCards.map((stat, index) => (
//         <div key={index} className="bg-white rounded-lg shadow p-6">
//           <div className="flex items-center justify-between">
//             <div>
//               <p className="text-sm text-gray-600">{stat.title}</p>
//               <p className="text-3xl font-bold mt-2">{stat.value}</p>
//             </div>
//             <div className={`${stat.bgColor} p-3 rounded-full`}>
//               <stat.icon className={`w-6 h-6 ${stat.color}`} />
//             </div>
//           </div>
//         </div>
//       ))}
//     </div>
//   );
// }
import { ArrowTrendingUpIcon, CheckCircleIcon, ExclamationTriangleIcon, ClockIcon } from '@heroicons/react/24/outline';

interface StatsProps {
  stats: {
    total_incidents: number;
    active_incidents: number;
    resolved_today: number;
    avg_resolution_time_minutes: number;
  } | null;
}

export function DashboardStats({ stats }: StatsProps) {
  // Handle null stats
  if (!stats) {
    return (
      <div className="text-center text-gray-500 py-8">
        Loading statistics...
      </div>
    );
  }

  const statCards = [
    {
      title: 'Total Incidents',
      value: stats.total_incidents || 0,
      icon: ExclamationTriangleIcon,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    {
      title: 'Active Incidents',
      value: stats.active_incidents || 0,
      icon: ArrowTrendingUpIcon,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100'
    },
    {
      title: 'Resolved Today',
      value: stats.resolved_today || 0,
      icon: CheckCircleIcon,
      color: 'text-green-600',
      bgColor: 'bg-green-100'
    },
    {
      title: 'Avg Resolution Time',
      value: `${Math.round(stats.avg_resolution_time_minutes || 0)}m`,
      icon: ClockIcon,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {statCards.map((stat, index) => (
        <div key={index} className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">{stat.title}</p>
              <p className="text-3xl font-bold mt-2">{stat.value}</p>
            </div>
            <div className={`${stat.bgColor} p-3 rounded-full`}>
              <stat.icon className={`w-6 h-6 ${stat.color}`} />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
