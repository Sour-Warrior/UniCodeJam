import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from "react"
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import {View} from 'react-native'


const App = () => {


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
}, []);

let artistList = []

data.artists.forEach((artist, index) => {artistList.push(
        <View style={{flexDirection: "row",  justifyContent: 'space-between'}}>
            <div class="col-2 mb-2">
              <div class="card" style={{flex: 1}}>
                <img src={artist.images[0].url} alt="Card image cap"/>
                  <div class="card-body">
                    <h5 class="card-title">{artist.name}</h5>
                  </div>
                </div>
        </div>    
        </View>
)})

return (
    <div className="App">
        <header className="App-header">
            <h1>React and flask</h1>
        </header>
        <div>
            {artistList}
        </div>
    </div>
);
}

export default App;
