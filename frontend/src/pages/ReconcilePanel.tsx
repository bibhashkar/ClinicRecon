import { useState } from 'react';
import { apiCall } from '../lib/api';
import { Card } from './Card'; // simple div with Tailwind
import { Loader2, Check, X } from 'lucide-react';

export default function ReconcilePanel({ apiKey }: { apiKey: string }) {
  const [input, setInput] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [approved, setApproved] = useState(false);

  const loadSample = async (num: number) => {
    // Load one of your 10 test cases (case_1_reconcile.json etc.)
    const sample = await import(`../../fixtures/case_${num}_reconcile.json`);
    setInput(JSON.stringify(sample.default, null, 2));
  };

  const reconcile = async () => {
    setLoading(true);
    try {
      const data = JSON.parse(input);
      const res = await apiCall('/reconcile/medication', data, apiKey);
      setResult(res);
      setApproved(false);
    } catch (err: any) {
      alert(err.message);
    }
    setLoading(false);
  };

  return (
    <div className="grid grid-cols-2 gap-8">
      {/* Input Side */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Input Conflicting Sources</h2>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="w-full h-96 font-mono text-sm p-4 border rounded-xl"
          placeholder="Paste JSON or click Load Sample"
        />
        <div className="flex gap-3 mt-4">
          <button onClick={() => loadSample(1)} className="px-6 py-3 bg-gray-200 rounded-lg">Load Sample 1 (Metformin)</button>
          <button onClick={() => loadSample(2)} className="px-6 py-3 bg-gray-200 rounded-lg">Load Sample 2 (Aspirin)</button>
          <button
            onClick={reconcile}
            disabled={loading}
            className="flex-1 bg-emerald-600 text-white py-3 rounded-xl font-semibold flex items-center justify-center gap-2"
          >
            {loading && <Loader2 className="animate-spin" />} Reconcile with AI
          </button>
        </div>
      </div>

      {/* Result Side */}
      {result && (
        <Card className="p-8">
          <h3 className="text-2xl font-bold text-emerald-700">{result.reconciled_medication}</h3>
          
          <div className="my-6">
            <div className="flex justify-between text-sm mb-2">
              <span>Confidence</span>
              <span>{(result.confidence_score * 100).toFixed(0)}%</span>
            </div>
            <div className="h-4 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-emerald-500 to-teal-500 transition-all"
                style={{ width: `${result.confidence_score * 100}%` }}
              />
            </div>
          </div>

          <div className="bg-gray-50 p-5 rounded-xl text-sm leading-relaxed">
            {result.reasoning}
          </div>

          <div className="mt-6 flex gap-3">
            <button
              onClick={() => setApproved(true)}
              className="flex-1 bg-emerald-600 text-white py-4 rounded-xl flex items-center justify-center gap-2"
            >
              <Check /> Approve & Update EHR
            </button>
            <button
              onClick={() => setApproved(false)}
              className="flex-1 bg-red-600 text-white py-4 rounded-xl flex items-center justify-center gap-2"
            >
              <X /> Reject Suggestion
            </button>
          </div>

          {approved && <p className="mt-4 text-emerald-600 font-medium">✅ Approved – ready for clinical use</p>}
        </Card>
      )}
    </div>
  );
}