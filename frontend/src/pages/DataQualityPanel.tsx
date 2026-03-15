import { useState } from 'react';
import { Loader2, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';
import ApiResponseDisplay from '../components/ApiResponseDisplay';

// Use the Vite dev-server proxy (configured in vite.config.ts), or a custom base at build time.
// In docker-compose mode, `/api/*` is proxied to the backend service.
const API_BASE = "http://localhost:8000";

export default function DataQualityPanel() {
  const [input, setInput] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const loadSample = (num: number) => {
    // Load sample data quality record
    fetch(`/fixtures/case_${num}_quality.json`)
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}: ${r.statusText}`);
        return r.json();
      })
      .then(data => setInput(JSON.stringify(data, null, 2)))
      .catch(err => {
        console.error('Error loading sample:', err);
        alert('Error loading sample: ' + err.message);
      });
  };

  const validate = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/validate/data-quality`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: input,
      });

      const text = await res.text();
      if (!res.ok) {
        throw new Error(text || `${res.status} ${res.statusText}`);
      }

      const data = JSON.parse(text);
      setResult(data);
    } catch (err: any) {
      console.error(err);
      alert('Error: ' + err.message);
    }
    setLoading(false);
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'high': return <XCircle className="w-4 h-4 text-red-500" />;
      case 'medium': return <AlertTriangle className="w-4 h-4 text-yellow-500" />;
      case 'low': return <CheckCircle className="w-4 h-4 text-green-500" />;
      default: return null;
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
      {/* Left: Input */}
      <div className="bg-white p-8 rounded-3xl shadow">
        <h2 className="text-2xl font-semibold mb-6">Data Quality Validation</h2>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="w-full h-96 font-mono text-sm p-6 border border-gray-200 rounded-2xl focus:outline-none"
          placeholder='Paste patient record JSON here or click "Load Sample"'
        />
        <div className="flex gap-4 mt-6">
          <button onClick={() => loadSample(1)} className="flex-1 py-4 bg-gray-100 hover:bg-gray-200 rounded-2xl font-medium">Load Sample 1</button>
          <button onClick={validate} disabled={loading} className="flex-1 py-4 bg-emerald-600 hover:bg-emerald-700 text-white rounded-2xl font-semibold flex items-center justify-center gap-2">
            {loading && <Loader2 className="animate-spin" />} Validate Quality
          </button>
        </div>
      </div>

      {/* Right: Result */}
      {result && (
        <div className="bg-white p-8 rounded-3xl shadow">
          <h3 className="text-3xl font-bold text-emerald-700">Quality Score: {result.overall_score}/100</h3>

          <div className="mt-8 space-y-4">
            {Object.entries(result.breakdown).map(([key, value]: [string, any]) => (
              <div key={key} className="flex justify-between items-center">
                <span className="capitalize">{key.replace('_', ' ')}:</span>
                <span className={`font-mono font-bold ${getScoreColor(value)}`}>{value}/100</span>
              </div>
            ))}
          </div>

          <div className="mt-8">
            <h4 className="text-lg font-semibold mb-4">Issues Detected</h4>
            {result.issues_detected.length === 0 ? (
              <p className="text-green-600">No issues detected ✅</p>
            ) : (
              <div className="space-y-3">
                {result.issues_detected.map((issue: any, index: number) => (
                  <div key={index} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                    {getSeverityIcon(issue.severity)}
                    <div>
                      <p className="font-medium">{issue.field}</p>
                      <p className="text-sm text-gray-600">{issue.issue}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Raw API Response */}
      <ApiResponseDisplay result={result} />
    </div>
  );
}