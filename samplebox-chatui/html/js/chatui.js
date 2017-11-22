
/**
 * API KEY
 */

const TRANSLATION_API_KEY = "YOUR_TRANSLATION_API_KEY";
const NATURAL_LANGUAGE_API_KEY = "YOUR_NATURAL_LANGUAGE_API_KEY";

/**
 * 初期化
 */

var session = new QiSession();

$(function () {
    startSubscribe(); // サブスクライバの登録
    //blowUserSelect(['はい','いいえ']);
    //blowPepperImg('https://s.yimg.jp/images/top/sp2/cmn/logo-170307.png');
});

/**
 * イベントサブスクライバ
 */
function startSubscribe() {
    session.service("ALMemory").then(function (ALMemory) {
        ALMemory.subscriber("ssa/blow-pepper").then(function (subscriber) {
            subscriber.signal.connect(blowPepper);
        });
        ALMemory.subscriber("ssa/blow-user").then(function (subscriber) {
            subscriber.signal.connect(blowUser);
        });
        ALMemory.subscriber("ssa/blow-debug").then(function (subscriber) {
            subscriber.signal.connect(blowDebugMsg);
        });
        ALMemory.subscriber("ssa/blow-imgshow").then(function (subscriber) {
            subscriber.signal.connect(blowPepperImg);
        });
        ALMemory.subscriber("ssa/blow-clear").then(function (subscriber) {
            subscriber.signal.connect(resetChatTalk);
        });
        ALMemory.subscriber("ssa/faceid").then(function (subscriber) {
            subscriber.signal.connect(changeFaceID);
        });
        ALMemory.subscriber("ssa/blow-select").then(function (subscriber) {
            subscriber.signal.connect(blowUserSelect);
        });
        ALMemory.subscriber("ssa/show-dialog").then(function (subscriber) {
            subscriber.signal.connect(showDialog);
        });
        ALMemory.subscriber("ssa/close-dialog").then(function (subscriber) {
            subscriber.signal.connect(closeDialog);
        });
    });
}

/**
 * 説明ダイアログの表示
 */
function showDialog(msg)
{
    var leftPosition = (($(window).width() - $("#usage-dialog").outerWidth(true)) / 2);
    $("#usage-dialog").css({"left": leftPosition + "px"});
    $("#usage-dialog").show();
    $(".dialog-close").on("click", function(){
        closeDialog();
    });
}

/**
 * 説明ダイアログの非表示
 */
function closeDialog(msg){ $("#usage-dialog").hide(); }

/**
 * Face IDを変更
 * @param {string} id
 */

// face ID
var faceTempID = "";

function changeFaceID(id) {
    faceTempID = id;
}

//チャットボックスクラスの要素数
var chatTalkLength = 0;

function resetChatTalk() {
    chatTalkLength = 0;
    selectElemntLength = 0;
    $('#chat-frame').empty();
}

/**
 * Pepperトーク吹き出しの表示
 * @param {string} msg メッセージです
 */
function blowPepper(msg) {
    chatTalkLength++;
    changeIcon(msg).done(function(imgPath){
        var htmlTemplate = ['<div class="chat-talk"><span class="talk-icon">',
                            '<img src="img/', imgPath, '" alt="pepper"/></span>',
                            '<span class="talk-content-container">',
                            '<span class="talk-content" ontouchstart="touchEvent(', chatTalkLength,
                            ')" ontouchend="touchendEvent(', chatTalkLength, ')"><p>', msg , '</p>',
                            '<button class="btn-translate" onclick="$(this).remove();appendPullDownMenu(',
                            chatTalkLength, ');">translate</button>',
                            '</span></div>'];
        var pepperTalk = $(htmlTemplate.join(""));
        pepperTalk.appendTo('#chat-frame').addClass('animated bounce');
        $("html,body").animate({ scrollTop: $('#chat-frame-end').offset().top});}
    ).fail(function(){
        console.log("error");
    });
}

/**
 * ユーザートーク吹き出しを表示
 * @param {string} msg メッセージです
 */
function blowUser(msg) {
    chatTalkLength++;
    var iconImg = "icon_user";
    if(faceTempID !== ""){ iconImg = faceTempID; }
    var htmlTemplate = ['<div class="chat-talk mytalk"><span class="talk-icon">',
                        '<img src="img/', iconImg, '.png" alt="user"/></span>',
                        '<span class="talk-content-container">',
                        '<span class="talk-content" ontouchstart="touchEvent(', chatTalkLength,
                        ')" ontouchend="touchendEvent(', chatTalkLength, ')"><p>', msg, '</p></span>',
                        '</span></div>'];
    var userTalk = $(htmlTemplate.join(""));
    userTalk.appendTo('#chat-frame').addClass('animated bounce');
    $("html,body").animate({ scrollTop: $('#chat-frame-end').offset().top });
}

