"use client";

import { useAuth } from "@pangeacyber/react-auth";
import styles from "./page.module.css";
import { redirect } from 'next/navigation';

export default function Home() {
  const { authenticated } = useAuth();

  if (!authenticated) {
    // redirect to homw
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
