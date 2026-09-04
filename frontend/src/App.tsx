import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import { Settings, Loader2, Upload } from 'lucide-react';
import { diffWords } from 'diff';

type PipelineEvent = {
  step: string;
  result?: {
    original: string;
    result: string;
    validation: any;
    artifacts: any[];
  }
};

export default function App() {
  const [activeTab, setActiveTab] = useState<'editor' | 'diff' | 'inspector' | 'settings'>('editor');
  const [processing, setProcessing] = useState(false);
  const [progressStep, setProgressStep] = useState<string>('');
  const [result, setResult] = useState<PipelineEvent['result'] | null>(null);

  const editor = useEditor({
    extensions: [StarterKit],
    content: '<p>Paste your text here to begin.</p>',
    editorProps: {
      attributes: {
        class: 'prose prose-sm sm:prose lg:prose-lg xl:prose-2xl focus:outline-none min-h-[500px] border border-gray-200 p-8 rounded shadow-sm',
      },
    },
  });

  const handleProcess = async () => {
    if (!editor) return;
    const text = editor.getText();
    setProcessing(true);
    setProgressStep('Starting...');
    setResult(null);
    setActiveTab('editor'); // keep them in editor to see progress overlay

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8765';
      const response = await fetch(`${apiUrl}/api/text/cando`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: text })
      });

      if (!response.body) throw new Error("No body");
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n').filter(Boolean);
        for (const line of lines) {
          const data = JSON.parse(line) as PipelineEvent;
          setProgressStep(data.step);
          if (data.step === 'Done' && data.result) {
            setResult(data.result);
            setActiveTab('diff');
          }
        }
      }
    } catch (e) {
      console.error(e);
      alert('Failed to process. Check if backend is running.');
    } finally {
      setProcessing(false);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setProcessing(true);
    setProgressStep('Processing file...');
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8765';
      const response = await fetch(`${apiUrl}/api/file/process`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('File processing failed');

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      
      let filename = `cando_processed.docx`;
      const disposition = response.headers.get('content-disposition');
      if (disposition && disposition.includes('filename="')) {
         filename = disposition.split('filename="')[1].split('"')[0];
      }
      
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      a.remove();
      
      setProgressStep('Download complete!');
      setTimeout(() => setProgressStep(''), 3000);
    } catch (e) {
      console.error(e);
      alert('Failed to process file.');
      setProgressStep('');
    } finally {
      setProcessing(false);
      event.target.value = ''; // Reset input
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center sticky top-0 z-10">
        <h1 className="text-xl font-semibold tracking-tight">CANDO</h1>
        <div className="flex space-x-4">
          <button onClick={() => setActiveTab('editor')} className={`px-3 py-1.5 rounded ${activeTab === 'editor' ? 'bg-gray-100 font-medium' : 'hover:bg-gray-50'}`}>Editor</button>
          <button onClick={() => setActiveTab('diff')} disabled={!result} className={`px-3 py-1.5 rounded disabled:opacity-50 ${activeTab === 'diff' ? 'bg-gray-100 font-medium' : 'hover:bg-gray-50'}`}>Diff</button>
          <button onClick={() => setActiveTab('inspector')} disabled={!result} className={`px-3 py-1.5 rounded disabled:opacity-50 ${activeTab === 'inspector' ? 'bg-gray-100 font-medium' : 'hover:bg-gray-50'}`}>Inspector</button>
          <button onClick={() => setActiveTab('settings')} className={`px-3 py-1.5 rounded ${activeTab === 'settings' ? 'bg-gray-100 font-medium' : 'hover:bg-gray-50'}`}>
            <Settings size={18} />
          </button>
        </div>
      </header>

      <main className="max-w-5xl mx-auto py-8 px-4">
        {activeTab === 'editor' && (
          <div className="relative">
            <div className="mb-4 flex justify-end space-x-3">
              <label className="cursor-pointer bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded font-medium flex items-center hover:bg-gray-50 disabled:opacity-50">
                <Upload className="mr-2" size={18} /> Upload DOCX/PDF
                <input type="file" accept=".docx,.pdf" className="hidden" onChange={handleFileUpload} disabled={processing} />
              </label>
              <button 
                onClick={handleProcess} 
                disabled={processing}
                className="bg-black text-white px-4 py-2 rounded font-medium flex items-center hover:bg-gray-800 disabled:bg-gray-400"
              >
                {processing ? <><Loader2 className="animate-spin mr-2" size={18} /> {progressStep}</> : 'Process Text'}
              </button>
            </div>
            <div className="bg-white">
              <EditorContent editor={editor} />
            </div>
          </div>
        )}

        {activeTab === 'diff' && result && (
          <DiffView original={result.original} revised={result.result} />
        )}

        {activeTab === 'inspector' && result && (
          <div className="bg-white border border-gray-200 rounded p-8">
            <h2 className="text-2xl font-semibold mb-6">Inspector Report</h2>
            <div className="mb-6">
              <h3 className="font-medium text-lg mb-2 border-b pb-2">Artifacts Cleared</h3>
              {result.artifacts.length === 0 ? <p className="text-gray-500">No hidden artifacts found.</p> : (
                <ul className="list-disc pl-5">
                  {result.artifacts.map((a, i) => (
                    <li key={i}>{a.count}x {a.type}</li>
                  ))}
                </ul>
              )}
            </div>
            <div>
              <h3 className="font-medium text-lg mb-2 border-b pb-2">Validation</h3>
              <p className={`font-medium ${result.validation.severity === 'ok' ? 'text-green-600' : 'text-orange-600'}`}>
                Status: {result.validation.severity.toUpperCase()}
              </p>
              <pre className="mt-4 bg-gray-50 p-4 rounded text-sm overflow-x-auto">
                {JSON.stringify(result.validation, null, 2)}
              </pre>
            </div>
          </div>
        )}

        {activeTab === 'settings' && (
          <div className="bg-white border border-gray-200 rounded p-8 max-w-lg mx-auto">
             <h2 className="text-2xl font-semibold mb-6">Settings</h2>
             <p className="text-gray-500 mb-4">Edit configuration in backend/.env for now. Phase 2 UI settings stub.</p>
          </div>
        )}
      </main>
    </div>
  );
}

function DiffView({ original, revised }: { original: string, revised: string }) {
  const diffs = diffWords(original, revised);

  return (
    <div className="bg-white border border-gray-200 rounded p-8 leading-relaxed text-lg">
      <div className="mb-6 flex space-x-6 text-sm font-medium border-b pb-4">
        <span className="flex items-center text-red-600 bg-red-50 px-2 py-1 rounded"><span className="mr-2">−</span> Removed</span>
        <span className="flex items-center text-green-600 bg-green-50 px-2 py-1 rounded"><span className="mr-2">+</span> Added</span>
      </div>
      <div>
        {diffs.map((part, index) => {
          if (part.added) {
            return <span key={index} className="bg-green-100 text-green-800 rounded px-0.5 mx-0.5">{part.value}</span>;
          }
          if (part.removed) {
            return <span key={index} className="bg-red-100 text-red-800 rounded px-0.5 mx-0.5 line-through opacity-70">{part.value}</span>;
          }
          return <span key={index}>{part.value}</span>;
        })}
      </div>
    </div>
  );
}
