import React from "react";
import ErrorMessage from "./ErrorMessage";

function FormInput({ label, type, name, placeholder, value, onChange, error }) {
  return (
    <div className="mb-3">
      <label className="form-label">{label}</label>
      <input
        type={type}
        name={name}
        className="form-control"
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        required
      />
      {error && <ErrorMessage message={error} />}
    </div>
  );
}

export default FormInput;
