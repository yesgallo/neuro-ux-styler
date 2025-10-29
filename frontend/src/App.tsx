import { BrowserRouter, Routes, Route } from 'react-router-dom'
import BrandForm from './components/BrandForm'
import ResultPage from './components/ResultPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<BrandForm />} />
        <Route path="/result" element={<ResultPage />} />
      </Routes>
    </BrowserRouter>
  )
}
