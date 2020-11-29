const router = require('express').Router();
let Dashboard = require('../models/dashboard.model');

router.route('/').get((req, res) => {
  Dashboard.find()
    .then(dashboard => res.json(dashboard))
    .catch(err => res.status(400).json('Error: ' + err));
});

router.route('/add').post((req, res) => {
  const userID = req.body.userID;

  const newDashboard = new Dashboard({userID});

  newDashboard.save()
    .then(() => res.json('Dashboard added!'))
    .catch(err => res.status(400).json('Error: ' + err));
});


module.exports = router;