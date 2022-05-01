importClass(org.jsoup.Jsoup);
const scriptName = "test";

var map = new Map([
  ["/test",true],
  ["/help",true]
])

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
      replier.reply("테스트!");
      //var connect = Jsoup.connect("https://young-masks-look-58-225-47-121.loca.lt/api/test?room="+room+"&id="+sender+"&msg="+msg).header("content-type", "application/json;charset=UTF-8");
      var connect = Jsoup.connect("https://young-masks-look-58-225-47-121.loca.lt/api"+order+"?room="+room+"&id="+sender+"&msg="+msg).header("content-type", "application/json;charset=UTF-8");
      var str = connect.ignoreContentType(true).get().text();
      replier.reply("data: " + str);
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