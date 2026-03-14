import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/Tabs'; // (see below)
import ReconcilePanel from './pages/ReconcilePanel';
import QualityPanel from './pages/QualityPanel';

function App() {
  const [apiKey, setApiKey] = useState('your-secret-api-key-for-basic-auth');

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-5xl mx-auto">
        <header className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-emerald-700">Onye Reconciliation Engine</h1>
          <p className="text-gray-600 mt-2">Clinical Data Reconciliation & Quality Validation</p>
        </header>

        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">API Key (for auth)</label>
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            className="w-96 px-4 py-2 border rounded-lg"
          />
        </div>

        <Tabs defaultValue="reconcile" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="reconcile">Medication Reconciliation</TabsTrigger>
            <TabsTrigger value="quality">Data Quality Validation</TabsTrigger>
          </TabsList>

          <TabsContent value="reconcile">
            <ReconcilePanel apiKey={apiKey} />
          </TabsContent>
          <TabsContent value="quality">
            <QualityPanel apiKey={apiKey} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}

export default App;