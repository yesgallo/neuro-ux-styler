import { useState } from 'react';
import { BrandInput } from '../types';
import { generateUXKit } from '../services/api';
import { useNavigate } from 'react-router-dom';

export default function BrandForm() {
  const [input, setInput] = useState<BrandInput>({
    name: '',
    mission: '',
    values: '',
    audience: '',
    sector: ''
  });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setInput(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const result = await generateUXKit(input);
      localStorage.setItem('uxKit', JSON.stringify(result));
      navigate('/result');
    } catch (err) {
      alert('Error generando el kit. Intenta de nuevo.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl mx-auto p-6 space-y-4">
      <h1 className="text-3xl font-bold text-gray-800">Neuro UX Styler</h1>
      <p className="text-gray-600">Describe tu marca y genera un UI Kit coherente.</p>

      {(['name', 'mission', 'values', 'audience', 'sector'] as const).map(field => (
        <div key={field}>
          <label className="block text-sm font-medium text-gray-700 capitalize">
            {field === 'audience' ? 'Público objetivo' : field}
          </label>
          <input
            type="text"
            name={field}
            value={input[field]}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            required
          />
        </div>
      ))}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 disabled:opacity-50"
      >
        {loading ? 'Generando...' : 'Generar UI Kit'}
      </button>
    </form>
  );
}