import { useAuth } from "@pangeacyber/react-auth";
import React from "react";

const AppBar = () => {
  // Get the authentication state, and login and logout functions from Pangea
  const {
    authenticated,
    login,
    logout
  } = useAuth();

  return (
    <header>
      <div className="nav">
        <h1>Fluffy Telegram</h1>
      </div>
      <div className="actions">
        {authenticated && (
          <button type="button" className="btn btn-primary" onClick={() => logout()}>
            Sign Out
          </button>
        )}
        {!authenticated && (
          <button type="button" className="btn btn-primary" onClick={() => login()}>
            Sign In
          </button>
        )}
      </div>
    </header>
  );
};

export default AppBar;
