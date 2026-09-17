import React, { useState } from "react";
import PredictionForm from "./components/PredictionForm";
import PredictionResult from "./components/PredictionResult";
import Dashboard from "./components/Dashboard";
import { predictHousePrice } from "./api";

export default function App() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);

  const handlePredict = async (features) => {
    setLoading(true);
    setError(null);
    try {
      const res = await predictHousePrice(features);
      setResult(res.data);
      setRefreshKey((k) => k + 1); // refresh dashboard after new prediction
    } catch (err) {
      setError(err?.response?.data?.detail || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <h1 style={styles.title}>🏠 PredictIQ</h1>
        <p style={styles.subtitle}>Smart ML house price prediction</p>
      </header>

      <main style={styles.main}>
        <div style={styles.topRow}>
          <PredictionForm onPredict={handlePredict} loading={loading} />
          <PredictionResult result={result} error={error} />
        </div>

        <Dashboard refreshKey={refreshKey} />
      </main>
    </div>
  );
}

const styles = {
  page: { minHeight: "100vh" },
  header: {
    background: "#1e3a5f",
    color: "#fff",
    padding: "28px 32px",
  },
  title: { margin: 0, fontSize: "1.8rem" },
  subtitle: { margin: "4px 0 0", opacity: 0.85 },
  main: { maxWidth: "1000px", margin: "0 auto", padding: "28px 20px" },
  topRow: {
    display: "grid",
    gridTemplateColumns: "2fr 1fr",
    gap: "20px",
    alignItems: "start",
  },
};
