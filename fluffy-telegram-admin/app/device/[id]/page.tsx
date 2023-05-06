"use client";

import { useAuth } from "@pangeacyber/react-auth";
import { usePathname } from 'next/navigation';
import { useState, useEffect } from 'react';
import { redirect } from 'next/navigation';

export default function Device() {
  const pathname = usePathname();
  const { authenticated } = useAuth();


  // Page needs:
  // A list of images
  // A way to upload an image
  // A way to set a URL for a new image

  if (!authenticated) {
    // redirect to home
    redirect('/')
  }
  else {
    // Load the images

    // Get the device Id
    const deviceId = pathname.split("/").at(-1);

    // build the url
    const url = `../api/func/image/${deviceId}`;
    // return (<p>{url}</p>)

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

    const images_list = data.map((image) => {
      var i = {
        url: `../api/func/image/${deviceId}/?image=${image}`,
        id: image
      }
      return i;
    });

    return (
      <div>
        <div className="container">
          <div className="row">
            <h2>Current images</h2>
          </div>
          <div className="row">
            {images_list.map((image) => (
              <div className="col-3">
                <div className='card h-100 pt-10'>
                  <img src={image.url} className="card-img" />
                </div>
              </div>
            ))}
          </div>
          <div className="row">
            <h2>Upload image</h2>
            <form>
              <div className="form-group">
                <label htmlFor="exampleFormControlInput1">Image URL</label>
                <input type="text" className="form-control" id="imageUrl" placeholder=""/>
                <button type="button" className="btn btn-primary" onClick={
                  (e) => {
                    // get the image url
                    const imageUrlControl = document.getElementById("imageUrl") as HTMLInputElement;
                    const imageUrl = imageUrlControl.value;

                    // build the url
                    const url = `../api/func/image/${deviceId}/?image_url=${imageUrl}`;

                    console.log(url);

                    // post to the URL
                    fetch(url, { method: 'POST' })
                      .then((res) => imageUrlControl.value = "")
                      .then(() => location.reload());
                  }
                }>Submit</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    )

  }
}