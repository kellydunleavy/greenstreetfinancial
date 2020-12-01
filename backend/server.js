const express = require("express");
const bodyParser = require("body-parser");
const app = express();
const app2 = express();
const mysql = require("mysql");
const cors = require('cors');
const mongoose = require("mongoose");

const db = mysql.createPool({
    host: "localhost",
    user: "root",
    password: "password",
    database: "cs411-39"
});

app.use(cors());
app2.use(cors());
app.use(express.json());
app2.use(express.json());
app.use(bodyParser.urlencoded({ extended: true }));

const uri = "mongodb+srv://<username>:<password>@cluster0.baluh.mongodb.net/cs411_finalproject?retryWrites=true&w=majority";
mongoose.connect(uri, { useNewUrlParser: true, useCreateIndex: true }
);
const connection = mongoose.connection;
connection.once('open', () => {
  console.log("MongoDB database connection established successfully");
})


// WATCHLIST

// selects all of the members of watchlist
app.get("/watchlist/api/get", (req, res) => {
    const sqlSelect = "SELECT * FROM Watchlist";
    db.query(sqlSelect, (err, result) => {
        res.send(result);
    });
});

// inserts an element into the watchlist
app.post("/watchlist/api/insert", (req, res) => {
    const stockSymbol = req.body.stockSymbol;
    const sentimentRating = req.body.sentimentRating;
    const patternType = req.body.patternType;

    const sqlInsert = 
        "INSERT INTO Watchlist (stockSymbol, sentimentRating, patternType) VALUES (?,?,?)";
    db.query(sqlInsert, [stockSymbol, sentimentRating, patternType], (err, result) => {
        console.log(result);
    });
});

// deletes a specific member of the watchlist
app.delete("/watchlist/api/delete/:member", (req, res)=> {
    const name = req.params.member;
    const sqlDelete = "DELETE FROM Watchlist WHERE stockSymbol = ?";    
    db.query(sqlDelete, name, (err, result) => {
        if (err) console.log(err);
    });
});

// updates the member of watchlist
app.put("/watchlist/api/update", (req, res)=> {
    const name = req.body.stockSymbol;
    const rating = req.body.sentimentRating;
    const sqlUpdate = "UPDATE Watchlist SET sentimentRating = ? WHERE stockSymbol = ?";    
    db.query(sqlUpdate, [rating, name], (err, result) => {
        if (err) console.log(err);
    });
});

// DIPBUYCHARTPATTERN

// selects all of the members of dipbuycharpattern
app.get("/dipbuychartpattern/api/get", (req, res) => {
    const sqlSelect = "SELECT * FROM DipBuyChartPattern";
    db.query(sqlSelect, (err, result) => {
        res.send(result);
    });
});

// inserts an element into dip buy chart pattern
app.post("/dipbuychartpattern/api/insert", (req, res) => {
    const stockSymbol = req.body.stockSymbol;
    const bidAskRatio = req.body.bidAskRatio;
    const volumeChange = req.body.volumeChange;
    const priceDrop = req.body.priceDrop;

    const sqlInsert = 
        "INSERT INTO DipBuyChartPattern (stockSymbol, bidAskRatio, volumeChange, priceDrop) VALUES (?,?,?,?)";
    db.query(sqlInsert, [stockSymbol, bidAskRatio, volumeChange, priceDrop], (err, result) => {
        console.log(result);
    });
});

// deletes a member of dip buy chart pattern
app.delete("/dipbuychartpattern/api/delete/:member", (req, res)=> {
    const name = req.params.member;
    const sqlDelete = "DELETE FROM DipBuyChartPattern WHERE stockSymbol = ?";    
    db.query(sqlDelete, name, (err, result) => {
        if (err) console.log(err);
    });
});

