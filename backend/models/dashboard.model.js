const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const dashboardSchema = new Schema({
    symbol: {
        type: String,
        required: false
    },
    userID: {
        type: String,
        required: false
    },
    pattern_type: {
        type: String,
        required: false
    },
    userNotes: {
        type: String,
        required: false
    }
  });

const Dashboard = mongoose.model('Dashboard', dashboardSchema);

module.exports = Dashboard;