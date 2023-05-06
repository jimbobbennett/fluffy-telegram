import { useAuth } from "@pangeacyber/react-auth";

import Link from "next/link";
import React from "react";

const AppBar = () => {
  const {
    authenticated,
    loading,
    error,
    user,
    client,
    login,
    logout,
    getToken,
  } = useAuth();

  return (
    <header>
      <div className="nav">
        <Link href={"/"}>Home</Link>
      </div>
      <div className="actions">
        {authenticated && (
          <button className="header-action" onClick={() => logout()}>
            Sign Out
          </button>
        )}
        {!authenticated && (
          <button className="header-action" onClick={() => login()}>
            Sign In
          </button>
        )}
      </div>
    </header>
  );
};

export default AppBar;
