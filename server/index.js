const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const app = express();

dotenv.config();
app.use(cors());
app.use(express.json());


const performanceRouter = require('./routes/performance');
app.use('/api/performance', performanceRouter);

const reviewRouter = require('./routes/review');
app.use('/api/review', reviewRouter);


// 예시 라우터
app.get('/', (req, res) => {
  res.send('공연시설 API 서버입니다');
});

// 서버 시작
const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`서버 실행 중: http://localhost:${PORT}`);
});