/**
 * デバック吹き出しを表示
 * @param {string} msg メッセージです
 */
function blowDebugMsg(msg) {
    chatTalkLength++;
    var htmlTemplate  = ['<p class="chat-talk"><span class="info-content">',
                         msg, '</span></p>'];
    var debugElm = $(htmlTemplate.join(""));
    $('#chat-frame').append(debugElm);
    $("html,body").animate({ scrollTop: $('#chat-frame-end').offset().top });
}

// ulエレメントの要素数
var selectElemntLength = 0;

/**
 * セレクトボタンを表示
 * @param {array} buttonArray セレクトボタンに表示する配列
 */
function blowUserSelect(buttonArray) {
    // 5秒待ってから _callbackUserSelect() を呼ぶ
    setTimeout(function(buttonArray) {
        _callbackUserSelect(buttonArray);
    }, 5000, buttonArray);
}

/**
 * セレクトボタンを表示（本体）
 * @param {array} buttonArray セレクトボタンに表示する配列
 */
function _callbackUserSelect(buttonArray) {
    var buttons = "";
    for(var i in buttonArray){
        buttons += ['<li onClick=selectClick("',
                    buttonArray[i], '",', selectElemntLength, ');>',
                    buttonArray[i], '</li>'].join("");
    }
    var htmlTemplate = ['<div class="select-frame"><ul class="select-frame-inner">', buttons, '</ul></div>'];
    var appendData = $(htmlTemplate.join(""));
    $('#chat-frame').append(appendData);
    selectElemntLength++;
    $("html,body").animate({ scrollTop: $('#chat-frame-end').offset().top });
}

/**
 * セレクトボタンの発火後処理
 * @param {string} mes
 * @param {int} index //指定しない場合はUIは変わらない,一度選択しても他の選択肢を選択可能
 */
function selectClick(mes, index){
    if(index !== undefined){
        var selectElements = document.getElementsByClassName("select-frame-inner");
        var li_elements = selectElements[index].getElementsByTagName("li");
        //onClick要素を削除する
        $(li_elements).removeAttr("onClick");
        for(var i = 0; i < li_elements.length; i++){
            if(li_elements[i].innerHTML == mes){
                li_elements[i].classList.add('selected');
            }
            else{
                li_elements[i].classList.add("disableSelect");
            }
        }
    }
    session.service("ALMemory").then(function (ALMemory) {
        ALMemory.raiseEvent("ssa-user-answer", mes);
    });
}

/**
 * 画像を表示
 * @param {string} url
 */
function blowPepperImg(url) {
    chatTalkLength++;
    var htmlTemplate = ['<p class="chat-talk"><span class="talk-content-container recommend">',
                        '<span class="talk-content" ><img src="', url, '"></span></span></p>'];
    var pepperTalk = $(htmlTemplate.join(""));
    pepperTalk.appendTo('#chat-frame').addClass('animated lightSpeedIn');
    $("html,body").animate({ scrollTop: $('#chat-frame-end').offset().top });
}

/**
 * テストコード（呼び出さない）
 */
function testChatUI() {
    var msgCount = 0;
    setInterval(function () {
        blowPepper('pepperSay ' + msgCount);
        var funcStr = "blowUser('userSay " + msgCount + "')";
        setTimeout(funcStr, 1000);
        msgCount += 1;
    }, 2000);
}

/* 翻訳システム */

// 長押し処理で使用
var touched = false;
// 長押しした時間
var touchTime = 0;
// 一回長押しすると、翻訳するまで、他の文章を翻訳できない使用にする
var showTranslationResult = false;

/**
 * タッチしたときに呼ばれる関数
 * @param {int} length chat-talkタグの要素数
 */
function touchEvent(length){
    touched = true;
    touchTime = 0;
    document.interval = setInterval(function(){
        touchTime += 100;
        if (touchTime == 1000) {
            // ロングタップ(タップから約1秒)時の処理
            // 翻訳プルダウンを表示
            if(!showTranslationResult) {appendPullDownMenu(length);}
        }
    }, 100);
    return false;
}

/**
 * 離したときに呼ばれる関数
 * @param {int} length chat-talkタグの要素数
 */
function touchendEvent(length){
    touched = false;
    clearInterval(document.interval);
    return false;
}

/**
 * 翻訳プルダウンメニューを追加
 * 後で、アニメーションを付け加える。
 * @param {int} length chat-talkタグの要素数
 */
