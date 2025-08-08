const express = require('express');
const router = express.Router();
const db = require('../db');

// 공연시설 목록 조회
router.get('/', async (req, res) => {
  try {
    const [rows] = await db.query('SELECT * FROM performance');
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: 'DB 조회 실패', details: err });
  }
});


module.exports = router;
