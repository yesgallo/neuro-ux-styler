import { useState } from 'react';

interface UXKit {
  explanation: string;
  palette: {
    primary: string;
    secondary: string;
    neutral: string[];
  };
  typography: {
    family: string;
    importUrl: string;
  };
  tokens: {
    radii: {
      sm: string;
      md: string;
      lg: string;
    };
    shadows: {
      sm: string;
      md: string;
      lg: string;
    };
  };
  exports: {
    css: string;
    json: object;
    figma: object;
  };
}

export default function ResultPage() {
  const [copiedColor, setCopiedColor] = useState<string | null>(null);
  
  // Mock data para demostración
  const kit: UXKit = {
    explanation: "Paleta vibrante y moderna que combina cyan energético con azul profesional, perfecta para una marca tech innovadora centrada en UX y neurociencia aplicada al diseño.",
    palette: {
      primary: "#00BCD4",
      secondary: "#2563EB",
      neutral: ["#1E293B", "#475569", "#94A3B8", "#E2E8F0", "#F8FAFC"]
    },
    typography: {
      family: "Inter",
      importUrl: "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    },
    tokens: {
      radii: { sm: "0.5rem", md: "0.75rem", lg: "1rem" },
      shadows: { 
        sm: "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        md: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
        lg: "0 10px 15px -3px rgba(0, 0, 0, 0.1)"
      }
    },
    exports: {
      css: ":root { --primary: #00BCD4; }",
      json: { primary: "#00BCD4" },
      figma: { primary: { value: "#00BCD4" } }
    }
  };

  const downloadFile = (content: string, filename: string) => {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const copyColor = (color: string) => {
    navigator.clipboard.writeText(color);
    setCopiedColor(color);
    setTimeout(() => setCopiedColor(null), 2000);
  };

  const colorPalette = [
    { color: kit.palette.primary, label: 'Primary' },
    { color: kit.palette.secondary, label: 'Secondary' },
    ...kit.palette.neutral.slice(0, 5).map((c, i) => ({ color: c, label: `Neutral ${i + 1}` }))
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 py-12 px-4 relative overflow-hidden">
      {/* Efectos de fondo */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-400/5 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-blue-600/5 rounded-full blur-3xl"></div>
      </div>

      <div className="max-w-5xl mx-auto relative z-10">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="text-6xl mb-4">🧠</div>
          <h1 className="text-4xl font-bold text-white mb-3 flex items-center justify-center gap-3">
            <span className="bg-gradient-to-r from-cyan-400 to-blue-600 bg-clip-text text-transparent">
              Tu UI Kit
            </span>
          </h1>
          <p className="text-slate-300 max-w-3xl mx-auto text-lg leading-relaxed">
            {kit.explanation}
          </p>
          <button className="mt-6 text-cyan-400 hover:text-cyan-300 transition-colors flex items-center gap-2 mx-auto group">
            <span className="group-hover:-translate-x-1 transition-transform inline-block">←</span>
            <span>Crear nuevo kit</span>
          </button>
        </div>

        {/* Paleta de colores */}
        <section className="bg-slate-900/50 backdrop-blur-xl rounded-2xl border border-slate-800/50 p-8 mb-6 shadow-2xl">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-cyan-400/10 to-blue-600/10 rounded-lg">
              <span className="text-2xl">🎨</span>
            </div>
            <h2 className="text-2xl font-semibold text-white">Paleta de colores</h2>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
            {colorPalette.map(({ color, label }) => (
              <div key={color} className="group">
                <div 
                  className="w-full aspect-square rounded-xl border-2 border-slate-700 mb-3 cursor-pointer hover:scale-105 transition-all duration-300 relative overflow-hidden shadow-lg"
                  style={{ backgroundColor: color }}
                  onClick={() => copyColor(color)}
                >
                  <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex items-center justify-center">
                    <span className="text-2xl opacity-0 group-hover:opacity-100 transition-opacity">
                      {copiedColor === color ? '✓' : '📋'}
                    </span>
                  </div>
                </div>
                <p className="text-xs text-slate-400 mb-1">{label}</p>
                <p className="text-xs font-mono text-slate-300">{color}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Tipografía */}
        <section className="bg-slate-900/50 backdrop-blur-xl rounded-2xl border border-slate-800/50 p-8 mb-6 shadow-2xl">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-cyan-400/10 to-blue-600/10 rounded-lg">
              <span className="text-2xl">Aa</span>
            </div>
            <h2 className="text-2xl font-semibold text-white">Tipografía</h2>
          </div>
          
          <div 
            className="p-6 bg-slate-800/50 rounded-xl border border-slate-700"
            style={{ fontFamily: kit.typography.family }}
          >
            <h3 className="text-3xl font-bold text-white mb-4">
              Aa Bb Cc 123
            </h3>
            <p className="text-slate-300 text-lg leading-relaxed mb-2">
              Este es un párrafo de ejemplo con la tipografía seleccionada. 
            </p>
            <p className="text-slate-400 text-sm">
              {kit.typography.family} es una fuente de Google Fonts gratuita y coherente con tu marca.
            </p>
          </div>
          
          <a 
            href={`https://fonts.google.com/specimen/${kit.typography.family.replace(' ', '+')}`}
            target="_blank"
            rel="noreferrer"
            className="mt-4 inline-flex items-center gap-2 text-cyan-400 hover:text-cyan-300 transition-colors text-sm group"
          >
            <span>Ver en Google Fonts</span>
            <span className="group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform inline-block">↗</span>
          </a>
        </section>

        {/* Componentes */}
        <section className="bg-slate-900/50 backdrop-blur-xl rounded-2xl border border-slate-800/50 p-8 mb-6 shadow-2xl">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-cyan-400/10 to-blue-600/10 rounded-lg">
              <span className="text-2xl">📦</span>
            </div>
            <h2 className="text-2xl font-semibold text-white">Componentes</h2>
          </div>
          
          <div className="space-y-6">
            {/* Botones */}
            <div className="flex flex-wrap gap-4">
              <button
                className="px-6 py-3 rounded-xl font-semibold transition-all duration-300 hover:scale-105 shadow-lg"
                style={{
                  backgroundColor: kit.palette.primary,
                  color: 'white',
                  fontFamily: kit.typography.family
                }}
              >
                Botón primario
              </button>
              <button
                className="px-6 py-3 rounded-xl font-semibold transition-all duration-300 hover:scale-105 border-2 shadow-lg"
                style={{
                  backgroundColor: 'transparent',
                  color: kit.palette.primary,
                  borderColor: kit.palette.primary,
                  fontFamily: kit.typography.family
                }}
              >
                Botón secundario
              </button>
            </div>

            {/* Tarjetas */}
            <div className="grid md:grid-cols-2 gap-4">
              <div 
                className="p-6 bg-slate-800/50 border border-slate-700 rounded-xl hover:border-cyan-400/50 transition-all duration-300 group"
                style={{ fontFamily: kit.typography.family }}
              >
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-cyan-400 to-blue-600 mb-4 group-hover:scale-110 transition-transform"></div>
                <h4 className="font-bold text-white text-lg mb-2">Tarjeta de ejemplo</h4>
                <p className="text-slate-400 text-sm">Contenido representativo de tu marca con estilo coherente.</p>
              </div>
              
              <div 
                className="p-6 bg-slate-800/50 border border-slate-700 rounded-xl hover:border-blue-600/50 transition-all duration-300 group"
                style={{ fontFamily: kit.typography.family }}
              >
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-600 to-cyan-400 mb-4 group-hover:scale-110 transition-transform"></div>
                <h4 className="font-bold text-white text-lg mb-2">Segunda tarjeta</h4>
                <p className="text-slate-400 text-sm">Ejemplo de variación manteniendo la identidad visual.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Descargas */}
        <section className="bg-gradient-to-br from-slate-900/80 to-slate-800/80 backdrop-blur-xl rounded-2xl border border-slate-700/50 p-8 shadow-2xl">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-br from-cyan-400/10 to-blue-600/10 rounded-lg">
              <span className="text-2xl">📥</span>
            </div>
            <h2 className="text-2xl font-semibold text-white">Descargar UI Kit</h2>
          </div>
          
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => downloadFile(kit.exports.css, 'variables.css')}
              className="px-6 py-3 bg-gradient-to-r from-cyan-400 to-cyan-500 text-white rounded-xl hover:from-cyan-500 hover:to-cyan-600 transition-all duration-300 font-semibold shadow-lg hover:shadow-cyan-400/50 hover:scale-105 flex items-center gap-2"
            >
              <span>📥</span>
              CSS Variables
            </button>
            <button
              onClick={() => downloadFile(JSON.stringify(kit.exports.json, null, 2), 'ux-kit.json')}
              className="px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-xl transition-all duration-300 font-semibold shadow-lg hover:scale-105 flex items-center gap-2"
            >
              <span>📥</span>
              JSON
            </button>
            <button
              onClick={() => downloadFile(JSON.stringify(kit.exports.figma, null, 2), 'figma-tokens.json')}
              className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white rounded-xl transition-all duration-300 font-semibold shadow-lg hover:shadow-purple-500/50 hover:scale-105 flex items-center gap-2"
            >
              <span>📥</span>
              Figma Tokens
            </button>
          </div>
          
          <p className="mt-6 text-slate-400 text-sm">
            💡 Los archivos descargados están listos para usar en tu proyecto o importar directamente en Figma.
          </p>
        </section>
      </div>
    </div>
  );
}
