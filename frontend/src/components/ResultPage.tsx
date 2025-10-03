import { useEffect, useState } from 'react';
import { UXKit } from '../types';

export default function ResultPage() {
  const [kit, setKit] = useState<UXKit | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem('uxKit');
    if (saved) {
      const parsed = JSON.parse(saved);
      setKit(parsed);
      // Cargar fuente
      const link = document.createElement('link');
      link.href = parsed.typography.importUrl;
      link.rel = 'stylesheet';
      document.head.appendChild(link);
    }
  }, []);

  if (!kit) return <div className="p-6">No se encontró resultado.</div>;

  const downloadFile = (content: string, filename: string, type = 'text/plain') => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      <h1 className="text-3xl font-bold">Tu UI Kit</h1>
      <p className="text-gray-600">{kit.explanation}</p>

      {/* Paleta */}
      <div>
        <h2 className="text-xl font-semibold mb-2">Paleta</h2>
        <div className="flex gap-4">
          <div className="w-16 h-16 rounded" style={{ backgroundColor: kit.palette.primary }}></div>
          <div className="w-16 h-16 rounded" style={{ backgroundColor: kit.palette.secondary }}></div>
          {kit.palette.neutral.slice(0, 3).map((color, i) => (
            <div key={i} className="w-12 h-12 rounded border" style={{ backgroundColor: color }}></div>
          ))}
        </div>
      </div>

      {/* Tipografía */}
      <div>
        <h2 className="text-xl font-semibold mb-2">Tipografía</h2>
        <p style={{ fontFamily: kit.typography.family }} className="text-2xl">
          {kit.typography.family} — Hola, esto es un ejemplo.
        </p>
      </div>

      {/* Botón de ejemplo */}
      <div>
        <h2 className="text-xl font-semibold mb-2">Componente: Botón</h2>
        <button
          className="px-4 py-2 rounded-md"
          style={{
            backgroundColor: kit.palette.primary,
            color: 'white',
            fontFamily: kit.typography.family,
            borderRadius: kit.tokens.radii.md
          }}
        >
          Botón primario
        </button>
      </div>

      {/* Exportación */}
      <div className="pt-6 border-t">
        <h2 className="text-xl font-semibold mb-4">Descargar</h2>
        <div className="flex gap-3">
          <button
            onClick={() => downloadFile(kit.exports.css, 'variables.css')}
            className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
          >
            Descargar CSS
          </button>
          <button
            onClick={() => downloadFile(JSON.stringify(kit.exports.json, null, 2), 'ux-kit.json')}
            className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
          >
            Descargar JSON
          </button>
          <button
            onClick={() => downloadFile(JSON.stringify(kit.exports.figma, null, 2), 'figma-tokens.json')}
            className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
          >
            Figma Tokens
          </button>
        </div>
      </div>
    </div>
  );
}