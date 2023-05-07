"use client";

import { useAuth } from "@pangeacyber/react-auth";
import { redirect } from 'next/navigation';
import { useState, useEffect } from 'react';

export default function Device() {
  const { authenticated, user } = useAuth();

  if (!authenticated) {
    // If we are not authenticated, redirect back to home
    redirect('/')
  }
  else {
    // Load the user details

    // Get the user email
    const userId = user.email;

    // build the url
    const url = `api/func/user/${userId}`;

    // Load the device for the user
    const [data, setData] = useState(null);
    const [isLoading, setLoading] = useState(false);

    useEffect(() => {
      setLoading(true);
      fetch(url)
        .then((res) => res.json())
        .then((data) => {
          setData(data);
          setLoading(false);
        });
    }, []);

    // If we are loading, display a loading spinner
    if (isLoading) return (
      <div className="d-flex justify-content-center align-content-center">
        <div>
          <div className="spinner-border text-primary" role="status">
          </div>
        </div>
      </div>
    );

    // If we have no data, display a message
    if (!data) return <p>No profile data</p>;

    // Redirect to the device page for the user
    redirect(`./device/${data.device}`)
  }
}