 
export interface Incident {
  id: number;
  title: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  status: 'detected' | 'analyzing' | 'resolving' | 'resolved' | 'failed';
  service_name: string;
  error_type: string;
  root_cause: string | null;
  resolution_steps: string[];
  detected_at: string;
  resolved_at: string | null;
  metadata?: Record<string, any>;
}

export interface IncidentAction {
  id: number;
  incident_id: number;
  action_type: string;
  description: string;
  result: Record<string, any>;
  success: number;
  created_at: string;
}

export interface DashboardStats {
  total_incidents: number;
  active_incidents: number;
  resolved_today: number;
  avg_resolution_time_minutes: number;
  severity_distribution: Record<string, number>;
  top_services: Array<{ service: string; count: number }>;
  daily_trend: Array<{ date: string; count: number }>;
}
