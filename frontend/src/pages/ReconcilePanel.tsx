import { useState } from 'react';
import { Loader2, CheckCircle, XCircle } from 'lucide-react';

// const API_BASE = import.meta.env.DEV ? '' : 'http://localhost:8000';
const API_BASE = 'http://localhost:8000';

export default function ReconcilePanel({ apiKey }: { apiKey: string }) {
  const [input, setInput] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<'idle' | 'approved' | 'rejected'>('idle');

  const loadSample = (num: number) => {
    // You already have these fixtures – just load one
    fetch(`/fixtures/case_${num}_reconcile.json`)
      .then(r => r.json())
      .then(data => setInput(JSON.stringify(data, null, 2)));
  };

  const reconcile = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/reconcile/medication`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': apiKey,
        },
        body: input,
      });
      const data = await res.json();
      setResult(data);
      setStatus('idle');
    } catch (err: any) {
      alert('Error: ' + err.message);
    }
    setLoading(false);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
      {/* Left: Input */}
      <div className="bg-white p-8 rounded-3xl shadow">
        <h2 className="text-2xl font-semibold mb-6">Input Conflicting Records</h2>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="w-full h-96 font-mono text-sm p-6 border border-gray-200 rounded-2xl focus:outline-none"
          placeholder='Paste JSON here or click "Load Sample"'
        />
        <div className="flex gap-4 mt-6">
          <button onClick={() => loadSample(1)} className="flex-1 py-4 bg-gray-100 hover:bg-gray-200 rounded-2xl font-medium">Load Sample 1 (Metformin)</button>
          <button onClick={reconcile} disabled={loading} className="flex-1 py-4 bg-emerald-600 hover:bg-emerald-700 text-white rounded-2xl font-semibold flex items-center justify-center gap-2">
            {loading && <Loader2 className="animate-spin" />} Reconcile with AI
          </button>
        </div>
      </div>

      {/* Right: Result */}
      {result && (
        <div className="bg-white p-8 rounded-3xl shadow">
          <h3 className="text-3xl font-bold text-emerald-700">{result.reconciled_medication}</h3>

          <div className="mt-8">
            <div className="flex justify-between mb-2 text-sm">
              <span>Confidence Score</span>
              <span className="font-mono">{(result.confidence_score * 100).toFixed(0)}%</span>
            </div>
            <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
              <div className="h-full bg-gradient-to-r from-emerald-500 to-teal-500" style={{ width: `${result.confidence_score * 100}%` }} />
            </div>
          </div>

          <div className="mt-8 bg-gray-50 p-6 rounded-2xl text-sm leading-relaxed">
            {result.reasoning}
          </div>

          <div className="mt-10 flex gap-4">
            <button
              onClick={() => setStatus('approved')}
              className="flex-1 py-5 bg-emerald-600 text-white rounded-2xl font-semibold flex items-center justify-center gap-3"
            >
              <CheckCircle className="w-6 h-6" /> Approve & Update EHR
            </button>
            <button
              onClick={() => setStatus('rejected')}
              className="flex-1 py-5 bg-red-600 text-white rounded-2xl font-semibold flex items-center justify-center gap-3"
            >
              <XCircle className="w-6 h-6" /> Reject Suggestion
            </button>
          </div>

          {status === 'approved' && <p className="mt-6 text-emerald-600 font-medium text-center">✅ Approved – ready for clinical use</p>}
        </div>
      )}
    </div>
  );
}