import React, { useEffect, useState } from "react";
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer,
} from "recharts";
import { getHistory, getMetrics } from "../api";

export default function Dashboard({ refreshKey }) {
  const [history, setHistory] = useState([]);
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    getHistory().then((res) => setHistory(res.data)).catch(() => {});
    getMetrics().then((res) => setMetrics(res.data)).catch(() => {});
  }, [refreshKey]);

  const trendData = history.map((h, i) => ({
    index: i + 1,
    price: h.predicted_value ?? h.predicted_value_usd,
  }));

  const accuracyData = metrics
    ? Object.entries(metrics.comparison).map(([name, m]) => ({
        model: name,
        R2: m.R2,
      }))
    : [];

  return (
    <div style={{ display: "grid", gap: "20px", marginTop: "24px" }}>
      <div style={styles.card}>
        <h3 style={styles.heading}>Prediction Trend (recent history)</h3>
        {trendData.length === 0 ? (
          <p style={{ color: "#7a8699" }}>No predictions logged yet.</p>
        ) : (
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="index" label={{ value: "Prediction #", position: "insideBottom", dy: 10 }} />
              <YAxis />
              <Tooltip formatter={(v) => `$${v.toLocaleString()}`} />
              <Line type="monotone" dataKey="price" stroke="#1e3a5f" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      <div style={styles.card}>
        <h3 style={styles.heading}>Model Accuracy Comparison (R²)</h3>
        {accuracyData.length === 0 ? (
          <p style={{ color: "#7a8699" }}>Metrics not available.</p>
        ) : (
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={accuracyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="model" />
              <YAxis domain={[0, 1]} />
              <Tooltip />
              <Legend />
              <Bar dataKey="R2" fill="#3a6ea5" />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}

const styles = {
  card: {
    background: "#fff",
    padding: "20px",
    borderRadius: "12px",
    boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
  },
  heading: { marginTop: 0, fontSize: "1.05rem", color: "#1e3a5f" },
};
