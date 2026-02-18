import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Round1 from "./pages/Round1";
import Round2 from "./pages/Round2";
import Round3 from "./pages/Round3";
import Round4 from "./pages/Round4";
import Winner from "./pages/Winner";






function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/round1" element={<Round1 />} />
      <Route path="/round2" element={<Round2 />} />
      <Route path="/round3" element={<Round3 />} />
      <Route path="/round4" element={<Round4 />} />
<Route path="/winner" element={<Winner />} />


    </Routes>
  );
}

export default App;
