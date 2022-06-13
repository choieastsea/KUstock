importClass(org.jsoup.Jsoup);
const scriptName = "test";

var map = new Map([
  ["/test",true],
  ["/help",true],
  ["/trade",true],
  ["/community",true],
  ["/stock",true],
  ["/chart",true],
  ["/kustock",true],
  ["/tutorial",true],
  ["/record", true],
  ["/easy", true]
]);
function response(room, msg, sender, isGroupChat, replier, imageDB, packageName) {
  var check = msg.trim()[0];
  if(check=="/"){
    var order = msg.split(" ")[0];
    var url = "https://a15d-222-109-202-99.jp.ngrok.io";
    if(map.get(order)){
      var connect = Jsoup.connect(url+"/api"+order+"?room="+room+"&id="+sender+"&msg="+msg)
      var str = JSON.parse(connect.ignoreContentType(true).get().text()).data;
      var rpy_msg = sender+"님의 명령어 \""+msg+"\" 실행결과 입니다.\n\n"
      rpy_msg += str.substring(0,str.length-1);
      replier.reply(rpy_msg);
    }else{
      var connect = Jsoup.connect(url+"/api/processing?room="+room+"&id="+sender+"&msg="+msg)
      var str = JSON.parse(connect.ignoreContentType(true).get().text()).data;
      if(str == "NOTFOUND")
        replier.reply("등록되지않은 명령어입니다.\n /help를 통해 명령어를 확인해주세요.");
      else{
        var rpy_msg = sender+"님의 명령어 \""+msg+"\" 실행결과 입니다.\n\n"
        rpy_msg += str.substring(0,str.length-1);
        replier.reply(rpy_msg);
      }
    }
  }
}



//아래 4개의 메소드는 액티비티 화면을 수정할때 사용됩니다.
function onCreate(savedInstanceState, activity) {
  var textView = new android.widget.TextView(activity);
  textView.setText("Hello, World!");
  textView.setTextColor(android.graphics.Color.DKGRAY);
  activity.setContentView(textView);
  
}

function onStart(activity) {}

function onResume(activity) {}

function onPause(activity) {}

function onStop(activity) {}
