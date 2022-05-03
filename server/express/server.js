const express = require("express");
const app = express();
const request = require("request-promise-native");  //for await request func
const PORT = 3000;
const dotenv =require("dotenv");
dotenv.config({ path: __dirname + "/./.env" });
const API_KEY =  process.env.MOVIE_API_KEY;
console.log(`${API_KEY}`);
//실행방법
//1. express 디렉토리에서 npm init
//2. nodemon server.js 로 실행 Example app listening at http://localhost:${PORT} 나오면 정상임
//3. 새로운 터미널 창에서 lt --port 3000 으로, 해당 포트를 배포한다.
//4. your url is : ~~~ 라고 나오는 부분이 서버의 외부 url이므로, 처음 들어가서 시작 버튼 눌러주면 정상 시작 된다.
//5. 메신저봇R에서는 해당 url로 테스트하면 된다.
app.get("/", (req, res) => {
  res.send(`<h1>Hello world</h1>`);
});
//"{root_url}/test?id=1&msg=안녕하세요" 로 요청왔을 때, 서버에서 전달할 내용에 대한 처리
app.get("/test?:id", (req, res) => {
  var msg = req.query.msg;
  var id = req.query.id;
  console.log(req.query);
  res.send(`
    <h1>${id}가 보낸 내용 : ${msg}</h1>
    <script>console.log('hello world');</script>
    `);
});

// server 정상 실행시
app.listen(PORT, () => {
  console.log(`Example app listening at http://localhost:${PORT}`);
});

app.get("/movie", async (req, res) => { // rest 기반 api 받아오기!
  console.log(`request on movie\t${API_KEY}`);
  const options = {
    uri: `https://api.themoviedb.org/3/movie/popular`,
    qs: {
      api_key: API_KEY,
    },
  };
  let returnHTML = "";
  await request(options, function (err, response, body) {
    //callback
    // console.log(response);
    const { results } = JSON.parse(body);
    // console.log(results);
    results.map((e) => {
      console.log(e.title);
      returnHTML += `${e.title}</br>`;
    });
  });
  console.log(returnHTML);
  res.send(`<h1>${returnHTML}</h1>`);
});

const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  database: 'test'
});