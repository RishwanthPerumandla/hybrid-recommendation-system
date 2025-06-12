// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import UserList from "./pages/UserList";
import UserDetail from "./pages/UserDetail"; // (to be created next)

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UserList />} />
        <Route path="/user/:id" element={<UserDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
