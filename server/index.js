const express = require('express');
const cors = require('cors');
const app = express();
const PORT = 4000;

app.use(cors());
app.use(express.json());

app.get('/api/hello', (req, res) => {
  res.json({ message: '안녕하세요 from Node.js' });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
