import React from "react";

const ProfileHeader = ({ username }) => {
  return (
    <header className="profile-header">
      <h1 className="profile-title">Welcome {username} </h1>
    </header>
  );
};

export default ProfileHeader;