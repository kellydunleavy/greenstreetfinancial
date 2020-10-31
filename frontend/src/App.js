import React, { useState, useEffect, isValidElement } from 'react';
import './App.css';
import Axios from "axios";

function App() {
  const [stockSymbol, setStockSymbol] = useState("");
  const [sentimentRating, setSentimentRating] = useState("");
  const [patternType, setPatternType] = useState("");
  const [watchListMembers, setWatchListMembers] = useState([]);

  const [newSentimentRating, setNewSentimentRating] = useState("");

  useEffect(()=> {
    Axios.get("http://localhost:3001/api/get").then((response)=> {
      setWatchListMembers(response.data);
    });
  }, []);

  const submitWatchlist = () => {
    Axios.post("http://localhost:3001/api/insert", {
      stockSymbol: stockSymbol, 
      sentimentRating: sentimentRating, 
      patternType: patternType
    });
    setWatchListMembers([
      ...watchListMembers, { stockSymbol: stockSymbol, sentimentRating: sentimentRating, patternType: patternType},
    ])
  };

  const deleteWatchlist = (member) => {
    Axios.delete(`http://localhost:3001/api/delete/${member}`);
  }

  const updateWatchlist = (member) => {
    Axios.put("http://localhost:3001/api/update", {
      stockSymbol: member, 
      sentimentRating: newSentimentRating,
      patternType: patternType
    });
    setNewSentimentRating("")
  }

  return (
    <div className="App">
      <h1>Green Street Financial</h1>
      <div className="form">
        <label>Stock symbol:</label>
        <input 
          type="text" 
          name="stockSymbol"
          onChange = {(e) => {
            setStockSymbol(e.target.value);
          }} 
          />
        <label>Sentiment rating:</label>
        <input 
          type="text" 
          name="sentimentRating"
          onChange = {(e) => {
            setSentimentRating(e.target.value);
          }} 
          />
        <label>Pattern type:</label>
        <input 
          type="text" 
          name="patternType"
          onChange = {(e) => {
            setPatternType(e.target.value);
          }} 
          />
        <button onClick={submitWatchlist}>Submit</button>

        {watchListMembers.map((val)=> {
          return (
            <div className="card">
              <h1>{val.stockSymbol}</h1>
              <p>{val.sentimentRating}</p>
              <p>{val.patternType}</p>
              <button onClick={() => {deleteWatchlist(val.stockSymbol)}}>Delete</button>
              <input type="text" id="updateInput" onChange={(e)=> {
                setNewSentimentRating(e.target.value)
              }}/>
              <button onClick={()=> {updateWatchlist(val.stockSymbol)}}>Update</button>
            </div>
            )})}
      </div>
    </div>
  );
}

export default App;
