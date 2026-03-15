import { useState } from 'react';
import ReconcilePanel from './pages/ReconcilePanel';
import DataQualityPanel from './pages/DataQualityPanel';

function App() {
  const [activeTab, setActiveTab] = useState<'reconcile' | 'quality'>('reconcile');

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <header className="text-center mb-10">
          <h1 className="text-5xl font-bold text-emerald-700 tracking-tight">Onye</h1>
          <p className="text-xl text-gray-600 mt-2">Clinical Data Reconciliation Engine</p>
        </header>        

        {/* Simple Tabs */}
        <div className="flex border-b mb-8">
          <button
            onClick={() => setActiveTab('reconcile')}
            className={`px-8 py-4 font-medium text-lg ${activeTab === 'reconcile' ? 'border-b-4 border-emerald-600 text-emerald-700' : 'text-gray-500'}`}
          >
            Medication Reconciliation
          </button>
          <button
            onClick={() => setActiveTab('quality')}
            className={`px-8 py-4 font-medium text-lg ${activeTab === 'quality' ? 'border-b-4 border-emerald-600 text-emerald-700' : 'text-gray-500'}`}
          >
            Data Quality Validation
          </button>
        </div>

        {activeTab === 'reconcile' && <ReconcilePanel apiKey={apiKey} />}
        {activeTab === 'quality' && <DataQualityPanel apiKey={apiKey} />}
      </div>
    </div>
  );
}

export default App;