import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import { Layout } from "./components/layout/Layout"
import { Landing } from "./pages/Landing"
import { Dashboard } from "./pages/Dashboard"
import { UploadPage } from "./pages/Upload"

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/welcome" element={<Landing />} />
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="upload" element={<UploadPage />} />
          <Route path="sessions" element={<div className="p-8">Sessions Page (Coming Soon)</div>} />
          <Route path="findings" element={<div className="p-8">Findings Page (Coming Soon)</div>} />
          <Route path="certificates" element={<div className="p-8">Certificates Page (Coming Soon)</div>} />
          <Route path="tls" element={<div className="p-8">TLS Intelligence (Coming Soon)</div>} />
          <Route path="ai" element={<div className="p-8">AI Intelligence (Coming Soon)</div>} />
          <Route path="trends" element={<div className="p-8">Posture Trends (Coming Soon)</div>} />
          <Route path="reports" element={<div className="p-8">Reports (Coming Soon)</div>} />
          <Route path="settings" element={<div className="p-8">Settings (Coming Soon)</div>} />
          <Route path="help" element={<div className="p-8">Help (Coming Soon)</div>} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
