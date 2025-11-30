 
import axios from 'axios';
import { Incident, DashboardStats, IncidentAction } from '@/types/incident';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const incidentApi = {
  // Get all incidents
  getIncidents: async (params?: {
    status?: string;
    severity?: string;
    service?: string;
    limit?: number;
    offset?: number;
  }): Promise<Incident[]> => {
    const response = await api.get('/incidents', { params });
    return response.data;
  },

  // Get incident by ID
  getIncident: async (id: number): Promise<Incident> => {
    const response = await api.get(`/incidents/${id}`);
    return response.data;
  },

  // Get incident actions
  getIncidentActions: async (id: number): Promise<IncidentAction[]> => {
    const response = await api.get(`/incidents/${id}/actions`);
    return response.data;
  },

  // Update incident status
  updateStatus: async (id: number, status: string): Promise<void> => {
    await api.put(`/incidents/${id}/status`, { status });
  },
};

export const analyticsApi = {
  // Get dashboard stats
  getDashboardStats: async (): Promise<DashboardStats> => {
    const response = await api.get('/analytics/dashboard');
    return response.data;
  },

  // Get MTTR
  getMTTR: async (days: number = 30): Promise<{ mttr_minutes: number; sample_size: number }> => {
    const response = await api.get('/analytics/mttr', { params: { days } });
    return response.data;
  },
};

export default api;
