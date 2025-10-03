import axios from 'axios';
import { BrandInput, UXKit } from '../types';

const API_BASE_URL = import.meta.env.DEV 
  ? 'http://localhost:8000' 
  : 'https://neuro-ux-styler-backend.onrender.com'; // Cambia según tu despliegue

export const generateUXKit = async (input: BrandInput): Promise<UXKit> => {
  const response = await axios.post(`${API_BASE_URL}/api/v1/generate`, input);
  return response.data;
};