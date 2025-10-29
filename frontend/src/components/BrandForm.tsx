import { useState } from 'react';

interface BrandInput {
  name: string;
  mission: string;
  values: string;
  audience: string;
  sector: string;
}

export default function BrandForm() {
  const [input, setInput] = useState<BrandInput>({
    name: '',
    mission: '',
    values: '',
    audience: '',
    sector: ''
  });
  const [loading, setLoading] = useState(false);
  const [focusedField, setFocusedField] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setInput(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async () => {
    if (!input.name || !input.mission || !input.values || !input.audience || !input.sector) {
      alert('Por favor completa todos los campos');
      return;
    }
    
    setLoading(true);
    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      console.log('Kit generado:', input);
      alert('¡UI Kit generado exitosamente!');
    } catch (err) {
      alert('Error generando el kit. Intenta de nuevo.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fields = [
    { key: 'name', label: 'Nombre de la marca', placeholder: 'Ej: EcoCart', emoji: '🏷️' },
    { key: 'mission', label: 'Misión', placeholder: 'Ej: Hacer el comercio sostenible', emoji: '🎯' },
    { key: 'values', label: 'Valores', placeholder: 'Ej: Sostenibilidad, transparencia', emoji: '💎' },
    { key: 'audience', label: 'Público objetivo', placeholder: 'Ej: Millennials conscientes', emoji: '👥' },
    { key: 'sector', label: 'Sector', placeholder: 'Ej: E-commerce, fintech', emoji: '🏢' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 flex items-center justify-center p-4 relative overflow-hidden">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 -left-20 w-96 h-96 bg-cyan-400/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 -right-20 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-r from-cyan-500/5 to-blue-600/5 rounded-full blur-3xl"></div>
      </div>

      <div className="w-full max-w-lg relative z-10">
        
        <div className="bg-slate-900/50 backdrop-blur-xl rounded-3xl shadow-2xl border border-slate-800/50 overflow-hidden">
         
          <div className="relative bg-gradient-to-br from-cyan-400 via-cyan-500 to-blue-600 p-8 pb-12">
            <div className="absolute inset-0 bg-black/10"></div>
            <div className="relative z-10 text-center">
              <div className="text-7xl mb-4">🧠</div>
              <h1 className="text-3xl font-bold text-white mb-2">
                NEURO
              </h1>
              <p className="text-2xl font-semibold text-blue-900 -mt-1 mb-3 tracking-wide">UX STYLER</p>
              <p className="text-cyan-50 text-sm font-light">Describe tu marca y genera un UI Kit coherente con IA</p>
            </div>
          </div>

          <div className="p-8 -mt-6 relative z-10">
            <div className="space-y-5">
              {fields.map(({ key, label, placeholder, emoji }) => (
                <div key={key} className="group">
                  <label className="block text-sm font-medium text-slate-300 mb-2 flex items-center gap-2">
                    <span className="text-lg">{emoji}</span>
                    {label}
                  </label>
                  <div className="relative">
                    <input
                      type="text"
                      name={key}
                      value={input[key as keyof BrandInput]}
                      onChange={handleChange}
                      onFocus={() => setFocusedField(key)}
                      onBlur={() => setFocusedField(null)}
                      placeholder={placeholder}
                      className="w-full px-4 py-3.5 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent transition-all duration-300 hover:bg-slate-800/70"
                    />
                    {focusedField === key && (
                      <div className="absolute inset-0 -z-10 bg-gradient-to-r from-cyan-400/20 to-blue-600/20 rounded-xl blur-lg"></div>
                    )}
                  </div>
                </div>
              ))}

              <button
                onClick={handleSubmit}
                disabled={loading}
                className="w-full mt-8 bg-gradient-to-r from-cyan-400 to-blue-600 hover:from-cyan-300 hover:to-blue-500 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-cyan-400/50 transform hover:scale-[1.02] active:scale-[0.98] flex items-center justify-center gap-2 group"
              >
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    <span>Generando tu kit...</span>
                  </>
                ) : (
                  <>
                    <span className="text-xl">✨</span>
                    <span>Generar UI Kit</span>
                  </>
                )}
              </button>
            </div>

            
            <div className="mt-8 pt-6 border-t border-slate-800/50 text-center">
              <p className="text-slate-500 text-xs">
                Desarrollo by yesgallo • NEURO UX Styler
              </p>
            </div>
          </div>
        </div>

        
        <div className="mt-4 flex justify-center gap-2">
          <div className="w-2 h-2 rounded-full bg-cyan-400/50"></div>
          <div className="w-2 h-2 rounded-full bg-cyan-500/50"></div>
          <div className="w-2 h-2 rounded-full bg-blue-600/50"></div>
        </div>
      </div>
    </div>
  );
}