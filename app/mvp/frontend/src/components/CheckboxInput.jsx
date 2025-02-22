import React from "react";

function CheckboxInput({ name, checked, onChange, label }) {
  return (
    <div className="mb-3">
      <input type="checkbox" name={name} checked={checked} onChange={onChange} />
      <label className="form-label"> {label}</label>
    </div>
  );
}

export default CheckboxInput