import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from "react"

function App() {


  const [data, setdata] = useState({
    name: "",
    artists: [],
    tracks: [],
});

// Using useEffect for single rendering
useEffect(() => {
    // Using fetch to fetch the api from 
    // flask server it will be redirected to proxy
    fetch("/data").then((res) =>
        res.json().then((data) => {
            // Setting a data from api
            setdata({
                name: data.Name,
                artists: data.artists,
                tracks: data.tracks,
            });
        })
    );
    console.log(data.artists)
}, []);

let artistList = []

data.artists.forEach((artist, index) => {artistList.push(<li key={index}>{artist.name}: {artist.genres[0]} + {artist.genres[1]}</li>)})

return (
    <div className="App">
        <header className="App-header">
            <h1>React and flask</h1>
            {/* Calling a data from setdata for showing */}
            <ul>{artistList}</ul>
        </header>
    </div>
);
}

export default App;
