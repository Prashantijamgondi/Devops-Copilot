'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';
import { IncidentChart } from '@/components/IncidentChart';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export default function AnalyticsPage() {
    const [stats, setStats] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetchAnalytics();
    }, []);

    const fetchAnalytics = async () => {
        try {
            setError(null);
            const response = await axios.get(`${API_BASE_URL}/analytics/dashboard`);
            setStats(response.data);
            setLoading(false);
        } catch (error: any) {
            console.error('Error fetching analytics:', error);
            setError(error.message || 'Failed to fetch analytics');
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-50">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <div className="text-xl text-gray-600">Loading analytics...</div>
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
                        onClick={fetchAnalytics}
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
                    <h1 className="text-4xl font-bold mb-2">Analytics</h1>
                    <p className="text-gray-600">Detailed insights and metrics</p>
                </div>

                {/* Key Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <div className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center justify-between mb-2">
                            <h3 className="text-sm font-medium text-gray-600">Total Incidents</h3>
                            <span className="text-2xl">📊</span>
                        </div>
                        <p className="text-3xl font-bold text-gray-900">{stats?.total_incidents || 0}</p>
                    </div>

                    <div className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center justify-between mb-2">
                            <h3 className="text-sm font-medium text-gray-600">Active Incidents</h3>
                            <span className="text-2xl">🔴</span>
                        </div>
                        <p className="text-3xl font-bold text-red-600">{stats?.active_incidents || 0}</p>
                    </div>

                    <div className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center justify-between mb-2">
                            <h3 className="text-sm font-medium text-gray-600">Resolved Today</h3>
                            <span className="text-2xl">✅</span>
                        </div>
                        <p className="text-3xl font-bold text-green-600">{stats?.resolved_today || 0}</p>
                    </div>

                    <div className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center justify-between mb-2">
                            <h3 className="text-sm font-medium text-gray-600">Avg Resolution Time</h3>
                            <span className="text-2xl">⏱️</span>
                        </div>
                        <p className="text-3xl font-bold text-blue-600">
                            {stats?.avg_resolution_time_minutes
                                ? `${Math.round(stats.avg_resolution_time_minutes)}m`
                                : '0m'}
                        </p>
                    </div>
                </div>

                {/* Charts */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                    {/* Daily Trend */}
                    <div className="bg-white rounded-lg shadow p-6">
                        <h3 className="text-lg font-semibold mb-4">Daily Incident Trend</h3>
                        {stats?.daily_trend && stats.daily_trend.length > 0 ? (
                            <IncidentChart data={stats.daily_trend} />
                        ) : (
                            <div className="text-center py-12 text-gray-500">
                                <div className="text-4xl mb-2">📈</div>
                                <p>No trend data available yet</p>
                            </div>
                        )}
                    </div>

                    {/* Severity Distribution */}
                    <div className="bg-white rounded-lg shadow p-6">
                        <h3 className="text-lg font-semibold mb-4">Severity Distribution</h3>
                        {stats?.severity_distribution && Object.keys(stats.severity_distribution).length > 0 ? (
                            <div className="space-y-4">
                                {Object.entries(stats.severity_distribution).map(([severity, count]: any) => {
                                    const total = stats.total_incidents || 1;
                                    const percentage = ((count / total) * 100).toFixed(1);

                                    const colors: any = {
                                        critical: 'bg-red-500',
                                        high: 'bg-orange-500',
                                        medium: 'bg-yellow-500',
                                        low: 'bg-blue-500',
                                    };

                                    return (
                                        <div key={severity}>
                                            <div className="flex justify-between items-center mb-1">
                                                <span className="capitalize font-medium">{severity}</span>
                                                <span className="text-sm text-gray-600">{count} ({percentage}%)</span>
                                            </div>
                                            <div className="w-full bg-gray-200 rounded-full h-3">
                                                <div
                                                    className={`${colors[severity.toLowerCase()] || 'bg-gray-500'} h-3 rounded-full transition-all`}
                                                    style={{ width: `${percentage}%` }}
                                                ></div>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        ) : (
                            <div className="text-center py-12 text-gray-500">
                                <div className="text-4xl mb-2">📊</div>
                                <p>No severity data available yet</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Top Services */}
                <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-lg font-semibold mb-4">Top Affected Services</h3>
                    {stats?.top_services && stats.top_services.length > 0 ? (
                        <div className="overflow-x-auto">
                            <table className="min-w-full divide-y divide-gray-200">
                                <thead>
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Service
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Incidents
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Percentage
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {stats.top_services.map((service: any, index: number) => {
                                        const percentage = ((service.count / stats.total_incidents) * 100).toFixed(1);
                                        return (
                                            <tr key={index}>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                                    {service.service_name}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                    {service.count}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                    <div className="flex items-center">
                                                        <div className="w-32 bg-gray-200 rounded-full h-2 mr-2">
                                                            <div
                                                                className="bg-blue-600 h-2 rounded-full"
                                                                style={{ width: `${percentage}%` }}
                                                            ></div>
                                                        </div>
                                                        <span>{percentage}%</span>
                                                    </div>
                                                </td>
                                            </tr>
                                        );
                                    })}
                                </tbody>
                            </table>
                        </div>
                    ) : (
                        <div className="text-center py-12 text-gray-500">
                            <div className="text-4xl mb-2">🔧</div>
                            <p>No service data available yet</p>
                        </div>
                    )}
                </div>
            </div>
        </main>
    );
}
