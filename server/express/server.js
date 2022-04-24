const express = require("express");
const app = express();
const PORT = 3000;

//실행방법
//1. express 디렉토리에서 npm init
//2. nodemon server.js 로 실행 Example app listening at http://localhost:${PORT} 나오면 정상임
//3. 새로운 터미널 창에서 lt --port 3000 으로, 해당 포트를 배포한다. 
//4. your url is : ~~~ 라고 나오는 부분이 서버의 외부 url이므로, 처음 들어가서 시작 버튼 눌러주면 정상 시작 된다.
//5. 메신저봇R에서는 해당 url로 테스트하면 된다.

//"{root_url}/test?id=1&msg=안녕하세요" 로 요청왔을 때, 서버에서 전달할 내용에 대한 처리 
app.get("/test?:id", (req, res) => {
  var msg = req.query.msg;
  var id = req.query.id;
  console.log(req.query);
  res.send(`
    <h1>test//${id}가 보낸 내용 : ${msg}</h1>
    <script>console.log('hello world');</script>
    `);
});

// server 정상 실행시
app.listen(PORT, () => {
  console.log(`Example app listening at http://localhost:${PORT}`);
});

