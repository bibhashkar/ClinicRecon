interface ApiResponseDisplayProps {
  result: any;
  title?: string;
}

export default function ApiResponseDisplay({ result, title = "REST API Response" }: ApiResponseDisplayProps) {
  if (!result) return null;

  return (
    <div className="bg-white rounded-3xl shadow mt-8 w-screen -ml-8 -mr-8 px-8 py-8">
      <h3 className="text-xl font-semibold mb-4">{title}</h3>
      <pre className="bg-gray-50 p-4 rounded-2xl text-sm overflow-x-auto font-mono">
        {JSON.stringify(result, null, 2)}
      </pre>
    </div>
  );
}