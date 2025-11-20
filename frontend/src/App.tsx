import { Routes, Route } from 'react-router-dom';
import Transactions from './pages/Transactions';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Routes>
        <Route path="/" element={<Transactions />} />
        <Route path="/transactions" element={<Transactions />} />
      </Routes>
    </div>
  );
}

export default App;
