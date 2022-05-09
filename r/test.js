importClass(org.jsoup.Jsoup);
const scriptName = "test";

var map = new Map([
  ["/test",true],
  ["/help",true],
  ["/trade",true],
  ["/community",true]
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
      var url = "https://tricky-berries-tie-121-124-42-134.loca.lt";
      var connect = Jsoup.connect(url+"/api"+order+"?room="+room+"&id="+sender+"&msg="+msg)
      var str = JSON.parse(connect.ignoreContentType(true).get().text());
      //replier.reply(str.data);
      replier.reply(str);
    }else{
      replier.reply("등록되지않은 명령어입니다.");
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