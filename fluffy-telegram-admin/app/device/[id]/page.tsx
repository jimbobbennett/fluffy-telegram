"use client";

import { useAuth } from "@pangeacyber/react-auth";
import { usePathname } from 'next/navigation';
import { useState, useEffect } from 'react';
import { redirect } from 'next/navigation';

export default function Device() {
  const pathname = usePathname();
  const { authenticated } = useAuth();

  if (!authenticated) {
    // If we are not authenticated, redirect to home
    redirect('/')
  }
  else {
    // Load the images

    // Get the device Id
    const deviceId = pathname.split("/").at(-1);

    // build the url
    const url = `../api/func/image/${deviceId}`;

    // Load the images for the device
    var [data, setData] = useState(null);
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

    // console.log(data);

    // if (!Array.isArray(data))
    // {
    //   data = [data];
    // }

    // Build the list of images
    const images_list = data.map((image: string) => {
      var i = {
        url: `../api/func/image/${deviceId}/?image=${image}`,
        id: image
      }
      return i;
    });

    // Render the page with images laid out in a grid, as well as a URL upload button
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
                <br />
                <input type="text" className="form-control" id="imageUrl" placeholder="" />
                <br />
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
                      .then((res) => {
                        if (res.ok) {
                          // if the URL is valid, clear the input
                          imageUrlControl.value = ""
                        }
                        else {
                          if (res.status == 403) {
                            // if the URL is malicious, display an error
                            alert("Error uploading image - URL is malicious")
                          }
                          else {
                            // if the URL is invalid, display an error
                            alert("Error uploading image")
                          }
                        }
                      })
                      .then(() => {
                        // reload the page to show the new image
                        location.reload()
                      });
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