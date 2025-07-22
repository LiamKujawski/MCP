'use client';

import { useEffect, useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface WorkflowStatus {
  workflow_id: string;
  status: string;
  phases_completed: string[];
  current_phase?: string | null;
  start_time: string;
  end_time?: string | null;
  error?: string | null;
}

export default function Dashboard() {
  const [workflowId, setWorkflowId] = useState<string | null>(null);
  const [status, setStatus] = useState<WorkflowStatus | null>(null);
  const [loading, setLoading] = useState(false);

  const startWorkflow = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/workflow/start`, {
        method: 'POST',
      });
      if (!res.ok) throw new Error('Request failed');
      const data: WorkflowStatus = await res.json();
      setWorkflowId(data.workflow_id);
      setStatus(data);
    } catch (err) {
      alert('Unable to start workflow. Please ensure the backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Poll for status updates
  useEffect(() => {
    if (!workflowId) return;
    const id = setInterval(async () => {
      try {
        const res = await fetch(`${API_URL}/workflow/${workflowId}/status`);
        if (!res.ok) throw new Error('Status fetch failed');
        const data: WorkflowStatus = await res.json();
        setStatus(data);
        // Stop polling once completed/failed
        if (data.status !== 'running') clearInterval(id);
      } catch (err) {
        console.error(err);
      }
    }, 3000);
    return () => clearInterval(id);
  }, [workflowId]);

  return (
    <main className="flex flex-col items-center p-8 min-h-screen bg-gray-50 dark:bg-black">
      <h1 className="text-4xl font-bold mb-8 text-center">MCP Control Panel</h1>

      <button
        onClick={startWorkflow}
        disabled={loading || !!workflowId}
        className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-semibold px-6 py-3 rounded-md shadow"
      >
        {loading ? 'Starting…' : 'Start Full Research → Synthesis Workflow'}
      </button>

      {status && (
        <section className="mt-10 w-full max-w-2xl">
          <h2 className="text-2xl font-semibold mb-4">Workflow Status</h2>
          <pre className="bg-white dark:bg-gray-900 p-4 rounded-md overflow-x-auto text-sm text-gray-800 dark:text-gray-100">
            {JSON.stringify(status, null, 2)}
          </pre>
        </section>
      )}
    </main>
  );
}