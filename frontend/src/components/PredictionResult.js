import React from "react";

export default function PredictionResult({ result, error }) {
  if (error) {
    return (
      <div style={{ ...styles.card, borderColor: "#c0392b" }}>
        <p style={{ color: "#c0392b", margin: 0 }}>Error: {error}</p>
      </div>
    );
  }

  if (!result) {
    return (
      <div style={styles.card}>
        <p style={{ margin: 0, color: "#7a8699" }}>
          Fill in the form and click "Predict Price" to see a result.
        </p>
      </div>
    );
  }

  return (
    <div style={styles.card}>
      <p style={styles.subtle}>Predicted median house value</p>
      <p style={styles.value}>
        ${result.predicted_value_usd.toLocaleString()}
      </p>
      <p style={styles.subtle}>Model used: {result.model_used}</p>
    </div>
  );
}

const styles = {
  card: {
    background: "#fff",
    padding: "24px",
    borderRadius: "12px",
    boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
    border: "1px solid transparent",
    textAlign: "center",
  },
  value: { fontSize: "2.2rem", fontWeight: 700, color: "#1e3a5f", margin: "8px 0" },
  subtle: { color: "#7a8699", margin: "4px 0", fontSize: "0.9rem" },
};