// updates a member of dip buy chart pattern
app.put("/dipbuychartpattern/api/update", (req, res)=> {
    const name = req.body.stockSymbol;
    const bidAskRatio = req.body.bidAskRatio;
    const volumeChange = req.body.volumeChange;
    const priceDrop = req.body.priceDrop;

    const sqlUpdate = "UPDATE DipBuyChartPattern SET (bidAskRatio, volumeChange, priceDrop) = (?,?,?) WHERE stockSymbol = ?";    
    db.query(sqlUpdate, [bidAskRatio, volumeChange, priceDrop, name], (err, result) => {
        if (err) console.log(err);
    });
});

// STOCK

// selects all of the members of stock
app.get("/stock/api/get", (req, res) => {
    const sqlSelect = "SELECT * FROM Stock";
    db.query(sqlSelect, (err, result) => {
        res.send(result);
    });
});

// inserts an element into stock
app.post("/stock/api/insert", (req, res) => {
    const stockSymbol = req.body.stockSymbol;
    const currentPrice = req.body.currentPrice;
    const volume = req.body.volume;
    const openingPrice = req.body.openingPrice;
    const previousClose = req.body.previousClose;

    const sqlInsert = 
        "INSERT INTO Stock (stockSymbol, currentPrice, volume, openingPrice, previousClose) VALUES (?,?,?,?,?)";
    db.query(sqlInsert, [stockSymbol, currentPrice, volume, openingPrice, previousClose], (err, result) => {
        console.log(result);
    });
});

// deletes a member of stock
app.delete("/stock/api/delete/:member", (req, res)=> {
    const name = req.params.member;
    const sqlDelete = "DELETE FROM Stock WHERE stockSymbol = ?";    
    db.query(sqlDelete, name, (err, result) => {
        if (err) console.log(err);
    });
});

// updates a member of stock
app.put("/stock/api/update", (req, res)=> {
    const stockSymbol = req.body.stockSymbol;
    const currentPrice = req.body.currentPrice;
    const volume = req.body.volume;
    const openingPrice = req.body.openingPrice;
    const previousClose = req.body.previousClose;

    const sqlUpdate = "UPDATE Stock SET (currentPrice, volume, openingPrice, previousClose) = (?,?,?) WHERE stockSymbol = ?";    
    db.query(sqlUpdate, [currentPrice, volume, openingPrice, previousClose, stockSymbol], (err, result) => {
        if (err) console.log(err);
    });
});

// USER

// selects all of the members of user
app.get("/user/api/get", (req, res) => {
    const sqlSelect = "SELECT * FROM User";
    db.query(sqlSelect, (err, result) => {
        res.send(result);
    });
});

// inserts an element into user
app.post("/user/api/insert", (req, res) => {
    const userId = req.body.userId;
    const stocksBought = req.body.stocksBought;
    const stocksSold = req.body.stocksSold;
    const portfolioValue = req.body.portfolioValue;

    const sqlInsert = 
        "INSERT INTO User (userId, stocksBought, stocksSold, portfolioValue) VALUES (?,?,?,?)";
    db.query(sqlInsert, [userId, stocksBought, stocksSold, portfolioValue], (err, result) => {
        console.log(result);
    });
});

// deletes a member of user
app.delete("/user/api/delete/:member", (req, res)=> {
    const name = req.params.member;
    const sqlDelete = "DELETE FROM User WHERE userId = ?";    
    db.query(sqlDelete, name, (err, result) => {
        if (err) console.log(err);
    });
});

// updates a member of user
app.put("/user/api/update", (req, res)=> {
    const userId = req.body.userId;
    const stocksBought = req.body.stocksBought;
    const stocksSold = req.body.stocksSold;
    const portfolioValue = req.body.portfolioValue;

    const sqlUpdate = "UPDATE User SET (stocksBought, stocksSold, portfolioValue) = (?,?,?) WHERE userId = ?";    
    db.query(sqlUpdate, [stocksBought, stocksSold, portfolioValue, userId], (err, result) => {
        if (err) console.log(err);
    });
});

app.listen(3001, () => {
    console.log("running on port 3001");
});
const dashboardsRouter = require('./routes/dashboards');
app2.use('/dashboards', dashboardsRouter);

app2.listen(3004, () => {
    console.log("running on port 3004");
});