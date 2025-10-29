import axios from 'axios'
import { BrandInput, UXKit } from '../types'

const API_BASE_URL = 'http://localhost:8000'

export const generateUXKit = async (input: BrandInput): Promise<UXKit> => {
  const response = await axios.post(`${API_BASE_URL}/api/v1/generate`, input)
  return response.data
}
