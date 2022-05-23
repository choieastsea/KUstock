importClass(org.jsoup.Jsoup);
const scriptName = "test";

var map = new Map([
  ["/test",true],
  ["/help",true],
  ["/trade",true],
  ["/community",true],
  ["/stock",true],
  ["/chart",true],
  ["/kustock",true]
]);

/**
 * (string) room
 * (string) sender
 * (boolean) isGroupChat
 * (void) replier.reply(message)
 * (boolean) replier.reply(room, message, hideErrorToast = false) // 전송 성공시 true, 실패시 false 반환
 * (string) imageDB.getProfileBase64()
 * (string) packageName
 */
function response(
  room,
  msg,
  sender,
  isGroupChat,
  replier,
  imageDB,
  packageName
) {
  var check = msg.trim()[0];
  if(check=="/"){
    var order = msg.split(" ")[0];
    if(map.get(order)){
      var url = "https://4063-222-109-202-99.jp.ngrok.io";
      var connect = Jsoup.connect(url+"/api"+order+"?room="+room+"&id="+sender+"&msg="+msg)
      var str = JSON.parse(connect.ignoreContentType(true).get().text());
      var rpy_msg = sender+"님의 명령어 "+msg+" 실행결과 입니다.\n"
      rpy_msg += str.data.substring(0,str.data.length-2)
      replier.reply(rpy_msg);
    }else{
      replier.reply("등록되지않은 명령어입니다.\n /help를 통해 명령어를 확인해주세요.");
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
