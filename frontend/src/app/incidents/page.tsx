'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';
import Link from 'next/link';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface Incident {
    id: string;
    title: string;
    description: string;
    severity: string;
    status: string;
    service_name: string;
    created_at: string;
    resolved_at?: string;
}

export default function IncidentsPage() {
    const [incidents, setIncidents] = useState<Incident[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [filter, setFilter] = useState<string>('all');

    useEffect(() => {
        fetchIncidents();
    }, []);

    const fetchIncidents = async () => {
        try {
            setError(null);
            const response = await axios.get(`${API_BASE_URL}/incidents?limit=100`);
            setIncidents(response.data);
            setLoading(false);
        } catch (error: any) {
            console.error('Error fetching incidents:', error);
            setError(error.message || 'Failed to fetch incidents');
            setLoading(false);
        }
    };

    const filteredIncidents = incidents.filter(incident => {
        if (filter === 'all') return true;
        if (filter === 'active') return incident.status !== 'resolved';
        if (filter === 'resolved') return incident.status === 'resolved';
        return incident.severity === filter;
    });

    const getSeverityColor = (severity: string) => {
        switch (severity.toLowerCase()) {
            case 'critical': return 'bg-red-100 text-red-800 border-red-200';
            case 'high': return 'bg-orange-100 text-orange-800 border-orange-200';
            case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
            case 'low': return 'bg-blue-100 text-blue-800 border-blue-200';
            default: return 'bg-gray-100 text-gray-800 border-gray-200';
        }
    };

    const getStatusColor = (status: string) => {
        switch (status.toLowerCase()) {
            case 'resolved': return 'bg-green-100 text-green-800';
            case 'investigating': return 'bg-yellow-100 text-yellow-800';
            case 'identified': return 'bg-orange-100 text-orange-800';
            default: return 'bg-gray-100 text-gray-800';
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-50">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <div className="text-xl text-gray-600">Loading incidents...</div>
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
                        onClick={fetchIncidents}
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
                <div className="mb-8">
                    <h1 className="text-4xl font-bold mb-2">Incidents</h1>
                    <p className="text-gray-600">View and manage all incidents</p>
                </div>

                {/* Filters */}
                <div className="bg-white rounded-lg shadow p-4 mb-6">
                    <div className="flex flex-wrap gap-2">
                        <button
                            onClick={() => setFilter('all')}
                            className={`px-4 py-2 rounded ${filter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
                        >
                            All ({incidents.length})
                        </button>
                        <button
                            onClick={() => setFilter('active')}
                            className={`px-4 py-2 rounded ${filter === 'active' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
                        >
                            Active ({incidents.filter(i => i.status !== 'resolved').length})
                        </button>
                        <button
                            onClick={() => setFilter('resolved')}
                            className={`px-4 py-2 rounded ${filter === 'resolved' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
                        >
                            Resolved ({incidents.filter(i => i.status === 'resolved').length})
                        </button>
                        <div className="border-l border-gray-300 mx-2"></div>
                        <button
                            onClick={() => setFilter('critical')}
                            className={`px-4 py-2 rounded ${filter === 'critical' ? 'bg-red-600 text-white' : 'bg-red-100 text-red-700 hover:bg-red-200'}`}
                        >
                            Critical
                        </button>
                        <button
                            onClick={() => setFilter('high')}
                            className={`px-4 py-2 rounded ${filter === 'high' ? 'bg-orange-600 text-white' : 'bg-orange-100 text-orange-700 hover:bg-orange-200'}`}
                        >
                            High
                        </button>
                        <button
                            onClick={() => setFilter('medium')}
                            className={`px-4 py-2 rounded ${filter === 'medium' ? 'bg-yellow-600 text-white' : 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200'}`}
                        >
                            Medium
                        </button>
                        <button
                            onClick={() => setFilter('low')}
                            className={`px-4 py-2 rounded ${filter === 'low' ? 'bg-blue-600 text-white' : 'bg-blue-100 text-blue-700 hover:bg-blue-200'}`}
                        >
                            Low
                        </button>
                    </div>
                </div>

                {/* Incidents List */}
                {filteredIncidents.length === 0 ? (
                    <div className="bg-white rounded-lg shadow p-12 text-center">
                        <div className="text-6xl mb-4">📋</div>
                        <h3 className="text-xl font-semibold text-gray-700 mb-2">No incidents found</h3>
                        <p className="text-gray-500">
                            {filter === 'all'
                                ? "No incidents have been reported yet."
                                : `No ${filter} incidents found.`}
                        </p>
                    </div>
                ) : (
                    <div className="space-y-4">
                        {filteredIncidents.map((incident) => (
                            <Link
                                key={incident.id}
                                href={`/incidents/${incident.id}`}
                                className="block bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6"
                            >
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-3 mb-2">
                                            <h3 className="text-xl font-semibold text-gray-900">{incident.title}</h3>
                                            <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getSeverityColor(incident.severity)}`}>
                                                {incident.severity.toUpperCase()}
                                            </span>
                                            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(incident.status)}`}>
                                                {incident.status}
                                            </span>
                                        </div>
                                        <p className="text-gray-600 mb-3">{incident.description}</p>
                                        <div className="flex items-center gap-4 text-sm text-gray-500">
                                            <span>🔧 {incident.service_name}</span>
                                            <span>📅 {new Date(incident.created_at).toLocaleString()}</span>
                                            {incident.resolved_at && (
                                                <span className="text-green-600">✅ Resolved {new Date(incident.resolved_at).toLocaleString()}</span>
                                            )}
                                        </div>
                                    </div>
                                    <div className="ml-4">
                                        <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                        </svg>
                                    </div>
                                </div>
                            </Link>
                        ))}
                    </div>
                )}
            </div>
        </main>
    );
}
