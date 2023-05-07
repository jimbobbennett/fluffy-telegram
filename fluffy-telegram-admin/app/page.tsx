"use client";

import { useAuth } from "@pangeacyber/react-auth";
import styles from "./page.module.css";
import { redirect } from 'next/navigation';

export default function Home() {
  // Get the authentication state from Pangea
  const { authenticated } = useAuth();

  if (!authenticated) {
    // If we are not authenticated, show the login page
    return (<div className={styles.card}>
      <h2>
       Please sign in
      </h2>
    </div>)
  }
  else {
    // Redirect to the device page
    redirect('/device');
  }
}
