const express = require('express');
const router = express.Router();
const db = require('../db');



// 리뷰 등록
// POST /api/review
router.post('/', async (req, res) => {
    const { facility_id, user, rating, content } = req.body;

    if (!facility_id || !user || !rating) {
      return res.status(400).json({ error: '필수 항목 누락' });
    }
  
    try {
      const [result] = await db.query(
        `INSERT INTO review (facility_id, user, rating, content)
         VALUES (?, ?, ?, ?)`,
        [facility_id, user, rating, content]
      );
  
      res.status(201).json({ review_id: result.insertId });
    } catch (err) {
      console.error(err);
      res.status(500).json({ error: '후기 등록 실패', details: err.message });
    }
  });
  
  module.exports = router;
