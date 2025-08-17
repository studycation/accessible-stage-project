const express = require('express');
const router = express.Router();
const db = require('../db');

// 시설 이름 매핑
const facilityLabels = {
  has_restaurant: '레스토랑',
  has_cafe: '카페',
  has_convenience_store: '편의점',
  has_kids_room: '놀이방',
  has_nursing_room: '수유실',
  has_disabled_parking: '장애인 주차장',
  has_disabled_restroom: '장애인 화장실',
  has_ramp: '경사로',
  has_elevator: '전용 엘리베이터',
  has_private_parking: '자체 주차장',
  has_public_parking: '공영 주차장'
};

// 공연시설 목록 조회
// GET /api/performance?cafe=1&nursing_room=1&disabled_restroom=1
router.get('/', async (req, res) => {
  try {
    const conditions = [];
    const params = [];

    // 편의/장애인/주차 시설 조건별 필터 처리
    if (req.query.cafe === '1') {
      conditions.push('c.has_cafe = 1');
    }
    if (req.query.nursing_room === '1') {
      conditions.push('c.has_nursing_room = 1');
    }
    if (req.query.disabled_restroom === '1') {
      conditions.push('a.has_disabled_restroom = 1');
    }

    const whereClause = conditions.length ? 'WHERE ' + conditions.join(' AND ') : '';

    const [rows] = await db.query(`
      SELECT p.*, c.has_cafe, c.has_nursing_room, a.has_disabled_restroom
      FROM performance p
      LEFT JOIN convenience c ON p.facility_id = c.facility_id
      LEFT JOIN accessibility a ON p.facility_id = a.facility_id
      ${whereClause}
    `);

    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: '공연시설 목록 조회 실패' });
  }
});

// 공연시설 상세 조회
// GET /api/performance/:id
router.get('/:id', async (req, res) => {
  const id = req.params.id;

  try {
    // 공연장 + 시설 정보 가져오기
    const [[facility]] = await db.query(
      `SELECT p.facility_id, p.facility_name, p.address,
              c.has_restaurant, c.has_cafe, c.has_convenience_store, c.has_kids_room, c.has_nursing_room,
              a.has_disabled_parking, a.has_disabled_restroom, a.has_ramp, a.has_elevator,
              k.has_private_parking, k.has_public_parking
       FROM performance p
       LEFT JOIN convenience c ON p.facility_id = c.facility_id
       LEFT JOIN accessibility a ON p.facility_id = a.facility_id
       LEFT JOIN parking k ON p.facility_id = k.facility_id
       WHERE p.facility_id = ?`,
      [id]
    );

    if (!facility) {
      return res.status(404).json({ error: '공연시설을 찾을 수 없습니다.' });
    }

    // 시설 정보 가공
    const available = [];
    const unavailable = [];

    for (const key in facilityLabels) {
      if (facility[key] === 1) {
        available.push(facilityLabels[key]);
      } else if (facility[key] === 0) {
        unavailable.push(facilityLabels[key]);
      }
    }

    // 공연 정보
    const [shows] = await db.query(
      `SELECT performance_id, title, datetime
       FROM perform_show
       WHERE facility_id = ?
       ORDER BY datetime ASC`,
      [id]
    );

    // 리뷰 정보 (review 테이블이 있다고 가정)
    const [reviews] = await db.query(
      `SELECT review_id, user, rating, content, created_at
       FROM review
       WHERE facility_id = ?
       ORDER BY created_at DESC`,
      [id]
    );

    res.json({
      facility_id: facility.facility_id,
      facility_name: facility.facility_name,
      address: facility.address,
      available,
      unavailable,
      shows,
      reviews
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: '공연장 상세 조회 실패', details: err.message });
  }
});



module.exports = router;
