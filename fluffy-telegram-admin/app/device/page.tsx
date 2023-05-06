"use client";

import { useAuth } from "@pangeacyber/react-auth";
import { usePathname, useSearchParams } from 'next/navigation';
import { redirect } from 'next/navigation';
import { useState, useEffect } from 'react';

export default function Device() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const { authenticated, user } = useAuth();

  if (!authenticated) {
    // redirect to home
    redirect('/')
  }
  else {
    // Load the user details

    // Get the user email
    const userId = user.email;

    // build the url
    const url = `api/func/user/${userId}`;

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
  
    if (isLoading) return <p>Loading...</p>;
    if (!data) return <p>No profile data</p>;

    redirect(`./device/${data.device}`)
  }
}