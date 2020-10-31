const express = require("express");
const bodyParser = require("body-parser");
const app = express();
const mysql = require("mysql");
const cors = require('cors');

const db = mysql.createPool({
    host: "localhost",
    user: "root",
    password: "password",
    database: "cs411-39"
});

app.use(cors());
app.use(express.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get("/api/get", (req, res) => {
    const sqlSelect = "SELECT * FROM Watchlist";
    db.query(sqlSelect, (err, result) => {
        res.send(result);
    });
});

app.post("/api/insert", (req, res) => {
    const stockSymbol = req.body.stockSymbol;
    const sentimentRating = req.body.sentimentRating;
    const patternType = req.body.patternType;

    const sqlInsert = 
        "INSERT INTO Watchlist (stockSymbol, sentimentRating, patternType) VALUES (?,?,?)";
    db.query(sqlInsert, [stockSymbol, sentimentRating, patternType], (err, result) => {
        console.log(result);
    });
});

app.delete("/api/delete/:member", (req, res)=> {
    const name = req.params.member;
    const sqlDelete = "DELETE FROM Watchlist WHERE stockSymbol = ?";    
    db.query(sqlDelete, name, (err, result) => {
        if (err) console.log(err);
    });
});

app.put("/api/update", (req, res)=> {
    const name = req.body.stockSymbol;
    const rating = req.body.sentimentRating;
    const sqlUpdate = "UPDATE Watchlist SET sentimentRating = ? WHERE stockSymbol = ?";    
    db.query(sqlUpdate, [rating, name], (err, result) => {
        if (err) console.log(err);
    });
});


app.listen(3001, () => {
    console.log("running on port 3001");
});