function appendPullDownMenu(length){
    $(this).css('color', 'red');
    showTranslationResult = true;
    var chatTalkElements = document.getElementsByClassName("chat-talk");
    var htmlTemplate = ['<div class="translatePullDown"><ul>',
                        '<li onclick=translationFromMes(', length, ',"en")>English</li>',
                        '<li onclick=translationFromMes(', length, ',"zh")>中文</li></ul></div>'];
    var pulldown = $(htmlTemplate.join(""));
    pulldown.appendTo(chatTalkElements[length-1]);
    if(length == chatTalkLength){
        $("html,body").animate({scrollTop:$('#chat-frame-end').offset().top});
    }
}

/**
 * Cloud Translation APIを介して翻訳
 * @param {int} length chat-talkタグの要素数
 * @param {string} lang 文字
 */
function translationFromMes(length, lang){
    var apiKey = TRANSLATION_API_KEY;
    var chatTalkElements = document.getElementsByClassName("chat-talk");
    // 一回翻訳させたら、もうさせない
    $(chatTalkElements[length-1]).find(".talk-content").removeAttr("ontouchstart");
    $(chatTalkElements[length-1]).find(".talk-content").removeAttr("ontouchend");
    // p要素が追加されているので気をつける
    var message = $(chatTalkElements[length-1]).find(".talk-content p").text();
    // プルダウンを削除
    $(chatTalkElements).find(".translatePullDown").remove();
    // 大文字でグローバルで設定できるように
    // ALMemoryでapiを管理したい
    dispLoading($(chatTalkElements[length-1]).find(".talk-content"));
    // ALMemoryでキーを操作する。
    $.ajax({
        url: 'https://translation.googleapis.com/language/translate/v2',
        type:'POST',
        dataType: 'json',
        data: {
            key: apiKey,
            q: message,
            target: lang
        },
        timeout: 10000
    }).done(function(data) {
        var translationResult = $(['<span class="translationResult-content">',
                                   data.data.translations[0].translatedText, '</span>'].join(""));
        //talk-contentに要素を追加する
        translationResult.appendTo($(chatTalkElements[length-1]).find(".talk-content"));
        showTranslationResult=false;
        removeLoading();
        if(length == chatTalkLength){
            $("html,body").animate({scrollTop:$('#chat-frame-end').offset().top});
        }
    }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
        blowDebugMsg("Translation API Error");
        var translationResult = $(['<span class="translationResult-content">',
                                   '翻訳できませんでした。',
                                   'I can\'t translate from this sentence.</span>'].join(""));
        //talk-contentに要素を追加する
        translationResult.appendTo($(chatTalkElements[length-1]).find(".talk-content"));
        showTranslationResult = false;
        removeLoading();
        if(length == chatTalkLength){
            $("html,body").animate({scrollTop:$('#chat-frame-end').offset().top});
        }
    });
}

/**
 * ローディング画像を表示
 * @param {object} element ローディング画像を追加する要素
 */
function dispLoading(element){
    console.log("show loading now");
    console.log(element);
    // 画面表示メッセージ
    var dispMsg = "";
    // ローディング画像が表示されていない場合のみ表示
    $(element).append("<div id='loading'><span class='loadingImg'>" + dispMsg + "</span></div>");
}

/**
 * ローディング画像を削除
 */
function removeLoading(){
    $('#loading').remove();
}

/**
 * アイコンの表示を切替
 * @param {string} msg 送信するメッセージ
 */
function changeIcon(msg){
    var dfd = $.Deferred();
    postCNLAPI(msg).done(function(data) {
        // resolveが実行された場合
        // data には上のdfd.resolveに渡したオブジェクトが入っている
        var response;
        if(data <= -0.5){ response = "unhappy.png"; }
        else if(data < 0.5){ response = "normal.png"; }
        else{ response = "happy.png"; }
        dfd.resolve(response);
    }).fail(function (error) {
        // rejectが実行された場合
        // alert("change Icon Error");
        dfd.resolve("normal.png");
    });
    return dfd.promise();
}

/**
 * Cloud Natural Language API
 * @param {string} msg 送信するメッセージ
 */
function postCNLAPI(msg){
    var apiKey = NATURAL_LANGUAGE_API_KEY;
    var dfd = $.Deferred();
    var op = {
        encodingType: "UTF8",
        document: {
            type: "PLAIN_TEXT",
            content: msg
        }
    };
    $.ajax({
        url: 'https://language.googleapis.com/v1/documents:analyzeSentiment?key=' + apiKey,
        type:'POST',
        dataType: 'json',
        data : JSON.stringify(op),
        contentType: 'application/JSON',
        timeout:10000
    }).done(function(data) {
        console.log(data);
        console.log("success");
        dfd.resolve(data.documentSentiment.score);
        // return  data;
    }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
        blowDebugMsg("Cloud Natural Language API Error");
        dfd.reject("error");
    });
    return dfd.promise();
}
