import { BrowserRouter, Routes, Route } from 'react-router-dom';
import BrandForm from './components/BrandForm';
import ResultPage from './components/ResultPage';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-white">
        <Routes>
          <Route path="/" element={<BrandForm />} />
          <Route path="/result" element={<ResultPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;