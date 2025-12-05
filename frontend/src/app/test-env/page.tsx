export default function TestEnv() {
    return (
        <div style={{ padding: '20px', fontFamily: 'monospace' }}>
            <h1>Environment Variables Test</h1>
            <p><strong>NEXT_PUBLIC_API_URL:</strong> {process.env.NEXT_PUBLIC_API_URL || 'NOT SET'}</p>
            <p><strong>NEXT_PUBLIC_WS_URL:</strong> {process.env.NEXT_PUBLIC_WS_URL || 'NOT SET'}</p>
        </div>
    );
}
