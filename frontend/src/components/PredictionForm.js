import React, { useState } from "react";

const NUMERIC_FIELDS = [
  { name: "longitude", label: "Longitude", default: -122.23, step: 0.01 },
  { name: "latitude", label: "Latitude", default: 37.88, step: 0.01 },
  { name: "housing_median_age", label: "House Median Age (yrs)", default: 41, step: 1 },
  { name: "total_rooms", label: "Total Rooms (block)", default: 880, step: 10 },
  { name: "total_bedrooms", label: "Total Bedrooms (block)", default: 129, step: 5 },
  { name: "population", label: "Population (block)", default: 322, step: 10 },
  { name: "households", label: "Households (block)", default: 126, step: 5 },
  { name: "median_income", label: "Median Income ($10k)", default: 8.3, step: 0.1 },
];

const OCEAN_OPTIONS = ["<1H OCEAN", "INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN"];

export default function PredictionForm({ onPredict, loading }) {
  const [values, setValues] = useState({
    ...Object.fromEntries(NUMERIC_FIELDS.map((f) => [f.name, f.default])),
    ocean_proximity: "NEAR BAY",
  });

  const handleChange = (name, val, isNumber = true) => {
    setValues((prev) => ({ ...prev, [name]: isNumber ? parseFloat(val) : val }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onPredict(values);
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <h2 style={styles.heading}>House / Block Details</h2>
      <div style={styles.grid}>
        {NUMERIC_FIELDS.map((f) => (
          <label key={f.name} style={styles.label}>
            {f.label}
            <input
              type="number"
              step={f.step}
              value={values[f.name]}
              onChange={(e) => handleChange(f.name, e.target.value)}
              style={styles.input}
              required
            />
          </label>
        ))}
        <label style={styles.label}>
          Ocean Proximity
          <select
            value={values.ocean_proximity}
            onChange={(e) => handleChange("ocean_proximity", e.target.value, false)}
            style={styles.input}
          >
            {OCEAN_OPTIONS.map((opt) => (
              <option key={opt} value={opt}>{opt}</option>
            ))}
          </select>
        </label>
      </div>
      <button type="submit" disabled={loading} style={styles.button}>
        {loading ? "Predicting..." : "Predict Price"}
      </button>
    </form>
  );
}

const styles = {
  form: {
    background: "#fff",
    padding: "24px",
    borderRadius: "12px",
    boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
  },
  heading: { marginTop: 0, fontSize: "1.2rem", color: "#1e3a5f" },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
    gap: "14px",
    marginBottom: "18px",
  },
  label: {
    display: "flex",
    flexDirection: "column",
    fontSize: "0.85rem",
    color: "#40506b",
    gap: "6px",
  },
  input: {
    padding: "8px 10px",
    borderRadius: "6px",
    border: "1px solid #c9d3e0",
    fontSize: "0.95rem",
  },
  button: {
    background: "#1e3a5f",
    color: "#fff",
    border: "none",
    padding: "10px 22px",
    borderRadius: "8px",
    fontSize: "1rem",
    cursor: "pointer",
  },
};
