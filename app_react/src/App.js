import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';
import { Dropzone } from '@mantine/dropzone';
import { Paper, Text } from '@mantine/core';


function ImageGallery() {
  const [imageUrls, setImageUrls] = useState([]);

  useEffect(() => {
    async function fetchImageUrls() {
      const apiUrl = 'http://127.0.0.1:8000/images';

      try {
        const response = await fetch(apiUrl);

        if (!response.ok) {
          throw new Error('La requête a échoué avec le statut : ' + response.status);
        }

        const data = await response.json();
        console.log(data)
        let urls = []
        for (const url in data) {
          urls.push(data[url])
        }
        console.log(urls)
        setImageUrls(urls);
      } catch (error) {
        console.error('Erreur lors de la récupération des URLs d\'images :', error);
      }
    }

    fetchImageUrls();
  }, []);

  
  return (
    <div>
      <h1>Image Gallery (from s3) </h1>
      <div class="images">
        {imageUrls.map((url, index) => (
          <img key={index} src={url} alt={`ok ${index}`} style={{ maxWidth: '200px', margin: '10px'}} />
        ))}
      </div>
    </div>
  );
}

function UploadFile() {
  const [uploadedFile, setUploadedFile] = useState(null); 



  const handleUpload = (files) => {
    setUploadedFile(files[0])
    if (uploadedFile) {
      const apiUrl = "http://127.0.0.1:8000/images/"
      const formData = new FormData();
      formData.append('file', uploadedFile)
      fetch(apiUrl, {
        method: "POST", 
        body: formData
      })
      .then(response => response.json()) 
      .then(data => {
        console.log('Response of the server : ', data); 
      })
      .catch(error => {
        console.error('Erreur lors de la requête POST :', error);
      });
  }};

  return (
    <div>
      <Dropzone onDrop={handleUpload}>
      {({ dragging }) => (
          <Paper padding="lg" shadow={dragging ? 'md' : 'sm'} style={{ textAlign: 'center' }}>
            {dragging ? 'Relâchez le fichier' : 'Faites glisser un fichier ici'}
          </Paper>
          
        )}
        <Text> Drop or click for adding an image </Text>
      </Dropzone>
      
    </div>
  )
};



// Méthode pour récupérer les différents tag disponible sur s3, et les afficher comme une liste à puce.

  


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        
          <div>
          Learn React
          </div>
          <div>
           
          <UploadFile />
          <ImageGallery />
         
         
          </div>
          
        
      </header>
    </div>
  );
}

export default App;
